import os, json, threading, time, uuid, shutil
from flask import Flask, request, send_from_directory, jsonify
from flask_cors import CORS

try:
    import yt_dlp as ytdlp  # yt-dlp preferred
except Exception:
    ytdlp = None

APP = Flask(__name__)
CORS(APP)

BASE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE, os.getenv("CJ_DATA_DIR", "data"))
DL_DIR = os.path.join(BASE, os.getenv("CJ_DOWNLOAD_DIR", "downloads"))
STATE_PATH = os.path.join(BASE, os.getenv("CJ_QUEUE_PATH", "data/state.json"))
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(DL_DIR, exist_ok=True)

_state_lock = threading.Lock()
_worker_started = False

def _load_state():
    if not os.path.exists(STATE_PATH):
        return {"jobs": []}
    with open(STATE_PATH, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except Exception:
            return {"jobs": []}

def _save_state(state):
    tmp = STATE_PATH + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    os.replace(tmp, STATE_PATH)

def _ffmpeg_available():
    return shutil.which("ffmpeg") is not None

def _process_job(job):
    if ytdlp is None:
        job["status"] = "waiting_ytdlp"
        return False

    url = job["url"]
    outtmpl = os.path.join(DL_DIR, "%(title).200B.%(ext)s")
    ydl_opts = {
        "outtmpl": outtmpl,
        "quiet": True,
        "no_warnings": True,
        "format": "bestaudio/best",
        # If ffmpeg exists we can post-process to mp3; otherwise leave original
        "postprocessors": ([{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }] if _ffmpeg_available() else []),
    }
    try:
        with ytdlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            # Build file path
            if "requested_downloads" in info and info["requested_downloads"]:
                fp = info["requested_downloads"][0]["filepath"]
            else:
                # fallback: guess
                ext = info.get("ext", "m4a")
                title = info.get("title", str(job["id"]))[:200]
                fp = os.path.join(DL_DIR, f"{title}.{ext}")
            rel = os.path.relpath(fp, DL_DIR).replace("\\", "/")
            job["status"] = "done"
            job["file"] = rel
            job["ts_done"] = int(time.time())
            return True
    except Exception as e:
        job["status"] = "error"
        job["error"] = str(e)[:300]
        job["ts_done"] = int(time.time())
        return False

def worker_loop():
    while True:
        time.sleep(1.5)
        with _state_lock:
            state = _load_state()
            # find first queued
            job = next((j for j in state["jobs"] if j.get("status") in (None, "queued", "waiting_ytdlp")), None)
            if not job:
                continue
            job["status"] = "working"
            _save_state(state)
        # process outside lock
        _process_job(job)
        # save
        with _state_lock:
            # replace job by id
            state = _load_state()
            for i, j in enumerate(state["jobs"]):
                if j["id"] == job["id"]:
                    state["jobs"][i] = job
                    break
            _save_state(state)

def ensure_worker():
    global _worker_started
    if not _worker_started:
        t = threading.Thread(target=worker_loop, daemon=True)
        t.start()
        _worker_started = True

@APP.route("/health")
def health():
    return jsonify({
        "ok": True,
        "yt_dlp": ytdlp is not None,
        "ffmpeg": _ffmpeg_available(),
        "downloads": len(os.listdir(DL_DIR)) if os.path.exists(DL_DIR) else 0
    })

@APP.route("/files/<path:path>")
def files(path):
    return send_from_directory(DL_DIR, path, as_attachment=False)

@APP.route("/recent")
def recent():
    items = []
    if os.path.exists(DL_DIR):
        for name in sorted(os.listdir(DL_DIR))[-50:]:
            p = os.path.join(DL_DIR, name)
            if os.path.isfile(p):
                items.append({
                    "file": name,
                    "url": "/files/" + name,
                    "size": os.path.getsize(p)
                })
    return jsonify({ "items": items })

@APP.route("/rip", methods=["POST"])
def rip():
    data = request.get_json(force=True, silent=True) or {}
    url = (data.get("url") or "").strip()
    if not url:
        return jsonify({"ok": False, "error": "no url"}), 400
    job = {
        "id": uuid.uuid4().hex[:12],
        "url": url,
        "status": "queued",
        "ts": int(time.time()),
    }
    with _state_lock:
        state = _load_state()
        state["jobs"].append(job)
        _save_state(state)
    ensure_worker()
    return jsonify({"ok": True, "id": job["id"]})

@APP.route("/bulk_rip", methods=["POST"])
def bulk_rip():
    data = request.get_json(force=True, silent=True) or {}
    urls = data.get("urls")
    csv_text = data.get("csv")
    collected = []

    if csv_text and not urls:
        for line in csv_text.splitlines():
            line = line.strip()
            if not line: continue
            if line.lower().startswith("url"):  # header
                continue
            # first column assumed URL
            if "," in line:
                line = line.split(",", 1)[0]
            collected.append(line)
    elif urls:
        collected = [u.strip() for u in urls if u.strip()]

    if not collected:
        return jsonify({"ok": False, "error": "no urls"}), 400

    with _state_lock:
        state = _load_state()
        for u in collected:
            state["jobs"].append({
                "id": uuid.uuid4().hex[:12],
                "url": u,
                "status": "queued",
                "ts": int(time.time()),
            })
        _save_state(state)

    ensure_worker()
    return jsonify({"ok": True, "count": len(collected)})

# Static simple health page for Netlify mirrors if needed
@APP.route("/")
def home():
    return jsonify({"cratejuice": "bulk rip API", "ok": True})

if __name__ == "__main__":
    ensure_worker()
    APP.run(host="0.0.0.0", port=int(os.getenv("PORT", "8000")))
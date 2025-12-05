# v3/backend/main.py
from fastapi import FastAPI, UploadFile, File, Body, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import csv, io, re
from typing import List, Optional

APP_NAME = "cratejuice-backend"
VERSION = "v3.0.0"

app = FastAPI(title="CrateJuice Backend", version=VERSION)

# --- CORS (lock down to your domains later) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # e.g. ["https://cratejuice.netlify.app", "https://main--cratejuice.netlify.app"]
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- Models ----------
class UrlList(BaseModel):
    urls: List[str]

class TextBlob(BaseModel):
    text: str

class Rows(BaseModel):
    rows: List[dict]  # [{"title": "...", "artist": "...", "url": "..."}]

# ---------- Root & health ----------
@app.get("/")
def root():
    return {
        "ok": True,
        "service": APP_NAME,
        "version": VERSION,
        "routes": ["/health", "/tools/extract_links", "/csv/normalize", "/csv/to_m3u", "/demo/playlist", "/docs"],
    }

@app.get("/health")
def health():
    return {"ok": True}

# ---------- Tiny utils ----------
URL_RE = re.compile(r"(https?://[^\s<>\"')]+)")

def _clean(s: Optional[str]) -> str:
    return (s or "").strip()

# ---------- Tools ----------
@app.post("/tools/extract_links")
def extract_links(blob: TextBlob):
    urls = URL_RE.findall(blob.text or "")
    # de-dup while preserving order
    seen, clean = set(), []
    for u in urls:
        if u not in seen:
            seen.add(u)
            clean.append(u)
    return {"count": len(clean), "urls": clean}

@app.post("/csv/normalize")
async def csv_normalize(file: UploadFile = File(...)):
    """
    Accepts a CSV (any header order). We output canonical header
    title,artist,url and drop duplicate rows by url.
    """
    content = await file.read()
    reader = csv.DictReader(io.StringIO(content.decode("utf-8", errors="ignore")))
    out = io.StringIO()
    writer = csv.DictWriter(out, fieldnames=["title", "artist", "url"])
    writer.writeheader()
    seen = set()
    for row in reader:
        title = _clean(row.get("title") or row.get("Title"))
        artist = _clean(row.get("artist") or row.get("Artist"))
        url = _clean(row.get("url") or row.get("URL") or row.get("link") or row.get("Link"))
        if not url:
            continue
        if url in seen:
            continue
        seen.add(url)
        writer.writerow({"title": title, "artist": artist, "url": url})
    return Response(out.getvalue(), media_type="text/csv")

@app.post("/csv/to_m3u")
def csv_to_m3u(rows: Rows, title: str = "CrateJuice"):
    """
    Build an M3U from JSON rows = [{title, artist, url}].
    """
    lines = ["#EXTM3U", f"#PLAYLIST:{title}"]
    for r in rows.rows:
        t = _clean(r.get("title"))
        a = _clean(r.get("artist"))
        u = _clean(r.get("url"))
        if not u:
            continue
        tag = f"#EXTINF:-1,{a+' - ' if a else ''}{t}" if (t or a) else "#EXTINF:-1,CrateJuice"
        lines.append(tag)
        lines.append(u)
    m3u = "\n".join(lines) + "\n"
    return Response(m3u, media_type="audio/x-mpegurl")

# ---------- Demo ----------
@app.get("/demo/playlist")
def demo_playlist():
    return {
        "name": "Crate Juice — Demo",
        "items": [
            {"title": "Mimi pick", "artist": "—", "url": "https://open.spotify.com/track/7rvIxPkDOKZIKpeEHY7Cpg9"},
            {"title": "Cbo pick",  "artist": "—", "url": "https://open.spotify.com/track/05WBwtLeaq9f6PCwloNM2B"},
        ],
    }

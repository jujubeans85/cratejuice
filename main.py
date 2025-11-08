
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel, HttpUrl
from typing import List, Optional
import os, subprocess, shutil, glob, time, re

APP_DIR = os.path.dirname(__file__)
STORE = os.path.join(APP_DIR, "store")
os.makedirs(STORE, exist_ok=True)

app = FastAPI(title="CrateJuice Ripper", version="0.1.0")

# CORS: allow any origin; in production set CJ_ALLOWED_ORIGIN env or restrict below
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SAFE = re.compile(r"[^a-zA-Z0-9._-]+")

def safe_name(s: str) -> str:
    s = SAFE.sub("_", s)
    return s.strip("_") or f"track_{int(time.time())}"

@app.get("/health")
def health():
    return {"ok": True, "mode": "ripper", "ffmpeg": shutil.which("ffmpeg") is not None}

@app.get("/recent")
def recent(limit: int = 25):
    files = sorted(glob.glob(os.path.join(STORE, "*.*")), key=os.path.getmtime, reverse=True)
    out = []
    for f in files[:limit]:
        bn = os.path.basename(f)
        out.append({
            "file": bn,
            "size": os.path.getsize(f),
            "ts": int(os.path.getmtime(f)),
            "url": f"/dl/{bn}"
        })
    return {"items": out}

@app.get("/dl/{fname}")
def dl(fname: str):
    path = os.path.join(STORE, fname)
    if not os.path.isfile(path):
        raise HTTPException(404, "Not found")
    return FileResponse(path, filename=fname, media_type="audio/mpeg")

class RipIn(BaseModel):
    url: HttpUrl
    title: Optional[str] = None

@app.post("/rip")
def rip(inp: RipIn):
    # target mp3 name
    title = inp.title or "track"
    outname = safe_name(title) + ".mp3"
    dest = os.path.join(STORE, outname)

    # Use yt-dlp to extract audio -> mp3 (requires ffmpeg, installed via apt.txt)
    cmd = [
        "yt-dlp",
        "-x",
        "--audio-format", "mp3",
        "-o", os.path.join(STORE, "%(title)s.%(ext)s"),
        str(inp.url)
    ]
    try:
        # Run and capture title from last file produced; then rename to safe mp3 name if needed
        subprocess.check_call(cmd)
        # pick newest file in STORE
        files = sorted(glob.glob(os.path.join(STORE, "*")), key=os.path.getmtime, reverse=True)
        if not files:
            raise RuntimeError("No file produced")
        latest = files[0]
        # If latest isn't mp3, try to find mp3
        if not latest.lower().endswith(".mp3"):
            candidates = [f for f in files if f.lower().endswith(".mp3")]
            if candidates:
                latest = candidates[0]
        # rename to safe name if different
        if os.path.abspath(latest) != os.path.abspath(dest):
            shutil.copy2(latest, dest)
        size = os.path.getsize(dest)
        return {"ok": True, "file": os.path.basename(dest), "size": size, "url": f"/dl/{os.path.basename(dest)}"}
    except subprocess.CalledProcessError as e:
        raise HTTPException(500, f"yt-dlp failed: {e}")

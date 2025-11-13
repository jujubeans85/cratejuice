# v3/backend/main.py
import os
import time

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# --- Create the app ---
app = FastAPI(title="CrateJuice v3 API")

# --- CORS (front-end is allowed to call the API) ---
FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN", "https://cratejuice.netlify.app")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_ORIGIN],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Simple root (optional, handy for quick tests) ---
@app.get("/")
def root():
    return {"crate": "juice", "status": "spinning"}

# --- Health check (Render + Netlify use this) ---
@app.get("/health")
def health():
    return {"ok": True}

# --- Status panel (for /status page, CI, etc.) ---
@app.get("/status")
def status():
    return {
        "crate": "juice",
        "status": "spinning",
        "git_sha": os.getenv("GIT_SHA", ""),
        "started_at": os.getenv("STARTED_AT", ""),
        "time": int(time.time()),
    }

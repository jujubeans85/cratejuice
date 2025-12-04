import os
import time
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="CrateJuice v3 API")

FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN", "*")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_ORIGIN],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"crate": "juice", "status": "spinning"}

@app.get("/health")
def health():
    return {"ok": True}

@app.get("/status")
def status():
    return {
        "crate": "juice",
        "status": "spinning",
        "git_sha": os.getenv("GIT_SHA", ""),
        "started_at": os.getenv("STARTED_AT", ""),
        "time": int(time.time()),
    }
from fastapi import FastAPI
app = FastAPI()

@app.get("/health")
def health():
    return {"ok": True}

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import random

app = FastAPI()

# CORS so Netlify frontend can talk to Render backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten later if you want
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Track(BaseModel):
    title: str
    artist: Optional[str] = None
    url: Optional[str] = None

# Initial crate – 8 tracks
tracks = [
    {"id": 1, "title": "Midnight City", "artist": "M83"},
    {"id": 2, "title": "Something Just Like This", "artist": "The Chainsmokers & Coldplay"},
    {"id": 3, "title": "Walking on a Dream", "artist": "Empire of the Sun"},
    {"id": 4, "title": "Pompeii (Audien Remix)", "artist": "Bastille"},
    {"id": 5, "title": "Sweet Disposition (Axwell & Dirty South Remix)", "artist": "The Temper Trap"},
    {"id": 6, "title": "Blue Monday (Above & Beyond Remix)", "artist": "New Order"},
    {"id": 7, "title": "Skinny Love", "artist": "Bon Iver"},
    {"id": 8, "title": "Kids (Soulwax Remix)", "artist": "MGMT"},
]
_next_id = len(tracks) + 1


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/tracks")
def list_tracks():
    return {"tracks": tracks}


@app.post("/tracks")
def add_track(track: Track):
    """Add a new track to the crate."""
    global _next_id
    new_track = {"id": _next_id, **track.dict()}
    tracks.append(new_track)
    _next_id += 1
    return new_track


@app.get("/tracks/random")
def random_track():
    """Return a random track from the crate."""
    if not tracks:
        return {"track": None}
    return {"track": random.choice(tracks)}

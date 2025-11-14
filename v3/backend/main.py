from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS — allow Netlify frontend to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # we can tighten later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/tracks")
def list_tracks():
    return {
        "tracks": [
            {"id": 1, "title": "Midnight City – M83"},
            {"id": 2, "title": "Something Just Like This – Chainsmokers & Coldplay"},
            {"id": 3, "title": "Walking on a Dream – Empire of the Sun"},
            {"id": 4, "title": "Pompeii (Audien Remix) – Bastille"},
            {"id": 5, "title": "Sweet Disposition (Axwell & Dirty South Remix) – The Temper Trap"},
            {"id": 6, "title": "Blue Monday (A&B Remix) – New Order"},
            {"id": 7, "title": "Skinny Love – Bon Iver"},
            {"id": 8, "title": "Kids (Soulwax Remix) – MGMT"},
        ]
    }

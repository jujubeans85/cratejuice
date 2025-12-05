# CrateJuice Friday Drop v3

**What’s inside**
- `v3/frontend/` — ready-to-ship static UI (TEST banner + Mimi/Cbo, plus 2‑Deck page)
- `v3/backend/` — FastAPI starter with `/health`
- `tools/` — SoundCloud CSV extractor + CSV→MP3 down-loader (yt‑dlp)
- `playlists/` — CSV/TXT starter for Vol. 1–15
- `netlify.toml` — proxies `/api/*` to your Render backend

**Deploy**
- Netlify → Base dir: `v3/frontend` ; Publish dir: `v3/frontend` ; Functions dir: `v3/frontend/netlify/functions` (optional placeholder ok)
- Render → Root Directory: `v3/backend` ; Build: `pip install -r requirements.txt` ; Start: `uvicorn main:app --host 0.0.0.0 --port $PORT`

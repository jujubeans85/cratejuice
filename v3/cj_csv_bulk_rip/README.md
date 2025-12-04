# CrateJuice — CSV → Bulk Rip (Zip Drop)

This bundle gives you:
- **Front-end** with a floating **SoundCloud → CSV** extractor panel (_one button_ bookmarklet) **and** a **CSV → Ripper** uploader.
- **Back-end (Flask)** with `/rip`, `/bulk_rip`, `/recent`, `/health`, static file serving for downloads.
- **Background worker thread** that tries to rip each queued URL using `yt-dlp` (to original audio container; no ffmpeg post-process required).

> If ffmpeg is available, files may be converted; otherwise originals are saved.

## Quick Start

### 1) Render (Backend)
Create a **Web Service** from `v3/backend/`:
- **Start command**: `gunicorn main:app`
- **Build Command**: `pip install -r requirements.txt`
- Recommended instance: a small paid tier avoids sleep.
- Set environment variables if needed:
  - `CJ_DOWNLOAD_DIR` (default: `downloads`)
  - `CJ_QUEUE_PATH` (default: `data/state.json`)

> After deploy, your API base will look like `https://cratejuice.onrender.com` (replace in Netlify).

### 2) Netlify (Frontend)
Deploy `v3/frontend/` and keep `netlify.toml` at the repo root.
Set the **Render base** in either of two ways:
- Edit `netlify.toml` `RENDER-BASE` to your Render hostname and redeploy, **or**
- Append `?api=https://cratejuice.onrender.com` to the page URL; the page saves it in localStorage.

### 3) Use
- On **SoundCloud**, click the **bookmarklet** (created via the panel) to download a CSV of all links found.
- Back at **CrateJuice page**, drop the CSV into the **CSV → Ripper** box (or paste). It will queue each link to `/bulk_rip`.
- Use **Refresh** to see `/recent` and play or download files.

## Health Check
- Backend: `GET /health` → `{ ok, yt_dlp, ffmpeg }`
- Frontend: `/health` → quick static OK page (200).

## Endpoints
- `POST /rip` JSON `{ "url": "..." }`
- `POST /bulk_rip` JSON `{ "urls": ["..."] }` **or** `{ "csv": "..." }`
- `GET /recent` → `{ items: [{file, url, size}] }`
- `GET /files/<path>` → serves downloaded files
- `GET /health` → health info

## Notes
- This worker is **best effort** inside the web dyno. For heavier ripping, run a separate **Render Worker** using the same code but `python worker.py` (not included here) or convert the thread to a separate service.
- If ffmpeg is missing, `yt-dlp` will still fetch bestaudio (e.g., m4a/webm). You can convert locally later.

— Built with love for MMI & CBO · CrateJuice™ 2025
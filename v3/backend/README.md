**CrateJuice Backend (v3/backend)**

Purpose: deploy this service to Render as the backend for CrateJuice.

Build note: Render runs the configured `buildCommand` before starting the service. This project relies on a `requirements.txt` file — ensure Render's build command installs those dependencies first, for example:

```bash
pip install -r requirements.txt
```

Start note: The service entrypoint is `main:app`. Example start command used on Render:

```bash
gunicorn main:app --bind 0.0.0.0:$PORT
```

Root directory: When configuring the Render service, set the "Root Directory" (or repo path) to `v3/backend` so `requirements.txt`, `main.py`, and other files are found.

Environment variables and tips:

- `CJ_MAP_PATH`: path to dynamic mapping file (defaults to `mapping/dynamic_mapping.json`).
- `PYTHON_VERSION`: set to a supported version (the existing `render.yaml` suggests `3.11.0`).

Quick checklist:

- `v3/backend/requirements.txt` exists and lists pinned deps.
- Render `buildCommand` runs `pip install -r requirements.txt`.
- Render `startCommand` uses `gunicorn main:app --bind 0.0.0.0:$PORT`.
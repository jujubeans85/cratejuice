# Render Backend — Full Dime
Root: `/backend`
Build: `pip install -r requirements.txt`
Start: `uvicorn main:app --host 0.0.0.0 --port $PORT`

Env (optional):
- CJ_MAP_PATH=mapping/dynamic_mapping.json

Endpoints:
- GET /health
- GET /qr?link=...
- GET /r/{id}  (uses mapping/dynamic_mapping.json)
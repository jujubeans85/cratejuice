from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, RedirectResponse, JSONResponse
import qrcode, io, os, json

app = FastAPI(title="CrateJuice API (Full Dime)")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.get("/health")
def health(): return {"status":"up"}

@app.get("/qr")
def qr(link: str = Query(...)):
    img = qrcode.make(link)
    buf = io.BytesIO(); img.save(buf, format="PNG"); buf.seek(0)
    return StreamingResponse(buf, media_type="image/png")

MAP_PATH = os.getenv("CJ_MAP_PATH", "mapping/dynamic_mapping.json")
try:
    with open(MAP_PATH, "r") as f:
        DYN = json.load(f)
    ID_MAP = {c["id"]: c["target"] for c in DYN.get("codes", [])}
except Exception as e:
    ID_MAP = {}
    print("WARN: dynamic mapping not loaded:", e)

@app.get("/r/{code_id}")
def dyn_redirect(code_id: str):
    url = ID_MAP.get(code_id)
    if not url:
        raise HTTPException(status_code=404, detail="Unknown code")
    return RedirectResponse(url)

@app.get("/map")
def get_map():
    return JSONResponse({"count": len(ID_MAP)})

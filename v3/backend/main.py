# v3/backend/main.py
# CrateJuice QR backend — reference baseline (FastAPI)
# Endpoints:
#   GET  /health
#   POST /api/qr/create                     {"slug": "...", "target_url": "...", "palette": "neon"}
#   GET  /api/qr/slug/{slug}
#   GET  /api/qr/plain/{slug}.png
#   GET  /api/qr/record/{slug}.png
#   GET  /api/qr/record_label/{slug}.png    ?caption=Hello
#   GET  /api/qr/anim/{slug}.gif
#   GET  /api/qr/sheet_plain.png            ?slugs=a,b,c...&dpi=300
#   GET  /api/qr/sheet_record.png           ?slugs=...&dpi=300

import io, os, math, sqlite3
from typing import Optional, List, Tuple
from dataclasses import dataclass

from fastapi import FastAPI, HTTPException, Query, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse
from pydantic import BaseModel

from PIL import Image, ImageDraw, ImageFilter
import qrcode
from qrcode.constants import ERROR_CORRECT_Q

# -----------------------------------------------------------------------------
# App + CORS
# -----------------------------------------------------------------------------
app = FastAPI(title="CrateJuice QR Backend", version="0.3.0")

def _env_list(name: str) -> List[str]:
    raw = os.getenv(name, "")
    if not raw:
        return []
    return [x.strip() for x in raw.split(",") if x.strip()]

CORS_ALLOW_ORIGINS = _env_list("CORS_ALLOW_ORIGINS") or [
    "https://cratejuice.netlify.app",
    "https://main--cratejuice.netlify.app",
    "http://localhost",
    "http://localhost:5173",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------------------------------------------------------
# Storage (SQLite with in-memory fallback)
# -----------------------------------------------------------------------------
DB_PATH = os.getenv("DB_PATH", os.path.join(os.path.dirname(__file__), "cj_qr.sqlite3"))
MEM_STORE = {}  # slug -> (target_url, palette)

def _db_conn():
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.execute(
            "CREATE TABLE IF NOT EXISTS slugs (slug TEXT PRIMARY KEY, target TEXT NOT NULL, palette TEXT)"
        )
        return conn
    except Exception:
        return None

def set_slug(slug: str, target: str, palette: Optional[str]):
    conn = _db_conn()
    if conn:
        conn.execute(
            "INSERT INTO slugs (slug, target, palette) VALUES (?, ?, ?) "
            "ON CONFLICT(slug) DO UPDATE SET target=excluded.target, palette=excluded.palette",
            (slug, target, palette),
        )
        conn.commit()
        conn.close()
    else:
        MEM_STORE[slug] = (target, palette)

def get_slug(slug: str) -> Tuple[str, Optional[str]]:
    conn = _db_conn()
    if conn:
        cur = conn.execute("SELECT target, palette FROM slugs WHERE slug = ?", (slug,))
        row = cur.fetchone()
        conn.close()
        if not row:
            raise HTTPException(status_code=404, detail="Slug not found")
        return row[0], row[1]
    else:
        if slug not in MEM_STORE:
            raise HTTPException(status_code=404, detail="Slug not found")
        return MEM_STORE[slug]

# -----------------------------------------------------------------------------
# Palettes (default = neon orange/blue grit)
# -----------------------------------------------------------------------------
@dataclass
class Palette:
    name: str
    bg: Tuple[int,int,int,int]
    record_dark: Tuple[int,int,int,int]
    record_light: Tuple[int,int,int,int]
    label: Tuple[int,int,int,int]
    qr_dark: Tuple[int,int,int,int]
    qr_light: Tuple[int,int,int,int]
    grit: Tuple[int,int,int,int]

PALETTES = {
    "neon": Palette(
        name="neon",
        bg=(10, 12, 18, 255),            # deep charcoal
        record_dark=(12,12,14,255),      # near-black vinyl
        record_light=(34,34,46,255),     # faint ring highlight
        label=(255,120,20,255),          # neon orange
        qr_dark=(0,0,0,255),             # QR dark
        qr_light=(248,248,248,255),      # QR light
        grit=(0, 200, 255, 25),          # subtle cyan grit specks
    ),
    "mono": Palette(
        name="mono",
        bg=(8,8,10,255),
        record_dark=(16,16,18,255),
        record_light=(52,52,60,255),
        label=(225,225,225,255),
        qr_dark=(0,0,0,255),
        qr_light=(255,255,255,255),
        grit=(255,255,255,15),
    ),
}

def _palette(name: Optional[str]) -> Palette:
    if name and name in PALETTES:
        return PALETTES[name]
    return PALETTES["neon"]

# -----------------------------------------------------------------------------
# Helpers: QR generation + record composition
# -----------------------------------------------------------------------------
def _qr_image(data: str, size: int, dark=(0,0,0,255), light=(255,255,255,255)) -> Image.Image:
    qr = qrcode.QRCode(
        version=None,
        error_correction=ERROR_CORRECT_Q,
        box_size=10,
        border=2,  # keep quiet zone tight
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color=tuple(dark[:3]), back_color=tuple(light[:3])).convert("RGBA")
    # Scale to exact size with sharp edges
    return img.resize((size, size), resample=Image.NEAREST)

def to_png_bytes(im: Image.Image, dpi: Optional[int]=None) -> bytes:
    bio = io.BytesIO()
    save_kwargs = {"optimize": True}
    if dpi:
        save_kwargs["dpi"] = (dpi, dpi)
    im.save(bio, format="PNG", **save_kwargs)
    return bio.getvalue()

def _grit_overlay(w: int, h: int, color=(0,200,255,25), step=32) -> Image.Image:
    """Light speckle overlay to get that neon grit vibe."""
    grit = Image.new("RGBA", (w, h), (0,0,0,0))
    d = ImageDraw.Draw(grit)
    for y in range(0, h, step):
        for x in range(0, w, step):
            r = 1
            d.ellipse((x-r, y-r, x+r, y+r), fill=color)
    return grit.filter(ImageFilter.GaussianBlur(0.5))

def compose_record_qr(slug: str, size: int, pal: Palette, target: Optional[str]=None) -> Image.Image:
    """Square vinyl record with grooves + label + scannable QR centered."""
    target_url = target
    if not target_url:
        target_url, _p = get_slug(slug)

    im = Image.new("RGBA", (size, size), pal.bg)

    # vinyl
    cx = cy = size // 2
    radius = int(size*0.48)
    draw = ImageDraw.Draw(im)
    draw.ellipse((cx-radius, cy-radius, cx+radius, cy+radius), fill=pal.record_dark)

    # grooves (faint concentric rings)
    inner = int(radius*0.35)
    for r in range(inner, radius, 6):
        a = 32  # alpha
        col = (pal.record_light[0], pal.record_light[1], pal.record_light[2], a)
        draw.ellipse((cx-r, cy-r, cx+r, cy+r), outline=col, width=1)

    # center label
    lab_r = int(radius*0.42)
    draw.ellipse((cx-lab_r, cy-lab_r, cx+lab_r, cy+lab_r), fill=pal.label)

    # tiny spindle hole
    hr = max(2, size//120)
    draw.ellipse((cx-hr, cy-hr, cx+hr, cy+hr), fill=(0,0,0,180))

    # QR sized to label
    qr_size = int(lab_r*1.5)  # bleed out a touch for scan confidence
    qr = _qr_image(target_url, qr_size, pal.qr_dark, pal.qr_light)
    # soft drop shadow
    shadow = Image.new("RGBA", qr.size, (0,0,0,0))
    sd = ImageDraw.Draw(shadow)
    sd.rectangle((0,0,qr.size[0],qr.size[1]), fill=(0,0,0,80))
    shadow = shadow.filter(ImageFilter.GaussianBlur(6))
    im.alpha_composite(shadow, (cx-qr_size//2+2, cy-qr_size//2+2))
    im.alpha_composite(qr, (cx-qr_size//2, cy-qr_size//2))

    # grit
    im.alpha_composite(_grit_overlay(size, size, pal.grit))
    return im

# -----------------------------------------------------------------------------
# Models
# -----------------------------------------------------------------------------
class CreateSlug(BaseModel):
    slug: str
    target_url: str
    palette: Optional[str] = None

# -----------------------------------------------------------------------------
# Routes
# -----------------------------------------------------------------------------
@app.get("/health")
def health():
    return {"ok": True}

@app.post("/api/qr/create")
def api_create_slug(payload: CreateSlug = Body(...)):
    if not payload.slug or not payload.target_url:
        raise HTTPException(400, "slug and target_url required")
    set_slug(payload.slug, payload.target_url, payload.palette)
    return {"ok": True, "slug": payload.slug}

@app.get("/api/qr/slug/{slug}")
def api_get_slug(slug: str):
    target, palette = get_slug(slug)
    return {"slug": slug, "target_url": target, "palette": palette or "neon"}

# --- Image endpoints ----------------------------------------------------------

@app.get("/api/qr/plain/{slug}.png")
def plain_qr(slug: str,
             size: int = Query(768, ge=128, le=4096),
             palette: Optional[str] = Query(None)):
    pal = _palette(palette or get_slug(slug)[1])
    target, _ = get_slug(slug)
    img = _qr_image(target, size, pal.qr_dark, pal.qr_light)
    return StreamingResponse(io.BytesIO(to_png_bytes(img)), media_type="image/png")

@app.get("/api/qr/record/{slug}.png")
def record_png(slug: str,
               size: int = Query(1024, ge=512, le=4096),
               palette: Optional[str] = Query(None)):
    pal = _palette(palette or get_slug(slug)[1])
    target, _ = get_slug(slug)
    img = compose_record_qr(slug, size, pal, target)
    return StreamingResponse(io.BytesIO(to_png_bytes(img)), media_type="image/png")

@app.get("/api/qr/record_label/{slug}.png")
def record_with_label(slug: str,
                      caption: str = Query("", max_length=64),
                      size: int = Query(1200, ge=512, le=4096),
                      palette: Optional[str] = Query(None)):
    pal = _palette(palette or get_slug(slug)[1])
    target, _ = get_slug(slug)
    img = compose_record_qr(slug, size, pal, target)
    if caption:
        draw = ImageDraw.Draw(img)
        y = int(size*0.9)
        draw.text((size//2, y), caption, fill=pal.qr_light, anchor="mm")
    return StreamingResponse(io.BytesIO(to_png_bytes(img)), media_type="image/png")

@app.get("/api/qr/anim/{slug}.gif")
def record_anim_gif(slug: str,
                    size: int = Query(768, ge=512, le=2048),
                    frames: int = Query(16, ge=8, le=48),
                    fps: int = Query(10, ge=4, le=30),
                    palette: Optional[str] = Query(None)):
    """Simple spin: rotate grooves; keep QR static (so it still scans)."""
    pal = _palette(palette or get_slug(slug)[1])
    target, _ = get_slug(slug)

    # Base without QR: draw record once
    base = Image.new("RGBA", (size, size), pal.bg)
    cx = cy = size // 2
    radius = int(size*0.48)
    draw = ImageDraw.Draw(base)
    draw.ellipse((cx-radius, cy-radius, cx+radius, cy+radius), fill=pal.record_dark)
    inner = int(radius*0.35)
    # grooves layer to rotate
    grooves = Image.new("RGBA", (size, size), (0,0,0,0))
    gd = ImageDraw.Draw(grooves)
    for r in range(inner, radius, 6):
        col = (pal.record_light[0], pal.record_light[1], pal.record_light[2], 32)
        gd.ellipse((cx-r, cy-r, cx+r, cy+ r), outline=col, width=1)

    # label
    lab_r = int(radius*0.42)
    draw.ellipse((cx-lab_r, cy-lab_r, cx+lab_r, cy+lab_r), fill=pal.label)
    hr = max(2, size//120)
    draw.ellipse((cx-hr, cy-hr, cx+hr, cy+hr), fill=(0,0,0,180))

    # static QR
    qr_size = int(lab_r*1.5)
    qr = _qr_image(target, qr_size, pal.qr_dark, pal.qr_light)

    frames_list = []
    for i in range(frames):
        ang = 360.0 * (i/frames)
        g_rot = grooves.rotate(ang, resample=Image.BICUBIC)
        frame = base.copy()
        frame.alpha_composite(g_rot)
        frame.alpha_composite(qr, (cx-qr_size//2, cy-qr_size//2))
        frame.alpha_composite(_grit_overlay(size, size, pal.grit))
        frames_list.append(frame)

    bio = io.BytesIO()
    frames_list[0].save(
        bio, format="GIF", save_all=True, append_images=frames_list[1:],
        duration=int(1000/fps), loop=0, disposal=2)
    return StreamingResponse(io.BytesIO(bio.getvalue()), media_type="image/gif")

# --- Sheets -------------------------------------------------------------------

def _grid_sheet(slugs: List[str], maker, dpi: int, pal: Palette) -> Image.Image:
    # A4 portrait @ 300dpi
    W, H = 2480, 3508
    cols, rows = 3, 4
    margin = 80
    cell_w = (W - (cols+1)*margin)//cols
    cell_h = (H - (rows+1)*margin)//rows
    size = min(cell_w, cell_h)

    page = Image.new("RGBA", (W, H), pal.bg)
    idx = 0
    for r in range(rows):
        for c in range(cols):
            if idx >= len(slugs): break
            tile = maker(slugs[idx], size, pal)
            x = margin + c*(size+margin)
            y = margin + r*(size+margin)
            page.alpha_composite(tile, (x, y))
            idx += 1
    return page

def _make_plain(slug: str, size: int, pal: Palette) -> Image.Image:
    target, _ = get_slug(slug)
    return _qr_image(target, size, pal.qr_dark, pal.qr_light)

def _make_record(slug: str, size: int, pal: Palette) -> Image.Image:
    target, _ = get_slug(slug)
    return compose_record_qr(slug, size, pal, target)

@app.get("/api/qr/sheet_plain.png")
def sheet_plain(slugs: str = Query("mimi-01,cbo-01,ma-01,boss-01,jbo-01,tim-01,friend-01,other-01,mimi-02,cbo-02,ma-02,boss-02"),
                dpi: int = Query(300, ge=150, le=600),
                palette: Optional[str] = Query(None)):
    pal = _palette(palette)
    items = [s.strip() for s in slugs.split(",") if s.strip()]
    page = _grid_sheet(items, _make_plain, dpi, pal)
    return StreamingResponse(io.BytesIO(to_png_bytes(page, dpi=dpi)), media_type="image/png")

@app.get("/api/qr/sheet_record.png")
def sheet_record(slugs: str = Query("mimi-01,cbo-01,ma-01,boss-01,jbo-01,tim-01,friend-01,other-01,mimi-02,cbo-02,ma-02,boss-02"),
                 dpi: int = Query(300, ge=150, le=600),
                 palette: Optional[str] = Query(None)):
    pal = _palette(palette)
    items = [s.strip() for s in slugs.split(",") if s.strip()]
    page = _grid_sheet(items, _make_record, dpi, pal)
    return StreamingResponse(io.BytesIO(to_png_bytes(page, dpi=dpi)), media_type="image/png")

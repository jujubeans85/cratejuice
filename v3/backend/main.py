import io, os, time, math, sqlite3, hashlib
from typing import List, Optional
from fastapi import FastAPI, Request, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from PIL import Image, ImageDraw, ImageFilter
import qrcode

APP_NAME = "CrateJuice QR Engine"
DB_PATH = os.environ.get("CJ_DB_PATH", "cjqr.db")

# -------------------------
# FastAPI app + CORS
# -------------------------
app = FastAPI(title=APP_NAME)

cors_origins = [
    "https://cratejuice.netlify.app",
    "https://main--cratejuice.netlify.app",
    os.environ.get("EXTRA_ORIGIN", "").strip() or "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# DB helpers
# -------------------------
def _db():
    con = sqlite3.connect(DB_PATH)
    con.execute("PRAGMA journal_mode=WAL;")
    con.row_factory = sqlite3.Row
    return con

def _init_db():
    con = _db()
    con.executescript("""
    CREATE TABLE IF NOT EXISTS slugs(
        slug TEXT PRIMARY KEY,
        target_url TEXT NOT NULL,
        title TEXT DEFAULT '',
        created_at INTEGER
    );
    CREATE TABLE IF NOT EXISTS claims(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        slug TEXT NOT NULL,
        ip TEXT,
        ua TEXT,
        lat REAL,
        lon REAL,
        approx INTEGER DEFAULT 1,
        created_at INTEGER
    );
    CREATE TABLE IF NOT EXISTS mints(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        slug TEXT NOT NULL,
        qty INTEGER NOT NULL,
        created_at INTEGER
    );
    """)
    con.commit()
    con.close()

@app.on_event("startup")
def _startup():
    _init_db()

# -------------------------
# Palettes (Image 2 vibe)
# -------------------------
PALETTES = {
    # "img2" = neon orange record on deep-navy / teal/purple accents
    "img2": {
        "bg": (10, 14, 26),          # deep navy
        "groove": (22, 26, 40),
        "vinyl": (14, 14, 18),
        "label": (255, 120, 28),     # neon orange
        "accent": (69, 38, 130),     # purple
        "accent2": (0, 200, 255),    # teal
        "qr_dark": (16, 16, 16),
        "qr_light": (248, 250, 252),
    },
    "mono": {
        "bg": (18,18,18),
        "groove": (28,28,28),
        "vinyl": (12,12,12),
        "label": (220,220,220),
        "accent": (90,90,90),
        "accent2": (150,150,150),
        "qr_dark": (0,0,0),
        "qr_light": (255,255,255),
    }
}

def _palette(name: Optional[str]):
    return PALETTES.get((name or "img2").lower(), PALETTES["img2"])

# -------------------------
# Slug registry
# -------------------------
def upsert_slug(slug: str, target_url: str, title: str = ""):
    con = _db()
    con.execute(
        "INSERT INTO slugs(slug, target_url, title, created_at) "
        "VALUES(?,?,?,?) "
        "ON CONFLICT(slug) DO UPDATE SET target_url=excluded.target_url, title=excluded.title",
        (slug, target_url, title, int(time.time()))
    )
    con.commit(); con.close()

def get_target(slug: str) -> str:
    con = _db()
    cur = con.execute("SELECT target_url FROM slugs WHERE slug=?", (slug,))
    row = cur.fetchone()
    con.close()
    if row: return row["target_url"]
    # fallback: still generate a QR pointing to site with slug tag
    return f"https://cratejuice.netlify.app/?s={slug}"

# -------------------------
# Record renderer
# -------------------------
def _qr_image(data: str, box: int, dark, light) -> Image.Image:
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_Q)
    qr.add_data(data); qr.make(fit=True)
    img = qr.make_image(fill_color=dark, back_color=light).convert("RGBA")
    w, h = img.size
    # scale to box
    scale = box / max(w, h)
    img = img.resize((int(w*scale), int(h*scale)), Image.NEAREST)
    return img

def _record_disc(size: int, pal) -> Image.Image:
    """
    Create a vinyl disc with grooves and a center label.
    Returns an RGBA image (square).
    """
    img = Image.new("RGBA", (size, size), pal["bg"])
    drw = ImageDraw.Draw(img)

    cx = cy = size // 2
    R = int(size*0.48)        # outer radius
    r_label = int(size*0.22)  # label radius
    r_hole = max(2, size // 120)

    # vinyl base
    drw.ellipse([cx-R, cy-R, cx+R, cy+R], fill=pal["vinyl"])

    # subtle radial vignette
    vignette = Image.new("L", (size, size), 0)
    vg = ImageDraw.Draw(vignette)
    vg.ellipse([cx-R, cy-R, cx+R, cy+R], fill=220)
    vignette = vignette.filter(ImageFilter.GaussianBlur(radius=size//18))
    img.putalpha(vignette)

    # grooves
    gcol = pal["groove"]
    for rr in range(R-4, r_label+8, -6):
        drw.ellipse([cx-rr, cy-rr, cx+rr, cy+rr], outline=gcol)

    # center label
    drw.ellipse([cx-r_label, cy-r_label, cx+r_label, cy+r_label], fill=pal["label"])
    # spindle hole
    drw.ellipse([cx-r_hole, cy-r_hole, cx+r_hole, cy+r_hole], fill=(0,0,0))

    return img

def compose_record_qr(slug: str, size: int, pal) -> Image.Image:
    record = _record_disc(size, pal)
    target = get_target(slug)

    # QR sits inside the label area
    qr_box = int(size * 0.28)
    qr_img = _qr_image(target, qr_box, pal["qr_dark"], pal["qr_light"])

    # paste centered
    x = (size - qr_img.width)//2
    y = (size - qr_img.height)//2
    record.alpha_composite(qr_img, (x, y))

    # subtle outer glow ring
    glow = Image.new("RGBA", record.size, (0,0,0,0))
    gd = ImageDraw.Draw(glow)
    cx = cy = size//2
    R = int(size*0.485)
    gd.ellipse([cx-R, cy-R, cx+R, cy+R], outline=pal["accent2"], width=2)
    glow = glow.filter(ImageFilter.GaussianBlur(radius=size//100))
    record = Image.alpha_composite(record, glow)
    return record

# -------------------------
# Helpers: bytes responses
# -------------------------
def to_png_bytes(img: Image.Image, dpi: Optional[int]=None) -> bytes:
    buf = io.BytesIO()
    save_kwargs = {"format": "PNG"}
    if dpi: save_kwargs["dpi"] = (dpi, dpi)
    img.save(buf, **save_kwargs)
    buf.seek(0)
    return buf.getvalue()

def to_gif_bytes(frames: List[Image.Image], duration_ms: int=60) -> bytes:
    buf = io.BytesIO()
    frames[0].save(buf, format="GIF", save_all=True,
                   append_images=frames[1:], loop=0, duration=duration_ms,
                   disposal=2)
    buf.seek(0)
    return buf.getvalue()

# -------------------------
# API
# -------------------------
@app.get("/health")
def health():
    return {"ok": True, "app": APP_NAME}

# Registry (create or update a slug)
@app.post("/api/qr/create")
async def create_slug(payload: dict):
    slug = (payload.get("slug") or "").strip()
    target = (payload.get("target_url") or "").strip()
    title = (payload.get("title") or "").strip()
    if not slug or not target:
        raise HTTPException(400, "slug and target_url are required")
    upsert_slug(slug, target, title)
    return {"ok": True, "slug": slug, "target_url": target}

# Mint batch (for bookkeeping)
@app.post("/api/qr/mint")
async def mint(payload: dict):
    slug = (payload.get("slug") or "").strip()
    qty = int(payload.get("qty") or 0)
    if not slug or qty <= 0:
        raise HTTPException(400, "slug and positive qty required")
    con = _db()
    con.execute("INSERT INTO mints(slug, qty, created_at) VALUES(?,?,?)", (slug, qty, int(time.time())))
    con.commit(); con.close()
    return {"ok": True, "slug": slug, "qty": qty}

# Claim a code (vague geo)
@app.post("/api/qr/claim")
async def claim(request: Request, payload: dict):
    slug = (payload.get("slug") or "").strip()
    if not slug:
        raise HTTPException(400, "slug required")
    # vague geo: round to ~1.1km (@ ~2 decimals) if provided
    lat = payload.get("lat"); lon = payload.get("lon")
    def _v(x): 
        try: return round(float(x), 2)
        except: return None
    lat = _v(lat); lon = _v(lon)
    ip = request.client.host if request.client else "0.0.0.0"
    ua = request.headers.get("user-agent", "")
    con = _db()
    con.execute(
        "INSERT INTO claims(slug, ip, ua, lat, lon, approx, created_at) VALUES(?,?,?,?,?,?,?)",
        (slug, ip, ua, lat, lon, 1, int(time.time()))
    )
    con.commit(); con.close()
    return {"ok": True, "slug": slug}

# Claim stats
@app.get("/api/qr/claims/{slug}")
def claims(slug: str):
    con = _db()
    cur = con.execute("SELECT COUNT(*) as c FROM claims WHERE slug=?", (slug,))
    total = cur.fetchone()["c"]
    cur = con.execute("SELECT lat, lon, COUNT(*) c FROM claims WHERE slug=? AND lat IS NOT NULL AND lon IS NOT NULL GROUP BY lat,lon", (slug,))
    clusters = [dict(r) for r in cur.fetchall()]
    con.close()
    return {"ok": True, "slug": slug, "total": total, "clusters": clusters}

# Static record PNG
@app.get("/api/qr/record/{slug}.png")
def record_png(slug: str, size: int = Query(1024, ge=256, le=4096), palette: Optional[str]=Query(None)):
    pal = _palette(palette)
    img = compose_record_qr(slug, size, pal)
    return StreamingResponse(io.BytesIO(to_png_bytes(img)), media_type="image/png")

# Animated record GIF (simple spin)
@app.get("/api/qr/anim/{slug}.gif")
def record_gif(slug: str, size: int = Query(768, ge=256, le=1024), frames: int = Query(24, ge=8, le=48), palette: Optional[str]=Query(None)):
    pal = _palette(palette)
    base = compose_record_qr(slug, size, pal)
    seq = []
    for i in range(frames):
        deg = int((360/frames)*i)
        seq.append(base.rotate(deg, resample=Image.BICUBIC, expand=False))
    return StreamingResponse(io.BytesIO(to_gif_bytes(seq, duration_ms=60)), media_type="image/gif")

# 12-up A4 sheet (PNG, 300 DPI suggested)
@app.get("/api/qr/sheet_record.png")
def sheet_png(
    slugs: str = Query("mimi-01,cbo-01,ma-01,boss-01,jbo-01,tim-01,friend-01,other-01,mimi-02,cbo-02,ma-02,boss-02"),
    dpi: int = Query(300, ge=150, le=600),
    palette: Optional[str]=Query(None),
):
    pal = _palette(palette)
    # A4 @300dpi = 3508 x 2480 (landscape or portrait). We'll do portrait (2480x3508).
    W, H = 2480, 3508
    cols, rows = 3, 4
    margin = 80
    cell_w = (W - (cols+1)*margin)//cols
    cell_h = (H - (rows+1)*margin)//rows
    size = min(cell_w, cell_h)

    page = Image.new("RGBA", (W, H), pal["bg"])
    items = [s.strip() for s in slugs.split(",") if s.strip()]
    idx = 0
    for r in range(rows):
        for c in range(cols):
            if idx >= len(items): break
            im = compose_record_qr(items[idx], size, pal)
            x = margin + c*(size+margin)
            y = margin + r*(size+margin)
            page.alpha_composite(im, (x, y))
            idx += 1

    return StreamingResponse(io.BytesIO(to_png_bytes(page, dpi=dpi)), media_type="image/png")
    
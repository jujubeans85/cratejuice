# --- CJ Dynamic QR (vinyl style) --------------------------------------------
from fastapi import APIRouter, HTTPException, Response, Query
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from PIL import Image, ImageDraw, ImageFilter
import qrcode, io, os, sqlite3, time, hashlib

qr = APIRouter(prefix="/api/qr", tags=["qr"])

DB_PATH = os.environ.get("QR_DB_PATH", "qr_links.sqlite")

def _db():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.execute("""CREATE TABLE IF NOT EXISTS qr_links (
        slug TEXT PRIMARY KEY,
        target_url TEXT NOT NULL,
        title TEXT,
        palette TEXT,
        active INTEGER DEFAULT 1,
        created_at INTEGER,
        updated_at INTEGER
    )""")
    conn.execute("""CREATE TABLE IF NOT EXISTS qr_scans (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        slug TEXT,
        ts INTEGER,
        ua TEXT,
        iphash TEXT,
        ref TEXT
    )""")
    return conn

DB = _db()

class QRCreate(BaseModel):
    slug: str
    target_url: str
    title: str | None = None
    palette: str | None = None
    active: bool = True

class QRUpdate(BaseModel):
    slug: str
    target_url: str | None = None
    title: str | None = None
    palette: str | None = None
    active: bool | None = None

PALETTES = {
    # dark modules on light label for max readability; gradients live under-frame
    "neon-orchid": {"fg":"#0b0b10","bg":"#fafbfd","accent":"#ff8cff"},
    "miami":       {"fg":"#0a0a0a","bg":"#ffffff","accent":"#00ffd4"},
    "cathd-grit":  {"fg":"#0a0a0a","bg":"#f7f7f7","accent":"#ff6a00"},  # your orange
}

def _choose_palette(name:str|None, fg:str|None, bg:str|None):
    if name and name in PALETTES: p = PALETTES[name].copy()
    else: p = PALETTES["cathd-grit"].copy()
    if fg: p["fg"]=fg
    if bg: p["bg"]=bg
    return p

def _make_qr_png(data:str, size:int, fg:str, bg:str):
    qr = qrcode.QRCode(
        version=None,
        box_size=max(2, size//220),
        border=2,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color=fg, back_color=bg).convert("RGBA")
    return img

def _vinyl_board(width:int, height:int, accent:str):
    # gradient slab with subtle grit + grooves frame
    img = Image.new("RGBA", (width, height), (0,0,0,0))
    base = Image.new("RGBA", (width, height), (18,18,22,255))
    # simple left->right gradient to echo your UI
    grad = Image.linear_gradient("L").resize((width,1)).resize((width,height))
    tint = Image.new("RGBA", (width,height), tuple(int(c,16) for c in (accent[1:3],accent[3:5],accent[5:7])) + (255,))
    grad_col = Image.composite(tint, base, grad)
    slab = Image.blend(base, grad_col, 0.22)

    # rounded panel
    panel = Image.new("RGBA",(width-40,height-40),(0,0,0,0))
    draw = ImageDraw.Draw(panel)
    draw.rounded_rectangle([0,0,width-40,height-40], radius=28, outline=(255,255,255,40), width=3, fill=(255,255,255,6))
    panel = panel.filter(ImageFilter.GaussianBlur(0.5))

    slab.alpha_composite(panel, (20,20))

    # vinyl “grooves” behind the QR area (subtle)
    g = ImageDraw.Draw(slab)
    cx, cy = width//2, height//2
    for r in range(70, min(cx,cy)-25, 7):
        a = 22  # alpha
        g.ellipse([cx-r, cy-r, cx+r, cy+r], outline=(255,255,255,a))
    return slab

def _compose_vinyl_qr(target_url:str, size:int, palette:dict, label:str|None):
    W = H = size
    board = _vinyl_board(W,H, palette["accent"])
    # center label
    label_r = int(W*0.30)
    center = Image.new("RGBA",(label_r*2,label_r*2),(0,0,0,0))
    d=ImageDraw.Draw(center)
    d.ellipse([0,0,2*label_r,2*label_r], fill=palette["bg"], outline=(20,20,26,80), width=6)

    # QR as square set into the label
    qr_size = int(label_r*1.6)
    qr_img = _make_qr_png(target_url, qr_size, fg=palette["fg"], bg=palette["bg"])
    # paste qr into a square hole centered
    qr_pos = (label_r - qr_img.width//2, label_r - qr_img.height//2)
    center.alpha_composite(qr_img, qr_pos)

    # mount center on board
    board.alpha_composite(center, (W//2 - label_r, H//2 - label_r))

    # slight grit/noise (safe)
    noise = Image.effect_noise((W,H), 6).convert("L")
    noise = Image.merge("RGBA", (noise,noise,noise, noise.point(lambda a: a*0.08)))
    board = Image.alpha_composite(board, noise)

    # optional title strip (bottom-left)
    if label:
        strip = Image.new("RGBA",(int(W*0.7), 52),(0,0,0,0))
        dd = ImageDraw.Draw(strip)
        dd.rounded_rectangle([0,0,strip.width,52], 16, fill=(0,0,0,120))
        dd.text((18,14), label, fill=(255,255,255,220))
        board.alpha_composite(strip, (24, H-24-52))

    return board

@qr.get("/{slug}.png")
def qr_image(slug:str,
             size:int=Query(1024, ge=300, le=2000),
             palette:str|None=None,
             fg:str|None=None, bg:str|None=None,
             label:str|None=None):
    c = DB.cursor()
    row = c.execute("SELECT target_url, palette, active FROM qr_links WHERE slug=?", (slug,)).fetchone()
    if not row: raise HTTPException(404, "Unknown slug")
    target_url, saved_palette, active = row
    if not active: raise HTTPException(403, "Slug inactive")
    pal = _choose_palette(palette or saved_palette, fg, bg)
    img = _compose_vinyl_qr(f"/api/qr/go/{slug}", size, pal, label)
    out = io.BytesIO()
    img.save(out, format="PNG")
    return Response(out.getvalue(), media_type="image/png")

@qr.get("/go/{slug}")
def go(slug:str, user_agent:str|None=None, x_forwarded_for:str|None=None, referer:str|None=None):
    c = DB.cursor()
    row = c.execute("SELECT target_url, active FROM qr_links WHERE slug=?", (slug,)).fetchone()
    if not row: raise HTTPException(404, "Unknown slug")
    target_url, active = row
    if not active: raise HTTPException(403, "Slug inactive")

    # log (coarse hashed IP if provided via proxy headers)
    ip = (x_forwarded_for or "").split(",")[0].strip()
    iphash = hashlib.sha1(ip.encode()).hexdigest()[:10] if ip else None
    DB.execute("INSERT INTO qr_scans(slug, ts, ua, iphash, ref) VALUES(?,?,?,?,?)",
               (slug, int(time.time()), user_agent, iphash, referer))
    DB.commit()
    # Redirect out
    return RedirectResponse(target_url, status_code=302)

@qr.post("/create")
def create_link(body:QRCreate):
    DB.execute("INSERT OR REPLACE INTO qr_links(slug, target_url, title, palette, active, created_at, updated_at) "
               "VALUES(?,?,?,?,?,?,?)",
               (body.slug, body.target_url, body.title, body.palette, 1 if body.active else 0, int(time.time()), int(time.time())))
    DB.commit()
    return {"ok": True, "slug": body.slug}

@qr.post("/update")
def update_link(body:QRUpdate):
    row = DB.execute("SELECT slug FROM qr_links WHERE slug=?", (body.slug,)).fetchone()
    if not row: raise HTTPException(404, "Unknown slug")
    fields, vals = [], []
    for k in ("target_url","title","palette"):
        v = getattr(body, k)
        if v is not None:
            fields.append(f"{k}=?"); vals.append(v)
    if body.active is not None:
        fields.append("active=?"); vals.append(1 if body.active else 0)
    fields.append("updated_at=?"); vals.append(int(time.time()))
    vals.append(body.slug)
    DB.execute(f"UPDATE qr_links SET {', '.join(fields)} WHERE slug=?", vals)
    DB.commit()
    return {"ok": True}

@qr.get("/sheet.png")
def sheet(slugs:str, cols:int=3, rows:int=4, margin:int=40, cell:int=700, palette:str|None=None):
    ids = [s.strip() for s in slugs.split(",") if s.strip()]
    W = cols*cell + (cols+1)*margin
    H = rows*cell + (rows+1)*margin
    sheet = Image.new("RGBA",(W,H),(255,255,255,255))
    c=0
    for r in range(rows):
        for col in range(cols):
            if c >= len(ids): break
            slug = ids[c]
            c += 1
            # reuse single image endpoint renderer
            row = DB.execute("SELECT target_url, palette, active, title FROM qr_links WHERE slug=?", (slug,)).fetchone()
            if not row: continue
            target_url, saved_palette, active, title = row
            pal = _choose_palette(palette or saved_palette, None, None)
            img = _compose_vinyl_qr(f"/api/qr/go/{slug}", cell, pal, title or slug)
            x = margin + col*(cell+margin)
            y = margin + r*(cell+margin)
            sheet.alpha_composite(img, (x,y))
    out = io.BytesIO()
    sheet.convert("RGB").save(out, format="PNG")
    return Response(out.getvalue(), media_type="image/png")
# --- mount router
app.include_router(qr)
# ---------------------------------------------------------------------------

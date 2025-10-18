#!/usr/bin/env python3
import argparse, json, os, pathlib, shutil, zipfile, re, random

ROOT = pathlib.Path(".").resolve()
PUB  = ROOT/"v3"/"frontend"/"public"
DATA = ROOT/"content"/"data"
GIFT = ROOT/"gift"
EXPO = ROOT/"exports"

THEMES = {
    "4boss": {"name":"4Boss","theme":"#ff8a00","accent":"#ffb84d","bg":"#130a03","icon":"icons/app_orange.svg"},
    "4mmi":  {"name":"4Mmi" ,"theme":"#2fcf6b","accent":"#19a95c","bg":"#08140d","icon":"icons/app_green.svg"},
    "4cbo":  {"name":"4Cbo" ,"theme":"#ffffff","accent":"#e6f5ff","bg":"#0a0a0a","icon":"icons/app_white.svg"},
    "dan":   {"name":"4Dan" ,"theme":"#d14fff","accent":"#ff7ee6","bg":"#0a0712","icon":"icons/app_pink.svg"},
    "opal":  {"name":"4Opal","theme":"#77F0E1","accent":"#B8F3FF","bg":"#0A0F12","icon":"icons/app_white.svg"},
    "danfun":{"name":"4Dan","theme":"#FF8AD9","accent":"#FFD580","bg":"#FFF5F8","icon":"icons/app_pink.svg"}
}

def copy_tree(src, dst):
    if dst.exists(): shutil.rmtree(dst)
    shutil.copytree(src, dst)

def default_tagline():
    fp = DATA/"taglines.json"
    if fp.exists():
        try:
            tags = json.loads(fp.read_text())
            if isinstance(tags, list) and tags:
                return str(tags[-1])
        except: pass
    return "Cbo Mmi- JuiceLuv"

def make_gift(tag, to, theme_key, note, tagline):
    theme = THEMES.get(theme_key.lower(), THEMES["dan"])
    tag_dir = GIFT/tag
    web_dir = tag_dir/"web"
    copy_tree(PUB, web_dir)

    # rewrite manifest name/theme/icon for this gift
    mf = json.loads((web_dir/"manifest.webmanifest").read_text())
    mf["name"] = mf["short_name"] = theme["name"]
    mf["theme_color"] = theme["theme"]
    mf["background_color"] = theme["bg"]
    (web_dir/"manifest.webmanifest").write_text(json.dumps(mf, indent=2))

    # swap icon in index
    idx_path = web_dir/"index.html"
    idx = idx_path.read_text()
    idx = re.sub(r'href="\.\/icons\/[^"]+\.svg"', 'href="./%s"' % theme["icon"], idx)
    idx_path.write_text(idx)

    # bake the splash with your note + tagline
    gift_path = web_dir/"gift.html"
    gift_html = gift_path.read_text()
    gift_html = gift_html.replace('const to = q.get("to") || "you";', 'const to = %s;' % json.dumps(to))
    gift_html = gift_html.replace('const msg = q.get("msg") || "Open me — there’s a crate inside, with a note on the label just for you.";', 'const msg = %s;' % json.dumps(note))
    gift_html = gift_html.replace('const tag = q.get("tagline") || "Cbo Mmi- JuiceLuv";', 'const tag = %s;' % json.dumps(tagline))
    gift_path.write_text(gift_html)

    # snapshot playlists into tag dir (immutable)
    snap_dir = tag_dir/"content"/"data"
    snap_dir.mkdir(parents=True, exist_ok=True)
    for name in ["playlist_8.json", "playlist_16.json", "playlist_all.json", "library.json", "taglines.json"]:
        src = DATA/name
        if src.exists(): shutil.copy2(src, snap_dir/name)

    # make an exports zip with tracks + portable player
    zpath = EXPO/f"{tag}_offgrid.zip"
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
        for p in ["index.html","app.js","style.css","service-worker.js","manifest.webmanifest","gift.html"]:
            z.write(web_dir/p, arcname=f"player/{p}")
        for ic in (web_dir/"icons").glob("*.svg"):
            z.write(ic, arcname=f"player/icons/{ic.name}")
        for js in snap_dir.glob("*.json"):
            z.write(js, arcname=f"content/data/{js.name}")
        z.writestr("README.txt", "Open player/index.html in any browser.\nPut your MP3s in offgrid-crates/ and keep the same filenames as the JSON.\n")
    return tag_dir, zpath

def main():
    ap = argparse.ArgumentParser(description="Freeze a gift build (PWA) + off-grid zip.")
    ap.add_argument("--tag", required=True, help="gift tag, e.g. gift-v1-mmi")
    ap.add_argument("--to",  required=True, help="recipient label: Mmi / Cbo / Boss / Dan")
    ap.add_argument("--theme", default="dan", help="4mmi / 4cbo / 4boss / dan / opal / danfun")
    ap.add_argument("--note", default="Open me — there’s a crate inside, with a note on the label just for you.")
    ap.add_argument("--tagline", default=None, help="center-label text on the vinyl")
    args = ap.parse_args()

    tag = args.tag
    to = args.to
    theme = args.theme
    note = args.note
    tagline = args.tagline or default_tagline()

    tag_dir, zpath = make_gift(tag, to, theme, note, tagline)
    print(f"✅ Gift built → {tag_dir}/web  |  Export ZIP → {zpath}")
    print(f"Netlify URL will be:  /gift/{tag}/  (after deploy)")
if __name__ == "__main__": main()

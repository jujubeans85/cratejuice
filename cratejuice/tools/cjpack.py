#!/usr/bin/env python3
import argparse, json, pathlib, shutil, zipfile, re
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

def default_tagline():
    p = DATA/"taglines.json"
    if p.exists():
        try:
            arr = json.loads(p.read_text())
            if isinstance(arr, list) and arr:
                return str(arr[-1])  # last line wins
        except:
            pass
    return "Cbo Mmi- JuiceLuv"

def copy_tree(src, dst):
    if dst.exists(): shutil.rmtree(dst)
    shutil.copytree(src, dst)

def make_gift(tag, to, theme_key, note, tagline):
    theme = THEMES.get(theme_key.lower(), THEMES["dan"])
    tag_dir = GIFT/tag
    web_dir = tag_dir/"web"
    copy_tree(PUB, web_dir)

    # rewrite manifest theme/name/icon
    mf = json.loads((web_dir/"manifest.webmanifest").read_text())
    mf["name"] = mf["short_name"] = theme["name"]
    mf["theme_color"] = theme["theme"]
    mf["background_color"] = theme["bg"]
    (web_dir/"manifest.webmanifest").write_text(json.dumps(mf, indent=2))

    # swap icon href in index
    idxp = web_dir/"index.html"
    idx = idxp.read_text()
    idx = re.sub(r'href="\.\/icons\/[^"]+\.svg"', f'href="./{theme["icon"]}"', idx)
    idxp.write_text(idx)

    # bake splash defaults
    gp = web_dir/"gift.html"
    html = gp.read_text()
    html = html.replace('const to = q.get("to") || "you";', f'const to = {json.dumps(to)};')
    html = html.replace('const msg = q.get("msg") || "Open me — there’s a crate inside, with a note on the label just for you.";', f'const msg = {json.dumps(note)};')
    html = html.replace('const tag = q.get("tagline") || "Cbo Mmi- JuiceLuv";', f'const tag = {json.dumps(tagline)};')
    gp.write_text(html)

    # snapshot JSON for immutability
    snap = tag_dir/"content"/"data"
    snap.mkdir(parents=True, exist_ok=True)
    for name in ["playlist_8.json","playlist_16.json","playlist_all.json","library.json","taglines.json"]:
        src = DATA/name
        if src.exists(): shutil.copy2(src, snap/name)

    # export portable player zip
    zpath = EXPO/f"{tag}_offgrid.zip"
    with zipfile.ZipFile(zpath,"w",zipfile.ZIP_DEFLATED) as z:
        for p in ["index.html","app.js","style.css","service-worker.js","manifest.webmanifest","gift.html"]:
            z.write(web_dir/p, arcname=f"player/{p}")
        for ic in (web_dir/"icons").glob("*.svg"):
            z.write(ic, arcname=f"player/icons/{ic.name}")
        for js in snap.glob("*.json"):
            z.write(js, arcname=f"content/data/{js.name}")
        z.writestr("README.txt","Open player/index.html in any browser.\nPut MP3s in offgrid-crates/ with same filenames as content/data JSON.\n")
    return tag_dir, zpath

def main():
    import argparse
    ap = argparse.ArgumentParser(description="Freeze a gift build (PWA) + off-grid zip.")
    ap.add_argument("--tag", required=True, help="gift tag, e.g. gift-dan-01")
    ap.add_argument("--to", required=True, help="recipient label")
    ap.add_argument("--theme", default="dan", help="4mmi / 4cbo / 4boss / dan / opal / danfun")
    ap.add_argument("--note", default="Open me — there’s a crate inside, with a note on the label just for you.")
    ap.add_argument("--tagline", default=None, help="center-label text on the vinyl (optional)")
    args = ap.parse_args()
    tag = args.tag; to=args.to; theme=args.theme; note=args.note
    tagline = args.tagline or default_tagline()
    tag_dir, zpath = make_gift(tag, to, theme, note, tagline)
    print(f"✅ Gift built → {tag_dir}/web  |  Export ZIP → {zpath}")
    print(f"Netlify route after deploy:  /gift/{tag}/")
if __name__ == "__main__": main()

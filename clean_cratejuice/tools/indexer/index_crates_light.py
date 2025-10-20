import json, pathlib
root = pathlib.Path(".").resolve()
crate_dir = root/"offgrid-crates"
outdir = root/"content"/"data"
outdir.mkdir(parents=True, exist_ok=True)
tracks=[]
for p in sorted(crate_dir.glob("*.mp3")):
    tracks.append({"id":p.stem, "title":p.stem, "artist":"", "file":f"../../offgrid-crates/{p.name}", "cover":"../public/cover_default.png"})
(outdir/"library.json").write_text(json.dumps({"tracks":{t["id"]:t for t in tracks}}, indent=2))
(outdir/"playlist_8.json").write_text(json.dumps(tracks[:8], indent=2))
(outdir/"playlist_16.json").write_text(json.dumps(tracks[:16], indent=2))
(outdir/"playlist_all.json").write_text(json.dumps(tracks, indent=2))
print(f"Indexed {len(tracks)} → {outdir}")

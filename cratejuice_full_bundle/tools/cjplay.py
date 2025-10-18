#!/usr/bin/env python3
import argparse, json, os, pathlib, random, shutil, subprocess, sys, time

ROOT = pathlib.Path(".").resolve()
DATA = ROOT/"content"/"data"

def which(cmd): return shutil.which(cmd) is not None

def load_playlist(path):
    js = json.loads(path.read_text())
    return js if isinstance(js, list) else js.get("tracks", [])

def play_ffplay(path, rate):
    cmd = ["ffplay","-nodisp","-autoexit","-loglevel","quiet"]
    if rate and rate!=1.0:
        at = max(0.5, min(2.0, rate))
        cmd += ["-af", f"atempo={at}"]
    cmd += [path]
    return subprocess.call(cmd)

def play_mpg123(path, rate):
    cents = int(1200*(rate-1.0))
    cmd = ["mpg123"]
    if cents: cmd += ["--pitch", str(cents)]
    cmd += [path]
    return subprocess.call(cmd)

def main():
    ap = argparse.ArgumentParser(description="CrateJuice terminal player (no browser).")
    ap.add_argument("--playlist", default=str(DATA/"playlist_8.json"))
    ap.add_argument("--surprise", type=int, default=12, help="% chaos jumps (0-100)")
    ap.add_argument("--rate", type=float, default=1.0, help="playback rate 0.5..1.5")
    args = ap.parse_args()

    tracks = load_playlist(pathlib.Path(args.playlist))
    if not tracks:
        print("No tracks found. Drop MP3s into offgrid-crates/ and index first.")
        sys.exit(1)

    print(f"⚓ CJ/CLI — {len(tracks)} tracks | surprise {args.surprise}% | rate {args.rate:.2f}x")
    order = list(range(len(tracks)))
    i=0
    while True:
        if random.random()*100 < args.surprise and len(order)>1:
            i = random.randrange(0, len(order))
        t = tracks[order[i]]
        src = t.get("file") or t.get("path") or ""
        title = t.get("title") or os.path.basename(src)
        print(f"\n▶ {i+1:02d}/{len(order)}  {title}")

        path = src
        if not os.path.exists(path):
            candidate = ROOT / src
            path = str(candidate)

        played=False
        if which("ffplay"):
            play_ffplay(path, args.rate); played=True
        elif which("mpg123"):
            play_mpg123(path, args.rate); played=True
        else:
            print("No ffplay or mpg123 found. Install one to hear audio.")
            time.sleep(2)

        i = (i+1) % len(order)

if __name__ == "__main__": main()

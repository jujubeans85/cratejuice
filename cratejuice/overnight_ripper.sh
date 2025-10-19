#!/bin/bash
# CrateJuice overnight ripper

CRATE="$HOME/cratejuice/offgrid-crates"
LIST="$HOME/cratejuice/content/data/riplist.txt"

mkdir -p "$CRATE"

while true; do
  echo "🔄 Checking $LIST at $(date)"
  if [ -f "$LIST" ]; then
    while IFS= read -r url; do
      [ -z "$url" ] && continue
      [[ "$url" =~ ^# ]] && continue
      echo "🎵 Ripping: $url"
      if ! yt-dlp --extract-audio --audio-format mp3 \
        -o "$CRATE/%(title)s.%(ext)s" "$url"; then
        echo "⚠️ Failed to download: $url"
      fi
    done < "$LIST"
  fi
  cd "$HOME/cratejuice" || { echo "Failed to change directory"; continue; }
  ./crate_run.sh
  echo "✅ Indexed at $(date)"
  sleep 600   # every 10 min
done

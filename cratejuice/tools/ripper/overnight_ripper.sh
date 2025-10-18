#!/bin/bash
set -e

echo "🌙 Overnight ripper running..."
LOGFILE="run.log"

while true; do
  echo "=== $(date) Checking riplist ===" | tee -a "$LOGFILE"

  # Make sure riplist exists
  if [ ! -f content/data/riplist.txt ]; then
    echo "No riplist.txt found. Create content/data/riplist.txt with URLs." | tee -a "$LOGFILE"
  else
    # Rip new tracks
    yt-dlp -x --audio-format mp3 -o "offgrid-crates/%(title)s.%(ext)s" -a content/data/riplist.txt | tee -a "$LOGFILE"

  echo "Sleeping 10 minu
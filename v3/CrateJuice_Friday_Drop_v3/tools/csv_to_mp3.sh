#!/bin/sh
set -eu

usage() {
  cat <<'EOF'
Usage:
  sh csv_to_mp3.sh <csv_or_txt> [output_dir]

Examples:
  sh csv_to_mp3.sh soundcloud_list.csv "$HOME/Documents/CRATE/MP3"
  DRY_RUN=1 sh csv_to_mp3.sh soundcloud_list.csv

Environment:
  YTDLP_BIN  downloader command (default: yt-dlp)
  DRY_RUN    set to 1 to print commands without downloading
EOF
}

fail() {
  printf 'ERROR: %s\n' "$*" >&2
  exit 1
}

[ "${1:-}" != "" ] || { usage; exit 64; }
[ "${1:-}" != "-h" ] && [ "${1:-}" != "--help" ] || { usage; exit 0; }

src=$1
out=${2:-"$HOME/Documents/CRATE/MP3"}
ytdlp=${YTDLP_BIN:-yt-dlp}

[ -f "$src" ] || fail "input file not found: $src"
mkdir -p "$out" || fail "cannot create output directory: $out"

if [ "${DRY_RUN:-0}" != "1" ] && ! command -v "$ytdlp" >/dev/null 2>&1; then
  fail "$ytdlp not found. Install yt-dlp first, or set YTDLP_BIN."
fi

tmp_base=${TMPDIR:-/tmp}/cratejuice_urls_$$
tmp_raw=${tmp_base}.raw
tmp_urls=${tmp_base}.urls
trap 'rm -f "$tmp_raw" "$tmp_urls"' EXIT HUP INT TERM

# Extract every HTTP(S) URL regardless of CSV column order. This avoids brittle
# comma splitting when titles themselves contain commas or quoted fields.
awk '
{
  line=$0
  sub(/^\xef\xbb\xbf/, "", line)
  gsub(/\r/, "", line)
  while (match(line, /https?:\/\/[^\",[:space:]]+/)) {
    print substr(line, RSTART, RLENGTH)
    line=substr(line, RSTART + RLENGTH)
  }
}
' "$src" > "$tmp_raw"

awk '!seen[$0]++' "$tmp_raw" > "$tmp_urls"
count=$(awk 'END { print NR+0 }' "$tmp_urls")
[ "$count" -gt 0 ] || fail "no HTTP(S) URLs found in: $src"

printf 'CRATEJUICE: %s unique URL(s) -> %s\n' "$count" "$out"

ok=0
failed=0
while IFS= read -r url || [ -n "$url" ]; do
  [ -n "$url" ] || continue
  if [ "${DRY_RUN:-0}" = "1" ]; then
    printf '%s\n' "$ytdlp -x --audio-format mp3 --audio-quality 0 -o $out/%(title)s.%(ext)s $url"
    ok=$((ok + 1))
    continue
  fi

  printf '\n[%s/%s] %s\n' "$((ok + failed + 1))" "$count" "$url"
  if "$ytdlp" \
      -x \
      --audio-format mp3 \
      --audio-quality 0 \
      --no-playlist \
      --continue \
      --no-overwrites \
      -o "$out/%(title)s.%(ext)s" \
      "$url"; then
    ok=$((ok + 1))
  else
    failed=$((failed + 1))
    printf 'FAILED: %s\n' "$url" >&2
  fi
done < "$tmp_urls"

printf '\nDONE: %s succeeded, %s failed.\n' "$ok" "$failed"
[ "$failed" -eq 0 ] || exit 2

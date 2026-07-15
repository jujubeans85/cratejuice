# Tools

## 1) SoundCloud → CSV (bookmarklet)
- Create a new bookmark and set its URL to the contents of `sc_extractor_bookmarklet.txt` (starts with `javascript:`).
- Open your SoundCloud list/likes page and click the bookmarklet.
- It auto-scrolls, scrapes titles + URLs, then downloads `soundcloud_list.csv`.

Alternative: open DevTools Console and paste `sc_extractor_console.js`.

## 2) CSV → MP3 in A-Shell / macOS (recommended)

Use the portable shell runner:

```sh
sh csv_to_mp3.sh soundcloud_list.csv "$HOME/Documents/CRATE/MP3"
```

Test the CSV without downloading anything:

```sh
DRY_RUN=1 sh csv_to_mp3.sh soundcloud_list.csv "$HOME/Documents/CRATE/MP3"
```

Requirements:
- `yt-dlp` must be available in A-Shell/macOS.
- Accepts CSV in any column order or a plain text file containing URLs.
- Handles quoted titles containing commas.
- Removes duplicate URLs.
- Creates the output folder automatically.
- Continues past failed downloads and reports the final success/failure count.
- Defaults to `$HOME/Documents/CRATE/MP3` when the output directory is omitted.

## 3) CSV → MP3 with Python (legacy desktop fallback)
Requires Python 3.11+ and `yt-dlp`.

```bash
pip install -U yt-dlp
python csv_to_mp3.py soundcloud_list.csv out_mp3/
```

- Accepts CSV with a `url` column **or** a plain text file of URLs (one per line).
- Writes MP3s into the output folder, with clean filenames.

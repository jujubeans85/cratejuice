# Tools

## 1) SoundCloud → CSV (bookmarklet)
- Create a new bookmark and set its URL to the contents of `sc_extractor_bookmarklet.txt` (starts with `javascript:`).
- Open your SoundCloud list/likes page and click the bookmarklet.
- It auto-scrolls, scrapes titles + URLs, then downloads `soundcloud_list.csv`.

Alternative: open DevTools Console and paste `sc_extractor_console.js`.

## 2) CSV → MP3 (offline downloader)
Requires Python 3.11+ and `yt-dlp`.

```bash
pip install -U yt-dlp
python csv_to_mp3.py soundcloud_list.csv out_mp3/
```

- Accepts CSV with a `url` column **or** a plain text file of URLs (one per line).
- Writes MP3s into the output folder, with clean filenames.

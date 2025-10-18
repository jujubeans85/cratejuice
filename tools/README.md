# CrateJuice Tools

This directory contains utility scripts for CrateJuice.

## qr_postcard.py

Generate QR code postcards from CrateJuice playlists.

### Usage

```bash
python3 tools/qr_postcard.py --playlist content/data/playlist_8.json \
                              --out postcards/playlist_8.pdf \
                              --title "CrateJuice v0"
```

### Arguments

- `--playlist`: Path to the playlist JSON file (required)
- `--out`: Output path for the PDF postcard (required)
- `--title`: Title for the postcard (optional, defaults to playlist title)

### Dependencies

The script requires the following Python packages:
- qrcode
- reportlab
- Pillow

Install them with:
```bash
pip3 install qrcode[pil] reportlab Pillow
```

### Playlist JSON Format

The playlist JSON should have the following structure:

```json
{
  "playlist_id": 8,
  "title": "CrateJuice v0",
  "description": "An awesome collection of tracks",
  "tracks": [
    {
      "id": 1,
      "title": "Track Title",
      "artist": "Artist Name",
      "url": "https://www.youtube.com/watch?v=...",
      "duration": "3:32"
    }
  ]
}
```

### Output

The script generates a PDF postcard with:
- Playlist title and description
- QR codes for each track URL
- Track information (title, artist, duration, URL)
- Professional formatting suitable for printing

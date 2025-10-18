# CrateJuice - Offline Music Indexer

This directory contains the CrateJuice offline music management system.

## Components

### Scripts

- **crate_run.sh** - Indexes MP3 files in `offgrid-crates/` and generates JSON playlists
- **overnight_ripper.sh** - Automated music downloader that runs continuously

### Tools

- **cjpack.py** - Creates gift packages
- **cjplay.py** - Plays crates

### Directories

- **offgrid-crates/** - Storage for MP3 files
- **content/data/** - Generated JSON playlists and configuration files
- **apps/indexer/** - Indexing application

## Usage

### Manual Indexing

To index MP3 files manually:

```bash
./crate_run.sh
```

This will:
1. Create the necessary directories
2. Index all MP3 files in `offgrid-crates/`
3. Generate JSON playlists in `content/data/`

### Overnight Ripper (Automated Downloads)

The overnight ripper automatically downloads music from URLs and indexes them:

```bash
./overnight_ripper.sh
```

**How it works:**
1. Reads URLs from `content/data/riplist.txt`
2. Downloads audio using `yt-dlp` (extracts audio as MP3)
3. Saves files to `offgrid-crates/`
4. Runs `crate_run.sh` to index the new files
5. Repeats every 10 minutes

**Setup:**
1. Install yt-dlp: `pip install yt-dlp` or `sudo apt install yt-dlp`
2. Add URLs to `content/data/riplist.txt` (one URL per line)
3. Run the script: `./overnight_ripper.sh`

**Example riplist.txt:**
```
https://www.youtube.com/watch?v=dQw4w9WgXcQ
https://soundcloud.com/artist/track
```

**Note:** The script runs in an infinite loop. To stop it, press Ctrl+C or kill the process.

## Requirements

- Python 3
- yt-dlp (for overnight_ripper.sh)

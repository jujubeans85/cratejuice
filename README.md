# Crate Juice v3

🧃 A modern, lightweight framework for music crates and audio playback with PWA support.

## Project Structure

```
cratejuice/           # Main production application
├── v3/frontend/public/  # PWA frontend with player, gifts, themes
├── apps/indexer/     # Track indexing tool
├── apps/ripper/      # Audio ripping tool
├── tools/            # CLI tools (cjpack, cjplay)
├── content/data/     # Playlists and track library
└── offgrid-crates/   # MP3 storage directory

v3/                   # Simple starter template (optional)
├── frontend/         # Basic HTML/CSS/JS example
└── backend/          # Flask API starter (optional)

apps/ripper/          # Convenience ripper wrapper
addurl                # Quick URL addition script
cjrip                 # Overnight ripper launcher
deploy.sh             # Production deployment helper
```

## Features

- ⚡ **Fast** - Optimized for performance
- 🎨 **Modern** - Clean and responsive design
- 🔧 **Flexible** - Easy to customize

## Getting Started

### Production Application (cratejuice/)

The main production-ready application with full PWA support:

```bash
# Run the deployment preparation
./deploy.sh

# Or manually index tracks and test
cd cratejuice
./crate_run.sh
python3 tools/cjplay.py --surprise 12
```

#### Adding Music

```bash
# Add URLs to rip (YouTube, SoundCloud, etc.)
./addurl "https://youtube.com/watch?v=VIDEO_ID"

# Or start the overnight ripper
./cjrip
```

#### Local Development

Serve the production frontend locally:

```bash
cd cratejuice/v3/frontend/public
python -m http.server 8000
```

Then visit `http://localhost:8000`

### Simple Starter Template (v3/)

A minimal example for learning - static HTML/CSS/JS frontend with optional Flask backend:

#### Frontend
```bash
cd v3/frontend
python -m http.server 8000
```

#### Backend (Optional)
```bash
cd v3/backend
pip install -r requirements.txt
python main.py
```

## Deployment

### Production Frontend (Netlify)

The main application deploys to Netlify from the `cratejuice/v3/frontend/public/` directory:

```bash
netlify deploy --prod --dir=cratejuice/v3/frontend/public
```

Configuration is in `netlify.toml` at the repository root.

### Optional Backend (Render)

The simple v3 backend starter can be deployed to Render if needed, though the production app is fully static and doesn't require it.

## License

© 2025 Crate Juice. All rights reserved.

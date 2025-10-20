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
- 📱 **iOS App Support** - Progressive Web App (PWA) installable on iOS devices

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

### GitHub Pages

The project includes a GitHub Actions workflow that automatically deploys to GitHub Pages on push to the main branch.

## 🚀 Quick Start

### Setup and Deploy
Run the setup script to prepare for deployment:
```bash
./setup-deployment.sh
```

This will verify all prerequisites and guide you through the deployment process.

## 📱 iOS App Installation

CrateJuice can be installed as a native-like app on iOS devices! See [iOS-INSTALLATION.md](iOS-INSTALLATION.md) for detailed instructions on how to:

- Install the PWA on iPhone/iPad
- Use the app like a native application
- Access offline features
- Troubleshoot common issues

**Quick Start for iOS:**
1. Open the deployed site in Safari on your iOS device
2. Tap the Share button
3. Select "Add to Home Screen"
4. Enjoy CrateJuice as a standalone app!

## 📖 Documentation

- **[iOS-INSTALLATION.md](iOS-INSTALLATION.md)** - Complete guide for installing on iOS devices
- **[DEPLOYMENT-GUIDE.md](DEPLOYMENT-GUIDE.md)** - Deployment options and configuration
- **[PRODUCTION.md](PRODUCTION.md)** - Production deployment checklist

## License

© 2025 Crate Juice. All rights reserved.

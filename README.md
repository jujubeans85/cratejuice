# Crate Juice v3

🧃 A modern, lightweight framework for building amazing web applications.

## Project Structure

```
v3/
├── frontend/          # Frontend application
│   ├── index.html    # Main HTML file
│   ├── style.css     # Styles
│   └── app.js        # JavaScript
└── backend/          # Backend API
    ├── main.py       # Flask application
    ├── requirements.txt
    └── render.yaml   # Render deployment config
```

## Features

- ⚡ **Fast** - Optimized for performance
- 🎨 **Modern** - Clean and responsive design
- 🔧 **Flexible** - Easy to customize
- 📱 **iOS App Support** - Progressive Web App (PWA) installable on iOS devices

## Getting Started

### Frontend

The frontend is a static web application that can be opened directly in a browser or served by any web server.

#### Local Development

Simply open `v3/frontend/index.html` in your browser, or use a local server:

```bash
cd v3/frontend
python -m http.server 8000
```

Then visit `http://localhost:8000`

### Backend

The backend is a Flask API server.

#### Installation

```bash
cd v3/backend
pip install -r requirements.txt
```

#### Running the Server

```bash
python main.py
```

The API will be available at `http://localhost:5000`

#### API Endpoints

- `GET /` - Welcome message
- `GET /api/health` - Health check
- `GET /api/features` - Get framework features
- `GET /api/info` - Get framework information

## Deployment

### Frontend (Netlify)

The frontend is configured to deploy on Netlify. The `netlify.toml` file contains the build configuration.

### Backend (Render)

The backend is configured to deploy on Render using the `render.yaml` configuration file.

### GitHub Pages

The project includes a GitHub Actions workflow that automatically deploys to GitHub Pages on push to the main branch.

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

## License

© 2025 Crate Juice. All rights reserved.

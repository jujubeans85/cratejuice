# Copilot Instructions for Crate Juice

## Project Overview

Crate Juice v3 is a modern, lightweight web framework featuring:
- A Python Flask backend API
- A vanilla JavaScript frontend (no framework dependencies)
- Simple deployment to Netlify (frontend) and Render (backend)

**Target Audience**: Web developers looking for a simple, performant framework
**Platform**: Web (Flask backend + vanilla JS frontend)

## Project Structure

```
cratejuice/
├── v3/                      # Main v3 application
│   ├── backend/            # Flask API server
│   │   ├── main.py        # Main Flask application
│   │   ├── requirements.txt
│   │   └── render.yaml    # Render deployment config
│   └── frontend/          # Static web application
│       ├── index.html     # Main HTML file
│       ├── style.css      # Styles
│       └── app.js         # JavaScript application
├── netlify.toml           # Netlify deployment config
└── README.md              # Project documentation
```

## Build & Test Commands

### Backend (Python Flask)

```bash
# Install dependencies
cd v3/backend
pip install -r requirements.txt

# Run development server
python main.py

# Test endpoints manually
curl http://localhost:5000/
curl http://localhost:5000/api/health
curl http://localhost:5000/api/features
curl http://localhost:5000/api/info
```

### Frontend (Vanilla JS)

```bash
# Serve locally for testing
cd v3/frontend
python -m http.server 8000

# Open in browser
# Visit http://localhost:8000
```

No build step required - the frontend is static HTML/CSS/JS.

## Coding Conventions

### Python (Backend)

- **Style**: Follow PEP 8 standards
- **Formatting**: Use 4 spaces for indentation
- **Docstrings**: Include docstrings for all functions and classes
- **Imports**: Group imports (standard library, third-party, local)
- **Error Handling**: Use appropriate HTTP status codes and JSON error responses
- **CORS**: Enabled for all endpoints via flask-cors

### JavaScript (Frontend)

- **Style**: Modern ES6+ JavaScript
- **Formatting**: Use 2 spaces for indentation
- **Naming**: 
  - Variables and functions: camelCase
  - Constants: UPPER_CASE
- **Comments**: Use clear, concise comments for complex logic
- **DOM Manipulation**: Use vanilla JavaScript (no jQuery or frameworks)
- **API Calls**: Use fetch() for async HTTP requests

### HTML/CSS

- **HTML**: Use semantic HTML5 elements
- **CSS**: 
  - Use CSS custom properties (variables) for theming
  - Follow BEM or similar naming convention for classes
  - Mobile-first responsive design
- **Accessibility**: Include proper ARIA labels and semantic elements

## API Conventions

All API endpoints return JSON:
- Success responses include relevant data
- Include descriptive field names
- Use proper HTTP status codes:
  - 200: Successful GET/PUT requests
  - 201: Successful POST (created)
  - 400: Bad request
  - 404: Not found
  - 500: Server error

## Deployment

### Frontend
- **Platform**: Netlify
- **Config**: `netlify.toml` in root
- **Build**: None required (static site)
- **Publish directory**: `v3/frontend`

### Backend
- **Platform**: Render
- **Config**: `v3/backend/render.yaml`
- **Runtime**: Python 3.11+
- **Environment Variables**:
  - `PORT`: Server port (default: 5000)
  - `FLASK_DEBUG`: Debug mode (default: False)

## Dependencies

### Backend
- Flask 3.0.0 - Web framework
- flask-cors 4.0.0 - CORS support
- gunicorn 22.0.0 - Production WSGI server

### Frontend
- No external dependencies (vanilla JS)

## Key Features

1. **Fast**: Optimized for performance with minimal dependencies
2. **Modern**: Clean, responsive design using modern web standards
3. **Flexible**: Easy to customize and extend

## Notes for Copilot

- Keep the codebase simple and lightweight
- Avoid adding unnecessary dependencies
- Maintain the vanilla JS approach in the frontend (no frameworks unless explicitly requested)
- Follow RESTful API design patterns for new endpoints
- Ensure all new endpoints include proper error handling and CORS support
- Test API endpoints manually as there is no automated test suite currently
- When modifying the backend, ensure changes are compatible with Flask 3.0.0
- Keep the frontend accessible and mobile-responsive

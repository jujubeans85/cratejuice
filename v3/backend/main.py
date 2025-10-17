"""
Crate Juice v3 Backend
A simple Flask API server for the Crate Juice framework
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    """Home endpoint"""
    return jsonify({
        'message': 'Welcome to Crate Juice v3 API',
        'version': '3.0.0',
        'status': 'running'
    })

@app.route('/api/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'cratejuice-backend'
    })

@app.route('/api/features')
def features():
    """Get framework features"""
    return jsonify({
        'features': [
            {
                'name': 'Fast',
                'description': 'Optimized for performance',
                'icon': '⚡'
            },
            {
                'name': 'Modern',
                'description': 'Clean and responsive design',
                'icon': '🎨'
            },
            {
                'name': 'Flexible',
                'description': 'Easy to customize',
                'icon': '🔧'
            }
        ]
    })

@app.route('/api/info')
def info():
    """Get framework information"""
    return jsonify({
        'name': 'Crate Juice',
        'version': '3.0.0',
        'description': 'A modern, lightweight framework for building amazing web applications',
        'author': 'Crate Juice Team'
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)

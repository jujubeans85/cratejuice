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

@app.route('/api/library')
def library():
    """Get music library"""
    return jsonify({
        'tracks': {
            '1': {
                'title': 'Midnight Drive',
                'artist': 'Synthwave Studios',
                'url': 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3',
                'duration': '3:24'
            },
            '2': {
                'title': 'Digital Dreams',
                'artist': 'Retro Collective',
                'url': 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3',
                'duration': '4:12'
            },
            '3': {
                'title': 'Neon Nights',
                'artist': 'Electric Avenue',
                'url': 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-3.mp3',
                'duration': '3:48'
            },
            '4': {
                'title': 'Cyber City',
                'artist': 'Future Bass',
                'url': 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-4.mp3',
                'duration': '4:01'
            },
            '5': {
                'title': 'Starlight Highway',
                'artist': 'Ambient Waves',
                'url': 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-5.mp3',
                'duration': '5:15'
            }
        }
    })

@app.route('/api/playlist')
def playlist():
    """Get playlist"""
    return jsonify(['1', '2', '3', '4', '5'])

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)

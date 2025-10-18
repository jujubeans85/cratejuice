"""
Crate Juice v3 Backend
A simple Flask API server for the Crate Juice framework
"""

from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
import os
import zipfile
import io

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

@app.route('/api/download/bundle')
def download_bundle():
    """Download the full Crate Juice v3 bundle as a zip file"""
    try:
        # Get the v3 directory path
        current_dir = os.path.dirname(os.path.abspath(__file__))
        v3_dir = os.path.dirname(current_dir)
        
        # Create an in-memory zip file
        memory_file = io.BytesIO()
        
        with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Add all files from the v3 directory
            for root, dirs, files in os.walk(v3_dir):
                # Skip __pycache__ and other unnecessary directories
                dirs[:] = [d for d in dirs if d not in ['__pycache__', '.git', 'venv', 'env']]
                
                for file in files:
                    # Skip .pyc files and other compiled files
                    if file.endswith(('.pyc', '.pyo', '.pyd')):
                        continue
                    
                    file_path = os.path.join(root, file)
                    # Calculate the archive name (relative to v3 directory)
                    arcname = os.path.join('cratejuice-v3', os.path.relpath(file_path, v3_dir))
                    zipf.write(file_path, arcname)
        
        # Seek to the beginning of the file
        memory_file.seek(0)
        
        return send_file(
            memory_file,
            mimetype='application/zip',
            as_attachment=True,
            download_name='cratejuice-v3.zip'
        )
    
    except Exception:
        return jsonify({
            'error': 'Failed to create bundle'
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)

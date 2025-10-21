#!/bin/bash
# Render.com Deployment Guide for CrateJuice v3 Backend

echo "🚀 CrateJuice v3 Backend - Render.com Deployment"
echo "=============================================="
echo ""

echo "📋 Pre-deployment Checklist:"
echo "✅ render.yaml configured"
echo "✅ requirements.txt ready"
echo "✅ main.py with Flask app"
echo "✅ Health check endpoint available"
echo ""

echo "🌐 Deployment Steps:"
echo "1. Push your code to GitHub"
echo "2. Go to https://render.com"
echo "3. Connect your GitHub repository"
echo "4. Render will automatically detect render.yaml"
echo "5. Your API will be available at: https://cratejuice-backend.onrender.com"
echo ""

echo "🔗 API Endpoints (after deployment):"
echo "- GET https://cratejuice-backend.onrender.com/"
echo "- GET https://cratejuice-backend.onrender.com/api/health"
echo "- GET https://cratejuice-backend.onrender.com/api/features"
echo "- GET https://cratejuice-backend.onrender.com/api/info"
echo ""

echo "⚙️  Configuration:"
echo "- Service: cratejuice-backend"
echo "- Plan: Free"
echo "- Region: Oregon"
echo "- Python: 3.11.0"
echo "- Start Command: gunicorn main:app --bind 0.0.0.0:\$PORT"
echo "- Health Check: /api/health"
echo ""

echo "🔧 Local Testing:"
echo "cd v3/backend"
echo "python3 main.py"
echo "# Test at http://localhost:5000"
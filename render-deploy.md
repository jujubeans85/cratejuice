# Render Deployment Guide

## Backend Deployment
1. Go to [Render Dashboard](https://render.com)
2. Connect your GitHub repository
3. Create new Web Service
4. Use these settings:
   - **Build Command**: `pip install -r v3/backend/requirements.txt`
   - **Start Command**: `gunicorn main:app`
   - **Environment**: Python 3.11
   - **Root Directory**: `v3/backend`

## Frontend Deployment
1. Create new Static Site
2. Settings:
   - **Build Command**: `cd cratejuice && ./crate_run.sh`
   - **Publish Directory**: `cratejuice/v3/frontend/public`
   - **Environment**: Static Site

## Auto-Deploy
- Every push to main branch triggers new deployment
- Free tier available
- Custom domains supported
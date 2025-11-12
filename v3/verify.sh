#!/usr/bin/env bash
# CrateJuice Verify ☮️ — checks backend + frontend sync in one shot

RENDER_URL="https://cratejuice-2.onrender.com/health"
NETLIFY_URL="https://cratejuice.netlify.app/api/health"

echo "☮️ Checking Render backend..."
RENDER_RESP=$(curl -s -o /dev/null -w "%{http_code}" $RENDER_URL)

if [ "$RENDER_RESP" = "200" ]; then
  echo "✅ Render backend alive ($RENDER_URL)"
else
  echo "❌ Render not responding (HTTP $RENDER_RESP)"
fi

sleep 1

echo "🌐 Checking Netlify front → Render proxy..."
NETLIFY_RESP=$(curl -s -o /dev/null -w "%{http_code}" $NETLIFY_URL)

if [ "$NETLIFY_RESP" = "200" ]; then
  echo "✅ Netlify front correctly proxying backend"
else
  echo "⚠️ Netlify proxy not ready yet (HTTP $NETLIFY_RESP)"
fi

echo "---------------------------------------------"
echo "If both ✅ show up, your Crate's heart is beating steady. 💜"
#!/bin/bash
echo "🧩 CrateJuice Render Verify starting..."
cd "$(dirname "$0")" || exit

# Clean install
pip install -r requirements.txt --quiet

# Sanity check backend entry
echo "🔍 Checking backend.main import..."
python - <<'PY'
import importlib.util
print("backend.main:", bool(importlib.util.find_spec("backend.main")))
PY

# Run temp test server
echo "🚀 Launching Uvicorn test..."
PYTHONPATH=.. uvicorn backend.main:app --host 0.0.0.0 --port 8000 --workers 1
chmod +x v3/backend/verify_render.sh
git add v3/backend/verify_render.sh
git commit -m "🧩 Add verify_render.sh for Render test"
git push origin main

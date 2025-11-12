#!/usr/bin/env bash
set -euo pipefail

RENDER_URL="https://cratejuice.onrender.com/health"
NETLIFY_URL="https://cratejuice.netlify.app/health"

echo "🔎 Pinging Render backend..."
R_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$RENDER_URL")
echo "Render → $R_CODE"

echo "🔎 Pinging Netlify proxy..."
N_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$NETLIFY_URL")
echo "Netlify → $N_CODE"

if [[ "$R_CODE" == "200" && "$N_CODE" == "200" ]]; then
  echo "✅ Both Render + Netlify OK"
  exit 0
else
  echo "❌ Something's off (Render:$R_CODE  Netlify:$N_CODE)"
  exit 1
fi
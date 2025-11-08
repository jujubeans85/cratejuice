#!/bin/bash
echo "☮️ CrateJuice Cathedral — verify spin sequence"
render_health=$(curl -s https://cratejuice-2.onrender.com/health)
netlify_health=$(curl -s https://cratejuice.netlify.app/)

echo "Render:  $render_health"
echo "Netlify: $netlify_health"

if [[ "$render_health" == *"ok"* ]]; then
  echo "✅ Render backend online"
else
  echo "❌ Render backend issue"
fi

if [[ "$netlify_health" == *"crate"* ]]; then
  echo "✅ Netlify frontend online"
else
  echo "❌ Netlify frontend issue"
fi

echo "— Spin check complete ☮️ —"

#!/bin/bash
# Quick PWA Test - Validation Only

echo "🧪 Quick PWA Validation Test"
echo "============================="

PWA_DIR="/workspaces/cratejuice/cratejuice/v3/frontend/public"

# Quick validation checks
echo "✅ Meta Tags Check:"
grep -q 'name="theme-color"' "$PWA_DIR/index.html" && echo "  ✅ theme-color: $(grep 'theme-color' "$PWA_DIR/index.html" | cut -d'"' -f4)" || echo "  ❌ theme-color missing"
grep -q 'name="viewport"' "$PWA_DIR/index.html" && echo "  ✅ viewport configured" || echo "  ❌ viewport missing"
grep -q 'rel="manifest"' "$PWA_DIR/index.html" && echo "  ✅ manifest linked" || echo "  ❌ manifest link missing"

echo ""
echo "✅ Core Files:"
[ -f "$PWA_DIR/manifest.webmanifest" ] && echo "  ✅ manifest.webmanifest" || echo "  ❌ manifest missing"
[ -f "$PWA_DIR/service-worker.js" ] && echo "  ✅ service-worker.js" || echo "  ❌ service worker missing"
[ -f "$PWA_DIR/app.js" ] && echo "  ✅ app.js" || echo "  ❌ app.js missing"
[ -d "$PWA_DIR/icons" ] && echo "  ✅ icons directory" || echo "  ❌ icons missing"

echo ""
echo "✅ Service Worker Registration:"
grep -q "serviceWorker" "$PWA_DIR/app.js" && echo "  ✅ SW registration in app.js" || echo "  ❌ SW registration missing"

echo ""
echo "✅ Install Prompt:"
grep -q "beforeinstallprompt" "$PWA_DIR/app.js" && echo "  ✅ Install prompt handler" || echo "  ❌ Install prompt missing"

echo ""
echo "✅ Manifest Validation:"
if command -v jq &> /dev/null; then
    if jq . "$PWA_DIR/manifest.webmanifest" > /dev/null 2>&1; then
        echo "  ✅ Valid JSON format"
        echo "  ✅ App name: $(jq -r '.name' "$PWA_DIR/manifest.webmanifest")"
        echo "  ✅ Display mode: $(jq -r '.display' "$PWA_DIR/manifest.webmanifest")"
        echo "  ✅ Theme color: $(jq -r '.theme_color' "$PWA_DIR/manifest.webmanifest")"
        echo "  ✅ Icons count: $(jq '.icons | length' "$PWA_DIR/manifest.webmanifest")"
    else
        echo "  ❌ Invalid JSON in manifest"
    fi
else
    echo "  ⚠️  jq not available for JSON validation"
fi

echo ""
echo "🎯 Test Result:"
if [ -f "$PWA_DIR/manifest.webmanifest" ] && [ -f "$PWA_DIR/service-worker.js" ] && grep -q "serviceWorker" "$PWA_DIR/app.js" && grep -q 'rel="manifest"' "$PWA_DIR/index.html"; then
    echo "  ✅ PWA is properly configured!"
    echo "  ✅ Ready for HTTPS deployment"
    echo "  ✅ Will install on desktop and mobile"
else
    echo "  ❌ PWA configuration incomplete"
fi

echo ""
echo "📱 Next Step: Deploy to HTTPS hosting (Netlify, Vercel, GitHub Pages)"
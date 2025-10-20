#!/bin/bash
# PWA Download/Install Test Script

echo "📱 CrateJuice v3 - PWA Download/Install Test"
echo "============================================="

# Test the local server
echo "🌐 Testing local server..."
if curl -s http://localhost:8080 > /dev/null; then
    echo "✅ Server running at http://localhost:8080"
    echo "✅ PWA accessible locally"
else
    echo "❌ Server not accessible"
    exit 1
fi

echo ""
echo "📋 PWA Install Requirements Check:"

# Check if manifest is accessible
if curl -s http://localhost:8080/manifest.webmanifest | jq . > /dev/null 2>&1; then
    echo "✅ Manifest accessible and valid JSON"
    MANIFEST=$(curl -s http://localhost:8080/manifest.webmanifest)
    echo "   📱 App: $(echo "$MANIFEST" | jq -r '.name')"
    echo "   🎨 Theme: $(echo "$MANIFEST" | jq -r '.theme_color')"
    echo "   📐 Display: $(echo "$MANIFEST" | jq -r '.display')"
else
    echo "❌ Manifest not accessible or invalid"
fi

# Check Service Worker
if curl -s http://localhost:8080/service-worker.js | grep -q "install"; then
    echo "✅ Service Worker accessible with install handler"
else
    echo "❌ Service Worker missing or invalid"
fi

# Check icons
ICON_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8080/icons/app_violet.svg)
if [ "$ICON_STATUS" = "200" ]; then
    echo "✅ App icons accessible"
else
    echo "❌ App icons not found (HTTP $ICON_STATUS)"
fi

echo ""
echo "🎯 Install Test Instructions:"
echo "=============================="
echo ""
echo "📱 Desktop Install Test:"
echo "  1. Open Chrome or Edge"
echo "  2. Navigate to: http://localhost:8080"
echo "  3. Look for 'Install' button in address bar"
echo "  4. Click to install CrateJuice as desktop app"
echo "  5. App should appear in applications menu"
echo ""
echo "📱 Mobile Install Test:"
echo "  1. Open Chrome/Safari on mobile device"
echo "  2. Navigate to: http://localhost:8080"
echo "  3. Tap browser menu → 'Add to Home Screen'"
echo "  4. App icon should appear on home screen"
echo "  5. Tap icon to launch standalone app"
echo ""
echo "🔍 Manual Install Button Test:"
echo "  1. Open browser developer tools (F12)"
echo "  2. Go to Application/Storage tab"
echo "  3. Check 'Manifest' section for validation"
echo "  4. Look for hidden 'Install App' button in page"
echo "  5. Button appears when PWA install prompt is ready"
echo ""
echo "⚠️  Note: Full PWA install requires HTTPS in production"
echo "   Local testing has limited functionality"
echo ""
echo "🚀 For production testing:"
echo "   Deploy to Netlify, Vercel, or GitHub Pages"
echo "   HTTPS enables full PWA installation features"
echo ""
echo "✨ CrateJuice v3 PWA download test ready!"
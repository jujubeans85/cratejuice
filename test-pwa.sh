#!/bin/bash
# PWA Download/Install Test Script for CrateJuice v3

echo "🧪 Testing CrateJuice v3 PWA Installation Features..."

# Test server
SERVER_URL="http://localhost:8080"
echo "📡 Testing server at $SERVER_URL"

# Test 1: Manifest file
echo "🔍 Test 1: Checking Web App Manifest..."
curl -s "$SERVER_URL/manifest.webmanifest" | jq . > /dev/null
if [ $? -eq 0 ]; then
    echo "✅ Manifest is valid JSON"
    MANIFEST_CONTENT=$(curl -s "$SERVER_URL/manifest.webmanifest")
    echo "📱 App Name: $(echo "$MANIFEST_CONTENT" | jq -r '.name')"
    echo "🎨 Theme Color: $(echo "$MANIFEST_CONTENT" | jq -r '.theme_color')"
    echo "📐 Display Mode: $(echo "$MANIFEST_CONTENT" | jq -r '.display')"
else
    echo "❌ Manifest validation failed"
fi

# Test 2: Service Worker
echo "🔍 Test 2: Checking Service Worker..."
curl -s "$SERVER_URL/service-worker.js" | head -1
if curl -s "$SERVER_URL/service-worker.js" | grep -q "CACHE"; then
    echo "✅ Service Worker contains caching logic"
else
    echo "❌ Service Worker missing or invalid"
fi

# Test 3: PWA Requirements
echo "🔍 Test 3: Checking PWA Requirements..."
if curl -s "$SERVER_URL/index.html" | grep -q 'rel="manifest"'; then
    echo "✅ HTML links to manifest"
else
    echo "❌ Missing manifest link in HTML"
fi

if curl -s "$SERVER_URL/index.html" | grep -q 'service-worker'; then
    echo "✅ Service Worker registration found"
else
    echo "❌ Service Worker registration missing"
fi

# Test 4: Icon availability
echo "🔍 Test 4: Checking App Icons..."
curl -s -o /dev/null -w "%{http_code}" "$SERVER_URL/icons/app_violet.svg" | grep -q "200"
if [ $? -eq 0 ]; then
    echo "✅ App icon is accessible"
else
    echo "❌ App icon not found"
fi

# Test 5: Offline capability test
echo "🔍 Test 5: Testing Core Files for Offline Support..."
for file in "index.html" "style.css" "app.js" "manifest.webmanifest"; do
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$SERVER_URL/$file")
    if [ "$HTTP_CODE" = "200" ]; then
        echo "✅ $file is accessible"
    else
        echo "❌ $file returned HTTP $HTTP_CODE"
    fi
done

echo ""
echo "🎯 PWA Installation Test Summary:"
echo "   📱 To test installation on desktop:"
echo "      1. Open Chrome/Edge at $SERVER_URL"
echo "      2. Look for 'Install' button in address bar"
echo "      3. Click to install as desktop app"
echo ""
echo "   📱 To test on mobile:"
echo "      1. Open in Chrome/Safari on mobile"
echo "      2. Use 'Add to Home Screen' option"
echo "      3. App should work offline after install"
echo ""
echo "✨ CrateJuice v3 PWA testing complete!"
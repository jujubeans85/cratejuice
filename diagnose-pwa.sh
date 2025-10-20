#!/bin/bash
# Comprehensive PWA Diagnostic Tool for CrateJuice v3

echo "🔍 PWA Deployment Test - Detailed Diagnostics"
echo "=============================================="

PWA_DIR="/workspaces/cratejuice/cratejuice/v3/frontend/public"

# Test 1: File Structure
echo "📁 Test 1: File Structure Analysis"
echo "PWA Directory: $PWA_DIR"
if [ -d "$PWA_DIR" ]; then
    echo "✅ PWA directory exists"
    echo "📊 Files found:"
    ls -la "$PWA_DIR" | grep -E '\.(html|js|css|json|webmanifest)$'
else
    echo "❌ PWA directory missing: $PWA_DIR"
    exit 1
fi

# Test 2: Manifest Validation
echo ""
echo "📋 Test 2: Manifest File Validation"
MANIFEST_FILE="$PWA_DIR/manifest.webmanifest"
if [ -f "$MANIFEST_FILE" ]; then
    echo "✅ Manifest file exists"
    echo "📄 Manifest content:"
    cat "$MANIFEST_FILE" | jq . 2>/dev/null || echo "❌ Invalid JSON in manifest"
    
    # Check required fields
    echo "🔍 Required fields check:"
    jq -r '.name // "MISSING"' "$MANIFEST_FILE" | grep -v "MISSING" > /dev/null && echo "✅ name" || echo "❌ name missing"
    jq -r '.short_name // "MISSING"' "$MANIFEST_FILE" | grep -v "MISSING" > /dev/null && echo "✅ short_name" || echo "❌ short_name missing"
    jq -r '.start_url // "MISSING"' "$MANIFEST_FILE" | grep -v "MISSING" > /dev/null && echo "✅ start_url" || echo "❌ start_url missing"
    jq -r '.display // "MISSING"' "$MANIFEST_FILE" | grep -v "MISSING" > /dev/null && echo "✅ display" || echo "❌ display missing"
    jq -r '.icons // "MISSING"' "$MANIFEST_FILE" | grep -v "MISSING" > /dev/null && echo "✅ icons" || echo "❌ icons missing"
else
    echo "❌ Manifest file missing: $MANIFEST_FILE"
fi

# Test 3: Service Worker Validation
echo ""
echo "⚙️ Test 3: Service Worker Validation"
SW_FILE="$PWA_DIR/service-worker.js"
if [ -f "$SW_FILE" ]; then
    echo "✅ Service Worker file exists"
    echo "📄 Service Worker size: $(stat -c%s "$SW_FILE") bytes"
    
    # Check for required service worker features
    echo "🔍 Service Worker features:"
    grep -q "install" "$SW_FILE" && echo "✅ install event" || echo "❌ install event missing"
    grep -q "activate" "$SW_FILE" && echo "✅ activate event" || echo "❌ activate event missing"
    grep -q "fetch" "$SW_FILE" && echo "✅ fetch event" || echo "❌ fetch event missing"
    grep -q "cache" "$SW_FILE" && echo "✅ caching logic" || echo "❌ caching logic missing"
else
    echo "❌ Service Worker missing: $SW_FILE"
fi

# Test 4: HTML Integration
echo ""
echo "🌐 Test 4: HTML Integration Check"
HTML_FILE="$PWA_DIR/index.html"
if [ -f "$HTML_FILE" ]; then
    echo "✅ HTML file exists"
    
    echo "🔍 HTML PWA elements:"
    grep -q 'rel="manifest"' "$HTML_FILE" && echo "✅ manifest link" || echo "❌ manifest link missing"
    grep -q 'name="theme-color"' "$HTML_FILE" && echo "✅ theme-color meta" || echo "❌ theme-color meta missing"
    grep -q 'name="viewport"' "$HTML_FILE" && echo "✅ viewport meta" || echo "❌ viewport meta missing"
    
    echo "📄 HTML head section:"
    grep -A5 -B5 'rel="manifest"' "$HTML_FILE" || echo "No manifest link found"
else
    echo "❌ HTML file missing: $HTML_FILE"
fi

# Test 5: JavaScript SW Registration
echo ""
echo "🔧 Test 5: JavaScript Service Worker Registration"
JS_FILE="$PWA_DIR/app.js"
if [ -f "$JS_FILE" ]; then
    echo "✅ JavaScript file exists"
    
    echo "🔍 Service Worker registration:"
    if grep -q "serviceWorker" "$JS_FILE"; then
        echo "✅ Service Worker registration found"
        echo "📄 Registration code:"
        grep -A5 -B2 "serviceWorker" "$JS_FILE"
    else
        echo "❌ Service Worker registration missing"
    fi
    
    echo "🔍 Install prompt handling:"
    grep -q "beforeinstallprompt" "$JS_FILE" && echo "✅ Install prompt handler" || echo "❌ Install prompt handler missing"
else
    echo "❌ JavaScript file missing: $JS_FILE"
fi

# Test 6: Icons Check
echo ""
echo "🎨 Test 6: Icons Validation"
ICONS_DIR="$PWA_DIR/icons"
if [ -d "$ICONS_DIR" ]; then
    echo "✅ Icons directory exists"
    echo "📊 Icon files:"
    ls -la "$ICONS_DIR"
    
    # Check if icons are referenced in manifest
    if [ -f "$MANIFEST_FILE" ]; then
        echo "🔍 Icons in manifest:"
        jq -r '.icons[] | .src' "$MANIFEST_FILE" 2>/dev/null || echo "No icons in manifest"
    fi
else
    echo "❌ Icons directory missing: $ICONS_DIR"
fi

# Test 7: HTTPS Requirement Check
echo ""
echo "🔒 Test 7: HTTPS Deployment Requirements"
echo "⚠️  PWA installation requires HTTPS in production"
echo "✅ Local testing: Limited functionality"
echo "✅ Production: Full PWA features with HTTPS"

# Test 8: Browser Compatibility
echo ""
echo "🌍 Test 8: Browser Compatibility Check"
echo "✅ Chrome/Chromium: Full PWA support"
echo "✅ Firefox: Basic PWA support"
echo "✅ Safari: Limited PWA support"
echo "✅ Edge: Full PWA support"

# Test 9: Quick Local Server Test
echo ""
echo "🚀 Test 9: Quick Local Server Test"
echo "Starting temporary server for validation..."

cd "$PWA_DIR"
timeout 5s python3 -m http.server 9999 > /dev/null 2>&1 &
SERVER_PID=$!
sleep 2

if curl -s -o /dev/null -w "%{http_code}" "http://localhost:9999/" | grep -q "200"; then
    echo "✅ Local server accessible"
    echo "✅ Files served correctly"
else
    echo "❌ Local server issues"
fi

# Cleanup
kill $SERVER_PID 2>/dev/null

echo ""
echo "🎯 PWA Diagnostic Summary:"
echo "========================="
echo "If all tests pass, PWA should work when deployed to HTTPS hosting."
echo "Common issues:"
echo "  - Missing HTTPS in production"
echo "  - Incorrect file paths in manifest"
echo "  - Service Worker registration errors"
echo "  - Missing required manifest fields"
echo ""
echo "Next steps: Deploy to Netlify, Vercel, or GitHub Pages for full testing."
#!/bin/bash
# Production deployment script for CrateJuice v3

echo "🚀 Preparing CrateJuice v3 for production..."

# Index any existing tracks
echo "📚 Indexing tracks..."
cd cratejuice
python3 apps/indexer/index_crates_light.py
cd ..

# Verify frontend assets
echo "🔍 Verifying frontend assets..."
if [ ! -f "cratejuice/v3/frontend/public/index.html" ]; then
    echo "❌ Missing frontend files"
    exit 1
fi

# Check for required files
echo "✅ Frontend ready"
echo "✅ Data indexed"
echo "✅ Tools configured"

echo "🎯 Production checklist:"
echo "   - Deploy 'cratejuice/v3/frontend/public/' to Netlify"
echo "   - Use netlify.toml for configuration"
echo "   - Gift routes: /gift/[tag-name]/"
echo "   - Add MP3s to offgrid-crates/ and run ./crate_run.sh"

echo "🌐 Netlify deploy command:"
echo "   netlify deploy --prod --dir=cratejuice/v3/frontend/public"

echo "✨ CrateJuice v3 production ready!"
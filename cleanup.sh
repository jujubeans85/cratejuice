#!/bin/bash
# CrateJuice Cleanup and Organization Script

echo "🧹 Starting CrateJuice cleanup and organization..."

# Backup current structure
echo "📦 Creating backup..."
tar -czf cratejuice_backup_$(date +%Y%m%d_%H%M%S).tar.gz cratejuice/ cratejuice_full_bundle/ cratejuice_turbo_repo/ v3/ 2>/dev/null || true

# Create clean directory structure
echo "📁 Creating clean directory structure..."
mkdir -p clean_cratejuice/{frontend,backend,tools,content,docs,scripts}

# Move the best version of frontend (enhanced with our styles)
echo "🎨 Moving enhanced frontend..."
if [ -d "cratejuice/v3/frontend" ]; then
    cp -r cratejuice/v3/frontend/* clean_cratejuice/frontend/
else
    cp -r v3/frontend/* clean_cratejuice/frontend/ 2>/dev/null || true
fi

# Move backend
echo "🔧 Moving backend..."
if [ -d "cratejuice_turbo_repo/apps/backend" ]; then
    cp -r cratejuice_turbo_repo/apps/backend/* clean_cratejuice/backend/
elif [ -d "v3/backend" ]; then
    cp -r v3/backend/* clean_cratejuice/backend/
fi

# Move tools and scripts
echo "🛠️ Moving tools..."
[ -d "cratejuice/tools" ] && cp -r cratejuice/tools/* clean_cratejuice/tools/ 2>/dev/null || true
[ -d "cratejuice/apps" ] && cp -r cratejuice/apps/* clean_cratejuice/tools/ 2>/dev/null || true
[ -f "addurl" ] && cp addurl clean_cratejuice/scripts/
[ -f "deploy.sh" ] && cp deploy.sh clean_cratejuice/scripts/

# Move content
echo "📄 Moving content..."
[ -d "cratejuice/content" ] && cp -r cratejuice/content/* clean_cratejuice/content/ 2>/dev/null || true
[ -d "content" ] && cp -r content/* clean_cratejuice/content/ 2>/dev/null || true

# Move documentation
echo "📚 Moving documentation..."
[ -f "README.md" ] && cp README.md clean_cratejuice/docs/
[ -f "PRODUCTION.md" ] && cp PRODUCTION.md clean_cratejuice/docs/
[ -d "cratejuice_turbo_repo/docs" ] && cp -r cratejuice_turbo_repo/docs/* clean_cratejuice/docs/ 2>/dev/null || true

# Copy important root files
echo "📋 Copying configuration..."
[ -f "netlify.toml" ] && cp netlify.toml clean_cratejuice/
[ -f ".gitignore" ] && cp .gitignore clean_cratejuice/

echo "✅ Cleanup complete! Clean structure created in clean_cratejuice/"
echo "📊 Directory comparison:"
du -sh cratejuice* v3/ clean_cratejuice/ 2>/dev/null | sort -hr
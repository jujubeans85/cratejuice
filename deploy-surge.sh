#!/bin/bash
# Quick deployment to Surge.sh

echo "🌊 Deploying CrateJuice v3 to Surge.sh..."

# Install surge if not present
if ! command -v surge &> /dev/null; then
    echo "Installing Surge.sh..."
    npm install -g surge
fi

# Prepare build
cd cratejuice
python3 apps/indexer/index_crates_light.py
cd ..

# Deploy to surge
cd cratejuice/v3/frontend/public
surge . cratejuice-v3.surge.sh

echo "✨ Deployed to https://cratejuice-v3.surge.sh"
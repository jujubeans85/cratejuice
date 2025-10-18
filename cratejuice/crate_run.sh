#!/bin/sh
set -e
mkdir -p offgrid-crates content/data
python3 apps/indexer/index_crates_light.py
echo "✅ Indexed. MP3s in ./offgrid-crates, JSON in content/data"

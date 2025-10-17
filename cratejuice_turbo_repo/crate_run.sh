#!/bin/sh
set -e

echo "⚡ CJ chain firing..."

# Ensure examples dir exists & seed with a default if empty
mkdir -p examples
[ -s examples/mycrates.txt ] || echo "https://www.youtube.com/watch?v=dQw4w9WgXcQ" > examples/mycrates.txt

# Pick an output directory that works in Codespaces or iSH
if [ -d /workspaces ]; then
  CRATE_DIR="/workspaces/cratejuice/offgrid-crates"
else
  CRATE_DIR="$HOME/Documents/offgrid-crates"
fi

export CRATE_DIR
mkdir -p "$CRATE_DIR"

# Run the indexer/ripper pipeline
python3 apps/indexer/index_crates_light.py examples/mycrates.txt "$CRATE_DIR" "$@"
chmod +x crate_run.sh
mkdir -p examples
echo "https://www.youtube.com/watch?v=dQw4w9WgXcQ" > examples/mycrates.txt
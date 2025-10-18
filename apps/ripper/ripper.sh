#!/bin/bash
# CrateJuice Ripper with add-mode support
# Usage: ./ripper.sh [add <URL>] [run] [help]

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
URLS_FILE="$REPO_ROOT/cratejuice/content/data/urls.txt"
RIPLIST_FILE="$REPO_ROOT/cratejuice/content/data/riplist.txt"
CRATE_DIR="$REPO_ROOT/cratejuice/offgrid-crates"
LOG_FILE="$REPO_ROOT/ripper.log"

# Ensure directories exist
mkdir -p "$(dirname "$URLS_FILE")"
mkdir -p "$CRATE_DIR"

show_help() {
    cat << EOF
🎵 CrateJuice Ripper

Usage:
  ./ripper.sh add <URL>     - Add URL to riplist
  ./ripper.sh run           - Start overnight ripper
  ./ripper.sh list          - Show queued URLs
  ./ripper.sh clear         - Clear all URLs
  ./ripper.sh help          - Show this help

Examples:
  ./ripper.sh add "https://youtube.com/watch?v=dQw4w9WgXcQ"
  ./ripper.sh add "https://soundcloud.com/artist/track"
  ./ripper.sh run

Files:
  URLs: $URLS_FILE
  Riplist: $RIPLIST_FILE
  Output: $CRATE_DIR
  Logs: $LOG_FILE
EOF
}

add_url() {
    local url="$1"
    if [[ -z "$url" ]]; then
        echo "❌ Error: No URL provided"
        echo "Usage: ./ripper.sh add <URL>"
        exit 1
    fi
    
    # Validate URL format
    if [[ ! "$url" =~ ^https?:// ]]; then
        echo "❌ Error: Invalid URL format. Must start with http:// or https://"
        exit 1
    fi
    
    # Add to both files for compatibility
    echo "$url" >> "$URLS_FILE"
    echo "$url" >> "$RIPLIST_FILE"
    
    echo "✅ Added URL to riplist: $url"
    echo "📋 Total URLs in queue: $(wc -l < "$URLS_FILE" 2>/dev/null || echo 0)"
}

list_urls() {
    if [[ -f "$URLS_FILE" ]]; then
        echo "📋 Queued URLs:"
        cat "$URLS_FILE" | grep -v '^#' | grep -v '^$' | nl
    else
        echo "📋 No URLs queued yet"
    fi
}

clear_urls() {
    > "$URLS_FILE"
    > "$RIPLIST_FILE"
    echo "🗑️ Cleared all URLs from queue"
}

run_ripper() {
    echo "🌙 Starting overnight ripper..."
    cd "$REPO_ROOT"
    exec ./cjrip
}

# Main command handling
case "${1:-help}" in
    "add")
        add_url "$2"
        ;;
    "run")
        run_ripper
        ;;
    "list")
        list_urls
        ;;
    "clear")
        clear_urls
        ;;
    "help"|"--help"|"-h")
        show_help
        ;;
    *)
        echo "❌ Unknown command: $1"
        show_help
        exit 1
        ;;
esac
#!/bin/bash
# CrateJuice Deployment Setup Script
# This script prepares the repository for deployment

set -e  # Exit on any error

echo "🧃 CrateJuice v3 - Deployment Setup"
echo "===================================="
echo ""

# Color codes for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to print colored output
print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo "ℹ️  $1"
}

# Check if we're in the right directory
if [ ! -d "cratejuice" ]; then
    print_error "Error: cratejuice directory not found!"
    print_info "Please run this script from the repository root."
    exit 1
fi

print_info "Checking prerequisites..."

# Check for Python
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed!"
    print_info "Please install Python 3 to continue."
    exit 1
fi
print_success "Python 3 found: $(python3 --version)"

# Check for Git
if ! command -v git &> /dev/null; then
    print_error "Git is not installed!"
    exit 1
fi
print_success "Git found: $(git --version | head -1)"

echo ""
print_info "Setting up project structure..."

# Create necessary directories
mkdir -p cratejuice/offgrid-crates
mkdir -p cratejuice/content/data
print_success "Directories created"

# Run the indexer to generate initial data files
echo ""
print_info "Running indexer to generate data files..."
cd cratejuice
./crate_run.sh
cd ..
print_success "Indexer completed"

# Verify frontend files exist
echo ""
print_info "Verifying frontend files..."
FRONTEND_DIR="cratejuice/v3/frontend/public"

required_files=(
    "$FRONTEND_DIR/index.html"
    "$FRONTEND_DIR/app.js"
    "$FRONTEND_DIR/style.css"
    "$FRONTEND_DIR/manifest.webmanifest"
    "$FRONTEND_DIR/service-worker.js"
    "$FRONTEND_DIR/gift.html"
)

all_files_exist=true
for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        print_success "Found: $(basename $file)"
    else
        print_error "Missing: $file"
        all_files_exist=false
    fi
done

if [ "$all_files_exist" = false ]; then
    print_error "Some required files are missing!"
    exit 1
fi

# Check for iOS meta tags
echo ""
print_info "Verifying iOS PWA configuration..."

if grep -q "apple-mobile-web-app-capable" "$FRONTEND_DIR/index.html"; then
    print_success "iOS meta tags found in index.html"
else
    print_warning "iOS meta tags not found in index.html"
fi

if grep -q "apple-touch-icon" "$FRONTEND_DIR/index.html"; then
    print_success "Apple touch icon configured"
else
    print_warning "Apple touch icon not configured"
fi

# Check manifest
if [ -f "$FRONTEND_DIR/manifest.webmanifest" ]; then
    if grep -q "standalone" "$FRONTEND_DIR/manifest.webmanifest"; then
        print_success "PWA manifest configured for standalone mode"
    else
        print_warning "Manifest display mode not set to standalone"
    fi
fi

# Check GitHub Actions workflow
echo ""
print_info "Checking GitHub Actions workflow..."

if [ -f ".github/workflows/pages.yml" ]; then
    print_success "GitHub Pages workflow found"
    print_info "Deployment will trigger automatically on push to main branch"
else
    print_warning "GitHub Pages workflow not found"
    print_info "You may need to set up deployment manually"
fi

# Git status
echo ""
print_info "Checking git status..."
if git diff --quiet && git diff --staged --quiet; then
    print_success "No uncommitted changes"
else
    print_warning "You have uncommitted changes"
    print_info "Run 'git status' to see changes"
fi

# Summary
echo ""
echo "===================================="
echo "🎉 Setup Complete!"
echo "===================================="
echo ""
print_info "Next steps:"
echo ""
echo "1. 📁 Add MP3 files to: cratejuice/offgrid-crates/"
echo "   Then run: cd cratejuice && ./crate_run.sh"
echo ""
echo "2. 🚀 Deploy to GitHub Pages:"
echo "   - Push to main branch for automatic deployment"
echo "   - Or manually trigger in Actions tab"
echo ""
echo "3. 📱 Test iOS installation:"
echo "   - Open deployed site in Safari on iOS"
echo "   - Tap Share → Add to Home Screen"
echo "   - See iOS-INSTALLATION.md for details"
echo ""
echo "4. 📚 Read the guides:"
echo "   - iOS-INSTALLATION.md - How to install on iOS"
echo "   - DEPLOYMENT-GUIDE.md - Deployment options"
echo "   - PRODUCTION.md - Production checklist"
echo ""
echo "🌐 Your site will be available at:"
echo "   https://$(git config --get remote.origin.url | sed 's/.*github.com[:/]\(.*\)\.git/\1/' | cut -d'/' -f1).github.io/cratejuice/"
echo ""
print_success "Happy deploying! 🧃"

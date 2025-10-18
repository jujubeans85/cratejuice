# 🧃 CrateJuice v3 - Production Ready

A modern, lightweight Progressive Web App for music crates, gifting, and audio playback.

## 🚀 Production Deployment

### Quick Deploy to Netlify:
```bash
# Install Netlify CLI (if needed)
npm install -g netlify-cli

# Deploy to production
netlify deploy --prod --dir=cratejuice/v3/frontend/public

# Or use the deployment script
./deploy.sh
```

### Manual Deployment:
1. **Upload** `cratejuice/v3/frontend/public/` to your web host
2. **Configure** redirects using `netlify.toml` 
3. **Test** the PWA and gift routes

## 🎵 Features

- **🎧 Web Player** - Modern audio player with shuffle/surprise and pitch control
- **🎁 Gift System** - Create themed gift packages with custom messages
- **📱 PWA Support** - Installable Progressive Web App with offline caching
- **🌙 Auto-Ripper** - Background URL processing for music collection
- **🎨 Multiple Themes** - 6 different visual themes (4Boss, 4Mmi, 4Cbo, Dan, Opal, DanFun)

## 📋 Production Checklist

### ✅ Core System:
- [x] PWA frontend deployed
- [x] Service worker for offline support
- [x] Responsive design
- [x] Audio controls with pitch/shuffle
- [x] Multiple playlist formats

### ✅ Gift System:
- [x] Gift route handling (`/gift/[tag]/`)
- [x] Theme customization
- [x] Custom messages and recipients
- [x] ZIP export functionality

### ✅ Data Management:
- [x] JSON-based track library
- [x] Automatic playlist generation
- [x] MP3 file indexing
- [x] Tagline management

## 🔧 Usage

### Adding Music:
```bash
# 1. Add MP3 files to offgrid-crates/
cp your-music.mp3 cratejuice/offgrid-crates/

# 2. Index the tracks
cd cratejuice && ./crate_run.sh

# 3. Playlists auto-generated in content/data/
```

### Creating Gifts:
```bash
# Create a themed gift package
python3 tools/cjpack.py \
  --tag gift-dan-01 \
  --to "Dan" \
  --theme danfun \
  --note "Custom message here"

# Deploy gift route: /gift/gift-dan-01/
```

### Auto-Ripper (Optional):
```bash
# Add URLs to riplist
echo "https://youtube.com/watch?v=VIDEO_ID" >> cratejuice/content/data/riplist.txt

# Start background ripper
./cjrip
```

## 🌐 Live URLs

- **Main Player**: `https://your-domain.com/`
- **Gift Routes**: `https://your-domain.com/gift/[tag-name]/`
- **API Endpoints**: All data served as static JSON

## 📁 Production Structure

```
cratejuice/v3/frontend/public/  ← Deploy this folder
├── index.html                 ← Main PWA
├── app.js                     ← Player logic
├── style.css                  ← Responsive styles
├── manifest.webmanifest       ← PWA config
├── service-worker.js          ← Offline support
├── gift.html                  ← Gift interface
└── icons/                     ← Theme icons
```

## 🔒 Security & Performance

- **Static files only** - No server-side code required
- **CDN ready** - All assets cacheable
- **Offline first** - Service worker caching
- **Mobile optimized** - Responsive design
- **No authentication** - Public music sharing

## 📞 Support

- **Repository**: github.com/jujubeans85/cratejuice
- **Issues**: Use GitHub Issues for bug reports
- **Docs**: See `/docs` for detailed guides

---

© 2025 CrateJuice. Built for music lovers by music lovers. 🎶
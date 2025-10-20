# 🚀 CrateJuice Deployment Guide

This guide covers deployment options for CrateJuice v3 with iOS PWA support.

## 📦 What's Deployed

- **Frontend PWA**: Full Progressive Web App with offline support
- **iOS Support**: Apple-specific meta tags and configurations
- **Service Worker**: Offline caching and background sync
- **Multiple Themes**: Gift packages with custom theming

## 🌐 Deployment Options

### Option 1: GitHub Pages (Recommended)

**Automatic Deployment** - Already configured!

The repository includes a GitHub Actions workflow that automatically deploys to GitHub Pages when you push to the `main` branch.

#### How it Works:
1. Push changes to `main` branch
2. GitHub Actions workflow triggers
3. Python indexer runs to process tracks
4. Frontend assets deployed to GitHub Pages
5. Available at: `https://[username].github.io/cratejuice/`

#### Manual Trigger:
You can also manually trigger deployment:
1. Go to repository → Actions tab
2. Select "Deploy to GitHub Pages" workflow
3. Click "Run workflow"

### Option 2: Netlify

Deploy to Netlify using the included configuration:

```bash
# Install Netlify CLI
npm install -g netlify-cli

# Deploy to production
netlify deploy --prod --dir=cratejuice/v3/frontend/public
```

**Configuration**: The `netlify.toml` file handles:
- Build commands
- Publish directory
- Redirects for gift routes
- SPA fallback routing

### Option 3: Vercel

Deploy to Vercel using the included configuration:

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
vercel --prod
```

**Configuration**: The `vercel.json` file handles:
- Static asset serving
- Route configuration
- Gift package routing

### Option 4: Manual Deployment

Deploy to any static hosting provider:

1. **Build the project:**
   ```bash
   cd cratejuice
   ./crate_run.sh
   ```

2. **Upload these files:**
   ```
   cratejuice/v3/frontend/public/
   ├── index.html          # Main PWA
   ├── gift.html           # Gift interface
   ├── app.js              # Application logic
   ├── style.css           # Styles
   ├── manifest.webmanifest # PWA config
   ├── service-worker.js   # Offline support
   ├── icons/              # App icons
   └── *.json              # Data files
   ```

3. **Configure your host:**
   - Enable HTTPS (required for PWA)
   - Set up SPA routing (all routes → index.html)
   - Configure gift routes: `/gift/*` → `/gift/*/index.html`

## 🔧 Pre-Deployment Checklist

### Essential Configuration
- [ ] HTTPS enabled (required for PWA and service workers)
- [ ] Domain/subdomain configured (if using custom domain)
- [ ] Service worker registration verified
- [ ] Manifest.webmanifest accessible at root

### iOS Specific
- [ ] Apple meta tags present in all HTML files
- [ ] Apple-touch-icon configured
- [ ] Viewport-fit set to "cover" for notch support
- [ ] Status bar style configured

### Content
- [ ] Music tracks indexed (run `./crate_run.sh`)
- [ ] Library.json and playlist.json generated
- [ ] Gift packages configured (if applicable)
- [ ] Default cover image present

### Testing
- [ ] Service worker registers successfully
- [ ] App installable on iOS Safari
- [ ] Offline mode works after first visit
- [ ] Audio playback functional
- [ ] Gift routes accessible

## 📱 Post-Deployment: iOS Installation

After deployment, users can install on iOS:

1. Open Safari on iPhone/iPad
2. Navigate to your deployed URL
3. Tap Share → "Add to Home Screen"
4. App installs with native-like experience

**Full instructions**: See [iOS-INSTALLATION.md](iOS-INSTALLATION.md)

## 🔍 Verify Deployment

### Check Service Worker
```javascript
// Open browser console on deployed site
navigator.serviceWorker.getRegistrations().then(registrations => {
  console.log('Service workers:', registrations);
});
```

### Check Manifest
Visit: `https://your-domain.com/manifest.webmanifest`

Should return valid JSON with:
- `name`: "CrateJuice"
- `display`: "standalone"
- `theme_color`: "#7e5bef"

### Check iOS Meta Tags
View page source and verify presence of:
```html
<meta name="apple-mobile-web-app-capable" content="yes" />
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent" />
```

### Test PWA Installation
1. Chrome DevTools → Application tab
2. Check "Manifest" section
3. Verify no errors
4. "Add to Home Screen" should be available

## 🐛 Troubleshooting

### Service Worker Not Registering
- **Issue**: Service worker registration fails
- **Solution**: 
  - Ensure site uses HTTPS
  - Check browser console for errors
  - Verify service-worker.js is accessible
  - Clear browser cache and try again

### iOS Installation Not Available
- **Issue**: "Add to Home Screen" option missing
- **Solution**:
  - Must use Safari browser (not Chrome/Firefox)
  - Ensure all apple meta tags present
  - Check manifest.webmanifest is valid
  - Try on iOS 11.3 or later

### Offline Mode Not Working
- **Issue**: App doesn't work offline
- **Solution**:
  - Visit site online first (caches assets)
  - Check service worker is registered
  - Verify cache strategy in service-worker.js
  - Check browser storage isn't full

### Gift Routes Not Working
- **Issue**: 404 errors on `/gift/[tag]/` URLs
- **Solution**:
  - Configure redirects (see netlify.toml)
  - Set up SPA fallback routing
  - Ensure gift.html is in correct location

## 📊 Monitoring Deployment

### GitHub Pages Status
- Check: Repository → Environments → github-pages
- View deployment history and URLs
- Check workflow runs in Actions tab

### Netlify Status
- Dashboard shows deployment status
- View logs for build errors
- Check deploy previews for branches

### Analytics (Optional)
Consider adding:
- Google Analytics for usage tracking
- Performance monitoring
- Error tracking (Sentry, etc.)

## 🔄 Updating Deployment

### Adding New Content
```bash
# Add MP3 files to offgrid-crates/
cp new-track.mp3 cratejuice/offgrid-crates/

# Re-index
cd cratejuice
./crate_run.sh

# Commit and push
git add .
git commit -m "Add new tracks"
git push origin main

# GitHub Actions will auto-deploy
```

### Updating iOS Support
- Modify manifest.webmanifest or meta tags
- Commit and push changes
- Users must reinstall app to get updates
- Or updates apply on next app launch

## 🆘 Support

Having deployment issues?

1. **Check workflow logs**: Actions tab → latest run
2. **Review configuration**: Verify all config files
3. **Test locally**: Ensure it works before deploying
4. **Open an issue**: Include error messages and logs

**Repository**: https://github.com/jujubeans85/cratejuice
**Issues**: https://github.com/jujubeans85/cratejuice/issues

---

© 2025 CrateJuice. Built for music lovers by music lovers. 🎶

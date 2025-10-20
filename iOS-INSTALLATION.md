# 📱 iOS App Installation Guide

CrateJuice is available as a Progressive Web App (PWA) that can be installed on iOS devices for a native app-like experience.

## ✨ Features When Installed on iOS

- **🏠 Home Screen Icon** - Launch CrateJuice like any native app
- **📱 Full Screen Experience** - No browser UI, just your music
- **⚡ Offline Support** - Access your crates even without internet
- **🔔 Background Audio** - Keep playing while using other apps
- **💾 Persistent Data** - Your preferences and playlists stay saved

## 📲 How to Install on iPhone/iPad

### Step 1: Open in Safari
1. Open **Safari** browser on your iOS device
2. Navigate to your CrateJuice URL (e.g., `https://yourdomain.com` or your GitHub Pages URL)

> ⚠️ **Important**: You must use Safari. Installation won't work in Chrome, Firefox, or other browsers on iOS.

### Step 2: Add to Home Screen
1. Tap the **Share** button (box with arrow pointing up) at the bottom of Safari
2. Scroll down and tap **"Add to Home Screen"**
3. Edit the name if desired (default: "CrateJuice")
4. Tap **"Add"** in the top-right corner

### Step 3: Launch the App
1. Find the CrateJuice icon on your home screen
2. Tap to launch - it will open in full-screen mode!
3. Enjoy your music crates 🎵

## 🎨 iOS-Specific Features

### Status Bar Styling
The app uses a translucent black status bar that blends beautifully with the dark theme.

### Viewport Optimization
- Full viewport coverage with `viewport-fit=cover`
- Optimized for iPhone notches and safe areas
- Portrait-primary orientation for best music experience

### App Icon
The app will use the violet CrateJuice icon by default. The icon appears crisp on all iOS devices including Retina displays.

## 🔧 Technical Details

### PWA Manifest Configuration
```json
{
  "name": "CrateJuice",
  "short_name": "CJ",
  "display": "standalone",
  "orientation": "portrait-primary",
  "theme_color": "#7e5bef",
  "background_color": "#0b0b0f"
}
```

### iOS Meta Tags
```html
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="CrateJuice">
<link rel="apple-touch-icon" href="./icons/app_violet.svg">
```

## 🎵 Using the App

### Main Player
- Browse your music crates
- Adjust shuffle/surprise level
- Control pitch/playback speed
- Download tracks for offline listening

### Gift Packages
- Access themed gift crates at `/gift/[tag-name]/`
- Personalized messages and theming
- Share music with friends

## 🐛 Troubleshooting

### App Won't Install
- **Solution**: Make sure you're using Safari browser
- Check that you're on iOS 11.3 or later

### Icon Not Showing
- **Solution**: Try removing and re-adding to home screen
- Clear Safari cache and try again

### Audio Not Playing
- **Solution**: Check that Silent Mode is off
- Ensure volume is turned up
- Grant audio permissions if prompted

### App Won't Open Offline
- **Solution**: Make sure you've opened the app at least once while online
- The service worker needs to cache resources on first visit

## 🔄 Updating the App

When updates are available:
1. Open the app
2. The service worker will download updates in the background
3. Close and reopen the app to apply updates
4. Or remove and reinstall from Safari for a fresh install

## 📊 Compatibility

- **Minimum iOS Version**: iOS 11.3+
- **Recommended**: iOS 14.0 or later
- **Devices**: iPhone, iPad, iPod touch
- **Browser Required**: Safari (for installation)

## 🌐 Deployment Notes

### GitHub Pages URL
If deployed to GitHub Pages, your URL will be:
```
https://[username].github.io/cratejuice/
```

### Custom Domain
If using a custom domain, ensure:
- HTTPS is enabled (required for PWA)
- DNS is properly configured
- Service worker is registered correctly

## 💡 Tips for Best Experience

1. **Install First**: Always install to home screen for best performance
2. **Grant Permissions**: Allow audio permissions when prompted
3. **Use Headphones**: For best audio quality and background playback
4. **Check Storage**: Ensure device has space for cached music
5. **Stay Updated**: Remove and reinstall occasionally to get latest features

## 🆘 Support

Having issues? Check our troubleshooting guide or open an issue on GitHub:
- **Repository**: https://github.com/jujubeans85/cratejuice
- **Issues**: https://github.com/jujubeans85/cratejuice/issues

---

© 2025 CrateJuice. Built for music lovers by music lovers. 🎶

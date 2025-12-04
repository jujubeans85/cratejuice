// Share links (keep yours, any format). Clean ID is extracted automatically.
const MIMI = 'https://open.spotify.com/track/7xvkPmKDOZIGKe2HY...?si=whatever';
const CBO  = 'https://open.spotify.com/track/05WBvrLeaq96FCw0NcMb2N...?si=whatever';

function trackIdFrom(url) {
  const m = String(url).match(/track\/([A-Za-z0-9]+)\b/);
  return m ? m[1] : null;
}

function openSpotify(shareUrl) {
  const id = trackIdFrom(shareUrl);
  if (!id) return;

  // 1) Inline embed fallback (always render something)
  const embed = `https://open.spotify.com/embed/track/${id}?utm_source=generator`;
  const player = document.getElementById('player');
  player.innerHTML =
    `<iframe src="${embed}" width="100%" height="160" frameborder="0"
       allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"
       loading="lazy"></iframe>`;

  // 2) Deep-link to the app (most reliable on iOS)
  const appLink = `spotify://track/${id}`;

  // 3) Clean web URL fallback (strip weird params, add nd=1)
  const webLink = `https://open.spotify.com/track/${id}?nd=1`;

  // Navigate to the app (same tab is more reliable on iOS)
  try { window.location.href = appLink; } catch (_) {}

  // If the app isn’t available / blocked, open clean web in a new tab shortly after
  setTimeout(() => {
    window.open(webLink, '_blank', 'noopener');
  }, 500);
}

// Wire buttons
document.getElementById('btnMimi').onclick = () => openSpotify(MIMI);
document.getElementById('btnCbo').onclick  = () => openSpotify(CBO);

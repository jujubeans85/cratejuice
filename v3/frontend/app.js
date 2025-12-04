// === Set your links here (any of these work): ===============================
// - Direct audio: https://example.com/whatever.mp3
// - SoundCloud track page: https://soundcloud.com/artist/track
// - YouTube link: https://www.youtube.com/watch?v=dQw4w9WgXcQ  (or youtu.be/...)
// - Spotify link: we'll show an "Open in app" button and embed nothing (iOS issue)
const MIMI_URL = 'assets/audio/mimi.mp3';
const CBO_URL  = 'assets/audio/cbo.mp3';// ===========================================================================

const slot = document.getElementById('playerSlot');
const openAppRow = document.getElementById('openAppRow');
const openInAppBtn = document.getElementById('openInApp');

document.getElementById('btnMimi').addEventListener('click', () => play(MIMI_URL, 'Mimi'));
document.getElementById('btnCbo').addEventListener('click',  () => play(CBO_URL,  'Cbo'));

function play(url, who){
  if(!url){ return renderMessage(`Set a track URL for ${who} in app.js first.`); }
  const t = classify(url);

  // Reset
  slot.innerHTML = '';
  openAppRow.hidden = true;
  openInAppBtn.onclick = null;

  if (t.kind === 'mp3') {
    slot.innerHTML = `<audio controls autoplay src="${escapeAttr(url)}"></audio>`;
    return;
  }
  if (t.kind === 'youtube' && t.id) {
    const src = `https://www.youtube.com/embed/${t.id}?autoplay=1&rel=0`;
    slot.innerHTML = `<iframe allow="autoplay; encrypted-media; picture-in-picture" src="${src}"></iframe>`;
    return;
  }
  if (t.kind === 'soundcloud') {
    const src = `https://w.soundcloud.com/player/?url=${encodeURIComponent(url)}&auto_play=true`;
    slot.innerHTML = `<iframe allow="autoplay" src="${src}"></iframe>`;
    return;
  }
  if (t.kind === 'spotify' && t.id) {
    // iOS Safari routinely blocks Spotify Web — push to the app instead.
    const appLink = `spotify://track/${t.id}`;
    const webLink = `https://open.spotify.com/track/${t.id}?nd=1`;

    openAppRow.hidden = false;
    openInAppBtn.onclick = () => {
      try { window.location.href = appLink; } catch(_) {}
      setTimeout(() => window.open(webLink, '_blank', 'noopener'), 400);
    };
    renderMessage('Spotify is blocked here. Tap “Open in App”.');
    return;
  }

  // Unknown → just open the link in a new tab
  window.open(url, '_blank', 'noopener');
  renderMessage('Opened in a new tab.');
}

function classify(u){
  const url = String(u);
  if (/\.(mp3|m4a|aac|wav|ogg)(\?|$)/i.test(url)) return {kind:'mp3'};
  if (/soundcloud\.com/i.test(url)) return {kind:'soundcloud'};
  if (/youtu\.be|youtube\.com/i.test(url)) return {kind:'youtube', id: ytId(url)};
  if (/spotify\.com\/track|^spotify:track:/i.test(url)) return {kind:'spotify', id: spotifyId(url)};
  return {kind:'other'};
}
function ytId(u){
  // handles youtu.be/ID and youtube.com/watch?v=ID
  const short = u.match(/youtu\.be\/([A-Za-z0-9_-]{11})/);
  if (short) return short[1];
  const long = u.match(/[?&]v=([A-Za-z0-9_-]{11})/);
  return long ? long[1] : null;
}
function spotifyId(u){
  const m1 = u.match(/spotify\.com\/track\/([A-Za-z0-9]+)/);
  if (m1) return m1[1];
  const m2 = u.match(/^spotify:track:([A-Za-z0-9]+)/);
  return m2 ? m2[1] : null;
}
function renderMessage(text){
  slot.innerHTML = `<div style="padding:10px;color:#cfe7ff">${escapeHtml(text)}</div>`;
}
function escapeAttr(s){ return String(s).replace(/"/g, '&quot;'); }
function escapeHtml(s){ return String(s).replace(/[&<>"]/g, m => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[m])); }

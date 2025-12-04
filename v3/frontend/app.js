// CrateJuice v3 — Live Crate (minimal + robust)

// Correct tracks
const CJ = {
  MIMI: 'https://open.spotify.com/track/61FHPHXfnA0SG9sGjkrHNo',
  CBO:  'https://open.spotify.com/track/23KpKEx7BEiILEiUzWpaql',
};

// --- Track URLs ---
// Embed versions (for inline iframe)
const MIMI_EMBED = "https://open.spotify.com/embed/track/7vxKPmBKOZiGKpeEHY7cpqe?utm_source=generator";
const CBO_EMBED  = "https://open.spotify.com/embed/track/05WBvrtLeaq9F6PcwoNbm2N?si=sgARHvT7RASPUDf0-ezSYQ&theme=0";

// Direct links (new tab fallback)
const MIMI_LINK = "https://open.spotify.com/track/7vxKPmBKOZiGKpeEHY7cpqe";
const CBO_LINK  = "https://open.spotify.com/track/05WBvrtLeaq9F6PcwoNbm2N";

// Feature flag: inline = true → render iframe; false → open new tab
const INLINE = true;

// --- Track URLs ---
// Embed versions (for inline iframe)
const MIMI_EMBED = "https://open.spotify.com/embed/track/7vxKPmBKOZiGKpeEHY7cpqe?utm_source=generator";
const CBO_EMBED  = "https://open.spotify.com/embed/track/05WBvrtLeaq9F6PcwoNbm2N?si=sgARHvT7RASPUDf0-ezSYQ&theme=0";

// Direct links (new tab fallback)
const MIMI_LINK = "https://open.spotify.com/track/7vxKPmBKOZiGKpeEHY7cpqe";
const CBO_LINK  = "https://open.spotify.com/track/05WBvrtLeaq9F6PcwoNbm2N";

// Feature flag: inline = true → render iframe; false → open new tab
const INLINE = true;

function renderInline(src) {
  const player = document.getElementById('player');
  if (!player) return window.open(src.replace('/embed',''), '_blank', 'noopener');
  player.innerHTML = `
    <iframe
      src="${src}"
      width="100%" height="152" frameborder="0"
      allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"
      loading="lazy" style="border-radius:12px"
    ></iframe>`;
  player.scrollIntoView({ behavior: 'smooth', block: 'center' });
}
// --- Track URLs ---
// Embed versions (for inline iframe)
const MIMI_EMBED = "https://open.spotify.com/embed/track/7vxKPmBKOZiGKpeEHY7cpqe?utm_source=generator";
const CBO_EMBED  = "https://open.spotify.com/embed/track/05WBvrtLeaq9F6PcwoNbm2N?si=sgARHvT7RASPUDf0-ezSYQ&theme=0";

// Direct links (new tab fallback)
const MIMI_LINK = "https://open.spotify.com/track/7vxKPmBKOZiGKpeEHY7cpqe";
const CBO_LINK  = "https://open.spotify.com/track/05WBvrtLeaq9F6PcwoNbm2N";

// Feature flag: inline = true → render iframe; false → open new tab
const INLINE = true;

// --- Track URLs ---
// Embed versions (for inline iframe)
const MIMI_EMBED = "https://open.spotify.com/embed/track/7vxKPmBKOZiGKpeEHY7cpqe?utm_source=generator";
const CBO_EMBED  = "https://open.spotify.com/embed/track/05WBvrtLeaq9F6PcwoNbm2N?si=sgARHvT7RASPUDf0-ezSYQ&theme=0";

// Direct links (new tab fallback)
const MIMI_LINK = "https://open.spotify.com/track/7vxKPmBKOZiGKpeEHY7cpqe";
const CBO_LINK  = "https://open.spotify.com/track/05WBvrtLeaq9F6PcwoNbm2N";

// Feature flag: inline = true → render iframe; false → open new tab
const INLINE = true;

function renderInline(src) {
  const player = document.getElementById('player');
  if (!player) return window.open(src.replace('/embed',''), '_blank', 'noopener');
  player.innerHTML = `
    <iframe
      src="${src}"
      width="100%" height="152" frameborder="0"
      allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"
      loading="lazy" style="border-radius:12px"
    ></iframe>`;
  player.scrollIntoView({ behavior: 'smooth', block: 'center' });
}

function playMimi(){
  if (INLINE) renderInline(MIMI_EMBED);
  else window.open(MIMI_LINK, '_blank', 'noopener');
}

function playCbo(){
  if (INLINE) renderInline(CBO_EMBED);
  else window.open(CBO_LINK, '_blank', 'noopener');
}

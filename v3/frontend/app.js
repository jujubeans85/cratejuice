// CrateJuice v3 — Live Crate (minimal + robust)

// Correct tracks
const CJ = {
  MIMI: 'https://open.spotify.com/track/61FHPHXfnA0SG9sGjkrHNo',
  CBO:  'https://open.spotify.com/track/23KpKEx7BEiILEiUzWpaql',
};

function playMimi() { window.open(CJ.MIMI, '_blank', 'noopener,noreferrer'); }
function playCbo()  { window.open(CJ.CBO,  '_blank', 'noopener,noreferrer'); }

// Ensure inline onclick works even in stricter setups:
window.playMimi = playMimi;
window.playCbo  = playCbo;

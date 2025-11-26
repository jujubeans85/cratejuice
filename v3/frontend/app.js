// CHANGE THESE TO ANY URLs YOU WANT
const TRACK_1 = "https://filesamples.com/samples/audio/mp3/sample3.mp3";
const TRACK_2 = "https://filesamples.com/samples/audio/mp3/sample4.mp3";

function playTrack(num) {
  const player = document.getElementById("player");
  player.src = num === 1 ? TRACK_1 : TRACK_2;
  player.play();
}
// Mimi's track (your link)
const MIMI = "https://open.spotify.com/embed/track/05WBwrL0aq96FCwObMm2NB";

// Replace this with CBO's Spotify link anytime
const CBO = "https://open.spotify.com/embed/track/2takcwOaAZWiXQijPHIx7B";

function playTrack(which) {
  const player = document.getElementById("player");
  const url = which === 1 ? MIMI : CBO;

  player.innerHTML = `
    <iframe 
      style="border-radius:12px" 
      src="${url}?utm_source=generator" 
      width="100%" 
      height="152" 
      frameBorder="0" 
      allowfullscreen="" 
      allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture">
    </iframe>
  `;
}
// --- Mimi & Cbo dual-track crate ---
const juiceCrate = {
  mimi: "https://open.spotify.com/track/7rvkPmKDGZIKpEZH7CpqQe?si=6DadVL7_Qaa4HhAF6SPxPw",
  cbo: "https://open.spotify.com/track/05WBwrL0aq96FCwObMm2NB?si=gARhVTf7RASPUbFQ-ezSYQ&context=spotify%3Aplaylist%3A37i9dQZF1EQnqst5TRi17F"
};

function playCrateTrack(name) {
  const url = juiceCrate[name];
  if (!url) return;
  window.open(url, "_blank");
}
// --- Live Crate: Mimi & Cbo buttons ---

function playMimi() {
  window.open(
    'https://open.spotify.com/track/7rvkPmKDGZIKpEZH7CpqQe?si=6DadVL7_Qaa4HhAF6SPxPw',
    '_blank',
    'noopener'
  );
}

function playCbo() {
  // TODO: paste Cbo's real Spotify track URL here
  window.open(
    'https://open.spotify.com/', // <--- replace with Cbo track link
    '_blank',
    'noopener'
  );
}
// --- Live Crate: Mimi & Cbo dual-track panel ---

const mimiTrackUrl = "https://open.spotify.com/track/7rvkPmKDGZIKpEZH7CpqQe?si=6DadVL7_Qaa4HhAF6SPxPw";
// If you want a different Cbo track later, just swap this URL:
const cboTrackUrl  = "https://open.spotify.com/track/23KpKEx7BEiILEiUzWpaql?si=Z1J7mcx2T66YIbFqS4zztQ";

function playMimi() {
  window.open("https://open.spotify.com/track/7rvkPmKDGZIKpEZH7CpqQe?si=6DadVL7_Qaa4HhAF6SPxPw", "_blank");
}

function playCbo() {
  window.open("https://open.spotify.com/track/05WBwrL0aq96FCwObMm2NB?si=gARhVTf7RASPUbFQ-ezSYQ", "_blank");
}

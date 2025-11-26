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

function playMimi() {
  window.open(
    "https://open.spotify.com/track/7rvkPmKDGZIKpEZH7CpqQe?si=6DadVL7_Qaa4HhAF6SPxPw",
    "_blank",
    "noopener"
  );
}

function playCbo() {
  window.open(
    "https://open.spotify.com/track/05WBwrL0aq96FCwObMm2NB?si=gARhVTf7RASPUbFQ-ezSYQ",
    "_blank",
    "noopener"
  );
}

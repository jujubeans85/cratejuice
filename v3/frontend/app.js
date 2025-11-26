// ----------------------
// CrateJuice v3 frontend
// Clean + corrected
// ----------------------

// Original player (kept intact for future use)
function playTrack(num) {
  const MIMI = "https://open.spotify.com/embed/track/7rvkPmKDGZIKpEZH7CpqQe?utm_source=generator";
  const CBO  = "https://open.spotify.com/embed/track/05WBwrL0aq96FCwObMm2NB?utm_source=generator";

  const which = num === 1 ? MIMI : CBO;
  const player = document.getElementById("player");

  player.innerHTML = `
    <iframe 
      src="${which}"
      style="border-radius:12px"
      width="100%"
      height="180"
      frameborder="0"
      allowfullscreen
      allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"
    ></iframe>
  `;
}

// ----------------------
// LIVE CRATE (Mimi & Cbo) — FINAL CLEAN VERSION
// ----------------------

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

// ----------------------
// End of file
// ----------------------

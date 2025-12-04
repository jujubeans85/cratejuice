/* CrateJuice v3 – Option A (new-tab only, no iframe) */

const MIMI = "https://open.spotify.com/track/7vxKPmBKOZiGKpeEHY7cpqe";
const CBO  = "https://open.spotify.com/track/05WBvrtLeaq9F6PcwoNbm2N";

function openTrack(url){
  // clean, popup-blocker friendly when called from a click
  window.open(url, "_blank", "noopener");
}

function playMimi(){ openTrack(MIMI); }
function playCbo(){  openTrack(CBO);  }

// wire up both ID and inline-onclick styles
document.addEventListener("DOMContentLoaded", () => {
  document.getElementById("btnMimi")?.addEventListener("click", playMimi);
  document.getElementById("btnCbo") ?.addEventListener("click", playCbo);
});
window.playMimi = playMimi;
window.playCbo  = playCbo;

/* CrateJuice v3 frontend — inline player + fallback */

// --- Track URLs ---
// Embed versions (inline iframe)
const MIMI_EMBED = "https://open.spotify.com/embed/track/7vxKPmBKOZiGKpeEHY7cpqe?utm_source=generator";
const CBO_EMBED  = "https://open.spotify.com/embed/track/05WBvrtLeaq9F6PcwoNbm2N?utm_source=generator&theme=0";

// Direct links (new-tab fallback)
const MIMI_LINK = "https://open.spotify.com/track/7vxKPmBKOZiGKpeEHY7cpqe";
const CBO_LINK  = "https://open.spotify.com/track/05WBvrtLeaq9F6PcwoNbm2N";

// Feature flag: set to false if you want only new-tab behavior
const INLINE = true;

/** Render an inline iframe player, else fallback to new tab */
function renderInline(src) {
  try {
    const player = document.getElementById("player");
    if (!player) {
      window.open(src.replace("/embed", ""), "_blank", "noopener");
      return;
    }
    player.innerHTML = `
      <iframe
        src="${src}"
        width="100%"
        height="152"
        frameborder="0"
        allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"
        loading="lazy"
        style="border-radius:12px"
      ></iframe>
    `;
    player.scrollIntoView({ behavior: "smooth", block: "center" });
  } catch (e) {
    // absolute fallback
    window.open(src.replace("/embed", ""), "_blank", "noopener");
  }
}

function playMimi() {
  if (INLINE) renderInline(MIMI_EMBED);
  else window.open(MIMI_LINK, "_blank", "noopener");
}

function playCbo() {
  if (INLINE) renderInline(CBO_EMBED);
  else window.open(CBO_LINK, "_blank", "noopener");
}

// Also wire up by ID in case inline onclicks are removed later
document.addEventListener("DOMContentLoaded", () => {
  const m = document.getElementById("btnMimi");
  const c = document.getElementById("btnCbo");
  if (m && !m.onclick) m.addEventListener("click", playMimi);
  if (c && !c.onclick) c.addEventListener("click", playCbo);
});

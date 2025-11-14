// Crate Juice v3 - Main Application Script

const API_BASE = "https://cjcathederal.onrender.com";

async function loadTracks() {
  try {
    const res = await fetch(`${API_BASE}/tracks`);
    const data = await res.json();

    const list = document.getElementById("tracks");
    if (!list) return;

    list.innerHTML = "";

    data.tracks.forEach((t) => {
      const card = document.createElement("article");
      card.className = "track-card";

      const title = document.createElement("h4");
      title.textContent = t.title;

      const meta = document.createElement("p");
      meta.className = "track-meta";
      meta.textContent = t.artist ? t.artist : "Unknown artist";

      card.appendChild(title);
      card.appendChild(meta);

      if (t.url) {
        const link = document.createElement("a");
        link.href = t.url;
        link.target = "_blank";
        link.rel = "noopener noreferrer";
        link.textContent = "Open link";
        link.className = "track-link";
        card.appendChild(link);
      }

      list.appendChild(card);
    });
  } catch (err) {
    console.error("Error loading tracks:", err);
  }
}

async function addTrack(event) {
  event.preventDefault();

  const titleEl = document.getElementById("track-title");
  const artistEl = document.getElementById("track-artist");
  const urlEl = document.getElementById("track-url");

  const track = {
    title: titleEl.value.trim(),
    artist: artistEl.value.trim() || null,
    url: urlEl.value.trim() || null,
  };

  if (!track.title) return;

  try:
    const res = await fetch(`${API_BASE}/tracks`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(track),
    });

    if (!res.ok) {
      console.error("Failed to add track");
      return;
    }

    // Clear form
    titleEl.value = "";
    artistEl.value = "";
    urlEl.value = "";

    // Reload list
    await loadTracks();
  } catch (err) {
    console.error("Error adding track:", err);
  }
}

async function spinRandom() {
  const display = document.getElementById("random-display");
  if (!display) return;

  display.textContent = "Spinning…";

  try {
    const res = await fetch(`${API_BASE}/tracks/random`);
    const data = await res.json();

    if (!data.track) {
      display.textContent = "No tracks in crate yet.";
      return;
    }

    const t = data.track;
    display.innerHTML = `
      <div class="random-card">
        <div class="random-title">${t.title}</div>
        <div class="random-artist">${t.artist || "Unknown artist"}</div>
        ${
          t.url
            ? `<a href="${t.url}" target="_blank" rel="noopener noreferrer" class="track-link">Open link</a>`
            : ""
        }
      </div>
    `;
  } catch (err) {
    console.error("Error getting random track:", err);
    display.textContent = "Error spinning crate.";
  }
}

document.addEventListener("DOMContentLoaded", () => {
  loadTracks();

  const form = document.getElementById("add-track-form");
  if (form) {
    form.addEventListener("submit", addTrack);
  }

  const randomBtn = document.getElementById("random-btn");
  if (randomBtn) {
    randomBtn.addEventListener("click", spinRandom);
  }
});

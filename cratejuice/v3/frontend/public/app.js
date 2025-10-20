const $ = sel => document.querySelector(sel);
const listEl = $("#list"), player = $("#player"), cover = $("#cover");
const pitch = $("#pitch"), pitchVal = $("#pitchVal");
const surprise = $("#surprise"), spVal = $("#surpriseVal");
const dl = $("#dl"); 

let playlist = [], current = null, library = {};

// Backend API configuration
const API_CONFIG = {
    baseUrl: window.location.hostname === 'localhost' 
        ? 'http://localhost:5000' 
        : 'https://cratejuice-backend.onrender.com',
    endpoints: {
        health: '/api/health',
        library: '/api/library',
        playlist: '/api/playlist'
    }
};

// API utility function
async function fetchAPI(endpoint) {
    try {
        const response = await fetch(`${API_CONFIG.baseUrl}${endpoint}`);
        if (!response.ok) {
            throw new Error(`API Error: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.log(`Backend API not available for ${endpoint}, using fallback`);
        return null;
    }
}

// Simple direct playlist data
const sampleTracks = [
  {
    id: "1",
    title: "Midnight Drive",
    artist: "Synthwave Studios",
    file: "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3",
    duration: "3:24"
  },
  {
    id: "2", 
    title: "Digital Dreams",
    artist: "Retro Collective",
    file: "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3",
    duration: "4:12"
  },
  {
    id: "3",
    title: "Neon Nights", 
    artist: "Electric Avenue",
    file: "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-3.mp3",
    duration: "3:48"
  },
  {
    id: "4",
    title: "Cyber City",
    artist: "Future Bass", 
    file: "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-4.mp3",
    duration: "4:01"
  },
  {
    id: "5",
    title: "Starlight Highway",
    artist: "Ambient Waves",
    file: "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-5.mp3", 
    duration: "5:15"
  }
];

async function loadData(){
  // Try to load from backend API first
  try {
    const backendLib = await fetchAPI(API_CONFIG.endpoints.library);
    const backendPlaylist = await fetchAPI(API_CONFIG.endpoints.playlist);
    
    if (backendLib && backendLib.tracks && Object.keys(backendLib.tracks).length > 0) {
      library = backendLib.tracks;
      if (backendPlaylist && Array.isArray(backendPlaylist)) {
        playlist = backendPlaylist.map(id => ({
          id,
          title: library[id]?.title || `Track ${id}`,
          artist: library[id]?.artist || 'Unknown Artist', 
          file: library[id]?.url || '',
          duration: library[id]?.duration || '0:00'
        })).filter(t => t.file);
      } else {
        playlist = Object.keys(library).map(id => ({
          id,
          title: library[id].title,
          artist: library[id].artist,
          file: library[id].url,
          duration: library[id].duration
        }));
      }
      console.log('✅ Loaded data from backend API');
    }
  } catch (error) {
    console.log('Backend API not available, trying local files');
  }
  
  // Fallback to local files if backend didn't work
  if (playlist.length === 0) {
    try {
      const lib = await fetch("./library.json").then(r=>r.json()).catch(()=>null);
      const p = await fetch("./playlist.json").then(r=>r.json()).catch(()=>null);
      
      if (lib && lib.tracks && Object.keys(lib.tracks).length > 0) {
        library = lib.tracks;
        if (p && Array.isArray(p)) {
          playlist = p.map(id => ({
            id,
            title: library[id]?.title || `Track ${id}`,
            artist: library[id]?.artist || 'Unknown Artist', 
            file: library[id]?.url || '',
            duration: library[id]?.duration || '0:00'
          })).filter(t => t.file);
        } else {
          playlist = Object.keys(library).map(id => ({
            id,
            title: library[id].title,
            artist: library[id].artist,
            file: library[id].url,
            duration: library[id].duration
          }));
        }
        console.log('✅ Loaded data from local files');
      }
    } catch (error) {
      console.log('Could not load local data files, using sample data');
    }
  }
  
  // Final fallback to sample data if everything else failed
  if (playlist.length === 0) {
    playlist = sampleTracks;
    console.log('✅ Using sample data');
  }
  
  console.log('Final playlist:', playlist);
  render();
}
function pickOrder(){
  const pct = Number(surprise.value)||0;
  const arr = [...playlist];
  const out=[]; while(arr.length){
    if(Math.random()*100<pct){ out.push(arr.splice(Math.floor(Math.random()*arr.length),1)[0]); }
    else { out.push(arr.shift()); }
  }
  return out;
}
function render(){
  console.log('Rendering with playlist:', playlist);
  spVal.textContent = surprise.value+"%";
  listEl.innerHTML = "";
  
  if (playlist.length === 0) {
    listEl.innerHTML = "<div style='color: #f5f5f7; padding: 20px; text-align: center;'>No tracks loaded. Check console for errors.</div>";
    return;
  }
  
  const order = pickOrder();
  order.forEach((t,i)=>{
    const div = document.createElement("div"); div.className="track";
    div.innerHTML = `<div class="meta"><div class="num">${i+1}</div><div><div class="title">${t.title||"Untitled"}</div><div class="artist">${t.artist||"Unknown Artist"}</div></div></div><button class="play">Play</button>`;
    div.querySelector(".play").addEventListener("click",()=>playTrack(t));
    listEl.appendChild(div);
  });
}
function playTrack(t){
  current = t;
  player.src = t.file;
  player.playbackRate = Number(pitch.value)||1;
  cover.src = t.cover || "./cover_default.png";
  player.play();
  dl.onclick = ()=>{ const a=document.createElement("a"); a.href=t.file; a.download=(t.title||"track")+".mp3"; a.click(); };
}
pitch.addEventListener("input", ()=>{ pitchVal.textContent = (Number(pitch.value)||1).toFixed(2)+"×"; player.playbackRate=Number(pitch.value)||1; });
surprise.addEventListener("change", render);

// Service Worker registration for PWA functionality
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('./service-worker.js')
      .then(registration => console.log('SW registered:', registration))
      .catch(error => console.log('SW registration failed:', error));
  });
}

let deferredPrompt;
window.addEventListener("beforeinstallprompt", (e)=>{ e.preventDefault(); deferredPrompt = e; const btn=document.getElementById("install"); btn.hidden=false; btn.onclick=async()=>{ btn.hidden=true; deferredPrompt.prompt(); await deferredPrompt.userChoice; deferredPrompt=null; };});
loadData();

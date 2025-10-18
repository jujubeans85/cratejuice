const $ = sel => document.querySelector(sel);
const listEl = $("#list"), player = $("#player"), cover = $("#cover");
const pitch = $("#pitch"), pitchVal = $("#pitchVal");
const surprise = $("#surprise"), spVal = $("#surpriseVal");
const dl = $("#dl"); let playlist = [], current = null, library = {};

async function loadData(){
  const p = await fetch("../../content/data/playlist_8.json").then(r=>r.json()).catch(()=>[]);
  const lib = await fetch("../../content/data/library.json").then(r=>r.json()).catch(()=>({tracks:{}}));
  playlist = Array.isArray(p) ? p : (p.tracks||[]); library = lib.tracks || {};
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
  spVal.textContent = surprise.value+"%";
  listEl.innerHTML = "";
  const order = pickOrder();
  order.forEach((t,i)=>{
    const div = document.createElement("div"); div.className="track";
    div.innerHTML = `<div class="meta"><div class="num">${i+1}</div><div><div class="title">${t.title||""}</div><div class="artist">${t.artist||""}</div></div></div><button class="play">Play</button>`;
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
let deferredPrompt;
window.addEventListener("beforeinstallprompt", (e)=>{ e.preventDefault(); deferredPrompt = e; const btn=document.getElementById("install"); btn.hidden=false; btn.onclick=async()=>{ btn.hidden=true; deferredPrompt.prompt(); await deferredPrompt.userChoice; deferredPrompt=null; };});
loadData();

// CrateJuice two-deck — local-first with Spotify fallback
const TRACKS = {
  mimi: {
    local: 'assets/audio/mimi.mp3',
    web: 'https://open.spotify.com/track/7xvkPmKDGZIKpeEHY7cp9e?si=sQaDvl7_Oaa4HhAF6SPxPw',
  },
  cbo: {
    local: 'assets/audio/cbo.mp3',
    web: 'https://open.spotify.com/track/05WBwrLeaq96FcwoNbm2N8?si=sgARHvT7RASPUDF0-e2SYQ',
  }
};

const A = document.getElementById('audioA');
const B = document.getElementById('audioB');

let A_hasLocal = false;
let B_hasLocal = false;

async function probe(src){
  try{
    const res = await fetch(src, { method:'HEAD' });
    return res.ok;
  }catch(e){ return false; }
}

function wireDeck(btnPlayId, btnStopId, audioEl, pitchId, statusId, track, setLocalFlag){
  const btnPlay = document.getElementById(btnPlayId);
  const btnStop = document.getElementById(btnStopId);
  const pitch = document.getElementById(pitchId);
  const status = document.getElementById(statusId);

  pitch.addEventListener('input', ()=>{ audioEl.playbackRate = parseFloat(pitch.value || 1); });

  btnPlay.addEventListener('click', ()=>{
    if(setLocalFlag()){
      audioEl.play().catch(()=>{});
    }else{
      window.open(track.web, '_blank', 'noopener');
    }
  });
  btnStop.addEventListener('click', ()=> audioEl.pause());

  status.textContent = 'Source: Checking…';
  probe(track.local).then(ok=>{
    if(ok){ audioEl.src = track.local; status.textContent = 'Source: Local file'; setLocalFlag(true); }
    else   { status.textContent = 'Source: Spotify'; setLocalFlag(false); }
  });
}

// Crossfader [-1..1] → sets A/B volumes
const xfader = () => {
  const slider = document.getElementById('xfader');
  const apply = ()=>{
    const v = parseFloat(slider.value || 0);
    const a = (v < 0) ? 1 : 1 - v;
    const b = (v > 0) ? 1 : 1 + v;
    A.volume = Math.max(0, Math.min(1, a));
    B.volume = Math.max(0, Math.min(1, b));
  };
  slider.addEventListener('input', apply);
  apply();
};

document.addEventListener('DOMContentLoaded', ()=>{
  wireDeck('playMimi','stopMimi',A,'pitchA','statusA',TRACKS.mimi,(val)=>{
    if(typeof val==='boolean') A_hasLocal = val; return A_hasLocal;
  });
  wireDeck('playCbo','stopCbo',B,'pitchB','statusB',TRACKS.cbo,(val)=>{
    if(typeof val==='boolean') B_hasLocal = val; return B_hasLocal;
  });
  xfader();
});
function openExternal(url) {
  try {
    const a = document.createElement('a');
    a.href = url;
    a.target = '_blank';
    a.rel = 'noopener noreferrer';
    document.body.appendChild(a);
    a.click();
    a.remove();
  } catch {
    // absolute last-ditch
    window.location.href = url;
  }
}

// Example wire-up
document.getElementById('mimiOpen').onclick = () =>
  openExternal('https://open.spotify.com/track/7rvIxPkDOKZIKpeEHY7Cpg9'); // your real link
document.getElementById('cboOpen').onclick = () =>
  openExternal('https://open.spotify.com/track/05WBwtLeaq9f6PCwloNM2B');   // your real link

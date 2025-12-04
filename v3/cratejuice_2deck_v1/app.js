// CrateJuice two‑deck starter
const SPOTIFY = {
  MIMI: 'https://open.spotify.com/track/61FHPHXfnA0SG9sGjkrHNo',
  CBO:  'https://open.spotify.com/track/23KpKEx7BEiILEiUzWpaql'
}
const a = document.getElementById('audioA');
const b = document.getElementById('audioB');
function mark(deck, on){ (document.getElementById(deck==='A'?'deckA':'deckB')).classList.toggle('playing', !!on); }
function safePlay(audioEl, fallbackUrl, deck){
  let erred = false;
  const onErr=()=>{erred=true;mark(deck,false);window.open(fallbackUrl,'_blank','noopener');};
  audioEl.addEventListener('error', onErr, {once:true});
  const p = audioEl.play();
  if(p && p.catch){ p.catch(()=>{ mark(deck,false); window.open(fallbackUrl,'_blank','noopener'); }); }
  else { // older browsers
    setTimeout(()=>{ if(audioEl.paused){ window.open(fallbackUrl,'_blank','noopener'); }}, 600); 
  }
  mark(deck,true);
}
function playMimi(){ safePlay(a, SPOTIFY.MIMI, 'A'); }
function playCbo(){ safePlay(b, SPOTIFY.CBO, 'B'); }
function pauseA(){ a.pause(); mark('A', false); }
function pauseB(){ b.pause(); mark('B', false); }
function setRate(deck,val){ (deck==='A'?a:b).playbackRate=parseFloat(val); }
function xFade(val){ const t=parseFloat(val)/100; a.volume=Math.cos(0.5*Math.PI*t); b.volume=Math.cos(0.5*Math.PI*(1-t)); }

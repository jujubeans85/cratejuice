let URL_A='https://spotify.link/5U9qgM6o9Db';
let URL_B='https://spotify.link/gBq4sC7p9Db';
function refreshLabels(){document.getElementById('urlA').textContent=URL_A;document.getElementById('urlB').textContent=URL_B;}
function openA(){window.open(URL_A,'_blank','noopener');}
function openB(){window.open(URL_B,'_blank','noopener');}
function swapA(){const u=prompt('New URL for Deck A:',URL_A||'');if(u){URL_A=u.trim();refreshLabels();}}
function swapB(){const u=prompt('New URL for Deck B:',URL_B||'');if(u){URL_B=u.trim();refreshLabels();}}
refreshLabels();

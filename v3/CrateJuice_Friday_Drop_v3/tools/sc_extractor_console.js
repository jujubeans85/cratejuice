// Paste in DevTools Console on a SoundCloud list page
(async()=>{const sleep=ms=>new Promise(r=>setTimeout(r,ms));
const clean=s=>String(s||'').replace(/\s+/g,' ').trim();
const rows=[];const seen=new Set();let lastH=0;let same=0;
for(let i=0;i<80;i++){window.scrollTo(0,document.body.scrollHeight);await sleep(700);
  let h=document.body.scrollHeight;if(h===lastH){same++;}else{same=0;lastH=h;} if(same>=3) break;}
const els=document.querySelectorAll('article,li,div a[href*="soundcloud.com"],a.sc-link-primary');
for(const el of els){let a=el.closest('a[href*="soundcloud.com"]')||el.querySelector?.('a')||el;
  let url=a&&a.href?new URL(a.href).href:''; if(!url||seen.has(url)) continue;
  let title=clean(el.textContent||a.textContent||''); let artist=title.split('·')[0]||'';
  rows.push([title,artist,url]); seen.add(url);}
const header='title,artist,url\n';
const csv=header+rows.map(r=>r.map(x=>`"${String(x).replace(/"/g,'""')}"`).join(',')).join('\n');
console.log(csv);
})();

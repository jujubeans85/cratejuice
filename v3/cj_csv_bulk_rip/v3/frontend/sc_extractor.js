/* CrateJuice — SoundCloud Extractor (One Button) */
const CJ_SC = (() => {
  const STATE = { enrich: true, limit: 300 };

  function uiReady() {
    const host = location.hostname;
    const onSC = /(^|\.)soundcloud\.com$/i.test(host);
    const shortSC = /(^|\.)on\.soundcloud\.com$/i.test(host);
    return { onSC, shortSC };
  }

  async function runExtractor({ enrich = true, limit = 300 } = {}) {
    const scFilter = (u) => {
      try {
        const url = new URL(u, location.origin);
        if (!/soundcloud\.com$/i.test(url.hostname)) return null;
        ['utm_source','utm_medium','utm_campaign','utm_term','utm_content','si','ref'].forEach(k => url.searchParams.delete(k));
        const p = url.pathname.replace(/\/+$/, '');
        if (!p || p === '/' || /^\/(you|discover|legal|pages|imprint|terms|privacy)/i.test(p)) return null;
        const parts = p.split('/').filter(Boolean);
        return (parts.length >= 2) ? url.toString() : null;
      } catch { return null; }
    };

    const anchors = [...document.querySelectorAll('a[href]')];
    const cleaned = anchors.map(a => scFilter(a.href)).filter(Boolean);
    const uniq = [...new Set(cleaned)].slice(0, limit);

    async function enrichOne(u) {
      try {
        const r = await fetch(`https://soundcloud.com/oembed?format=json&url=${encodeURIComponent(u)}`);
        if (!r.ok) return { url: u };
        const j = await r.json();
        return {
          url: u,
          title: j.title || '',
          author: j.author_name || '',
          type: (j.html && j.html.includes('playlists')) ? 'set' : (j.type || '')
        };
      } catch {
        return { url: u };
      }
    }

    let rows;
    if (enrich) {
      rows = [];
      for (let i = 0; i < uniq.length; i++) {
        rows.push(await enrichOne(uniq[i]));
        await new Promise(r => setTimeout(r, 60));
      }
    } else {
      rows = uniq.map(u => ({ url: u }));
    }

    const headers = ['url','title','author','type'];
    const esc = (s='') => `"${String(s).replace(/"/g,'""')}"`;
    const csv = [headers.join(',')]
      .concat(rows.map(r => [r.url, r.title || '', r.author || '', r.type || ''].map(esc).join(',')))
      .join('\n');

    try { await navigator.clipboard.writeText(csv); } catch {}
    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url; a.download = 'soundcloud_links.csv';
    document.body.appendChild(a); a.click(); a.remove();
    URL.revokeObjectURL(url);
    alert(`CrateJuice: grabbed ${rows.length} link(s). CSV downloaded${enrich ? ' (with titles)' : ''}.`);
  }

  function makeBookmarklet(enrich = true, limit = 300) {
    const core = `(async(()=>{const E=${enrich},L=${limit},F=u=>{try{const e=new URL(u,location.origin);if(!/soundcloud\\.com$/i.test(e.hostname))return null;["utm_source","utm_medium","utm_campaign","utm_term","utm_content","si","ref"].forEach(k=>e.searchParams.delete(k));const p=e.pathname.replace(/\\+$/,"");if(!p||"/"===p||/^\\/(you|discover|legal|pages|imprint|terms|privacy)/i.test(p))return null;return p.split("/").filter(Boolean).length>=2?e.toString():null}catch{return null}},A=[...document.querySelectorAll("a[href]")].map(a=>a.href),C=[...new Set(A.map(F).filter(Boolean))].slice(0,L),en=async u=>{try{const r=await fetch("https://soundcloud.com/oembed?format=json&url="+encodeURIComponent(u));if(!r.ok)return{url:u};const j=await r.json();return{url:u,title:j.title||"",author:j.author_name||"",type:j.html&&j.html.includes("playlists")?"set":j.type||""}}catch{return{url:u}}};let rows;if(E){rows=[];for(let i=0;i<C.length;i++){rows.push(await en(C[i]));await new Promise(s=>setTimeout(s,60))}}else{rows=C.map(u=>({url:u}))}const H=["url","title","author","type"],esc=s=>\"\"\${String(s||\"\").replace(/\"/g,'\\"\\"')}\\"",csv=[H.join(",")].concat(rows.map(r=>[r.url,r.title||"",r.author||"",r.type||""].map(esc).join(","))).join("\\n");try{await navigator.clipboard.writeText(csv)}catch{}const b=new Blob([csv],{type:"text/csv;charset=utf-8;"}),x=URL.createObjectURL(b),a=document.createElement("a");a.href=x;a.download="soundcloud_links.csv";document.body.appendChild(a);a.click();a.remove();URL.revokeObjectURL(x);alert("CrateJuice: grabbed "+rows.length+" link(s). CSV downloaded"+(E?" (with titles)":"")+".");})();`;
    return 'javascript:' + core;
  }

  function mountPanel(containerId = 'cj-sc-panel') {
    if (document.getElementById(containerId)) return;
    const wrap = document.createElement('div');
    wrap.id = containerId;
    wrap.style = 'position:fixed;right:16px;bottom:16px;z-index:9999;background:#141416;border:1px solid #2a2a2d;border-radius:12px;padding:12px;font:14px/1.3 system-ui;color:#eee;box-shadow:0 8px 24px rgba(0,0,0,.35)';
    wrap.innerHTML = `
      <div style="display:flex;gap:8px;align-items:center;justify-content:space-between;margin-bottom:8px">
        <strong>SC → CSV</strong>
        <label style="display:flex;align-items:center;gap:6px;opacity:.8">
          <input type="checkbox" id="cj_enrich" checked/> Enrich titles
        </label>
      </div>
      <div style="display:flex;gap:8px;flex-wrap:wrap">
        <button id="cj_run" style="padding:.6rem 1rem;border:1px solid #444;background:#ff6a00;color:#111;border-radius:8px;font-weight:700;cursor:pointer">Grab on this page</button>
        <button id="cj_copy" class="secondary" style="padding:.6rem 1rem;border:1px solid #444;background:#1b1c1f;color:#ddd;border-radius:8px;cursor:pointer">Copy bookmarklet</button>
        <a id="cj_link" href="#" style="padding:.6rem 1rem;border:1px dashed #444;border-radius:8px;color:#ddd;text-decoration:none">Run bookmarklet</a>
      </div>
      <div style="opacity:.7;margin-top:8px;font-size:12px">
        Tip: open any SoundCloud playlist/user/likes page, then tap <em>Run bookmarklet</em> (iPad: add it to Bookmarks first).
      </div>
    `;
    document.body.appendChild(wrap);

    document.getElementById('cj_enrich').onchange = (e)=>{ updateBookmarkletLink(e.target.checked); };
    document.getElementById('cj_run').onclick = async ()=>{
      const h = location.hostname;
      const onSC = /(^|\.)soundcloud\.com$/i.test(h);
      if (!onSC) { alert('Open this on a soundcloud.com page and try again, or use the bookmarklet.'); return; }
      runExtractor({ enrich: document.getElementById('cj_enrich').checked });
    };
    document.getElementById('cj_copy').onclick = async ()=>{
      const bm = makeBookmarklet(document.getElementById('cj_enrich').checked);
      try { await navigator.clipboard.writeText(bm); alert('Bookmarklet copied. Create a bookmark and paste this into the URL field.'); }
      catch { prompt('Copy this bookmarklet code:', bm); }
    };
    function updateBookmarkletLink(checked=true){
      const bm = makeBookmarklet(checked);
      const link = document.getElementById('cj_link');
      link.setAttribute('href', bm);
    }
    updateBookmarkletLink(true);
  }

  return { mountPanel, runExtractor, makeBookmarklet };
})();
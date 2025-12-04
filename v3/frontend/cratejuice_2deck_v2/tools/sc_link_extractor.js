// SoundCloud link extractor (console/run-in-page)
(function(){
  const hrefs=[...document.querySelectorAll('a[href]')].map(a=>a.href);
  const uniq=[...new Set(hrefs)].filter(u=>/soundcloud\.com\//.test(u));
  const tracks=uniq.filter(u=>/(\/tracks\/|\/sets\/|soundcloud\.com\/[^/]+\/[^/]+$)/.test(u));
  const out=tracks.join('\n');
  console.log(out);
  try{navigator.clipboard.writeText(out);}catch(e){};
})();
/* SoundCloud link extractor (bookmarklet-friendly) */
(function(){
  const as=[...document.querySelectorAll('a[href]')];
  const good=as.map(a=>a.href).filter(u=>/soundcloud\.com\//.test(u));
  const dedup=[...new Set(good)];
  const tracks=dedup.filter(u=>/(\/tracks\/|\/sets\/|soundcloud\.com\/[^/]+\/[^/]+$)/.test(u));
  const out=tracks.join('\n');
  console.log('Found %d links:\n%s', tracks.length, out);
  try{navigator.clipboard.writeText(out);}catch(e){}
})();
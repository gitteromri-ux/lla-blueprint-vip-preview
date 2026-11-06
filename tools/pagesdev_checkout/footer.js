/* From pages.dev blueprint/index.html, function popup(): the popup footer (Continue + 14-day refund note) and the
   first start-date pre-selection, copied verbatim. Left out on purpose: the September promo labels and summary in the
   same function ($149 / $179 / save $249), which would show old prices next to the November offer. */
(function(){
  function popup(){
    try{ if(!document.getElementById('llaCoPrefetch')){ var pf=document.createElement('link'); pf.id='llaCoPrefetch'; pf.rel='prefetch'; pf.href='checkout.html'; pf.as='document'; document.head.appendChild(pf); } }catch(e){}
    var dlg=document.querySelector('#enrollModal .em-dialog'); if(!dlg||dlg.querySelector('.mock-footer')) return;
    var f=document.createElement('div'); f.className='mock-footer';
    var g2=document.getElementById('emGo2'), g1=document.getElementById('emGo1');
    if(g2) f.appendChild(g2); if(g1) f.appendChild(g1);
    var h=document.createElement('p'); h.className='mock-hint'; h.innerHTML='<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="#006EFF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/><path d="M9 12l2 2 4-4"/></svg> <b>14-day full refund.</b> Not for you? Email us, every cent back.'; f.appendChild(h);
    dlg.appendChild(f);
    var tries=0; (function pick(){ var cards=[].slice.call(document.querySelectorAll('#dpList .dp-card')).filter(function(c){return !c.querySelector('.dp-late')});
      var c=cards.find(function(c){return /Sep\s*22/.test(c.textContent)})||cards[0];
      if(c){ if(c.getAttribute('aria-checked')!=='true') c.click(); } else if(tries++<20) setTimeout(pick,150); })();
  }
  function run(){ try{popup();}catch(e){} }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',run); else run();
  window.addEventListener('load',function(){ setTimeout(run,300); setTimeout(run,1500); });
  document.addEventListener('click',function(e){ if(e.target.closest('a[href^="checkout.html"],[data-checkout-open]')) setTimeout(run,50); },true);
})();

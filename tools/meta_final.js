(function(){
  var cta=document.querySelector('#llaFloatCta'),pricing=document.getElementById('pricing'),fin=document.getElementById('apply');
  function upd(){
    if(!cta) return;
    var over=false;
    [pricing,fin].forEach(function(el){if(!el)return;var r=el.getBoundingClientRect();if(r.top<innerHeight*0.75&&r.bottom>innerHeight*0.25)over=true;});
    cta.classList.toggle('is-visible',window.scrollY>140);
    cta.classList.toggle('mf-hide',over);
  }
  addEventListener('scroll',upd,{passive:true});addEventListener('resize',upd);upd();
  function pillCase(){var mo=document.querySelector('#llaFloatCta .mo');if(mo&&/MONTH/.test(mo.textContent))mo.textContent='Month 1';}
  document.addEventListener('DOMContentLoaded',function(){setTimeout(pillCase,0);});addEventListener('lla:pricing',function(){setTimeout(pillCase,0);});addEventListener('load',pillCase);
  document.querySelectorAll('[data-preview-enroll]').forEach(function(a){a.addEventListener('click',function(e){e.preventDefault();var n=a.parentNode.querySelector('.pk-previewnote');if(n)n.hidden=false;});});
})();

(function(){
  /* the hero cells motion always plays (muted, inline), on phones too */
  var v=document.querySelector('#hero video.mf-cells'); if(!v) return;
  v.muted=true; v.setAttribute('muted',''); v.setAttribute('playsinline',''); v.loop=true;
  function go(){ try{ if(v.preload==='none') v.preload='auto'; var p=v.play(); if(p&&p.catch) p.catch(function(){}); }catch(e){} }
  if(document.readyState!=='loading') go(); else document.addEventListener('DOMContentLoaded',go);
  addEventListener('load',go); addEventListener('touchstart',go,{once:true,passive:true}); addEventListener('scroll',go,{once:true,passive:true});
})();

/* Syllabus: tapping a phase card opens a panel under the cards with that phase's classes (one at a time) */
(function(){
  var wrap=document.querySelector('#syllabus .curriculum-phases'); if(!wrap) return;
  var blocks=[].slice.call(wrap.querySelectorAll('.phase-block'));
  var panel=document.createElement('div'); panel.className='mf-phase-panel'; panel.hidden=true; panel.setAttribute('aria-live','polite');
  wrap.parentNode.insertBefore(panel, wrap.nextSibling);
  function txt(el,sel){ var x=el.querySelector(sel); return x?x.innerHTML:''; }
  function show(b){
    blocks.forEach(function(x){ x.classList.remove('mf-open'); x.setAttribute('aria-expanded','false'); });
    if(!b){ panel.hidden=true; panel.innerHTML=''; return; }
    b.classList.add('mf-open'); b.setAttribute('aria-expanded','true');
    var items=[].slice.call(b.querySelectorAll('.curriculum-item')).map(function(it){ return '<li><i>'+txt(it,'.curriculum-num')+'</i><span>'+txt(it,'h3')+'</span></li>'; }).join('');
    var ben=b.querySelector('.phase-benefit');
    panel.setAttribute('data-phase', b.getAttribute('data-phase'));
    panel.innerHTML='<div class="mf-pp-head"><span class="mf-pp-num">'+txt(b,'.phase-block-num')+'</span><span class="mf-pp-name">'+txt(b,'.phase-block-name')+'</span><span class="mf-pp-label">'+txt(b,'.phase-block-label')+'</span></div>'+(ben?'<p class="mf-pp-ben">'+ben.innerHTML+'</p>':'')+'<ol class="mf-pp-list">'+items+'</ol>';
    panel.hidden=false;
    if(window.innerWidth<901){ setTimeout(function(){ panel.scrollIntoView({behavior:'smooth',block:'nearest'}); },60); }
  }
  blocks.forEach(function(b){
    b.setAttribute('role','button'); b.setAttribute('tabindex','0'); b.setAttribute('aria-expanded','false');
    function toggle(){ show(b.classList.contains('mf-open')?null:b); }
    b.addEventListener('click',function(e){ if(e.target.closest('a')) return; toggle(); });
    b.addEventListener('keydown',function(e){ if(e.key==='Enter'||e.key===' '){ e.preventDefault(); toggle(); } });
  });
})();

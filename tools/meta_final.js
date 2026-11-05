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

(function(){
  /* CGM fold: draw the glowing curves when the fold comes into view */
  var f=document.getElementById('cgm'); if(!f||!('IntersectionObserver' in window)) return;
  var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){f.classList.remove('cgm7-anim');void f.offsetWidth;f.classList.add('cgm7-anim');io.disconnect();}});},{threshold:.25});
  io.observe(f);
})();

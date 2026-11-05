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
  if(!window.matchMedia||!matchMedia('(max-width:760px)').matches) return;
  var sets=document.querySelectorAll('.topic-grid-v2,.nov-incl-grid,.skills-grid,.teachers-grid-live');
  var extra=[document.querySelector('.value .value-card'),document.querySelector('.testimonials .quote-card')];
  extra.forEach(function(c){if(c&&c.parentNode)sets=Array.prototype.concat.call([],Array.prototype.slice.call(sets),[c.parentNode]);});
  Array.prototype.forEach.call(sets,function(g){if(!g||g.nextElementSibling&&g.nextElementSibling.classList.contains('mf-swipe'))return;var p=document.createElement('p');p.className='mf-swipe';p.textContent='Swipe for more';g.insertAdjacentElement('afterend',p);});
})();
(function(){
  /* the hero cells motion always plays (muted, inline), on phones too */
  var v=document.querySelector('#hero video.mf-cells'); if(!v) return;
  v.muted=true; v.setAttribute('muted',''); v.setAttribute('playsinline',''); v.loop=true;
  function go(){ try{ if(v.preload==='none') v.preload='auto'; var p=v.play(); if(p&&p.catch) p.catch(function(){}); }catch(e){} }
  if(document.readyState!=='loading') go(); else document.addEventListener('DOMContentLoaded',go);
  addEventListener('load',go); addEventListener('touchstart',go,{once:true,passive:true}); addEventListener('scroll',go,{once:true,passive:true});
})();

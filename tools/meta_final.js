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



/* Round 60 (Omri: "too long scrolling" in an opened session on phones): the three parts of a session
   (Learning Goals, 50-Minute Flow, Between-Session Work) become three tabs on phones and three columns on desktop. */
(function () {
  var inners = document.querySelectorAll('#syllabus .curriculum-body-inner');
  [].forEach.call(inners, function (inner) {
    var labels = [].filter.call(inner.children, function (c) { return c.classList.contains('curriculum-section-label'); });
    if (labels.length < 2) return;
    var tabs = document.createElement('div'); tabs.className = 'mf-sess-tabs'; tabs.setAttribute('role', 'tablist');
    var wrap = document.createElement('div'); wrap.className = 'mf-sess-panels';
    labels.forEach(function (lab, i) {
      var panel = document.createElement('div'); panel.className = 'mf-sess-panel' + (i === 0 ? ' is-on' : '');
      var n = lab.nextElementSibling; panel.appendChild(lab);
      while (n && !n.classList.contains('curriculum-section-label')) { var nx = n.nextElementSibling; panel.appendChild(n); n = nx; }
      wrap.appendChild(panel);
      var b = document.createElement('button'); b.type = 'button'; b.className = 'mf-sess-tab' + (i === 0 ? ' is-on' : '');
      b.setAttribute('role', 'tab'); b.setAttribute('aria-selected', i === 0 ? 'true' : 'false'); var tx = lab.textContent.replace(/\u00a0/g, ' ').trim(), sp = tx.lastIndexOf(' '); b.textContent = sp > 0 ? tx.slice(0, sp) + '\n' + tx.slice(sp + 1) : tx;
      b.addEventListener('click', function (e) {
        e.stopPropagation();
        [].forEach.call(tabs.children, function (x, j) { x.classList.toggle('is-on', j === i); x.setAttribute('aria-selected', j === i ? 'true' : 'false'); });
        [].forEach.call(wrap.children, function (x, j) { x.classList.toggle('is-on', j === i); });
        var body = inner.closest('.curriculum-body');
        if (body && body.style.maxHeight && body.style.maxHeight !== '0px') body.style.maxHeight = body.scrollHeight + 'px';
      });
      tabs.appendChild(b);
    });
    while (inner.firstChild) inner.removeChild(inner.firstChild);
    inner.appendChild(tabs); inner.appendChild(wrap);
  });
})();

/* Hero film sound button: the pages.dev page binds it in its own script, which was not carried over (6 Nov fix, copied from pages.dev). */
(function () {
  function bind() {
    document.querySelectorAll('.film-sound').forEach(function (btn) {
      if (btn.__llaSound) return; btn.__llaSound = true;
      var v = btn.parentElement.querySelector('video'); if (!v) return;
      btn.addEventListener('click', function (e) {
        e.preventDefault(); e.stopPropagation();
        v.muted = !v.muted;
        if (!v.muted) { if (v._julieRequestPlay) v._julieRequestPlay(); else { var p = v.play(); if (p && p.catch) p.catch(function () {}); } }
        btn.setAttribute('aria-pressed', v.muted ? 'false' : 'true'); btn.classList.toggle('is-on', !v.muted);
      });
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', bind); else bind();
})();

(() => {
  'use strict';
  const plans = {
    blueprint: {name:'The Longevity Blueprint', first:79, monthly:169, total:755},
    vip: {name:'The Longevity Blueprint VIP', first:129, monthly:229, total:1045}
  };
  let selected='blueprint', stage=1, saved={};
  const dialog=document.createElement('dialog');
  dialog.className='bp-dialog';
  dialog.setAttribute('aria-label','Blueprint enrollment preview');
  document.body.append(dialog);
  const label=document.createElement('div');
  label.className='bp-review-label';
  label.textContent='Review preview · Payments disabled';
  document.body.append(label);
  new IntersectionObserver(es=>es.forEach(e=>document.body.classList.toggle(e.target.id==='hero'?'bp-onhero':'bp-onoffer',e.isIntersecting))).observe(document.querySelector('#hero'));
  new IntersectionObserver(es=>es.forEach(e=>document.body.classList.toggle('bp-onoffer',e.isIntersecting))).observe(document.querySelector('#offer'));
  document.querySelectorAll('.curriculum-tab').forEach(tab=>tab.addEventListener('click',()=>{
    document.querySelectorAll('.curriculum-tab').forEach(t=>{t.classList.toggle('is-active',t===tab);t.setAttribute('aria-selected',String(t===tab))});
    document.querySelectorAll('.phase-block').forEach(p=>p.classList.toggle('is-active',p.dataset.phase===tab.dataset.phaseTab));
  }));
  window.toggleCurriculum=btn=>btn.closest('.curriculum-item').classList.toggle('active');
  document.querySelectorAll('[data-faq]').forEach(btn=>btn.addEventListener('click',e=>{
    e.preventDefault();e.stopImmediatePropagation();
    const item=btn.closest('.faq-item');item.classList.toggle('open');btn.setAttribute('aria-expanded',String(item.classList.contains('open')));
  },true));
  const navToggle=document.querySelector('#fnNavToggle'),drawer=document.querySelector('.fn-drawer');
  if(navToggle&&drawer){
    const close=()=>{drawer.classList.remove('is-open');document.body.classList.remove('nav-open');navToggle.setAttribute('aria-expanded','false')};
    navToggle.onclick=()=>{drawer.classList.toggle('is-open');document.body.classList.toggle('nav-open');navToggle.setAttribute('aria-expanded',String(drawer.classList.contains('is-open')))};
    const closeBtn=document.querySelector('#fnDrawerClose');if(closeBtn)closeBtn.onclick=close;
    drawer.querySelectorAll('a').forEach(a=>a.addEventListener('click',close));
  }
  const esc=s=>String(s||'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  function summary(){
    const p=plans[selected];
    return `<div class="bp-summary"><div class="bp-summary-row"><span>First month</span><span>$${p.first}</span></div><div class="bp-summary-row"><span>Four monthly payments</span><span>4 × $${p.monthly}</span></div><div class="bp-summary-row"><strong>Total course price</strong><strong>$${p.total}</strong></div></div>`;
  }
  function render(){
    const p=plans[selected];
    dialog.innerHTML=`<div class="bp-dialog-inner"><button type="button" class="bp-close" aria-label="Close enrollment">×</button><div class="bp-stage"><span class="${stage===1?'active':''}">1. Your package</span><span class="${stage===2?'active':''}">2. Your details</span><span class="${stage===3?'active':''}">3. Review</span></div><h2>${p.name}</h2>${
    stage===1?`<p>${selected==='vip'?'Full Blueprint access, monthly one-to-one guidance, two CGMs and continuing-learning benefits.':'18 live sessions, your personal protocol, a CGM and lifetime recordings.'}</p>${summary()}<button class="bp-button" id="bpContinue"><span>Continue With ${selected==='vip'?'VIP':'Blueprint'}</span><span>→</span></button><button class="bp-back" id="bpSwitch">Compare ${selected==='vip'?'Blueprint':'VIP'} instead</button>`:
    stage===2?`<p>Review the enrollment flow. These details stay in this preview and are not sent to the CRM.</p><form id="bpForm"><div class="bp-form"><label class="wide">Full name<input name="name" autocomplete="name" required value="${esc(saved.name)}"></label><label>Email address<input name="email" type="email" autocomplete="email" required value="${esc(saved.email)}"></label><label>Phone number<input name="phone" type="tel" autocomplete="tel" required value="${esc(saved.phone)}"></label></div><button class="bp-button" type="submit"><span>Review My Package</span><span>→</span></button></form><button class="bp-back" id="bpBack">Back to package</button>`:
    `<p>Your package and payment schedule.</p>${summary()}<div class="bp-summary-row"><span>Student</span><strong>${esc(saved.name)}</strong></div><div class="bp-summary-row"><span>Email</span><span>${esc(saved.email)}</span></div><p class="bp-safety">Preview only. No enrollment, CRM record or payment has been created. Class availability and the new installment terms must be verified before this version is opened for purchases.</p><button class="bp-button bp-disabled" disabled><span>Payments are disabled in this preview</span></button><button class="bp-back" id="bpBack">Back to details</button>`
    }</div>`;
    dialog.querySelector('.bp-close').onclick=()=>dialog.close();
    const next=dialog.querySelector('#bpContinue');if(next)next.onclick=()=>{stage=2;render()};
    const sw=dialog.querySelector('#bpSwitch');if(sw)sw.onclick=()=>{selected=selected==='vip'?'blueprint':'vip';render()};
    const back=dialog.querySelector('#bpBack');if(back)back.onclick=()=>{stage--;render()};
    const form=dialog.querySelector('#bpForm');if(form)form.onsubmit=e=>{e.preventDefault();saved=Object.fromEntries(new FormData(form));stage=3;render()};
    dialog.scrollTop=0;
  }
  function open(plan){selected=plans[plan]?plan:'blueprint';stage=1;render();if(!dialog.open)dialog.showModal()}
  window.addEventListener('click',e=>{
    const a=e.target.closest('a');
    if(!a)return;
    const href=a.getAttribute('href')||'';
    if(a.dataset.bpPlan||/checkout\.html/.test(href)){
      e.preventDefault();e.stopImmediatePropagation();
      if(a.dataset.bpPlan)open(a.dataset.bpPlan);
      else {document.querySelector('#offer').scrollIntoView({behavior:'smooth',block:'start'});}
    }
  },true);
  dialog.addEventListener('click',e=>{if(e.target===dialog)dialog.close()});
  document.addEventListener('submit',e=>{if(!e.target.closest('.bp-dialog'))e.preventDefault()},true);
  if(location.pathname.endsWith('checkout.html'))open(new URLSearchParams(location.search).get('plan'));
})();

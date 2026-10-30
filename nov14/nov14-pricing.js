(function(){
 'use strict';
 const $=s=>document.querySelector(s),all=s=>[...document.querySelectorAll(s)];
 let pending=false;
 function text(s,v){all(s).forEach(e=>{if(e.textContent!==v)e.textContent=v})}
 function html(s,v){all(s).forEach(e=>{if(e.innerHTML!==v)e.innerHTML=v})}
 function render(){
  pending=false;const P=window.LLA_PROMO;if(!P)return;
  const active=P.active,first=active?79:169,total=active?755:845;
  const upfront=window.LLA_ECOMM_PLANS?.resolvePlan()==='upfront';
  const checkout=!!document.getElementById('sumRow1V');
  if(!checkout){
   text('#pp [data-pl="upfront"] .pp-sub','Total $799 USD, one payment');
   html('.att-price','<span class="att-big">$79</span><span class="att-unit">Month 1<br><s>$169</s></span>');
   text('#enroll-mini .fn-pc-was','November offer');
   html('#enroll-mini .lla-mini-price','<b><sup>$</sup>79</b><span>Month 1<br>then 4 × $169 · $755 total</span>');
   text('#fnExit p b','Regular tuition: $169 per month');
   text('#mockBar .l b','$79 month 1');
   const band=$('#emStep2 .em-band .b-v');
   if(band){band.setAttribute('data-no-promo','');html('#emStep2 .em-band .b-v',upfront?'$799 <small>USD one payment</small>':(active?'<s style="opacity:.65;margin-right:8px">$169</s>':'')+'$'+first+' <small>Month 1 · then 4 × $169<br>$'+total+' total</small>');}
   html('#pp [data-pl="monthly"] .pp-price','$'+first+' <small>Month 1</small>');
   html('#pp [data-pl="monthly"] .pp-sub','Then 4 × $169 · $'+total+' total');
   const sum=$('#emSum');
   if(sum){
    sum.classList.add('credit-summary');sum.setAttribute('data-no-promo','');
    const content='<p class="credit-heading">'+(active?'November offer: $79 first month':'Regular plan')+'</p><div class="credit-first">'+(active?'<s>$169</s>':'')+'<strong>$'+first+'</strong><span>Month 1</span></div><div class="credit-line"><span>Months 2–5</span><b>4 × $169</b></div><div class="credit-line"><span>Total tuition</span><b>$'+total+'</b></div>';
    if(sum.innerHTML!==content)sum.innerHTML=content;
   }
   const msg=$('#emPromoMsg');
   if(msg&&msg.classList.contains('ok'))text('#emPromoMsg',upfront?'$799 one payment.':'November offer applied: $79 first month.');
   text('.att-big-offer','$79');
  }
  // Pricing card is indicative. On checkout, only its verified CRM quote controls amounts.
 }
 function schedule(){if(!pending){pending=true;setTimeout(render,20)}}
 const root=$('#enrollModal')||document.body;
 if(root)new MutationObserver(schedule).observe(root,{childList:true,subtree:true,characterData:true});
 window.addEventListener('click',e=>{
  const code=e.target.closest('[data-credit-code]');if(!code)return;
  e.preventDefault();e.stopImmediatePropagation();
  const v=code.dataset.creditCode,field=$('#codeInput')||$('#attCodeInput');
  if(field){field.value=v;field.dispatchEvent(new Event('input',{bubbles:true}));}
  const modal=$('#enrollModal');
  if(modal?.classList.contains('open')){const input=$('#emPromo');if(input){input.value=v;input.dispatchEvent(new Event('input',{bubbles:true}));$('#emApply')?.click();}}
  else{window.LLA_PROMO?.activate(v);field?.focus({preventScroll:true});$('#offer')?.scrollIntoView({behavior:'smooth',block:'start'});}
  schedule();
 },true);
 window.addEventListener('lla:pricing',schedule);
 document.addEventListener('click',schedule);
 document.addEventListener('DOMContentLoaded',schedule);window.addEventListener('load',schedule);
 render();setTimeout(render,1200);setTimeout(render,2800);
})();

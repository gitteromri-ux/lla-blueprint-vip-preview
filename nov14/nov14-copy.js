/* Text-only adaptation of the original pages.dev components. No design replacement. */
(function(){
 const descriptions=[
  'Plan meals using protein, fiber and food processing. Compare your glucose responses to foods and meal timing, and understand gut health.',
  'Understand sleep architecture and circadian rhythm. Test light, temperature, wake time and evening meals using your sleep log.',
  'Plan strength, cardio, stability and balance. Understand VO₂ max and compare glucose responses to post-meal movement.',
  'Evaluate supplement evidence and wearable data. Distinguish clinical trials from anecdotes and review decisions with your clinician.',
  'Understand the relationship between stress and glucose. Practise breathing and body-reset tools, then record your responses.',
  'Combine health data and daily habits into your written Blueprint. Include social connection, a tracking schedule and a 90-day plan.'
 ];
 function text(selector,value){const e=document.querySelector(selector);if(e&&e.textContent!==value)e.textContent=value}
 function html(selector,value){const e=document.querySelector(selector);if(e&&e.innerHTML!==value)e.innerHTML=value}
 function apply(){
  
  if(!document.getElementById('attendee-source-field-styles')){
   const css=[...document.querySelectorAll('style')].map(s=>s.textContent).join('\n');
   const rules=[...css.matchAll(/([^{}]*#enrollModal[^{}]*\.em-in[^{}]*)\{([^{}]*)\}/g)];
   const style=document.createElement('style');style.id='attendee-source-field-styles';
   style.textContent=rules.map(m=>m[1].replaceAll('#enrollModal','#ask')+'{'+m[2]+'}\n'+m[1].replaceAll('#enrollModal','.attendee-coupon')+'{'+m[2]+'}').join('\n')+'\n.attendee-coupon button[data-coupon]{color:inherit}html{scroll-padding-top:130px}';
   document.head.append(style);
  }
  document.querySelectorAll('#learn-com .topic-v2-desc').forEach((p,i)=>{if(descriptions[i])p.textContent=descriptions[i]});
  html('#included h2','What the course <em>includes</em>');
  html('#cgm h2','Abbott Lingo sensor <em>and app</em>');
  html('#syllabus h2','The 18-class <em>syllabus</em>');
  html('#teachers h2','Course <em>faculty</em>');
  html('#mechanism h2','Course <em>timeline</em>');
  text('#mechanism .fn-lead','Confirm your class with the enrollment team. Complete 18 weekly sessions and develop your written Blueprint.');
  const steps=document.querySelectorAll('#mechanism .fn-journey-step');
  if(steps[0]){steps[0].querySelector('h3').textContent='Enrollment and platform access';steps[0].querySelector('p').textContent='The team confirms your class, coupon and enrollment details, then explains access to the learning platform.'}
  if(steps[1])steps[1].querySelector('p').textContent='50 minutes live with your instructor and classmates. Your available start date and weekly meeting time are confirmed by the enrollment team.';
  if(steps[3])steps[3].querySelector('h3').textContent='Weekly learning and practice';
  html('#whatitis h2','How the live <em>course works</em>');
  const methodTitles=['Live classes and recordings','Health data and weekly practice','Group discussion and peer feedback','Your written protocol'];
  document.querySelectorAll('#whatitis .pdp-value-card h3').forEach((h,i)=>{if(methodTitles[i])h.textContent=methodTitles[i]});
  html('#faq h2','Frequently asked <em>questions</em>');
  document.querySelectorAll('#faq .faq-item').forEach(item=>{
   if(/How much does it cost/i.test(item.textContent)){const answer=item.querySelector('.faq-a-inner');if(answer)answer.textContent='Tuition is $79 for your first month, then four monthly payments of $169, $755 in total. Julie\u2019s VIP Masterclass on November 14, the Abbott Lingo sensor and the learning platform are included. One payment of $799 is also available at checkout.'}
  });
  const strip=document.getElementById('mockStrip');if(strip)strip.innerHTML='<span class="t lg">Julie\u2019s VIP Masterclass, live November 14, is included free</span><span class="t sm"><a href="#enrollModal" data-enroll-course="1">Julie\u2019s Masterclass included&nbsp;&middot;&nbsp;<b>$79 month 1</b></a></span>';
  // The captured source places this initializer before the carousel markup.
  // Run the original one-card scroll behavior after that markup exists.
  const rail=document.getElementById('tgRail');
  if(rail&&!rail.dataset.attendeeBound){
   rail.dataset.attendeeBound='1';
   const step=()=>{const card=rail.querySelector('.topic-v2');return card?card.getBoundingClientRect().width+20:400};
   document.querySelector('#learn-com .tg-prev')?.addEventListener('click',()=>rail.scrollBy({left:-step(),behavior:'smooth'}));
   document.querySelector('#learn-com .tg-next')?.addEventListener('click',()=>rail.scrollBy({left:step(),behavior:'smooth'}));
   const observer=new IntersectionObserver(entries=>entries.forEach(entry=>{const video=entry.target;if(entry.isIntersecting&&!matchMedia('(prefers-reduced-motion:reduce)').matches)video.play().catch(()=>{});else video.pause()}),{threshold:.2});
   rail.querySelectorAll('video').forEach(video=>{
    video.muted=true;
    if(!video.poster)video.poster=video.src.replace('/assets/','/assets/posters/').replace(/\.mp4(?:\?.*)?$/,'.jpg');
    observer.observe(video);
   });
  }
 }
 apply();document.addEventListener('DOMContentLoaded',apply);window.addEventListener('load',apply);setTimeout(apply,1000);setTimeout(()=>{apply();document.documentElement.dataset.attendeeReady='stable'},2500);
 document.addEventListener('click',function(e){
  const code=e.target.closest('[data-coupon]');if(code){const field=document.getElementById('codeInput');if(field)field.value=code.dataset.coupon;}
  const a=e.target.closest('a[href="#offer"],a[href="#ask"],a[href="#learn-com"]');
  if(a){e.preventDefault();e.stopImmediatePropagation();document.querySelector(a.getAttribute('href'))?.scrollIntoView({behavior:'smooth'});}
 },true);
})();

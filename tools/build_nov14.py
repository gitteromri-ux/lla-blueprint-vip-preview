import re, os, shutil, sys
SRC='/home/user/lla-course-checkout/dist'; OUT='/home/user/lla-blueprint-vip-preview/nov14'
os.makedirs(OUT, exist_ok=True)
t=open(f'{SRC}/index.html',encoding='utf-8').read()
log=[]
def sub1(pattern, repl, flags=re.S, count=1, name=''):
    global t
    new, n = re.subn(pattern, repl, t, count=count, flags=flags)
    log.append(f'{name or pattern[:40]}: {n}')
    t = new
    return n

# 1. CSP: allow the live site's scripts/styles from the preview host
sub1(r"script-src 'self' 'unsafe-inline'", "script-src 'self' 'unsafe-inline' https://longevitylifeacademy.pages.dev", name='csp script')
sub1(r"style-src 'self' 'unsafe-inline'", "style-src 'self' 'unsafe-inline' https://longevitylifeacademy.pages.dev", name='csp style')
sub1(r"media-src 'self' https://longevitylifeacademy.pages.dev", "media-src 'self' https://longevitylifeacademy.pages.dev https://gitteromri-ux.github.io", name='csp media')
# 2. Remove GTM (preview must not run production tags)
sub1(r"<!-- Google Tag Manager -->.*?<!-- End Google Tag Manager -->", "<!-- GTM removed on preview -->", name='gtm head')
sub1(r"<noscript><iframe[^>]*googletagmanager[^<]*</iframe></noscript>", "", name='gtm noscript')
# 3. Preview CRM env: staging by default on the preview host (explicit ?env=production overrides)
sub1(r"window\.LLA_ECOMM_CONFIG\.env  = new URLSearchParams\(location\.search\)\.get\('env'\) === 'staging' \? 'staging' : 'production';",
     "window.LLA_ECOMM_CONFIG.env  = (function(){var e=new URLSearchParams(location.search).get('env');if(e==='staging')return 'staging';if(e==='production')return 'production';return /github\\.io$/.test(location.hostname)?'staging':'production';})();", name='env')
# 4. Hero copy
hero_start=t.index('<section class="pdp-hero pdp-hero--cine" id="hero">'); hero_end=t.index('</section>',hero_start)
hero=t[hero_start:hero_end]
hero_new=hero
hero_new,n1=re.subn(r'<h1 class="pdp-cine-h1[^"]*">.*?</h1>', '<p class="nov14-badge"><span class="nov14-dot" aria-hidden="true"></span>Live on Zoom <i></i> Saturday, November 14 <i></i> 1:00 PM ET <i></i> Limited seats</p>\n    <h1 class="pdp-cine-h1 pdp-cine-h1--v59 pdp-cine-h1--approved">The 2nd slowest-aging woman on earth reveals her protocol, <span class="pdp-cine-blue">live on November 14.</span></h1>', hero_new, flags=re.S)
hero_new,n2=re.subn(r'(<p class="pdp-cine-sub pdp-cine-sub--approved"[^>]*>).*?</p>', r'\1Julie Gibson Clark’s 90-minute VIP Masterclass, with her private Q&amp;A, is included free when you enroll in The Longevity Blueprint: 18 live classes with LLA’s certified longevity faculty, the Abbott Lingo CGM shipped free, and your own written protocol.</p>\n    <p class="nov14-price"><b>$79</b> for your first month, over 50% off <i></i> 14-day full refund</p>', hero_new, flags=re.S)
hero_new,n3=re.subn(r'<div class="pdp-cine-ctas">.*?</div>\s*</div>', '<div class="pdp-cine-ctas">\n      <a href="#enrollModal" class="pdp-cine-cta" data-fn-cta="hero" data-enroll-course="1">Enroll now\n        <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 5l7 7-7 7"></path></svg>\n      </a>\n      <a href="#offer" class="nov14-cta-2">See everything included</a>\n    </div>\n    </div>', hero_new, count=1, flags=re.S)
hero_new,n4=re.subn(r'<figcaption><b>Julie Gibson Clark</b><span>[^<]*</span></figcaption>', '<figcaption><b>Julie Gibson Clark</b><span>2nd slowest-aging woman on earth. Hosts the VIP Masterclass, November 14.</span></figcaption>', hero_new)
log.append(f'hero h1 {n1} sub {n2} ctas {n3} figcaption {n4}')
t=t[:hero_start]+hero_new+t[hero_end:]

# 5. Sections: extract and reorder
def block(sid):
    m=re.search(r'<section[^>]*\bid="%s"'%sid,t); s=m.start(); e=t.index('</section>',s)+len('</section>'); return s,e
ids=['hero','learn-com','included','cgm','vip','syllabus','teachers','institution','journal','mechanism','whatitis','offer','ask','faq','enroll-mini']
blocks={}
for sid in ids:
    s,e=block(sid); blocks[sid]=t[s:e]
first=min(block(s)[0] for s in ids); last=max(block(s)[1] for s in ids)
between=t[first:last]
# everything between sections that is not a section (scripts, links) must be preserved: collect the non-section residue in order
residue=[]; pos=first
for sid in sorted(ids, key=lambda x: block(x)[0]):
    s,e=block(sid); residue.append(t[pos:s]); pos=e
residue.append(t[pos:last])
res_join=''.join(x for x in residue if x.strip())
log.append(f'residue between sections: {len(res_join)} chars: '+re.sub(r'\s+',' ',res_join)[:300])

# new clarity strip
strip='''
<section id="nov14-clarity" class="lla-incl is-light nov14-clarity">
  <div class="container">
    <div class="nov14-grid">
      <article class="lla-incl-card" style="--c1:#006EFF;--c2:#5EB6FF"><span class="n">You enroll in</span><h3>The Longevity Blueprint</h3><p>18 live classes over 18 weeks with LLA’s certified longevity faculty. Abbott Lingo CGM shipped free. Your personal protocol by week 18.</p><b>$79 first month</b></article>
      <article class="lla-incl-card" style="--c1:#7C5CFF;--c2:#B79DFF"><span class="n">Included free</span><h3>Julie’s VIP Masterclass, November 14</h3><p>90 minutes live on Zoom with the 2nd slowest-aging woman on earth, plus her private Q&amp;A. Julie hosts the masterclass; your course is taught by LLA faculty.</p><b>$99 value, included</b></article>
      <article class="lla-incl-card" style="--c1:#22B27A;--c2:#7DE5C1"><span class="n">Your protection</span><h3>14-day full refund</h3><p>Not for you? Email us within 14 days of registration and every cent comes back.</p><b>Included</b></article>
    </div>
  </div>
</section>
'''
# 6. Offer rewrite
offer=blocks['offer']
offer_new=re.sub(r'<p class="lp-lead">.*?</p>', '<p class="lp-lead">18 live classes with LLA’s longevity faculty, Julie Gibson Clark’s VIP Masterclass on November 14, and an Abbott Lingo glucose sensor. Nothing extra to buy, ever.</p>', offer, count=1, flags=re.S)
card_new='''<aside class="lp-card">
        <p class="lp-plan credit-plan-label">Launch offer. Over 50% off your first month.</p>
        <div class="lp-big credit-month-one" data-no-promo data-credit-price><s aria-label="Regular first payment">$169</s><strong>$79</strong><span>Month 1</span></div>
        <div class="credit-rest" data-no-promo><span>Months 2 to 5</span><b>$169 <span style="font-size:16px;font-weight:400">/ month</span></b></div>
        <p class="lp-total credit-total" data-no-promo><b>$755 total</b><small>Five payments. Nothing else to pay. The sensor ships to your door.</small></p>
        <a href="#enrollModal" class="lp-cta" id="offerEnroll" data-fn-cta="offer" data-enroll-course="1">Enroll now</a>
        <p class="lp-trust"><b>14-day full refund.</b> Questions before you enroll? Call +1-888-230-5110.</p>
      </aside>'''
offer_new,n5=re.subn(r'<aside class="lp-card">.*?</aside>', card_new, offer_new, count=1, flags=re.S)
list_new='''<ul class="lp-bul">
          <li><i style="--c1:#006EFF;--c2:#5EB6FF"></i><span><b>18 live classes, one a week.</b> 50 minutes on Zoom with a certified longevity instructor, recorded for you.</span></li>
          <li><i style="--c1:#22B27A;--c2:#7DE5C1"></i><span><b>The six pillars of longevity.</b> Nutrition, sleep, movement, supplements, stress, your protocol.</span></li>
          <li><i style="--c1:#7C5CFF;--c2:#B79DFF"></i><span><b>Julie Gibson Clark’s VIP Masterclass, live November 14.</b> 90 minutes plus her private Q&amp;A. A $99 value, included free.</span></li>
          <li><i style="--c1:#FF7A45;--c2:#FFB38A"></i><span><b>Abbott Lingo glucose sensor and app.</b> Shipped to your door, included.</span></li>
          <li><i style="--c1:#0FB5D6;--c2:#7DE5FF"></i><span><b>Your personal Longevity Blueprint.</b> Built on your own numbers by week 18.</span></li>
          <li><i style="--c1:#22E39A;--c2:#7DE5C1"></i><span><b>14-day full refund.</b> Every cent back if it is not for you.</span></li>
          <!-- NOV14 TODO: add the new inclusions from Omri's offer message here -->
        </ul>'''
offer_new,n6=re.subn(r'<ul class="lp-bul">.*?</ul>', list_new, offer_new, count=1, flags=re.S)
log.append(f'offer card {n5} list {n6}')
blocks['offer']=offer_new
# 7. VIP rewrite
vip=blocks['vip']
vip_new=re.sub(r'<h2 class="lla-vip-h2">.*?</h2>', '<h2 class="lla-vip-h2">Free for Blueprint students: Julie’s VIP Masterclass, <em>live November 14.</em></h2>', vip, count=1, flags=re.S)
vip_new=re.sub(r'<p class="lla-vip-sub">.*?</p>', '<p class="lla-vip-sub">90 minutes on Zoom with the 2nd slowest-aging woman on earth, plus her private Q&amp;A. A $99 value, included with your enrollment. Seats are limited.</p>', vip_new, count=1, flags=re.S)
vip_new=re.sub(r'<ul class="lla-vip-list">.*?</ul>', '''<ul class="lla-vip-list">
            <li><strong>Saturday, November 14, 1:00 PM ET, live on Zoom.</strong> Nothing is pre-recorded.</li>
            <li><strong>90 minutes with Julie, then her private Q&amp;A.</strong> Her protocol, her numbers, your questions.</li>
            <li><strong>Included free with The Longevity Blueprint.</strong> Your Zoom link arrives by email once you are enrolled.</li>
          </ul>''', vip_new, count=1, flags=re.S)
vip_new=re.sub(r'<a href="#offer" class="lla-vip-btn"[^>]*>.*?</a>', '<a href="#enrollModal" class="lla-vip-btn" data-fn-cta="vip" data-enroll-course="1">Enroll now <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14M12 5l7 7-7 7"></path></svg></a>', vip_new, count=1, flags=re.S)
vip_new=re.sub(r'<p class="lla-vip-after">.*?</p>', '<p class="lla-vip-after">Julie hosts the masterclass. The 18-class course is taught by LLA’s certified longevity faculty.</p>', vip_new, count=1, flags=re.S)
blocks['vip']=vip_new
# 8. Included cards: card 04 -> Nov 14; add refund card
inc=blocks['included']
inc_new=re.sub(r'(<article class="lla-incl-card" style="--c1:#7C5CFF;--c2:#B79DFF"><span class="n">04</span><h3>)[^<]*(</h3><p>)[^<]*(</p><b>)[^<]*(</b>)', r'\1Julie Gibson Clark’s VIP Masterclass, November 14\2Live on Zoom, 90 minutes plus Q&amp;A with the 2nd slowest-aging woman on earth. Free for Blueprint students.\3$99 value, included\4', inc, count=1)
inc_new=inc_new.replace('</article>\n    </div>', '</article>\n      <article class="lla-incl-card" style="--c1:#22E39A;--c2:#7DE5C1"><span class="n">06</span><h3>14-day full refund</h3><p>Not for you? Email us within 14 days of registration and every cent comes back.</p><b>Included</b></article>\n    </div>',1)
blocks['included']=inc_new
# 9. Pillar videos: no eager preload on the preview
blocks['learn-com']=blocks['learn-com'].replace('preload="auto" data-lla-autoplay="1"','preload="metadata" data-lla-autoplay="1"')
# 10. Reassemble in the new order
order=['hero','nov14-clarity','offer','vip','learn-com','syllabus','included','cgm','teachers','institution','journal','whatitis','mechanism','faq','ask','enroll-mini']
blocks['nov14-clarity']=strip
assembled='\n'.join(blocks[s] for s in order)+'\n'+res_join
t=t[:first]+assembled+t[last:]
# 11. Title / description
sub1(r'<title>.*?</title>', '<title>The Longevity Blueprint | $79 first month, Julie’s VIP Masterclass on November 14 included</title>', name='title')
# 12. Script and stylesheet swaps
sub1(r'<link rel="stylesheet" href="launch-flow\.css\?v=hero4">', '<link rel="stylesheet" href="nov14-flow.css?v=1">', name='flow css')
sub1(r'<script src="launch-flow\.js\?v=hero4" defer>', '<script src="nov14-flow.js?v=1" defer>', name='flow js')
sub1(r'<script src="exact-attendee-copy\.js\?v=hero4">', '<script src="nov14-copy.js?v=1">', name='copy js')
sub1(r'<script src="attendee-pricing\.js\?v=launch2" defer>', '<script src="nov14-pricing.js?v=1" defer>', name='pricing js')
sub1(r'<script src="blueprint/assets/lla-promo\.js\?v=credit79-1" defer="">', '<script src="nov14-promo.js?v=1" defer=""></script><script src="blueprint/assets/__unused.js" defer="" style="display:none" hidden>', name='promo js')
t=t.replace('<script src="blueprint/assets/__unused.js" defer="" style="display:none" hidden></script>','')
sub1(r'<script src="https://longevitylifeacademy\.pages\.dev/assets/lla-promo\.js\?v=r17"', '<script src="nov14-promo.js?v=1"', name='promo preload', count=0)
# 13. mockStrip + mockBar
sub1(r'<div id="mockBar"><div class="l"><i>The Longevity Blueprint</i><b>\$179<small>/ mo</small></b></div><a href="#offer" data-fn-cta="floater">Enroll Now</a></div>', '<div id="mockBar"><div class="l"><i>The Longevity Blueprint</i><b>$79 month 1</b></div><a href="#enrollModal" data-fn-cta="floater" data-enroll-course="1">Enroll now</a></div>', name='mockBar')
# 14. Fold styles
style='''<style id="nov14-fold">
html body#lpRoot .nov14-badge{display:inline-flex;flex-wrap:wrap;align-items:center;gap:6px 0;margin:0 0 14px;padding:9px 16px 9px 12px;border-radius:999px;background:rgba(0,110,255,.16);border:1px solid rgba(125,229,255,.45);font:700 13px/1.3 Inter,sans-serif;letter-spacing:.06em;text-transform:uppercase;color:#dceaff;box-shadow:0 0 30px -8px rgba(125,229,255,.55)}
html body#lpRoot .nov14-badge .nov14-dot{width:9px;height:9px;border-radius:50%;background:#22E39A;box-shadow:0 0 14px #22E39A;margin-right:10px}
html body#lpRoot .nov14-badge i{display:inline-block;width:1px;height:11px;background:rgba(255,255,255,.35);margin:0 10px;vertical-align:middle}
html body#lpRoot .nov14-price{font:500 18px/1.5 Inter,sans-serif;color:#dceaff;margin:-8px 0 22px}
html body#lpRoot .nov14-price b{font:700 22px/1 Inter,sans-serif;color:#fff}
html body#lpRoot .nov14-price i{display:inline-block;width:1px;height:12px;background:rgba(255,255,255,.35);margin:0 10px;vertical-align:middle}
html body#lpRoot .nov14-cta-2{display:inline-flex;align-items:center;min-height:52px;padding:0 20px;border-radius:999px;border:1px solid rgba(255,255,255,.35);color:#fff;font:600 16px/1 Inter,sans-serif;text-decoration:none;background:rgba(255,255,255,.06)}
html body#lpRoot .nov14-cta-2:hover{background:rgba(255,255,255,.12)}
html body#lpRoot .nov14-clarity{padding:44px 0 36px}
html body#lpRoot .nov14-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}
html body#lpRoot .nov14-grid .lla-incl-card{min-height:0;padding:26px 24px 24px}
html body#lpRoot .nov14-grid .lla-incl-card .n{font:700 12px/1 Inter,sans-serif;letter-spacing:.14em;text-transform:uppercase;color:#5B6B8C}
html body#lpRoot .nov14-grid .lla-incl-card h3{font:600 24px/1.2 "Playfair Display",Georgia,serif;color:#0B1B33;margin:6px 0 4px}
html body#lpRoot .nov14-grid .lla-incl-card p{font:400 16px/1.55 Inter,sans-serif;color:#29385A;margin:0}
html body#lpRoot .nov14-grid .lla-incl-card b{margin-top:auto;font:700 14px/1 Inter,sans-serif;color:#006EFF}
html body#lpRoot #offer .lp-card .lp-cta{margin:4px 0 18px;text-decoration:none;background:#006EFF;color:#fff}
html body#lpRoot #offer .lp-card .lp-cta:hover{background:#0a5fd9}
@media (max-width:900px){html body#lpRoot .nov14-grid{grid-template-columns:1fr;gap:12px}html body#lpRoot .nov14-clarity{padding:28px 0 20px}html body#lpRoot .nov14-badge{font-size:12px;padding:8px 12px 8px 10px}html body#lpRoot .nov14-badge i{margin:0 7px}html body#lpRoot .nov14-price{font-size:17px}html body#lpRoot .pdp-cine-ctas .nov14-cta-2{width:100%;justify-content:center}html body#lpRoot #hero .pdp-cine-sub--approved{font-size:17px!important;line-height:1.5!important}html body#lpRoot #vip .lla-vip-grid{display:grid!important;grid-template-columns:1fr!important;gap:24px!important}html body#lpRoot #vip .lla-vip-portrait img{max-width:280px;border-radius:18px}}
</style>
</head>'''
sub1(r'<div class="lla-vip-grid lla-slider">', '<div class="lla-vip-grid">', name='vip slider off')
sub1(r'<p>18 live sessions, live classes, Abbott Lingo CGM included\.</p>', lambda m: '<p>18 live classes, the Abbott Lingo CGM and Julie’s VIP Masterclass on November 14, all included.</p>', name='enroll-mini lead')
sub1(r'</head>', style, name='fold style')
open(f'{OUT}/index.html','w',encoding='utf-8').write(t)
# ---- support files ----
for f in ['exact-source-design.css','guest-mobile.css','guest-mobile.js','attendee-pricing.css','attendee-form.js','checkout.html','_headers']:
    shutil.copy(f'{SRC}/{f}', f'{OUT}/{f}')
os.makedirs(f'{OUT}/blueprint/assets',exist_ok=True)
for f in ['eteacher-ecomm.js','blueprint-hotfix-state.js','nanp-state-autofill.js','ecom-layer.js','lla-country.js','lla-promo.js']:
    shutil.copy(f'{SRC}/blueprint/assets/{f}', f'{OUT}/blueprint/assets/{f}')
shutil.copy(f'{SRC}/blueprint/privacy.html', f'{OUT}/blueprint/privacy.html') if os.path.exists(f'{SRC}/blueprint/privacy.html') else None
# checkout.html: same CSP + env patch
c=open(f'{OUT}/checkout.html',encoding='utf-8').read()
c=c.replace("script-src 'self' 'unsafe-inline'","script-src 'self' 'unsafe-inline' https://longevitylifeacademy.pages.dev",1).replace("style-src 'self' 'unsafe-inline'","style-src 'self' 'unsafe-inline' https://longevitylifeacademy.pages.dev",1)
open(f'{OUT}/checkout.html','w',encoding='utf-8').write(c)
# attendee-form.js: preview host => staging for the question form
a=open(f'{OUT}/attendee-form.js',encoding='utf-8').read()
a=a.replace("var env=explicitEnv==='staging'||(qa&&explicitEnv!=='production')?'staging':'production';","var env=explicitEnv==='staging'||(qa&&explicitEnv!=='production')||(/github\\.io$/.test(location.hostname)&&explicitEnv!=='production')?'staging':'production';",1)
open(f'{OUT}/attendee-form.js','w',encoding='utf-8').write(a)
# nov14-flow.css: launch-flow.css without the vip hide
fc=open(f'{SRC}/launch-flow.css',encoding='utf-8').read().replace('#vip{display:none!important}\n','')
open(f'{OUT}/nov14-flow.css','w',encoding='utf-8').write(fc)
# nov14-promo.js: $79 launch price active by default (no code needed); codes still accepted
p=open(f'{SRC}/blueprint/assets/lla-promo.js',encoding='utf-8').read()
p=p.replace("const initial=valid(q.get('code'))?normalize(q.get('code')):valid(stored())?normalize(stored()):'JULIE249';","const initial=valid(q.get('code'))?normalize(q.get('code')):valid(stored())?normalize(stored()):'MASTERCLASS-VIP';",1)
p=p.replace("active:q.get('promo')!=='off'&&(valid(q.get('code'))||valid(stored())||q.get('promo')==='on'),","active:q.get('promo')!=='off',",1)
assert "active:q.get('promo')!=='off'," in p
open(f'{OUT}/nov14-promo.js','w',encoding='utf-8').write(p)
# nov14-flow.js: CTA wiring + modal open + mockBar, no hero/vip/order rewrites
fl=open(f'{SRC}/launch-flow.js',encoding='utf-8').read()
fl=fl.replace("""  document.getElementById('vip')?.remove();
  const headline=document.querySelector('#hero h1'),sub=document.querySelector('#hero .pdp-cine-sub');
  if(headline)headline.innerHTML='Build your personal longevity protocol in <span class="pdp-cine-blue">18 live classes.</span>';
  if(sub)sub.textContent='18 live small-group classes with Julie and the LLA faculty. Abbott Lingo CGM shipped free. You leave with a written protocol built on your own numbers.';
  if(hero&&pillars&&syllabus&&offer){
   if(hero.nextElementSibling!==pillars)hero.insertAdjacentElement('afterend',pillars);
   if(pillars.nextElementSibling!==syllabus)pillars.insertAdjacentElement('afterend',syllabus);
   if(syllabus.nextElementSibling!==offer)syllabus.insertAdjacentElement('afterend',offer);
  }
""","")
fl=fl.replace("""  if(hero&&!document.getElementById('heroCouponNote')){
   const cta=hero.querySelector('.pdp-cine-cta');
   if(cta)cta.insertAdjacentHTML('afterend','<p id="heroCouponNote">Masterclass credit · <b>JULIE249</b> / <b>MASTERCLASS-VIP</b></p>');
  }
""","")
fl=fl.replace("a.href='#enrollModal';a.dataset.enrollCourse='1';if(a.textContent!=='Enroll now')a.textContent='Enroll now';","a.href='#enrollModal';a.dataset.enrollCourse='1';if(!a.classList.contains('nov14-cta-2')&&a.textContent!=='Enroll now')a.textContent='Enroll now';")
fl=fl.replace("const code=(input?.value||window.LLA_PROMO?.code||'JULIE249').trim().toUpperCase();","const code=(input?.value||window.LLA_PROMO?.code||'MASTERCLASS-VIP').trim().toUpperCase();")
assert 'heroCouponNote' not in fl and "getElementById('vip')" not in fl
open(f'{OUT}/nov14-flow.js','w',encoding='utf-8').write(fl)
# nov14-copy.js: section headings + pillar descriptions + rail, no hero/offer/strip rewrites
cp=open(f'{SRC}/exact-attendee-copy.js',encoding='utf-8').read()
cp=cp.replace("document.title='The Longevity Blueprint | Masterclass attendee course information';","")
for line in ["  html('#hero h1','Build your personal longevity protocol in <span class=\"pdp-cine-blue\">18 live classes.</span>');\n",
             "  html('#hero .pdp-cine-sub','18 live small-group classes with Julie and the LLA faculty. Abbott Lingo CGM shipped free. You leave with a written protocol built on your own numbers.');\n",
             "  text('#hero figcaption span','Founding Faculty, Longevity Life Academy');\n",
             "  const heroCTA=document.querySelector('#hero .pdp-cine-cta');if(heroCTA){heroCTA.href='#offer';heroCTA.dataset.enrollCourse='1';heroCTA.innerHTML='Enroll now';}\n",
             "  html('#vip h2',\"Julie's VIP <em>Longevity Masterclass</em>\");\n",
             "  html('#offer h2','Tuition and <em>coupon codes</em>');\n",
             "  text('#offer .lp-lead','18 live classes, learning-platform access, Julie’s VIP masterclass and one Abbott Lingo sensor with U.S. shipping.');\n",
             "  text('#offer .lp-big b','79');text('#offer .lp-saverow s','$169 / month');\n",
             "  text('#offer .lp-pill','Masterclass credit');\n",
             "  html('#offer .lp-total','<b>$755 total</b><small>$90 masterclass credit applied to month 1.</small>');\n",
             "  text('#codeApply','Apply code and enroll');\n",
             "  text('#offer .lp-julie-t b','Masterclass attendee code');\n",
             "  html('#offer .lp-trust','<b>Full refund within 14 days of registration.</b> Questions? Call +1-888-230-5110.');\n",
             "  document.querySelectorAll('a[href*=\"checkout.html\"]').forEach(a=>{a.href='#offer';a.removeAttribute('data-plan')});\n",
             "  document.querySelectorAll('header a[href=\"#offer\"]').forEach(a=>{a.textContent='Enroll now';a.dataset.enrollCourse='1'});\n"]:
    assert line in cp, line[:60]
    cp=cp.replace(line,"")
STRIP_NEW="  const strip=document.getElementById('mockStrip');if(strip)strip.innerHTML='<span class=\"t lg\">Julie\\u2019s VIP Masterclass, live November 14, is included free</span><span class=\"t sm\"><a href=\"#enrollModal\" data-enroll-course=\"1\">Julie\\u2019s Masterclass included&nbsp;&middot;&nbsp;<b>$79 month 1</b></a></span>';\n"
cp,nstrip=re.subn(r"  const strip=document\.getElementById\('mockStrip'\);if\(strip\)strip\.innerHTML=.*?\n", lambda m: STRIP_NEW, cp, count=1, flags=re.S)
assert nstrip==1, 'mockStrip rewrite not found'
cp=re.sub(r"  const bar=document\.getElementById\('mockBar'\);if\(bar\)\{.*?\}\n", "", cp, count=1, flags=re.S)
FAQ_NEW="answer.textContent='Tuition is $79 for your first month, then four monthly payments of $169, $755 in total. Julie\\u2019s VIP Masterclass on November 14, the Abbott Lingo sensor and the learning platform are included. One payment of $799 is also available at checkout.'"
cp,nfaq=re.subn(r"answer\.textContent='Regular tuition is \$169 per month for five months[^']*'", lambda m: FAQ_NEW, cp, count=1)
assert nfaq==1, 'FAQ cost answer not found'
assert '#hero h1' not in cp and 'coupon codes' not in cp
open(f'{OUT}/nov14-copy.js','w',encoding='utf-8').write(cp)
# nov14-pricing.js: keep modal pricing, drop the offer/strip/FAQ credit-code rewrites
pr=open(f'{SRC}/attendee-pricing.js',encoding='utf-8').read()
start=pr.index("   text('#offer .lp-plan','Regular plan: $169 × 5');"); end=pr.index("   text('#pp [data-pl=\"upfront\"] .pp-sub'")
pr=pr[:start]+pr[end:]
pr=re.sub(r"   all\('#faq \.faq-item'\)\.forEach\(e=>\{if\(/How much does it cost/i.*?\n", "", pr, count=1, flags=re.S)
pr=re.sub(r"   html\('\.att-line',.*?\n", "", pr, count=1)
assert "   html('#offer .lp-lead','18 live classes, your learning platform, Julie’s masterclass and an Abbott Lingo sensor.');\n" in pr
pr=pr.replace("   html('#offer .lp-lead','18 live classes, your learning platform, Julie’s masterclass and an Abbott Lingo sensor.');\n","")
pr=pr.replace("   text('#enroll-mini .fn-pc-was','Masterclass credit');","   text('#enroll-mini .fn-pc-was','Launch offer');")
pr=re.sub(r"   const strip=\$\('#mockStrip'\);\n   if\(strip\)\{.*?\n", "", pr, count=1, flags=re.S)
assert "(active?'Masterclass credit':'Regular plan')" in pr
pr=pr.replace("(active?'Masterclass credit':'Regular plan')","(active?'Launch offer: $79 first month':'Regular plan')")
pr=pr.replace("text('#emPromoMsg',upfront?'Code applied. $799 one payment.':'Masterclass credit applied.');","text('#emPromoMsg',upfront?'$799 one payment.':'Launch offer applied: $79 first month.');")
assert 'JULIE249' not in pr.split('function render')[1].split('// Pricing card')[0], 'codes still in render'
open(f'{OUT}/nov14-pricing.js','w',encoding='utf-8').write(pr)
print('\n'.join(log)); print('written', OUT, 'index bytes', len(t))

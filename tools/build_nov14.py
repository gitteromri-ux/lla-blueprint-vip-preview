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
# 4. Hero: untouched (exact live hero; copy applied by nov14-flow.js / nov14-copy.js as on the live page)
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
offer_new=re.sub(r'<p class="lp-lead">Online sign-ups in November only.</p>', '<p class="lp-lead">Live 18-week course, free Abbott Lingo CGM, $100 cash back. Online sign-ups in November only.</p>', offer, count=1, flags=re.S)
card_new='''<div class="pc2">
        <svg width="0" height="0" aria-hidden="true" style="position:absolute"><defs><linearGradient id="pc2g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#5EB6FF"/><stop offset="1" stop-color="#006EFF"/></linearGradient></defs></svg>
        <div class="pc2-benefits">
          <div class="pc2-eyebrow">The Longevity Blueprint</div>
          <h3 class="pc2-title">Everything you need to build your own longevity protocol.</h3>
          <ul class="pc2-list">
            <li><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="12" fill="url(#pc2g)"/><path d="M7.2 12.5l3 3 6.6-6.9" fill="none" stroke="#fff" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg><div><b>18-week live course</b><span>Small groups, live online, one class a week.</span></div></li>
            <li><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="12" fill="url(#pc2g)"/><path d="M7.2 12.5l3 3 6.6-6.9" fill="none" stroke="#fff" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg><div><b>Your own longevity protocol</b><span>Tailored to your numbers.</span></div></li>
            <li><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="12" fill="url(#pc2g)"/><path d="M7.2 12.5l3 3 6.6-6.9" fill="none" stroke="#fff" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg><div><b>Free Abbott Lingo CGM</b><span>Shipped to you.</span></div></li>
            <li><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="12" fill="url(#pc2g)"/><path d="M7.2 12.5l3 3 6.6-6.9" fill="none" stroke="#fff" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg><div><b>$100 cash back</b><span>On your next course.</span></div></li>
          </ul>
          <div class="pc2-vip"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2.6l2.9 6 6.6.9-4.8 4.6 1.2 6.5L12 17.5l-5.9 3.1 1.2-6.5L2.5 9.5l6.6-.9z" fill="currentColor"/></svg><div><b>Free VIP access to Julie Gibson Clark’s Masterclass</b><span>90-minute masterclass and Q&amp;A, live on Zoom</span></div><em>Nov 14</em></div>
          <a href="#enrollModal" class="pc2-cta pc2-cta--m" data-fn-cta="offer-m" data-enroll-course="1">Enroll now</a>
        </div>
        <div class="pc2-price" data-no-promo data-credit-price>
          <div class="pc2-badge"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20.6 13.4l-7.2 7.2a2 2 0 0 1-2.8 0L3.4 13.4A2 2 0 0 1 2.8 12V4a2 2 0 0 1 2-2h8a2 2 0 0 1 1.4.6l7.2 7.2a2 2 0 0 1 0 2.8z" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/><circle cx="7.5" cy="7.5" r="1.6" fill="currentColor"/></svg>50% off your first month</div>
          <div class="pc2-now"><span class="cur">$</span>79</div>
          <div class="pc2-per">First month</div>
          <div class="pc2-chips"><s>Regular $169</s><span class="save">You save $90</span></div>
          <div class="pc2-then">Then <b>$169</b> a month for 4 months</div>
          <a href="#enrollModal" class="pc2-cta" id="offerEnroll" data-fn-cta="offer" data-enroll-course="1">Enroll now</a>
          <p class="pc2-note">14-day try-out refund · Online sign-ups in November only</p>
        </div>
      </div>'''
offer_new,n5=re.subn(r'<aside class="lp-card[^"]*">.*?</aside>', card_new, offer_new, count=1, flags=re.S)
offer_new,n6=re.subn(r'\s*<div class="lp-list">.*?</ul>\s*</div>', '', offer_new, count=1, flags=re.S)
log.append(f'offer card {n5} list {n6}')
blocks['offer']=offer_new
# 7. VIP rewrite
vip=blocks['vip']
vip_new=re.sub(r'<h2 class="lla-vip-h2">.*?</h2>', '<h2 class="lla-vip-h2">Learn to age slower from the 2nd slowest aging human on earth. <em>Free when you enroll.</em></h2>', vip, count=1, flags=re.S)
vip_new=re.sub(r'<p class="lla-vip-sub">.*?</p>', '<p class="lla-vip-sub">The Longevity Masterclass of the Year. Live on Zoom, November 14. Your VIP seat is included.</p>', vip_new, count=1, flags=re.S)
vip_new=re.sub(r'<h3 class="lla-vip-offer-h">.*?</h3>', '<h3 class="lla-vip-offer-h">Bonus: Julie’s VIP Longevity Masterclass, November 14</h3>', vip_new, count=1, flags=re.S)
vip_new=re.sub(r'<ul class="lla-vip-list">.*?</ul>', '''<ul class="lla-vip-list">
            <li><strong>90 minutes live with Julie,</strong> then her private VIP Q&amp;A.</li>
            <li><strong>Saturday, November 14, 1:00 PM ET,</strong> on Zoom.</li>
            <li><strong>Free with your enrollment.</strong> Zoom link by email.</li>
          </ul>''', vip_new, count=1, flags=re.S)
vip_new=re.sub(r'<a href="#offer" class="lla-vip-btn"[^>]*>.*?</a>', '<a href="#enrollModal" class="lla-vip-btn" data-fn-cta="vip" data-enroll-course="1">Enroll now <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14M12 5l7 7-7 7"></path></svg></a>', vip_new, count=1, flags=re.S)
vip_new=re.sub(r'<p class="lla-vip-after">.*?</p>', '<p class="lla-vip-after">Julie hosts the masterclass. LLA’s faculty teach the course.</p>', vip_new, count=1, flags=re.S)
vip_new=re.sub(r'\s*<p class="lla-vip-bio">.*?</p>', '', vip_new, count=1, flags=re.S)
blocks['vip']=vip_new
# 8. Included cards: one card per line of the November offer
cards=[('#006EFF','#5EB6FF','Live 18-week course','Small groups. One class a week, recorded.','Included'),
 ('#22B27A','#7DE5C1','The 6 pillars of longevity','Top instructors.','Included'),
 ('#0FB5D6','#7DE5FF','Your protocol in 18 weeks','Built on your own numbers.','Included'),
 ('#FF7A45','#FFB38A','Free Abbott Lingo CGM','Shipped to your home.','Included'),
 ('#22E39A','#7DE5C1','$100 cash back','On your next course.','November only'),
 ('#7C5CFF','#B79DFF','Julie’s VIP Masterclass','Live, November 14. Plus private Q&amp;A.','Bonus, free'),
 ('#006EFF','#5EB6FF','14-day try-out refund','Course fee back, no questions.','Included')]
arts='\n'.join('      <article class="lla-incl-card" style="--c1:%s;--c2:%s"><span class="n">%02d</span><h3>%s</h3><p>%s</p><b>%s</b></article>'%(c1,c2,i+1,h,p,b) for i,(c1,c2,h,p,b) in enumerate(cards))
inc=blocks['included']
inc_new,n8=re.subn(r'(<div class="lla-incl-grid lla-slider">).*?(\n\s*</div>)', lambda m: m.group(1)+'\n'+arts+m.group(2), inc, count=1, flags=re.S)
log.append(f'included grid {n8}')
blocks['included']=inc_new
# 9. Pillar videos: no eager preload on the preview
blocks['learn-com']=blocks['learn-com'].replace('preload="auto" data-lla-autoplay="1"','preload="metadata" data-lla-autoplay="1"')
# 10. Reassemble in the new order
order=['hero', 'learn-com', 'syllabus', 'offer', 'vip', 'included', 'cgm', 'teachers', 'institution', 'journal', 'whatitis', 'mechanism', 'faq', 'ask', 'enroll-mini']
blocks['nov14-clarity']=strip
assembled='\n'.join(blocks[s] for s in order)+'\n'+res_join
t=t[:first]+assembled+t[last:]
# 11. Title / description
sub1(r'<title>.*?</title>', '<title>The Longevity Blueprint | November offer: $79 first month</title>', name='title')
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
html body#lpRoot #offer .lp-grid{display:block!important;grid-template-columns:none!important;max-width:none!important}
html body#lpRoot #offer .lp-list,html body#lpRoot #included{display:none!important}
html body#lpRoot #offer .pc2{position:relative;display:grid;grid-template-columns:1.15fr .85fr;border-radius:28px;overflow:hidden;background:linear-gradient(160deg,#0d327f 0%,#071b4c 48%,#03102e 100%);box-shadow:0 44px 90px -34px rgba(0,25,80,.8),0 0 0 1px rgba(255,255,255,.08) inset;color:#fff}
html body#lpRoot #offer .pc2::before{content:"";position:absolute;top:-40%;right:-10%;width:60%;height:140%;background:radial-gradient(closest-side,rgba(94,182,255,.32),transparent 72%);pointer-events:none}
html body#lpRoot #offer .pc2-benefits{position:relative;padding:46px 44px 42px}
html body#lpRoot #offer .pc2-eyebrow{font:700 13px/1 Inter,sans-serif;letter-spacing:.16em;text-transform:uppercase;color:#9ecbff;margin:0}
html body#lpRoot #offer .pc2-title{font:500 clamp(30px,3vw,42px)/1.12 "Playfair Display",Georgia,serif;color:#fff;margin:14px 0 30px;max-width:19ch;letter-spacing:-.01em}
html body#lpRoot #offer .pc2-list{list-style:none;margin:0;padding:0;display:grid;gap:20px}
html body#lpRoot #offer .pc2-list li{display:flex;gap:16px;align-items:flex-start;padding:0}
html body#lpRoot #offer .pc2-list li::before{content:none}
html body#lpRoot #offer .pc2-list svg{flex:0 0 28px;width:28px;height:28px;margin-top:1px;filter:drop-shadow(0 6px 14px rgba(0,110,255,.6))}
html body#lpRoot #offer .pc2-list b{display:block;font:700 21px/1.25 Inter,sans-serif;color:#fff}
html body#lpRoot #offer .pc2-list span{display:block;font:400 16px/1.45 Inter,sans-serif;color:#c9dcf8;margin-top:4px}
html body#lpRoot #offer .pc2-vip{position:relative;margin:26px 0 0;display:flex;align-items:center;gap:16px;padding:18px 20px;border-radius:18px;background:linear-gradient(135deg,rgba(124,92,255,.48),rgba(183,157,255,.18));border:1px solid rgba(183,157,255,.7);box-shadow:0 24px 44px -26px rgba(124,92,255,1)}
html body#lpRoot #offer .pc2-vip svg{flex:0 0 30px;width:30px;height:30px;color:#E6DDFF;filter:drop-shadow(0 0 10px rgba(183,157,255,1))}
html body#lpRoot #offer .pc2-vip div{flex:1 1 auto;min-width:0}
html body#lpRoot #offer .pc2-vip b{display:block;font:700 19px/1.25 Inter,sans-serif;color:#fff}
html body#lpRoot #offer .pc2-vip span{display:block;font:400 15px/1.4 Inter,sans-serif;color:#DDD3FF;margin-top:4px}
html body#lpRoot #offer .pc2-vip em{font:700 13px/1 Inter,sans-serif;font-style:normal;letter-spacing:.06em;text-transform:uppercase;color:#2a1a66;background:#E6DDFF;border-radius:999px;padding:10px 12px;white-space:nowrap}
html body#lpRoot #offer .pc2-price{position:relative;margin:22px 22px 22px 0;padding:36px 32px 28px;border-radius:22px;background:#fff;border:1px solid rgba(94,182,255,.75);box-shadow:0 0 0 1px rgba(94,182,255,.35),0 0 52px rgba(94,182,255,.6),0 40px 80px -30px rgba(0,0,0,.75);display:flex;flex-direction:column;align-items:flex-start;justify-content:center;color:#0a244e}
html body#lpRoot #offer .pc2-badge{display:inline-flex;align-items:center;gap:8px;padding:11px 15px;border-radius:999px;background:linear-gradient(90deg,#006EFF,#5EB6FF);color:#fff;font:700 14px/1 Inter,sans-serif;letter-spacing:.06em;text-transform:uppercase;box-shadow:0 0 0 4px rgba(94,182,255,.18),0 14px 28px -10px rgba(0,110,255,.9)}
html body#lpRoot #offer .pc2-badge svg{width:16px;height:16px;flex:0 0 16px}
html body#lpRoot #offer .pc2-now{display:flex;align-items:baseline;margin:18px 0 0;padding:0 0 4px;font:500 clamp(96px,8.6vw,124px)/1.08 "Playfair Display",Georgia,serif;color:#0a244e;letter-spacing:-.045em}
html body#lpRoot #offer .pc2-now .cur{font-size:.42em;color:#006EFF;margin-right:4px;letter-spacing:0}
html body#lpRoot #offer .pc2-per{display:block;clear:both;margin:4px 0 16px;font:700 15px/1.2 Inter,sans-serif;letter-spacing:.14em;text-transform:uppercase;color:#006EFF}
html body#lpRoot #offer .pc2-chips{display:flex;align-items:center;gap:10px;flex-wrap:wrap}
html body#lpRoot #offer .pc2-chips s{font:600 17px/1 Inter,sans-serif;color:#7a8aa3;text-decoration:line-through;text-decoration-thickness:2px}
html body#lpRoot #offer .pc2-chips .save{font:700 13.5px/1 Inter,sans-serif;color:#0b7a4f;background:rgba(34,178,122,.12);border:1px solid rgba(34,178,122,.5);border-radius:999px;padding:9px 12px;letter-spacing:.06em;text-transform:uppercase;white-space:nowrap}
html body#lpRoot #offer .pc2-then{margin:20px 0 24px;font:500 19px/1.4 Inter,sans-serif;color:#203957}
html body#lpRoot #offer .pc2-then b{color:#0a244e;font-weight:800}
html body#lpRoot #offer .pc2-cta{display:block;width:100%;padding:20px 20px;border-radius:16px;background:#006EFF;color:#fff;font:800 19px/1 Inter,sans-serif;text-align:center;text-decoration:none;box-shadow:0 0 0 5px rgba(94,182,255,.22),0 22px 44px -12px rgba(0,110,255,.95);transition:transform .15s ease,background .15s ease}
html body#lpRoot #offer .pc2-cta:hover{background:#0a5fd9;transform:translateY(-1px)}
html body#lpRoot #offer .pc2-note{margin:14px 0 0;width:100%;font:500 14px/1.5 Inter,sans-serif;color:#5b6f8c;text-align:center}
html body#lpRoot #offer .pc2-cta--m{display:none}
@media (max-width:900px){
html body#lpRoot #offer .pc2{grid-template-columns:1fr;border-radius:24px}
html body#lpRoot #offer .pc2-price{order:-1;margin:12px 12px 0;padding:22px 20px 20px;align-items:stretch;text-align:left}
html body#lpRoot #offer .pc2-now{font-size:88px;margin-top:12px}
html body#lpRoot #offer .pc2-then{margin:14px 0 18px}
html body#lpRoot #offer .pc2-benefits{padding:24px 18px 22px}
html body#lpRoot #offer .pc2-title{font-size:26px;margin:10px 0 18px}
html body#lpRoot #offer .pc2-list{gap:12px}
html body#lpRoot #offer .pc2-list svg{width:24px;height:24px;flex-basis:24px}
html body#lpRoot #offer .pc2-list b{font-size:18px}
html body#lpRoot #offer .pc2-list span{font-size:15px;margin-top:2px}
html body#lpRoot #offer .pc2-vip{margin-top:18px;padding:14px;gap:12px}
html body#lpRoot #offer .pc2-vip b{font-size:16.5px}
html body#lpRoot #offer .pc2-vip span{font-size:14px}
html body#lpRoot #offer .pc2-cta--m{display:block;margin:18px 0 0}
html body#lpRoot #vip .lla-vip-grid{display:grid!important;grid-template-columns:1fr!important;gap:24px!important}
}
#mockStrip .strip-cta{display:inline-flex;align-items:center;height:30px;padding:0 14px;margin-left:14px;border-radius:999px;background:#fff;color:#006EFF;font:700 13px/1 Inter,sans-serif;text-decoration:none;letter-spacing:.02em;vertical-align:middle}
#mockStrip .strip-cta:hover{background:#eaf2ff}
#llaWa{position:fixed;right:16px;bottom:calc(92px + env(safe-area-inset-bottom));z-index:9991;display:inline-flex;align-items:center;gap:10px;height:56px;padding:0 18px 0 12px;border-radius:999px;background:#25D366;color:#fff;font:700 15px/1 Inter,sans-serif;text-decoration:none;box-shadow:0 14px 34px -10px rgba(37,211,102,.9),0 0 0 4px rgba(37,211,102,.18)}
#llaWa svg{width:30px;height:30px;flex:0 0 30px}
#llaWa:hover{background:#1ebe5b}
body:has(#enrollModal.open) #llaWa,html.guest-menu-open #llaWa{display:none!important}
#et-bumpyard-widget{display:none!important}
@media(max-width:600px){#llaWa{right:12px;bottom:calc(84px + env(safe-area-inset-bottom));height:52px;width:52px;padding:0;justify-content:center}#llaWa span{display:none}}
</style>
</head>'''
sub1(r'<div class="lla-vip-grid lla-slider">', '<div class="lla-vip-grid">', name='vip slider off')
sub1(r'<div class="lla-incl-grid lla-slider">', '<div class="lla-incl-grid">', name='included slider off')
sub1(r'<p>18 live sessions, live classes, Abbott Lingo CGM included\.</p>', lambda m: '<p>18-week course, Lingo CGM, $100 cash back, Julie’s Masterclass. All included.</p>', name='enroll-mini lead')
sub1(r'</head>', style, name='fold style')
# mini enrol CTA opens the enrol modal like every other Enroll button
def _mini_fix(m):
    tag=m.group(0)
    if 'data-enroll-course' in tag: return tag
    tag=re.sub(r'href="[^"]*"','href="#enrollModal"',tag,count=1); return tag.replace('<a ','<a data-enroll-course="1" ',1)
_ms=re.search(r'<section[^>]*\bid="enroll-mini"',t).start(); _me=t.index('</section>',_ms)
t=t[:_ms]+re.sub(r'<a [^>]*>',_mini_fix,t[_ms:_me])+t[_me:]

t=t.replace('</body>','<a id="llaWa" href="https://wa.me/12015023701?text=Hi%2C%20I%20have%20a%20question%20about%20The%20Longevity%20Blueprint." target="_blank" rel="noopener" aria-label="Chat with us on WhatsApp"><svg viewBox="0 0 32 32" aria-hidden="true"><path fill="#fff" d="M16 3C8.8 3 3 8.7 3 15.8c0 2.5.7 4.9 2 7L3 29l6.4-1.9c2 1.1 4.3 1.7 6.6 1.7 7.2 0 13-5.7 13-12.8S23.2 3 16 3zm0 23.4c-2.1 0-4.1-.6-5.9-1.6l-.4-.2-3.8 1.1 1.2-3.6-.3-.4a10.3 10.3 0 0 1-1.7-5.9C5.1 10 10 5.2 16 5.2s10.9 4.8 10.9 10.6S22 26.4 16 26.4zm6-7.8c-.3-.2-1.9-1-2.2-1.1-.3-.1-.5-.2-.7.2l-1 1.2c-.2.2-.4.2-.7.1-.3-.2-1.4-.5-2.6-1.6-1-.9-1.6-1.9-1.8-2.2-.2-.3 0-.5.1-.7l.5-.6.3-.5c.1-.2 0-.4 0-.6l-1-2.4c-.3-.6-.5-.5-.7-.5h-.6c-.2 0-.6.1-.9.4-.3.3-1.2 1.1-1.2 2.8s1.2 3.3 1.4 3.5c.2.2 2.4 3.6 5.8 5 .8.3 1.4.5 1.9.7.8.3 1.5.2 2.1.1.6-.1 1.9-.8 2.2-1.5.3-.7.3-1.4.2-1.5-.1-.2-.3-.3-.6-.4z"/></svg><span>WhatsApp</span></a>\n'+'</body>',1)
open(f'{OUT}/index.html','w',encoding='utf-8').write(t)
# ---- support files ----
for f in ['exact-source-design.css','guest-mobile.css','guest-mobile.js','attendee-pricing.css','attendee-form.js','checkout.html','_headers']:
    shutil.copy(f'{SRC}/{f}', f'{OUT}/{f}')
os.makedirs(f'{OUT}/blueprint/assets',exist_ok=True)
for f in ['eteacher-ecomm.js','blueprint-hotfix-state.js','nanp-state-autofill.js','ecom-layer.js','lla-country.js','lla-promo.js']:
    shutil.copy(f'{SRC}/blueprint/assets/{f}', f'{OUT}/blueprint/assets/{f}')
shutil.copy(f'{SRC}/blueprint/privacy.html', f'{OUT}/blueprint/privacy.html') if os.path.exists(f'{SRC}/blueprint/privacy.html') else None
# live checkout lives at /blueprint/checkout.html with its own assets: publish it with the files it references
for d in ['brand','eteacher','instructors','pay','wa']:
    if os.path.isdir(f'{SRC}/blueprint/assets/{d}'):
        shutil.copytree(f'{SRC}/blueprint/assets/{d}', f'{OUT}/blueprint/assets/{d}', dirs_exist_ok=True, ignore=shutil.ignore_patterns('*.mp4','*.webm','*.mov'))
for f in ['elements.bundle.min.js','eteacher-leads.js','julie-brand-motion-v7.js','lla-clickid-v20260922.js','lla-logo-dark-text-clean@2x.png','lla-logo-exact-transparent@2x.png','lla-logo-nav.png','lla-relay-receipts.js']:
    if os.path.exists(f'{SRC}/blueprint/assets/{f}'): shutil.copy(f'{SRC}/blueprint/assets/{f}', f'{OUT}/blueprint/assets/{f}')
bc=open(f'{SRC}/blueprint/checkout.html',encoding='utf-8').read()
old_env="window.LLA_ECOMM_CONFIG.env  = (_q.get('env') === 'staging') ? 'staging' : 'production';"
assert old_env in bc, 'checkout env line'
bc=bc.replace(old_env,"window.LLA_ECOMM_CONFIG.env  = (_q.get('env') === 'staging') ? 'staging' : ((_q.get('env') === 'production') ? 'production' : (/github\\.io$/.test(location.hostname) ? 'staging' : 'production'));",1)
open(f'{OUT}/blueprint/checkout.html','w',encoding='utf-8').write(bc)
log.append('blueprint checkout published')
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
fl=fl.replace("  document.getElementById('vip')?.remove();\n","")
_reorder="""  if(hero&&pillars&&syllabus&&offer){
   if(hero.nextElementSibling!==pillars)hero.insertAdjacentElement('afterend',pillars);
   if(pillars.nextElementSibling!==syllabus)pillars.insertAdjacentElement('afterend',syllabus);
   if(syllabus.nextElementSibling!==offer)syllabus.insertAdjacentElement('afterend',offer);
  }
"""
assert _reorder in fl, 'reorder block'
fl=fl.replace(_reorder,"")
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
cp=cp.replace("html('#included h2','What the course <em>includes</em>');","html('#included h2','What <em>you get</em>');")
for line in ["  html('#vip h2',\"Julie's VIP <em>Longevity Masterclass</em>\");\n",
             "  html('#offer h2','Tuition and <em>coupon codes</em>');\n",
             "  text('#offer .lp-lead','18 live classes, learning-platform access, Julie’s VIP masterclass and one Abbott Lingo sensor with U.S. shipping.');\n",
             "  text('#offer .lp-big b','79');text('#offer .lp-saverow s','$169 / month');\n",
             "  text('#offer .lp-pill','Masterclass credit');\n",
             "  html('#offer .lp-total','<b>$755 total</b><small>$90 masterclass credit applied to month 1.</small>');\n",
             "  text('#codeApply','Apply code and enroll');\n",
             "  text('#offer .lp-julie-t b','Masterclass attendee code');\n",
             "  html('#offer .lp-trust','<b>Full refund within 14 days of registration.</b> Questions? Call +1-888-230-5110.');\n",
             "  document.querySelectorAll('header a[href=\"#offer\"]').forEach(a=>{a.textContent='Enroll now';a.dataset.enrollCourse='1'});\n"]:
    assert line in cp, line[:60]
    cp=cp.replace(line,"")
STRIP_NEW="  const strip=document.getElementById('mockStrip');if(strip)strip.innerHTML='<span class=\"t lg\">November offer: $79 first month, Julie\\u2019s VIP Masterclass included free</span><span class=\"t sm\"><a href=\"#enrollModal\" data-enroll-course=\"1\">November offer&nbsp;&middot;&nbsp;<b>$79 month 1</b></a></span>';\n"
cp,nstrip=re.subn(r"  const strip=document\.getElementById\('mockStrip'\);if\(strip\)strip\.innerHTML=.*?\n", lambda m: STRIP_NEW, cp, count=1, flags=re.S)
assert nstrip==1, 'mockStrip rewrite not found'
cp=re.sub(r"  const bar=document\.getElementById\('mockBar'\);if\(bar\)\{.*?\}\n", "", cp, count=1, flags=re.S)
FAQ_NEW="answer.textContent='November offer: $79 first month, then $169 a month for four months, $755 total. Course, Lingo CGM, $100 cash back and Julie\\u2019s VIP Masterclass included. One payment of $799 also available.'"
cp,nfaq=re.subn(r"answer\.textContent='Regular tuition is \$169 per month for five months[^']*'", lambda m: FAQ_NEW, cp, count=1)
assert nfaq==1, 'FAQ cost answer not found'
assert 'coupon codes' not in cp and "html('#hero h1'" in cp
open(f'{OUT}/nov14-copy.js','w',encoding='utf-8').write(cp)
# nov14-pricing.js: keep modal pricing, drop the offer/strip/FAQ credit-code rewrites
pr=open(f'{SRC}/attendee-pricing.js',encoding='utf-8').read()
start=pr.index("   text('#offer .lp-plan','Regular plan: $169 × 5');"); end=pr.index("   text('#pp [data-pl=\"upfront\"] .pp-sub'")
pr=pr[:start]+pr[end:]
pr=re.sub(r"   all\('#faq \.faq-item'\)\.forEach\(e=>\{if\(/How much does it cost/i.*?\n", "", pr, count=1, flags=re.S)
pr=re.sub(r"   html\('\.att-line',.*?\n", "", pr, count=1)
assert "   html('#offer .lp-lead','18 live classes, your learning platform, Julie’s masterclass and an Abbott Lingo sensor.');\n" in pr
pr=pr.replace("   html('#offer .lp-lead','18 live classes, your learning platform, Julie’s masterclass and an Abbott Lingo sensor.');\n","")
pr=pr.replace("   text('#enroll-mini .fn-pc-was','Masterclass credit');","   text('#enroll-mini .fn-pc-was','November offer');")
pr=re.sub(r"   const strip=\$\('#mockStrip'\);\n   if\(strip\)\{.*?\n", "", pr, count=1, flags=re.S)
assert "(active?'Masterclass credit':'Regular plan')" in pr
pr=pr.replace("(active?'Masterclass credit':'Regular plan')","(active?'November offer: $79 first month':'Regular plan')")
pr=pr.replace("text('#emPromoMsg',upfront?'Code applied. $799 one payment.':'Masterclass credit applied.');","text('#emPromoMsg',upfront?'$799 one payment.':'November offer applied: $79 first month.');")
assert 'JULIE249' not in pr.split('function render')[1].split('// Pricing card')[0], 'codes still in render'
pr=pr.replace("text('#mockBar .l b','$79 month 1');","text('#mockBar .l b','$79 first month, over 50% off');")
assert '$79 first month, over 50% off' in pr
open(f'{OUT}/nov14-pricing.js','w',encoding='utf-8').write(pr)
print('\n'.join(log)); print('written', OUT, 'index bytes', len(t))

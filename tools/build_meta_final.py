#!/usr/bin/env python3
"""Build meta-final/index.html: the longevitylifeacademy.com homepage, with Omri's corrections.

Source of truth for design and copy: longevitylifeacademy.com (Longevity-Academy.github.io, index.html).
Pricing card: the masterclass pk-card component (julie-masterclass, julie-v7.css / julie-v8.css).
Longevity news: the masterclass "As featured in" band and press cards (dv-lla-news-card).

Preview safety: every tracking, CRM and checkout script is removed so the preview fires nothing.
The production checkout belongs to eTeacher and is left unchanged; it is not copied here.

Usage: python3 tools/build_meta_final.py <com index.html> <masterclass index.html> <press.css> <out.html>
"""
import re
import sys

COM, MC, PRESS_CSS, OUT = sys.argv[1:5]
BASE = 'https://longevitylifeacademy.com/'
s = open(COM, encoding='utf-8').read()
mc = open(MC, encoding='utf-8').read()
press_css = open(PRESS_CSS, encoding='utf-8').read()
log = []


def must_replace(old, new, count=1):
    global s
    n = s.count(old)
    if n != count:
        raise SystemExit(f'expected {count} of {old[:80]!r}, found {n}')
    s = s.replace(old, new)


def section_bounds(text, start_marker):
    """Return (start, end) of the <section> that starts at start_marker, depth-aware."""
    a = text.find(start_marker)
    if a < 0:
        raise SystemExit(f'missing {start_marker}')
    depth, i = 0, a
    pat = re.compile(r'<section\b|</section>')
    for m in pat.finditer(text, a):
        depth += 1 if m.group(0) == '<section' else -1
        if depth == 0:
            return a, m.end()
    raise SystemExit(f'unclosed {start_marker}')


def remove_section(marker):
    global s
    a, b = section_bounds(s, marker)
    s = s[:a] + s[b:]
    log.append(f'removed section {marker}')


# 1. Tracking, CRM and checkout scripts out (preview must fire nothing).
def drop_scripts(pred, label):
    global s
    out, n = [], 0
    last = 0
    for m in re.finditer(r'<script\b([^>]*)>(.*?)</script>', s, flags=re.S):
        if pred(m.group(1), m.group(2)):
            out.append(s[last:m.start()])
            last = m.end()
            n += 1
    out.append(s[last:])
    s = ''.join(out)
    log.append(f'dropped {n} script(s): {label}')
    return n


drop_scripts(lambda a, b: "PIXEL='1440305917310328'" in b, 'Meta pixel')
drop_scripts(lambda a, b: 'gtm.start' in b, 'GTM')
drop_scripts(lambda a, b: any(x in a for x in ['lla-page-meta.js', 'lla-funnel.js', 'ai-attribution.js',
                                                'lla-promo.js', 'eteacher-ecomm.js', 'nov-offer.js',
                                                'nanp-state-autofill.js', 'lla-country.js']), 'tracking/promo/checkout files')
drop_scripts(lambda a, b: 'ETEACHER_ENV' in b, 'eTeacher lead submit')
drop_scripts(lambda a, b: 'LLA_CAMPAIGN_IDS' in b, 'campaign ids')
drop_scripts(lambda a, b: 'purchase path runs in e-commerce mode' in b, 'ecomm mode')
drop_scripts(lambda a, b: "getElementById('enrollModal')" in b, 'enroll modal')
drop_scripts(lambda a, b: "getElementById('emCountry')" in b, 'enroll country sync')
drop_scripts(lambda a, b: "getElementById('llaFloatCta')" in b, 'floater click script (replaced below)')
s = re.sub(r'<!-- Google Tag Manager \(noscript\) -->.*?<!-- End Google Tag Manager \(noscript\) -->', '', s, flags=re.S)
s = re.sub(r'<noscript>\s*<img[^>]*facebook\.com/tr[^>]*>\s*</noscript>', '', s)

# 2. Promo strip out (the offer goes into the floating bar).
s = re.sub(r'<div id="novStrip".*?</div>\s*', '', s, count=1, flags=re.S)
log.append('removed promo strip')

# 3. Folds removed: coupon tuition (replaced by the masterclass card), sideways sliders,
#    hover-only diagram, bio-age quiz and the Apply form.
remove_section('<section class="how-v2" id="how">')
remove_section('<section class="value">')
remove_section('<section class="deepdive">')
remove_section('<section class="bioquiz">')
remove_section('<section class="lead-gen lead-gen-v2" id="lead-gen">')
a, b = section_bounds(s, '<section class="nov-offer" id="offer">')
s = s[:a] + '%%PRICING%%' + s[b:]
log.append('replaced coupon tuition fold with the masterclass pricing card')

# 4. Pricing fold in the masterclass card design.
PRICING = '''<section class="mc-pricing" id="pricing" style="scroll-margin-top:84px">
  <div class="pk-shell">
    <header class="pk-head">
      <span class="eyebrow">November offer</span>
      <h2 class="section-title">One price. <span class="pk-accent">Everything included.</span></h2>
      <p class="pk-sub">Live 18-week course, free Abbott Lingo CGM, $100 cash back. Online sign-ups in November only.</p>
      <div class="pk-dates" aria-label="Class start dates">
        <span class="pk-date"><b>Mon, Nov 23</b><i>8:00 PM ET</i></span>
        <span class="pk-or">or</span>
        <span class="pk-date"><b>Wed, Nov 25</b><i>12:00 PM ET</i></span>
      </div>
    </header>
    <article class="pk-card pk-vip">
      <div class="pk-top"><span class="pk-tier">November offer</span><span class="pk-len">55% off month one</span></div>
      <div class="pk-pricerow">
        <div class="pk-price"><sup>$</sup>79</div>
        <div class="pk-pricemeta"><s>$169</s><span>Month 1</span></div>
        <h3 class="pk-title">The Longevity <em>Blueprint</em></h3>
      </div>
      <dl class="pk-spec">
        <div><dt>Then</dt><dd>$169 a month for 4 months</dd></div>
        <div><dt>You get</dt><dd><ul class="pk-ul">
          <li>Your personal longevity protocol, built in 18 weeks</li>
          <li>Bonus: Julie Gibson Clark's VIP Masterclass, live November 14</li>
          <li>Free Abbott Lingo CGM, shipped to your home</li>
          <li>18 live classes in small groups, top instructors</li>
          <li>The 6 pillars of longevity, one pillar at a time</li>
          <li>$100 cash back on your next course</li>
        </ul></dd></div>
        <div><dt>Refund</dt><dd>14-day try-out refund on the course</dd></div>
      </dl>
      <a class="pk-btn" href="#pricing" data-preview-enroll><span>Enroll now</span><span class="pk-arr" aria-hidden="true">&rarr;</span></a>
      <p class="pk-previewnote" hidden>Preview. At launch this button opens eTeacher's existing checkout, unchanged.</p>
    </article>
    <p class="pk-foot">14-day try-out refund on the course. Online sign-ups in November only. Questions? Call <a href="tel:+18882305110">+1-888-230-5110</a>.</p>
  </div>
</section>'''
s = s.replace('%%PRICING%%', PRICING)

# 5. Longevity news (masterclass press band and cards), placed after Julie's VIP fold.
i = mc.find('<section class="mq-band">')
band = mc[i:mc.find('</section>', i) + 10]
j = mc.find('<section class="fold f-ink v8-press" id="press">')
press = mc[j:mc.find('</section>', mc.find('v8-press-foot', j)) + 10]
press = re.sub(r'src="assets/(?:instructors|press-people)/([^"]+)"', r'src="press/\1"', press)
press = press.replace('<section class="fold f-ink v8-press" id="press">', '<section class="v8-press mc-news" id="press">')
press = re.sub(r'<div class="shead reveal">.*?</div>',
               '<div class="mc-news-head"><span class="eyebrow">In the press</span>'
               '<h2 class="section-title">Julie in <span class="pk-accent">the press.</span></h2>'
               '<p class="section-subtitle">Fortune, Business Insider, The Sun, Daily Mail, AS, Yahoo Finance, AP News, '
               'The Globe and Mail. Every card links to the original article.</p></div>', press, count=1, flags=re.S)
press = press.replace(' reveal"', '"')
a, b = section_bounds(s, '<section class="nov-vip" id="vip">')
s = s[:b] + '\n<div class="mc-band">' + band + '</div>\n' + press + s[b:]
log.append('added Longevity news (press band and cards) after the VIP fold')

# 6. Copy fixes (Julie bonus is free with enrollment, no codes, no $99, Enroll only).
must_replace('A $99 seat, free with the Blueprint when you enroll with your masterclass code.',
             'Free with enrollment.')
must_replace('<li><b>How you get it.</b> Enroll in the Blueprint with code <span class="nov-code">JULIE249</span> or '
             '<span class="nov-code">MASTERCLASS-VIP</span>. The code is pre-filled in the coupon box above.</li>',
             '<li><b>How you get it.</b> Enroll in the Blueprint in November. Your VIP seat is included free with enrollment.</li>')
must_replace('<a href="#offer" class="nov-vip-cta" data-nov-open>Reserve My Seat',
             '<a href="#pricing" class="nov-vip-cta">Enroll Now')
must_replace('<span class="tag">$99 value, included</span>', '<span class="tag">Included</span>')
must_replace('Applications are open for the next class. Your personal longevity protocol starts here.',
             'Online sign-ups in November only. Your personal longevity protocol starts here.')
s = re.sub(r'(<a href="#lead-gen" class="btn-primary">\s*)Apply Now', r'\1Enroll Now', s)
s = s.replace('<a href="#lead-gen" class="nav-cta">Apply Now</a>', '<a href="#pricing" class="nav-cta">Enroll Now</a>')
s = s.replace('<a href="#lead-gen" class="mobile-nav-link mobile-nav-cta">Apply Now</a>',
              '<a href="#pricing" class="mobile-nav-link mobile-nav-cta">Enroll Now</a>')
s = s.replace('<a href="pricing.html" class="nav-pricing">Pricing</a>', '<a href="#pricing" class="nav-pricing">Pricing</a>')
s = s.replace('<a href="pricing.html" class="mobile-nav-link">Pricing</a>', '<a href="#pricing" class="mobile-nav-link">Pricing</a>')
s = s.replace('      <a href="biological-age-light.html">Bio-Age Quiz</a>\n', '')
s = s.replace('    <a href="biological-age-light.html" class="mobile-nav-link">Bio-Age Quiz</a>\n', '')

# FAQ cost answer: the November offer, no codes (rest of the .com answer kept).
must_replace('In November, tuition is $79 for month 1 with code JULIE249 or MASTERCLASS-VIP, then four monthly payments of $169 ($755 total; regular plan $169 x 5). Tuition includes',
             "November offer: $79 first month, then $169 a month for four months. Course, Lingo CGM, $100 cash back and Julie's VIP Masterclass included. Tuition includes")

# 7. Floating bar: same homepage design, carries the offer.
must_replace('aria-label="Enroll now in The Longevity Blueprint, $79 for month 1"',
             'aria-label="November offer, 55% off month one. $79 for month 1. Enroll now"')
must_replace('<span class="lla-cta-eyebrow">Enroll Now</span>', '<span class="lla-cta-eyebrow">November offer</span>')
must_replace('<span class="lla-cta-title">The Longevity Blueprint</span>', '<span class="lla-cta-title">55% off month one</span>')
must_replace('<span class="price">$79</span><span class="mo">MONTH 1</span>', '<span class="price">$79</span><span class="mo">Month 1</span>')
s = s.replace('<a href="/#lead-gen" class="lla-float-cta" id="llaFloatCta"', '<a href="#pricing" class="lla-float-cta" id="llaFloatCta"')

# 8. Logo: crisp emblem and wordmark in the nav (the tagline version shrank to an unreadable smear).
must_replace('<img src="assets/lla-logo-exact-transparent@2x.png?v=9" alt="Longevity Life Academy" class="nav-logo-img" width="1314" height="596">',
             '<img src="assets/lla-logo-no-tagline@2x.png" alt="Longevity Life Academy" class="nav-logo-img" width="1268" height="397">')

# 9. Remaining in-page links: Apply/coupon anchors go to the price card.
s = s.replace('href="/#lead-gen"', 'href="#pricing"').replace('href="#lead-gen"', 'href="#pricing"')
s = s.replace('href="#offer"', 'href="#pricing"').replace('href="/#offer"', 'href="#pricing"')
s = re.sub(r'\sdata-checkout-open(="[^"]*")?', '', s)
s = re.sub(r'\sdata-nov-open(="[^"]*")?', '', s)


# 10. Asset URLs point at longevitylifeacademy.com so the copy loads the live files.
def absu(u):
    if re.match(r'^(https?:|data:|#|mailto:|tel:|javascript:|press/)', u) or u == '':
        return u
    return BASE + u.lstrip('/')


def attr_fix(m):
    name, q, val = m.group(1), m.group(2), m.group(3)
    if name == 'srcset':
        val = ', '.join(' '.join([absu(p.strip().split(' ')[0])] + p.strip().split(' ')[1:]) for p in val.split(','))
        return f'{name}={q}{val}{q}'
    return f'{name}={q}{absu(val)}{q}'


s = re.sub(r'\b(src|poster|srcset|data-src)=(["\'])(.*?)\2', attr_fix, s)
s = re.sub(r'(<link\b[^>]*\bhref=)(["\'])(.*?)\2', lambda m: m.group(1) + m.group(2) + absu(m.group(3)) + m.group(2), s)


def a_fix(m):
    val = m.group(2)
    if val.startswith('/#'):
        val = val[1:]
    elif not re.match(r'^(https?:|#|mailto:|tel:|javascript:)', val):
        val = BASE + val.lstrip('/')
    return m.group(1) + val + '"'


s = re.sub(r'(<a\b[^>]*?\bhref=")([^"]*)"', a_fix, s)


def css_url_fix(block):
    return re.sub(r'url\(\s*([\'"]?)(?!https?:|data:|#)([^\'")]+)\1\s*\)', lambda m: f"url({m.group(1)}{absu(m.group(2))}{m.group(1)})", block)


s = re.sub(r'(<style\b[^>]*>)(.*?)(</style>)', lambda m: m.group(1) + css_url_fix(m.group(2)) + m.group(3), s, flags=re.S)
s = re.sub(r'style="([^"]*url\([^"]*)"', lambda m: 'style="' + css_url_fix(m.group(1)) + '"', s)

# 11. Head: preview title, noindex. The .com CSP is dropped on the preview host so .com's images and videos can load cross-origin.
s = re.sub(r'<meta http-equiv="Content-Security-Policy"[^>]*>', '', s, count=1)
s = re.sub(r'<title>.*?</title>', '<title>The Longevity Blueprint | November offer: $79 first month</title>', s, count=1, flags=re.S)
s = s.replace('<head>', '<head>\n<meta name="robots" content="noindex, nofollow">', 1)

# 12. Styles for the new parts and the type fixes.
EXTRA_CSS = '''
<style id="meta-final-fixes">
/* Nav logo: crisp, no blur filter */
.nav-logo-img{height:46px!important;width:auto!important;max-width:none!important;filter:none!important}
@media (max-width:768px){.nav-logo-img{height:36px!important}}

/* Masterclass pricing card (julie-v7 + julie-v8 values, scoped to #pricing) */
.mc-pricing{position:relative;padding:110px 0 100px;background:radial-gradient(70% 50% at 50% 0%,rgba(0,110,255,.22),transparent 70%),linear-gradient(180deg,#050B18 0%,#081633 55%,#050B18 100%);color:#fff;overflow:hidden}
.mc-pricing .pk-shell{position:relative;z-index:1;max-width:980px;margin:0 auto;padding:0 40px}
.mc-pricing .pk-head{text-align:center;max-width:860px;margin:0 auto 44px}
.mc-pricing .pk-head .eyebrow{display:block;margin-bottom:14px}
.mc-pricing .pk-head .section-title{color:#fff;margin:0}
.mc-pricing .pk-accent,.mc-news .pk-accent{color:#4DA3FF}
.mc-pricing .pk-sub{margin:20px auto 0;font-size:clamp(19px,1.5vw,22px);line-height:1.6;color:#C9D7EE;max-width:58ch}
.mc-pricing .pk-dates{display:flex;align-items:center;justify-content:center;gap:16px;flex-wrap:wrap;margin-top:30px}
.mc-pricing .pk-date{display:inline-flex;flex-direction:column;align-items:flex-start;gap:2px;padding:14px 24px 14px 22px;border-radius:14px;background:linear-gradient(180deg,rgba(255,255,255,.10),rgba(255,255,255,.04));border:1px solid rgba(124,196,255,.28);box-shadow:0 1px 0 rgba(255,255,255,.12) inset,0 12px 30px -14px rgba(0,0,0,.7);position:relative;text-align:left}
.mc-pricing .pk-date::before{content:"";position:absolute;left:0;top:14px;bottom:14px;width:3px;border-radius:3px;background:linear-gradient(180deg,#7CC4FF,#006EFF);box-shadow:0 0 12px rgba(77,163,255,.9)}
.mc-pricing .pk-date b{font-family:'Codec Pro','Inter',sans-serif;font-weight:700;font-size:20px;color:#fff}
.mc-pricing .pk-date i{font-style:normal;font-size:16px;font-weight:600;color:#9DBDF0;letter-spacing:.02em}
.mc-pricing .pk-or{font-family:'Instrument Serif',Georgia,serif;font-style:italic;font-size:24px;color:#7CC4FF}
.mc-pricing .pk-card{position:relative;display:flex;flex-direction:column;padding:40px 46px 40px;border-radius:32px;isolation:isolate;overflow:hidden;max-width:820px;margin:0 auto}
.mc-pricing .pk-card::before{content:"";position:absolute;inset:0;border-radius:inherit;padding:1px;pointer-events:none;z-index:2;-webkit-mask:linear-gradient(#000 0 0) content-box,linear-gradient(#000 0 0);-webkit-mask-composite:xor;mask-composite:exclude;background:linear-gradient(160deg,rgba(255,255,255,.95),rgba(124,196,255,.35) 45%,rgba(143,227,255,.9))}
.mc-pricing .pk-vip{background:radial-gradient(90% 70% at 100% 0%,rgba(124,196,255,.55),transparent 55%),radial-gradient(70% 50% at 0% 100%,rgba(143,227,255,.28),transparent 60%),linear-gradient(160deg,#0B3B8F 0%,#0A56D8 48%,#006EFF 100%);color:#fff;box-shadow:0 1px 0 rgba(255,255,255,.35) inset,0 2px 4px rgba(0,20,60,.5),0 24px 50px -20px rgba(0,71,179,.8),0 70px 140px -50px rgba(0,110,255,.75)}
.mc-pricing .pk-vip::after{content:"";position:absolute;right:-120px;top:-120px;width:420px;height:420px;border-radius:50%;z-index:0;pointer-events:none;background:radial-gradient(circle,rgba(255,255,255,.35),transparent 65%);filter:blur(18px)}
.mc-pricing .pk-card>*{position:relative;z-index:1}
.mc-pricing .pk-top{display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap}
.mc-pricing .pk-tier{font-size:16px;font-weight:800;letter-spacing:.06em;color:#fff;display:inline-flex;align-items:center;gap:10px}
.mc-pricing .pk-tier::before{content:"";width:9px;height:9px;border-radius:50%;background:#8FE3FF;box-shadow:0 0 0 3px rgba(143,227,255,.25),0 0 12px rgba(143,227,255,1)}
.mc-pricing .pk-len{font-size:16px;font-weight:700;padding:9px 16px;border-radius:999px;background:rgba(255,255,255,.16);color:#fff;border:1px solid rgba(255,255,255,.32)}
.mc-pricing .pk-pricerow{display:flex;align-items:center;gap:14px 20px;flex-wrap:wrap;margin-top:24px}
.mc-pricing .pk-price{font-family:'Codec Pro','Inter',sans-serif;font-weight:800;font-size:clamp(88px,7.4vw,112px);line-height:.9;letter-spacing:-.05em;color:#fff;display:flex;align-items:flex-start;text-shadow:0 2px 0 rgba(0,40,120,.35),0 12px 40px rgba(0,0,0,.35)}
.mc-pricing .pk-price sup{font-size:.4em;line-height:1;margin-top:.22em;margin-right:.06em;font-weight:700;letter-spacing:0}
.mc-pricing .pk-pricemeta{display:flex;flex-direction:column;gap:2px;font-family:'Codec Pro','Inter',sans-serif}
.mc-pricing .pk-pricemeta s{font-size:24px;font-weight:700;color:#BFD7F7}
.mc-pricing .pk-pricemeta span{font-size:19px;font-weight:600;color:#fff}
.mc-pricing .pk-title{flex:1 1 260px;margin:0;font-family:'Codec Pro','Inter',sans-serif;font-weight:700;font-size:clamp(28px,2.4vw,36px);line-height:1.15;letter-spacing:-.02em;color:#fff}
.mc-pricing .pk-title em{font-family:'Instrument Serif',Georgia,serif;font-style:italic;font-weight:400;color:#BFE3FF}
.mc-pricing .pk-spec{margin:28px 0 30px;display:grid}
.mc-pricing .pk-spec>div{display:grid;grid-template-columns:120px 1fr;gap:18px;align-items:baseline;padding:16px 0;border-top:1px solid rgba(255,255,255,.18)}
.mc-pricing .pk-spec>div:last-child{border-bottom:1px solid rgba(255,255,255,.18)}
.mc-pricing .pk-spec dt{font-size:16px;font-weight:800;letter-spacing:.04em;color:#BFE3FF;margin:0}
.mc-pricing .pk-spec dd{margin:0;font-size:21px;line-height:1.5;font-weight:600;color:#fff}
.mc-pricing .pk-ul{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:1fr 1fr;gap:10px 28px}
.mc-pricing .pk-ul li{position:relative;padding-left:22px;font:500 19px/1.42 Inter,sans-serif;color:#fff}
.mc-pricing .pk-ul li::before{content:'';position:absolute;left:1px;top:10px;width:9px;height:9px;border-radius:50%;background:#8FE3FF;box-shadow:0 0 8px rgba(143,227,255,.9)}
.mc-pricing .pk-btn{display:flex;justify-content:space-between;align-items:center;gap:14px;padding:22px 34px;min-height:66px;border-radius:18px;font-family:'Inter',sans-serif;font-weight:800;font-size:21px;text-decoration:none;background:linear-gradient(180deg,#FFFFFF 0%,#EAF3FF 100%);color:#0047B3;box-shadow:0 1px 0 #fff inset,0 -1px 0 rgba(0,40,120,.15) inset,0 2px 3px rgba(0,20,60,.35),0 14px 30px -10px rgba(0,20,60,.6),0 0 40px -6px rgba(143,227,255,.55);transition:transform .25s cubic-bezier(.22,1,.36,1)}
.mc-pricing .pk-btn:hover{transform:translateY(-2px)}
.mc-pricing .pk-btn .pk-arr{font-size:24px;line-height:1}
.mc-pricing .pk-previewnote{margin:14px 0 0;font-size:16px;color:#DCEBFF;text-align:center}
.mc-pricing .pk-foot{text-align:center;margin:30px auto 0;font-size:18px;line-height:1.6;color:#B7C7E3;max-width:60ch}
.mc-pricing .pk-foot a{color:#fff;text-decoration:underline}
@media (max-width:760px){
  .mc-pricing{padding:80px 0 72px}
  .mc-pricing .pk-shell{padding:0 16px}
  .mc-pricing .pk-head{margin-bottom:30px}
  .mc-pricing .pk-sub{font-size:19px}
  .mc-pricing .pk-date b{font-size:18px}
  .mc-pricing .pk-card{padding:28px 22px 26px;border-radius:24px}
  .mc-pricing .pk-tier,.mc-pricing .pk-len{font-size:15px}
  .mc-pricing .pk-price{font-size:88px}
  .mc-pricing .pk-title{font-size:32px;flex-basis:100%}
  .mc-pricing .pk-spec{margin:22px 0 24px}
  .mc-pricing .pk-spec>div{grid-template-columns:1fr;gap:6px;padding:14px 0}
  .mc-pricing .pk-spec dt{font-size:16px}
  .mc-pricing .pk-spec dd{font-size:21px}
  .mc-pricing .pk-ul{grid-template-columns:1fr;gap:10px}
  .mc-pricing .pk-ul li{font-size:20px}
  .mc-pricing .pk-btn{font-size:21px;padding:19px 24px}
  .mc-pricing .pk-foot{font-size:17px}
}

/* Longevity news: masterclass press band and cards */
.mc-band,.mc-news{--blue:#006EFF;--ease:cubic-bezier(.22,1,.36,1);--gutter:clamp(20px,4vw,64px);--ink:#0b0e13;--ink-3:#5B6B8C;--ink-4:#8B97B3;--navy:#0A2240;--r-md:22px;--shadow-card:0 1px 0 rgba(255,255,255,.7) inset,0 30px 70px -34px rgba(10,34,64,.4),0 2px 8px -2px rgba(10,34,64,.08);--silver-2:#E6ECF5;--sky:#6FA8FF;--v7-ease:cubic-bezier(.22,1,.36,1);--v7-ice:#EEF4FC;--v7-md:#3E5A7C;--v7-shadow-light:0 1px 0 #fff inset,0 1px 2px rgba(10,30,58,.10),0 20px 44px -20px rgba(10,30,58,.30),0 60px 120px -50px rgba(0,110,255,.28);--v7-td:#0A1E3A;--v8-ease:cubic-bezier(.22,1,.36,1)}
.mc-news{padding:100px 0 90px;background:linear-gradient(180deg,#F4F8FE 0%,#EAF1FB 100%)}
.mc-news-head{text-align:center;max-width:860px;margin:0 auto 40px}
.mc-news-head .eyebrow{display:block;margin-bottom:12px}
.mc-news-head .section-subtitle{margin:16px auto 0;max-width:720px}
@media (max-width:760px){
  body #press.mc-news{padding:72px 0 64px!important}
  body #press.mc-news .v8-pressgrid{display:grid!important;grid-template-columns:1fr!important;gap:14px!important;overflow:visible!important;scroll-snap-type:none!important;padding:0!important;margin:0!important}
  body #press.mc-news .v8-pressgrid>a.dv-lla-news-card{width:auto!important;min-width:0!important;max-width:none!important;flex:none!important;display:grid!important;grid-template-columns:116px 1fr!important;grid-template-rows:auto!important;align-items:stretch!important;height:auto!important}
  body #press.mc-news .v8-pressgrid>a.dv-lla-news-card .dv-lla-news-media{height:100%!important;min-height:140px!important;aspect-ratio:auto!important;border-radius:0!important}
  body #press.mc-news .v8-pressgrid>a.dv-lla-news-card .dv-lla-news-media img{height:100%!important;width:100%!important;object-fit:cover!important}
  body #press.mc-news .v8-pressgrid>a.dv-lla-news-card .dv-lla-news-body{padding:14px 16px!important;gap:6px!important}
  body #press.mc-news .v8-pressgrid>a.dv-lla-news-card h3{font-size:17px!important;line-height:1.35!important;margin:4px 0!important}
  body #press.mc-news .v8-pressgrid>a.dv-lla-news-card .dv-lla-news-outlet{font-size:14px!important}
  body #press.mc-news .v8-pressgrid>a.dv-lla-news-card .dv-lla-news-meta{font-size:14px!important}
  body #press.mc-news .v8-pressgrid>a.dv-lla-news-card:nth-child(n+5){display:none!important}
  body #press.mc-news.show-all .v8-pressgrid>a.dv-lla-news-card:nth-child(n+5){display:grid!important}
  body #press.mc-news .v8-press-nav{display:none!important}
  body #press.mc-news .mc-news-more{display:flex!important}
}
.mc-news-more{display:none;margin:18px auto 0;justify-content:center}
.mc-news-more button{font:700 18px/1 Inter,sans-serif;color:#0047B3;background:#fff;border:1px solid rgba(0,110,255,.3);border-radius:999px;padding:16px 26px;box-shadow:0 10px 24px -14px rgba(10,30,58,.4)}
.mc-news.show-all .mc-news-more{display:none!important}
''' + press_css + '''

/* Floating bar: same homepage design, larger type */
.lla-float-cta .lla-cta-eyebrow{font-size:13px!important;letter-spacing:.08em!important}
.lla-float-cta .lla-cta-title{font-size:18px!important}
.lla-float-cta .lla-cta-pill .price{font-size:22px!important}
.lla-float-cta .lla-cta-pill .mo{font-size:13px!important}
.lla-float-cta.mf-hide{opacity:0!important;pointer-events:none!important;transform:translateY(20px)!important}
@media (min-width:721px){.lla-float-cta{top:auto!important;bottom:24px!important;left:0!important;right:0!important;margin:0 auto!important;width:max-content!important;max-width:calc(100% - 48px)!important}}
@media (max-width:768px){
  .lla-float-cta .lla-cta-eyebrow{font-size:12px!important}
  .lla-float-cta .lla-cta-title{font-size:16px!important}
  .lla-float-cta .lla-cta-pill .price{font-size:20px!important}
  .lla-float-cta .lla-cta-pill .mo{font-size:12px!important}
}

/* Jordan Lattimore: face higher in the card */
.teacher-card-live-photo img[alt="Jordan Lattimore"]{object-position:50% 22%!important;transform:scale(1.18);transform-origin:50% 80%}

/* Type: nothing under 16px for reading text; labels at least 13px (Omri: tiny text everywhere) */
section .eyebrow,.mc-band .feat{font-size:15px!important}
body section.topics .topic-v2-desc{font-size:17px!important;line-height:1.5!important}
body section.topics .topic-v2-num{font-size:15px!important}
.topics .topic-v2-num{font-size:15px!important}
.curriculum .curriculum-section-label{font-size:14px!important}
.curriculum li,.curriculum .curriculum-flow,.curriculum .curriculum-work{font-size:17px!important;line-height:1.55!important}
.curriculum h3{font-size:18px!important}
.curriculum .curriculum-tab-meta{font-size:13.5px!important}
.curriculum .curriculum-tab-num{font-size:14px!important}
.curriculum .curriculum-tab-name{font-size:16px!important}
.curriculum .phase-block-label{font-size:16px!important}
.nov-incl .tag{font-size:14px!important}
.nov-incl-card p{font-size:17px!important;line-height:1.55!important}
.nov-incl-card h3{font-size:20px!important}
.nov-vip figcaption{font-size:16px!important}
.nov-vip .nov-vip-after{font-size:16px!important}
.nov-vip li,.nov-vip .nov-vip-bio{font-size:18px!important;line-height:1.6!important}
.cgm-fold span{font-size:17px!important}
.cgm-fold .cgm-fold-eyebrow{font-size:14px!important}
.cgm-fold .cgm-fold-cta{font-size:16px!important}
.about p{font-size:19px!important;line-height:1.65!important}
.about .about-powered-label{font-size:15px!important}
.about .about-powered-desc{font-size:18px!important;line-height:1.6!important}
.about .hero-powered-stats li>span{font-size:14px!important}
.about .hero-powered-stats strong{font-size:26px!important}
.about .unit{font-size:18px!important}
.instructors .teacher-card-live-bio{font-size:16.5px!important;line-height:1.55!important}
.instructors .teacher-card-live-role{font-size:13.5px!important}
.testimonials .quote-meta{font-size:14.5px!important}
.testimonials p,.testimonials blockquote{font-size:17px!important;line-height:1.6!important}
.skills .skill-eyebrow{font-size:14px!important}
.hero .trustpilot span{font-size:14px!important}
.faq .faq-num{font-size:15px!important}
.faq .faq-a-inner{font-size:17.5px!important;line-height:1.65!important}
.mc-news .dv-lla-news-meta,.mc-news .dv-lla-news-meta em,.mc-news .dv-lla-news-outlet{font-size:15px!important}
.footer a,.footer p{font-size:16px!important}
.footer h4,.footer div,.footer .brand-name-codec{font-size:14px!important}
@media (min-width:769px){.nav .nav-links a{font-size:16px!important}}
@media (max-width:768px){.hero .hero-sub{font-size:17.5px!important}}

</style>
'''
s = s.replace('</head>', EXTRA_CSS + '</head>', 1)

# 13. Small scripts: floater show/hide, preview enroll note, news "show all", press arrows.
EXTRA_JS = '''
<script>
(function(){
  var cta=document.getElementById('llaFloatCta'),pricing=document.getElementById('pricing'),fin=document.getElementById('apply');
  function upd(){
    if(!cta) return;
    var y=window.scrollY,over=false;
    [pricing,fin].forEach(function(el){if(!el)return;var r=el.getBoundingClientRect();if(r.top<innerHeight*0.75&&r.bottom>innerHeight*0.25)over=true;});
    cta.classList.toggle('is-visible',y>140);
    cta.classList.toggle('mf-hide',over);
  }
  addEventListener('scroll',upd,{passive:true});addEventListener('resize',upd);upd();
  document.querySelectorAll('[data-preview-enroll]').forEach(function(a){a.addEventListener('click',function(e){e.preventDefault();var n=a.parentNode.querySelector('.pk-previewnote');if(n)n.hidden=false;});});
  var news=document.querySelector('.mc-news');
  if(news){var g=news.querySelector('.v8-pressgrid');var wrap=document.createElement('div');wrap.className='mc-news-more';wrap.innerHTML='<button type="button">Show all 9 articles</button>';
    (news.querySelector('.v8-press-nav')||g).insertAdjacentElement('afterend',wrap);
    wrap.querySelector('button').addEventListener('click',function(){news.classList.add('show-all');});
    document.querySelectorAll('.v8-press-btn').forEach(function(b){b.addEventListener('click',function(){var c=g.querySelector('.dv-lla-news-card');var w=c?c.getBoundingClientRect().width+28:420;g.scrollBy({left:w*parseInt(b.dataset.dir,10),behavior:'smooth'});});});}
})();
</script>
'''
s = s.replace('</body>', EXTRA_JS + '</body>', 1)

open(OUT, 'w', encoding='utf-8').write(s)
print('\n'.join(log))
print('bytes', len(s))

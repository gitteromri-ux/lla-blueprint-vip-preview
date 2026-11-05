#!/usr/bin/env python3
"""Build the Final website for Meta from Omri's review-file selection (claude-selection.json).

Design source: the longevitylifeacademy.com homepage code. Hero: the pages.dev cinematic video hero.
Pricing: the masterclass pk-card (blue VIP card). CGM: new compact fold (asked for by Omri).

Outputs, from one build:
  preview     meta-final/index.html          tracking, CRM and checkout scripts stripped; .com assets absolute.
  production  meta-final/PRODUCTION-index.html.txt
              identical page with .com's tracking and eTeacher's checkout intact (relative .com paths),
              CSP widened only for the pages.dev hero video and player. Rename to index.html on .com.

Usage: python3 tools/build_meta_final.py <com index.html> <pages.dev nov14 index.html> <hero.css> <outdir>
"""
import os
import re
import sys

COM, DEV, HERO_CSS, OUTDIR = sys.argv[1:5]
WWW = 'https://www.longevitylifeacademy.com/'
HERE = os.path.dirname(os.path.abspath(__file__))
com_src = open(COM, encoding='utf-8').read()
dev = open(DEV, encoding='utf-8').read()
hero_css = open(HERO_CSS, encoding='utf-8').read()


def bounds(text, marker):
    a = text.find(marker)
    if a < 0:
        raise SystemExit(f'missing {marker}')
    depth = 0
    for m in re.finditer(r'<section\b|</section>', text[a:]):
        depth += 1 if m.group(0) == '<section' else -1
        if depth == 0:
            return a, a + m.end()
    raise SystemExit(f'unclosed {marker}')


# ---------------------------------------------------------------- pieces
a, b = bounds(dev, '<section class="pdp-hero pdp-hero--cine" id="hero">')
DEV_HERO = dev[a:b]
DEV_HERO = DEV_HERO.replace('<a href="#offer" class="pdp-cine-cta" data-fn-cta="hero">Reserve My Seat',
                            '<a href="#lead-gen" class="pdp-cine-cta">Enroll now')
assert 'Enroll now' in DEV_HERO
DEV_HERO = DEV_HERO.replace('4.6 on Trustpilot, 600+ reviews <i></i> ', '')
DEV_HERO = re.sub(r'<h1 class="pdp-cine-h1[^"]*">.*?</h1>', '<h1 class="pdp-cine-h1">It\'s Your Life.<br><span class="pdp-cine-blue">Live It Well.</span></h1>', DEV_HERO, count=1, flags=re.S)
DEV_HERO = re.sub(r'<p class="pdp-cine-sub[^"]*"[^>]*>.*?</p>', '<p class="pdp-cine-sub mf-hero-sub"><strong>The longevity course</strong>, a guided protocol built around <em>your biology, your numbers</em>, and the daily practice that turns the next decades into your strongest.</p>', DEV_HERO, count=1, flags=re.S)
assert 'mf-hero-sub' in DEV_HERO and 'Live It Well' in DEV_HERO
# pages.dev 'What you'll learn' (the 18 classes, week by week), multi-colour per phase
a, b = bounds(dev, '<section class="curriculum pr-light lp-white lp-numbered is-light"')
DEV_LEARN = dev[a:b]
DEV_LEARN = DEV_LEARN.replace('<section class="curriculum pr-light lp-white lp-numbered is-light"', '<section class="curriculum mf-learn"', 1)
PH = {'1': '#1F6BFF', '2': '#0FA58A', '3': '#F2662B', '4': '#7A4DFF'}
for k, c in PH.items():
    DEV_LEARN = DEV_LEARN.replace(f'data-phase-tab="{k}"', f'data-phase-tab="{k}" style="--ph:{c}"')
    DEV_LEARN = re.sub(r'(<div class="phase-block[^"]*" data-phase="' + k + r'")', r'\1 style="--ph:' + c + '"', DEV_LEARN)
DEV_LEARN = re.sub(r'href="#offer"', 'href="#lead-gen"', DEV_LEARN)
JULIE = open(os.path.join(HERE, 'meta_final_julie.html'), encoding='utf-8').read()
m = re.search(r'<script id="lla-r11-lazy-video">.*?</script>', dev, flags=re.S)
AUTOPLAY_JS = m.group(0) if m else ''
assert AUTOPLAY_JS, 'pages.dev autoplay script not found'

PRICING = open(os.path.join(HERE, 'meta_final_pricing.html'), encoding='utf-8').read()
CGM = open(os.path.join(HERE, 'meta_final_cgm.html'), encoding='utf-8').read()

ORDER = [  # Omri's review-file order (claude-selection.json); hero, pricing and CGM are replaced.
    ('hero', '<section class="hero" id="hero">', None),
    ('topics', '<section class="topics">', None),
    ('syllabus', '<section class="curriculum" id="syllabus">', DEV_LEARN),
    ('pricing', '<section class="nov-offer" id="offer">', PRICING),
    ('julie', '<section class="nov-vip" id="vip">', JULIE),
    ('included', '<section class="nov-incl" id="included">', None),
    ('cgm', '<section class="cgm-fold" id="cgm">', CGM),
    ('about', '<section class="about" id="about">', None),
    ('trust', '<section class="trust-strip"', None),
    ('teachers', '<section class="instructors" id="teachers">', None),
    ('how', '<section class="how-v2" id="how">', None),
    ('news', '<section class="skills" id="skills">', None),
    ('why', '<section class="value">', None),
    ('systems', '<section class="deepdive">', None),
    ('form', '<section class="lead-gen lead-gen-v2" id="lead-gen">', None),
    ('quiz', '<section class="bioquiz">', None),
    ('reviews', '<section class="testimonials">', None),
    ('faq', '<section class="faq" id="faq">', None),
    ('final', '<section class="final-cta" id="apply">', None),
]
DROPPED = []


def assemble(s):
    spans = {name: bounds(s, marker) for name, marker, _ in ORDER}
    first = min(x[0] for x in spans.values())
    last = max(x[1] for x in spans.values())
    ranges = sorted(list(spans.values()) + [bounds(s, d) for d in DROPPED])
    leftovers, pos = [], first
    for x, y in ranges:
        leftovers.append(s[pos:x])
        pos = y
    extra = ''.join(leftovers)
    stray = re.sub(r'<!--.*?-->|\s+', '', extra, flags=re.S)
    body = '\n'.join(rep if rep is not None else s[spans[name][0]:spans[name][1]] for name, _, rep in ORDER)
    # keep any non-fold markup that sat between folds (scripts, widgets) after the folds
    keep = re.sub(r'<!--.*?-->', '', extra, flags=re.S) if stray else ''
    return s[:first] + body + '\n' + keep + s[last:], stray


def must(s, old, new, count=1):
    n = s.count(old)
    if n != count:
        raise SystemExit(f'expected {count} of {old[:90]!r}, found {n}')
    return s.replace(old, new)


# ---------------------------------------------------------------- common edits (both outputs)
def common(s):
    s = re.sub(r'<div id="novStrip".*?</div>\s*', '', s, count=1, flags=re.S)  # promo strip out
    s = re.sub(r'<html\b([^>]*)>', lambda m: '<html' + (m.group(1).replace('class="', 'class="mf ') if 'class="' in m.group(1) else m.group(1) + ' class="mf"') + '>', s, count=1)
    s, stray = assemble(s)
    a, b = bounds(s, '<section class="hero" id="hero">')
    hero = s[a:b]
    hero = must(hero, '<img src="assets/hero-cgm.jpg" alt="Continuous glucose monitor and personalized health protocol" class="hero-image" loading="eager" fetchpriority="high">',
                '<video class="hero-image mf-cells" src="https://longevitylifeacademy.pages.dev/assets/cells-light.mp4" poster="https://longevitylifeacademy.pages.dev/assets/cells-poster.jpg" autoplay muted loop playsinline preload="auto" aria-hidden="true"></video>')
    film = re.search(r'<figure class="lla-film">.*?</figure>', DEV_HERO, flags=re.S).group(0)
    hero = re.sub(r'<h1 class="hero-title">.*?</h1>', '<h1 class="hero-title">Your personal longevity protocol,<br><span class="life-blue">built in 18 weeks.</span></h1>', hero, count=1, flags=re.S)
    hero = re.sub(r'<p class="hero-sub">.*?</p>', '<p class="hero-sub">Live small-group classes with certified longevity instructors. A free Abbott Lingo glucose sensor shipped to your home. You finish with a written protocol built on your own numbers.</p>', hero, count=1, flags=re.S)
    # Trustpilot: no pill (Omri). One clean rating line.
    tp = ('<div class="mf-tp" role="img" aria-label="Rated 4.6 out of 5 on Trustpilot, 600+ verified reviews">'
          '<span class="mf-tp-logo"><svg viewBox="0 0 24 24" aria-hidden="true"><path fill="#00B67A" d="M12 1.5l2.9 8.2H24l-7.1 5.2 2.7 8.6L12 18.3l-7.6 5.2 2.7-8.6L0 9.7h9.1z"/></svg><b>Trustpilot</b></span>'
          '<span class="mf-tp-stars">' + ''.join('<i><svg viewBox="0 0 24 24" aria-hidden="true"><path fill="#fff" d="M12 3.6l2.3 6.1h6.4l-5.1 3.9 1.9 6.3L12 16l-5.5 3.9 1.9-6.3-5.1-3.9h6.4z"/></svg></i>' for _ in range(5)) + '</span>'
          '<span class="mf-tp-score"><b>4.6</b> / 5</span><span class="mf-tp-count">600+ verified reviews</span></div>')
    hero = re.sub(r'<div class="trustpilot trustpilot--top">.*?600\+ verified reviews</span>\s*</div>', tp, hero, count=1, flags=re.S)
    assert 'mf-tp' in hero, 'trustpilot replace failed'
    hero = hero[:hero.rfind('</section>')] + '<div class="mf-hero-film">' + film + '</div>\n</section>'
    s = s[:a] + hero + s[b:]
    if stray:
        print('note: non-fold markup between folds kept after the folds:', stray[:200])
    # client logos: three more sets so the coloured logos run as a continuous band
    m = re.search(r'(<div class="trust-strip-track">)(.*?)(</div>\s*</div>\s*</section>)', s, flags=re.S)
    if m:
        logos = re.sub(r'<!--.*?-->', '', m.group(2), flags=re.S)
        extra = re.sub(r'alt="[^"]*"', 'alt=""', logos).replace('title="', 'aria-hidden="true" data-title="')
        s = s[:m.start(2)] + logos + extra + extra + s[m.end(2):]
    s = s.replace('</head>', '<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,500;0,600;0,700;1,400;1,500;1,600;1,700&display=swap" rel="stylesheet">\n</head>', 1)
    s = must(s, '<span class="tag">$99 value, included</span>', '<span class="tag">Included</span>')
    s = must(s, '<span style="color:#006EFF;">Doesn\'t Have Time to Teach You.</span>', '<span class="mf-lb">Doesn\'t Have Time to Teach You.</span>')
    s = must(s, 'In November, tuition is $79 for month 1 with code JULIE249 or MASTERCLASS-VIP, then four monthly payments of $169 '
                '($755 total; regular plan $169 x 5). Tuition includes',
             "November offer: $79 first month, then $169 a month for four months. Course, Lingo CGM, $100 cash back and "
             "Julie's VIP Masterclass included. Tuition includes")
    s = must(s, 'Applications are open for the next class. Your personal longevity protocol starts here.',
             'Online sign-ups in November only. Your personal longevity protocol starts here.')
    s = re.sub(r'(<a href="#lead-gen" class="btn-primary">\s*)Apply Now', r'\1Enroll Now', s)
    s = s.replace('<a href="#lead-gen" class="nav-cta">Apply Now</a>', '<a href="#lead-gen" class="nav-cta">Enroll Now</a>')
    s = s.replace('<a href="#lead-gen" class="mobile-nav-link mobile-nav-cta">Apply Now</a>', '<a href="#lead-gen" class="mobile-nav-link mobile-nav-cta">Enroll Now</a>')
    s = s.replace('<a href="pricing.html" class="nav-pricing">Pricing</a>', '<a href="#pricing" class="nav-pricing">Pricing</a>')
    s = s.replace('<a href="pricing.html" class="mobile-nav-link">Pricing</a>', '<a href="#pricing" class="mobile-nav-link">Pricing</a>')
    s = s.replace('      <a href="biological-age-light.html">Bio-Age Quiz</a>\n', '')
    s = s.replace('    <a href="biological-age-light.html" class="mobile-nav-link">Bio-Age Quiz</a>\n', '')
    s = s.replace('href="#offer"', 'href="#lead-gen"')
    s = must(s, 'aria-label="Enroll now in The Longevity Blueprint, $79 for month 1"', 'aria-label="November offer, 55% off month one, $79 for month 1. Enroll now"')
    s = must(s, '<span class="lla-cta-eyebrow">Enroll Now</span>', '<span class="lla-cta-eyebrow">November offer</span>')
    s = must(s, '<span class="lla-cta-title">The Longevity Blueprint</span>', '<span class="lla-cta-title">55% off month one</span>')
    s = must(s, '<span class="mo">MONTH 1</span>', '<span class="mo">Month 1</span>')
    s = must(s, '<img src="assets/lla-logo-exact-transparent@2x.png?v=9" alt="Longevity Life Academy" class="nav-logo-img" width="1314" height="596">',
             '<img src="assets/lla-logo-no-tagline@2x.png" alt="Longevity Life Academy" class="nav-logo-img" width="1268" height="397">')
    s = re.sub(r'<title>.*?</title>', '<title>The Longevity Blueprint | November offer: $79 first month</title>', s, count=1, flags=re.S)
    # Credibility audit: no dashes or arrows in running text (buttons keep their arrow icons)
    s = s.replace('Register &rarr; Choose your dates &rarr; Pay online &middot; done in 2 minutes', 'Register, choose your dates, pay online, done in 2 minutes')

    def clean_text(m):
        t = m.group(0)
        t = re.sub(r'(\d)\s*(?:–|&ndash;)\s*(\d)', r'\1 to \2', t)
        t = re.sub(r'\s+(?:→|&rarr;)\s+(?=\w)', ', ', t)
        t = re.sub(r'\s*(?:—|&mdash;)\s*', ', ', t)
        return t

    head_end = s.find('<body')
    parts = re.split(r'(<script\b.*?</script>|<style\b.*?</style>)', s[head_end:], flags=re.S)
    parts = [p if p.startswith('<script') or p.startswith('<style') else re.sub(r'>[^<]+<', clean_text, p) for p in parts]
    s = s[:head_end] + ''.join(parts)
    # Round 9 (Omri: Playfair italic display, consistent on all headers): headers with a line break and no accent span
    # get the text after the break marked as the italic accent. Markup only, the wording is unchanged.
    def _acc(m):
        inner = m.group(3)
        if '<span' in inner or '<em' in inner or '<br>' not in inner:
            return m.group(0)
        a, b = inner.split('<br>', 1)
        return m.group(1) + a + '<br><span class="mf-acc">' + b + '</span>' + m.group(4)
    s = re.sub(r'(<h2 class="(section-title|bioquiz-title|how-v2-title)[^"]*"[^>]*>)(.*?)(</h2>)', _acc, s, flags=re.S)
    css = open(os.path.join(HERE, 'meta_final.css'), encoding='utf-8').read().replace('/*%%HERO_CSS%%*/', '').replace('/*%%NEW_FOLDS%%*/', open(os.path.join(HERE, 'meta_final_newfolds.css'), encoding='utf-8').read()).replace('/*%%JULIE_CSS%%*/', open(os.path.join(HERE, 'masterclass_julie.css'), encoding='utf-8').read()).replace('/*%%BRAND%%*/', open(os.path.join(HERE, 'meta_final_fix.css'), encoding='utf-8').read())
    s = s.replace('</head>', '<style id="meta-final">\n' + css + '\n</style>\n</head>', 1)
    js = open(os.path.join(HERE, 'meta_final.js'), encoding='utf-8').read()
    s = s.replace('</body>', AUTOPLAY_JS + '\n<script>\n' + js + '\n</script>\n</body>', 1)
    return s


def drop_scripts(s, pred):
    return re.sub(r'<script\b([^>]*)>(.*?)</script>', lambda m: '' if pred(m.group(1), m.group(2)) else m.group(0), s, flags=re.S)


# ---------------------------------------------------------------- preview: nothing fires
def preview(s):
    s = drop_scripts(s, lambda a, b: "PIXEL='1440305917310328'" in b or 'gtm.start' in b
                     or any(x in a for x in ['lla-page-meta.js', 'lla-funnel.js', 'ai-attribution.js', 'lla-promo.js',
                                             'eteacher-ecomm.js', 'nov-offer.js', 'nanp-state-autofill.js', 'lla-country.js'])
                     or any(x in b for x in ['ETEACHER_ENV', 'LLA_CAMPAIGN_IDS', 'purchase path runs in e-commerce mode',
                                             "getElementById('enrollModal')", "getElementById('emCountry')", "getElementById('llaFloatCta')"]))
    s = re.sub(r'<!-- Google Tag Manager \(noscript\) -->.*?<!-- End Google Tag Manager \(noscript\) -->', '', s, flags=re.S)
    s = re.sub(r'<meta http-equiv="Content-Security-Policy"[^>]*>', '', s, count=1)
    s = s.replace('<head>', '<head>\n<meta name="robots" content="noindex, nofollow">', 1)
    s = s.replace('href="/#lead-gen"', 'href="#pricing"').replace('href="#lead-gen"', 'href="#pricing"')
    s = re.sub(r'\sdata-checkout-open(="[^"]*")?', '', s)
    s = re.sub(r'\sdata-nov-open(="[^"]*")?', '', s)
    s = s.replace('</body>', '<script>document.querySelectorAll("#lead-gen form").forEach(function(f){f.addEventListener("submit",function(e){e.preventDefault();e.stopImmediatePropagation();var n=f.querySelector(".mf-formnote");if(!n){n=document.createElement("p");n.className="mf-formnote";n.textContent="Preview. On longevitylifeacademy.com this form goes to the admissions team, unchanged.";f.appendChild(n);}},true);});</script>\n</body>', 1)
    s = must(s, '<a class="pk-btn" href="#pricing">', '<a class="pk-btn" href="#pricing" data-preview-enroll>')
    s = must(s, '<p class="pk-refund">', '<p class="pk-previewnote" hidden>Preview. On longevitylifeacademy.com this button opens eTeacher\'s checkout, unchanged.</p><p class="pk-refund">')

    def absu(u):
        if re.match(r'^(https?:|data:|#|mailto:|tel:|javascript:)', u) or u == '':
            return u
        return WWW + u.lstrip('/')

    def attr(m):
        n, q, v = m.groups()
        if n == 'srcset':
            v = ', '.join(' '.join([absu(p.strip().split(' ')[0])] + p.strip().split(' ')[1:]) for p in v.split(','))
            return f'{n}={q}{v}{q}'
        return f'{n}={q}{absu(v)}{q}'
    s = s.replace('mfasset:', 'https://gitteromri-ux.github.io/lla-blueprint-vip-preview/meta-final/assets/')
    s = re.sub(r'\b(src|poster|srcset|data-src)=(["\'])(.*?)\2', attr, s)
    s = re.sub(r'(<link\b[^>]*\bhref=)(["\'])(.*?)\2', lambda m: m.group(1) + m.group(2) + absu(m.group(3)) + m.group(2), s)
    s = re.sub(r'(<a\b[^>]*?\bhref=")([^"]*)"',
               lambda m: m.group(1) + (m.group(2)[1:] if m.group(2).startswith('/#') else (m.group(2) if re.match(r'^(https?:|#|mailto:|tel:|javascript:)', m.group(2)) else WWW + m.group(2).lstrip('/'))) + '"', s)

    def cssu(block):
        return re.sub(r'url\(\s*([\'"]?)(?!https?:|data:|#)([^\'")]+)\1\s*\)', lambda m: f"url({m.group(1)}{absu(m.group(2))}{m.group(1)})", block)
    s = re.sub(r'(<style\b[^>]*>)(.*?)(</style>)', lambda m: m.group(1) + cssu(m.group(2)) + m.group(3), s, flags=re.S)
    s = re.sub(r'style="([^"]*url\([^"]*)"', lambda m: 'style="' + cssu(m.group(1)) + '"', s)
    return s


# ---------------------------------------------------------------- production: .com tracking and eTeacher checkout intact
def production(s):
    pd = 'https://longevitylifeacademy.pages.dev'

    def csp(m):
        c = m.group(1)
        c = c.replace("script-src 'self' 'unsafe-inline'", f"script-src 'self' 'unsafe-inline' {pd}", 1)
        c = c.replace("media-src 'self'", f"media-src 'self' {pd} blob:", 1)
        return f'<meta http-equiv="Content-Security-Policy" content="{c}">'
    s = s.replace('mfasset:', 'assets/mf/')
    return re.sub(r'<meta http-equiv="Content-Security-Policy" content="([^"]*)">', csp, s, count=1)


base = common(com_src)
os.makedirs(OUTDIR, exist_ok=True)
pv, pr = preview(base), production(base)
open(os.path.join(OUTDIR, 'index.html'), 'w', encoding='utf-8').write(pv)
open(os.path.join(OUTDIR, 'PRODUCTION-index.html.txt'), 'w', encoding='utf-8').write(pr)
print('preview', len(pv), 'production', len(pr))

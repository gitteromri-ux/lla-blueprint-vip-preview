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
PH = {'1': '#006EFF', '2': '#0A1E3A', '3': '#3BA7FF', '4': '#1B4FD8'}
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

ORDER = [  # Omri 6 Nov (latest): hero, six pillars, syllabus, Julie, pricing, CGM, instructors, how it works, about, logos, reviews, blog, Six Systems, why different, quiz, form, FAQ
    ('hero', '<section class="hero" id="hero">', None),
    ('topics', '<section class="topics">', None),
    ('syllabus', '<section class="curriculum" id="syllabus">', None),  # Omri 6 Nov: the longevitylifeacademy.com fold itself, colours and fonts optimized
    ('julie', '<section class="nov-vip" id="vip">', JULIE),
    ('pricing', '<section class="nov-offer" id="offer">', PRICING),
    ('cgm', '<section class="cgm-fold" id="cgm">', CGM),
    ('teachers', '<section class="instructors" id="teachers">', None),
    ('how', '<section class="how-v2" id="how">', None),
    ('about', '<section class="about" id="about">', None),
    ('trust', '<section class="trust-strip"', None),
    ('reviews', '<section class="testimonials">', None),
    ('news', '<section class="skills" id="skills">', None),
    ('systems', '<section class="deepdive">', None),
    ('why', '<section class="value">', None),
    ('quiz', '<section class="bioquiz">', None),
    ('form', '<section class="lead-gen lead-gen-v2" id="lead-gen">', None),  # Omri (latest): the form is huge, it can be at the end
    ('faq', '<section class="faq" id="faq">', None),
]
DROPPED = ['<section class="nov-incl" id="included">', '<section class="final-cta" id="apply">']  # Omri 6 Nov: course includes and the final banner are not in his order


def assemble(s):
    spans = {name: bounds(s, marker) for name, marker, _ in ORDER}
    dropped = [bounds(s, d) for d in DROPPED]
    first = min(x[0] for x in list(spans.values()) + dropped)
    last = max(x[1] for x in list(spans.values()) + dropped)
    ranges = sorted(list(spans.values()) + dropped)
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


def opt(s, old, new):
    """Like must(), for text inside a fold that may be dropped from the page."""
    return s.replace(old, new, 1) if old in s else s


def must(s, old, new, count=1):
    n = s.count(old)
    if n != count:
        raise SystemExit(f'expected {count} of {old[:90]!r}, found {n}')
    return s.replace(old, new)


# ---------------------------------------------------------------- common edits (both outputs)
def r39(s):
    """Round 39 (Omri's review board, round 38). Copy and markup changes only; styles live in meta_final_r39.css."""
    # Hero: the last headline line is set a little smaller
    s = must(s, '<br>built in 18 weeks.</h1>', '<br><span class="mf-h1-last">built in 18 weeks.</span></h1>')
    # Six pillars: each card title starts with Master
    a = s.find('<section class="topics'); b = s.find('</section>', a)
    sec = s[a:b]; sec, n = re.subn(r'(<h3 class="topic-v2-title">)(.*?)(</h3>)', r'\1Master \2\3', sec)
    assert n == 6, 'pillar titles'
    s = s[:a] + sec + s[b:]
    # How It Works: the ecommerce flow from our pages.dev site ("How it works, start to finish"); class times left out (pages.dev and the checkout differ)
    steps = [
        ('Day one', 'Enroll in three clicks', 'Register, pick your class, pay. Your platform login arrives straight away.'),
        ('Week one', 'Your first live session', '50 minutes live with your instructor and your classmates, weekly at the time you choose at checkout.'),
        ('Before lesson five', 'Your Abbott Lingo arrives', 'Shipped free to your address. You start reading your own glucose data in class.'),
        ('Weeks one to eighteen', 'Learn it, then live it', 'Eighteen live sessions across four phases. Each week you practice the protocol on your own body.'),
        ('Week eighteen', 'Your Personal Longevity Blueprint', 'You finish with a written protocol built on your numbers. It stays yours.'),
    ]
    cards = ''.join(f'\n          <div class="how-v2-card mf-how{i+1}"><span class="how-v2-num">{i+1:02d}</span><span class="how-v2-card-meta">{t}</span><h3 class="how-v2-card-title">{h}</h3><p class="how-v2-card-desc">{d}</p></div>' for i, (t, h, d) in enumerate(steps))
    a = s.find('<div class="how-v2-track" id="howTrack">'); assert a > 0
    b = s.find('</div>\n      </div>', a)
    first = s.find('<div class="how-v2-card"', a)
    last_end = s.rfind('</div>', a, b)
    seg = s[a:b]
    seg2, n = re.subn(r'\s*<div class="how-v2-card"[^>]*>.*?</div>', '', seg, flags=re.S)
    assert n == 6, 'how cards'
    seg2 = seg2.replace('<div class="how-v2-track" id="howTrack">', '<div class="how-v2-track" id="howTrack">' + cards, 1)
    s = s[:a] + seg2 + s[b:]
    s = must(s, '<p class="how-v2-sub">Six clear steps from enrollment to your personal longevity protocol.</p>', '<p class="how-v2-sub">How it works, start to finish. Enroll today. Sensor at your door by week five. Your Blueprint by week 18.</p>')
    # Why different: the shorter card texts from our pages.dev site
    why = {
        '1': 'Every session is live with a certified instructor and your classmates. You ask questions in real time and get real answers. Recordings are there if you miss one.',
        '2': 'You do not memorize facts about glucose or sleep. You watch them move in your own body. CGM readings and lifestyle logs shape every session.',
        '3': 'You will know your classmates by name and they will know yours. Peer coaching in the final weeks builds the accountability that keeps the protocol alive.',
        '4': 'The course ends with your personal longevity blueprint, tested against your body over 18 weeks. The one deliverable designed to outlast the course.',
    }
    for k, txt in why.items():
        s, n = re.subn(r'(<div class="value-card reveal" data-accent="' + k + r'">\s*<h3 class="value-title">.*?</h3>\s*<p class="value-desc">).*?(</p>)', lambda m: m.group(1) + txt + m.group(2), s, count=1, flags=re.S)
        assert n == 1, 'why ' + k
    # Application form: one clean ecommerce button
    s, n = re.subn(r'(<a href="#"[^>]*class="lg-buy">)\s*<span class="lg-buy-main">.*?</span>\s*<span class="lg-buy-sub">.*?</span>\s*(</a>)', r'\1<span class="lg-buy-main">Enroll Online Now</span><span class="lg-buy-arr" aria-hidden="true">&rarr;</span>\2', s, count=1, flags=re.S)
    assert n == 1, 'lg-buy'
    # Syllabus: the phase label breaks after the phase number on phones
    # Syllabus phase cards: one hierarchy in every card (number, name, sessions)
    s, n = re.subn(r'<span class="phase-block-label">Phase (\d),\s*(Sessions [^<]*)</span>\s*<span class="phase-block-name">([^<]*)</span>',
                   lambda m: '<span class="phase-block-num">0' + m.group(1) + '</span><span class="phase-block-name">' + m.group(3) + '</span><span class="phase-block-label">' + m.group(2) + '</span>', s)
    # .com syllabus: ranges in words (no en dashes), middle dot to comma
    a = s.find('<section class="curriculum" id="syllabus">'); b = s.find('</section>', a)
    if a > 0:
        sec = s[a:b]
        sec = re.sub(r'(\d+)\s*[\u2013\u2014]\s*(\d+)', r'\1 to \2', sec)
        sec = sec.replace('Phase 1 \u00b7 ', 'Phase 1, ').replace('Phase 2 \u00b7 ', 'Phase 2, ').replace('Phase 3 \u00b7 ', 'Phase 3, ').replace('Phase 4 \u00b7 ', 'Phase 4, ')
        sec = sec.replace(' \u00b7 ', ', ')
        sec = re.sub(r'([A-Za-z])\s*[\u2013\u2014]\s*([A-Za-z])', r'\1-\2', sec)
        s = s[:a] + sec + s[b:]
    # Application form: shorter placeholders so they fit the two-column phone layout
    s = must(s, 'placeholder="Your first name"', 'placeholder="First name"')
    s = must(s, 'placeholder="Your last name"', 'placeholder="Last name"')
    # About: the first sentence becomes a large statement, the rest a wider paragraph (Omri, round 40 board)
    s, n = re.subn(r'<p class="about-lead about-lead--gal">\s*(Longevity Life Academy was built on a simple belief, that everyone\s+deserves a science-backed protocol for a longer, healthier life\.)\s*(We assembled.*?)</p>',
                   lambda m: '<p class="about-statement">' + re.sub(r'\s+', ' ', m.group(1)) + '</p>\n        <p class="about-lead about-lead--gal">' + re.sub(r'\s+', ' ', m.group(2)).strip() + '</p>', s, count=1, flags=re.S)
    assert n == 1, 'about statement'
    # Final banner: the November-only line is out
    s = opt(s, '<p class="final-cta-sub">Online sign-ups in November only. Your personal longevity protocol starts here.</p>', '<p class="final-cta-sub">Your personal longevity protocol starts here.</p>')
    return s


def no_orphans(s):
    """No one-word last lines: join the last two words of short text blocks with a non-breaking space (outside scripts and styles)."""
    parts = re.split(r'(<script\b.*?</script>|<style\b.*?</style>)', s, flags=re.S)
    pat = re.compile(r'(\w[\w,\'\u2019.&;$%+-]*) ([\w\'\u2019$%+.,!?&;-]{1,14}?)(</(?:p|h1|h2|h3|h4|li|b|em|strong|span|a|div|figcaption)>)')
    for i in range(0, len(parts), 2):
        parts[i] = pat.sub(lambda m: m.group(1) + '&nbsp;' + m.group(2) + m.group(3), parts[i])
    return ''.join(parts)


def common(s):
    s = re.sub(r'<div id="novStrip".*?</div>\s*', '', s, count=1, flags=re.S)  # promo strip out
    s = re.sub(r'<html\b([^>]*)>', lambda m: '<html' + (m.group(1).replace('class="', 'class="mf ') if 'class="' in m.group(1) else m.group(1) + ' class="mf"') + '>', s, count=1)
    s, stray = assemble(s)
    a, b = bounds(s, '<section class="hero" id="hero">')
    hero = s[a:b]
    hero = must(hero, '<img src="assets/hero-cgm.jpg" alt="Continuous glucose monitor and personalized health protocol" class="hero-image" loading="eager" fetchpriority="high">',
                '<video class="hero-image mf-cells" src="https://longevitylifeacademy.pages.dev/assets/cells-light.mp4" poster="https://longevitylifeacademy.pages.dev/assets/cells-poster.jpg" autoplay muted loop playsinline preload="auto" aria-hidden="true"></video>')
    film = re.search(r'<figure class="lla-film">.*?</figure>', DEV_HERO, flags=re.S).group(0)
    hero = re.sub(r'<h1 class="hero-title">.*?</h1>', '<h1 class="hero-title">Your personal <span class="life-blue">longevity protocol,</span><br>built in 18 weeks.</h1>', hero, count=1, flags=re.S)
    hero = re.sub(r'<p class="hero-sub">.*?</p>', '<p class="hero-sub">Live small-group classes with certified longevity instructors. A free Abbott Lingo glucose sensor shipped to your home. You finish with a written protocol built on your own numbers.</p>', hero, count=1, flags=re.S)
    # Trustpilot (Omri, 5 Nov late): next to the CTA, not on top. Standard Trustpilot mini layout: logo, green star boxes, score and review count.
    star = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="#fff" d="M12 3.6l2.3 6.1h6.4l-5.1 3.9 1.9 6.3L12 16l-5.5 3.9 1.9-6.3-5.1-3.9h6.4z"/></svg>'
    tp = ('<div class="mf-tp" role="img" aria-label="Rated 4.6 out of 5 on Trustpilot, based on 600+ reviews">'
          '<span class="mf-tp-logo"><svg viewBox="0 0 24 24" aria-hidden="true"><path fill="#00B67A" d="M12 1.5l2.9 8.2H24l-7.1 5.2 2.7 8.6L12 18.3l-7.6 5.2 2.7-8.6L0 9.7h9.1z"/></svg><b>Trustpilot</b></span>'
          '<span class="mf-tp-stars">' + ''.join('<i>' + star + '</i>' for _ in range(4)) + '<i class="mf-tp-half">' + star + '</i></span>'
          '<span class="mf-tp-score"><b>4.6</b><em>|</em>600+ reviews</span></div>')
    hero = re.sub(r'\s*<!--[^>]*trust pill[^>]*-->', '', hero, count=1)
    hero = re.sub(r'<div class="trustpilot trustpilot--top">.*?600\+ verified reviews</span>\s*</div>\s*', '', hero, count=1, flags=re.S)
    hero = re.sub(r'(<a href="#syllabus" class="btn-ghost">.*?</a>)', lambda m: m.group(1) + '\n      ' + tp, hero, count=1, flags=re.S)
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
    s = opt(s, '<span class="tag">$99 value, included</span>', '<span class="tag">Included</span>')
    s = must(s, '<span style="color:#006EFF;">Doesn\'t Have Time to Teach You.</span>', '<span class="mf-lb">Doesn\'t Have Time to Teach You.</span>')
    s = must(s, 'In November, tuition is $79 for month 1 with code JULIE249 or MASTERCLASS-VIP, then four monthly payments of $169 '
                '($755 total; regular plan $169 x 5). Tuition includes',
             "November offer: $79 first month, then $169 a month for four months. Course, Lingo CGM, $100 credits back towards your next course and "
             "Julie's VIP Masterclass included. Tuition includes")
    s = opt(s, 'Applications are open for the next class. Your personal longevity protocol starts here.',
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

    # Syllabus "50-Minute Flow": the .com arrows between steps become full stops (not commas), each step starts with a capital
    def _flow(m):
        steps = [x.strip() for x in re.split(r'\s*(?:→|&rarr;)\s*', m.group(2)) if x.strip()]
        steps = [x[0].upper() + x[1:] for x in steps]
        # Omri 6 Nov: "not run on texts". Each step of the flow is its own numbered line.
        return '<ol class="curriculum-flow mf-steps">' + ''.join('<li>' + x + '</li>' for x in steps) + '</ol>'
    s = re.sub(r'(<p class="curriculum-flow">)(.*?)(</p>)', _flow, s, flags=re.S)

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
    s = must(s, 'NAD precursors, Vitamin D, omega-3s, creatine, senolytics, the short list of supplements with real human data, and the long list of marketing dressed up as science.',
             'The short list of supplements with real human data, and the long list of marketing dressed up as science.')
    s = must(s, 'Zone 2 cardio for mitochondrial health, VO2 max as the strongest predictor of all-cause mortality, CGM-driven metabolic tracking, ApoB management, and the sleep architecture that drives recovery.',
             'Zone 2 cardio, VO2 max, CGM-driven metabolic tracking, ApoB management, and the sleep that drives recovery.')
    s = must(s, 'Skin as a real-time biomarker of systemic aging, collagen turnover, oxidative stress, glycation, UV damage, and the topical and oral interventions with actual clinical evidence behind them.',
             'Skin as a real-time biomarker of aging, and the treatments with actual clinical evidence behind them.')
    # Round 24: handover and reviewer copy fixes (no dashes in ranges, no hover on phones, no exclamation marks, one action word, typos)
    s = re.sub(r'Sessions (\d+)-(\d+)', r'Sessions \1 to \2', s)
    s = must(s, ' Hover to explore each domain.</p>', '</p>')
    s = must(s, '<h3 class="form-thankyou-headline">Thank You!</h3>', '<h3 class="form-thankyou-headline">Thank you.</h3>')
    s = must(s, '<li><a href="#lead-gen">Apply</a></li>', '<li><a href="#lead-gen">Enroll</a></li>')
    # About, eTeacher paragraph: two unimportant words out for fewer lines (Omri, 5 Nov late)
    s, n1 = re.subn(r'with a dynamic,\s+personalized', 'with a personalized', s, count=1)
    s, n2 = re.subn(r'Our proven,\s+teacher-led', 'Our teacher-led', s, count=1)
    assert n1 == 1 and n2 == 1, 'eTeacher paragraph trim failed'
    s = must(s, 'our Continuous Glucose Monitor (CGM) is included with enrollment', 'Our continuous glucose monitor (CGM) is included with enrollment')
    s = s.replace('Trustpilot · 5 stars · Sept 2025', 'Trustpilot · 5 stars · September 2025')
    s = must(s, 'energy, and habits, get an estimate of how', 'energy, and habits, and get an estimate of how')
    s = must(s, '>Privacy</a> · <a href="support/"', '>Privacy</a>\n        <a href="support/"')
    # Round 25: top-folds and desktop review copy fixes (Omri: shorten texts if needed; .com wording trimmed)
    for a, b in [
        ('Incorporate a daily routine that transforms your kitchen into a medicine cabinet by adopting plant-forward, nutrient-dense food patterns that combat inflammation and promote cellular rejuvenation.',
         'Transform your kitchen into a medicine cabinet with plant-forward, nutrient-dense food patterns that combat inflammation.'),
        ('Actionable, science-backed protocols to optimize your sleep architecture and activate cellular repair, reduce inflammation, and reverse biological aging. Sleep is the most underutilized longevity lever, regulating cortisol rhythm, HGH secretion, glymphatic clearance, and metabolic repair. Your protocol starts here.',
         'Science-backed protocols to optimize your sleep architecture and activate cellular repair. Sleep is the most underutilized longevity lever.'),
        ('Transform your approach to aging by building a resilient body, focusing on functional strength, Zone 2 endurance, and stability to maximize both your lifespan and healthspan.',
         'Build a resilient body with functional strength, Zone 2 endurance, and stability to maximize your healthspan.'),
        ('Targeted compounds, NAD+ precursors (NMN/NR), omega-3s, D3 + K2, magnesium, rapamycin, metformin, berberine, deployed against specific biomarker gaps, not stacked by trend. CGM, HRV, and sleep data turn every protocol into a feedback loop.',
         'Targeted compounds deployed against specific biomarker gaps, not stacked by trend. Your data turns every protocol into a feedback loop.'),
        ('Chronic stress drives cortisol dysregulation, HPA-axis dysfunction, accelerated telomere attrition, and rising allostatic load, measurable upstream contributors to cardiovascular and metabolic disease. The protocol uses autonomic nervous system regulation, structured breathwork, deliberate cold exposure, vagal tone training, and social connection as a validated mortality predictor, to keep biology resilient, not relaxed.',
         'Structured breathwork, deliberate cold exposure, vagal tone training, and social connection keep your biology resilient, not just relaxed.'),
        ('Generic health advice ends here: your protocol is built from your own bloodwork, lipid sub-particles, ApoB, fasting insulin, inflammatory markers, body composition, and continuous wearable data. This is Medicine 3.0 in practice, a proactive, individualized plan that iterates against your biomarkers and risk profile, so every intervention is measured, owned, and adjusted to your biology.',
         'Generic health advice ends here. Your protocol is built from your own bloodwork, biomarkers, and wearable data.'),
        ('<h3>continuous glucose monitor: Seeing the Invisible</h3>', '<h3>Continuous Glucose Monitor: Seeing the Invisible</h3>'),
        ('<p class="curriculum-flow">continuous glucose monitor applied live', '<p class="curriculum-flow">Continuous glucose monitor applied live'),
        ('<p class="curriculum-flow">continuous glucose monitor data review', '<p class="curriculum-flow">Continuous glucose monitor data review'),
        ('<span class="phase-block-name">Data &amp; Discovery</span>', '<span class="phase-block-name">Data and Discovery</span>'),
        ('<span class="phase-block-name">Integration &amp; Blueprint</span>', '<span class="phase-block-name">Integration and Blueprint</span>'),
        ('Baseline Self-Assessment', 'Baseline Self&#8209;Assessment'), ('the Gut-Brain-Glucose Axis', 'the Gut&#8209;Brain&#8209;Glucose Axis'), ('Intent-setting close', 'Intent&#8209;setting close'),
        ('certified longevity instructors. A free Abbott Lingo', 'certified longevity instructors. A&nbsp;free Abbott Lingo'),
        ('A live session with the 2nd slowest-aging woman on earth.', 'A live session with the 2nd slowest-aging woman on Earth.'),
        ('<div class="hex-center-sub">12 sessions</div>', '<div class="hex-center-sub">18 live classes</div>'),
        ('Rejuvenation Olympics + A leading voice', 'Rejuvenation Olympics. A leading voice'),
        ('Enroll Online Now &middot; $79 month 1/mo', 'Enroll Online Now &middot; $79 first month'),
        ('<h2 class="how-v2-title">How It Works</h2>', '<h2 class="how-v2-title">How It <em class="mf-acc">Works</em></h2>'),
    ]:
        if a in s:
            s = s.replace(a, b)
        else:
            print('note: not found:', a[:60])
    s = s.replace(' \\u2014 ', ', ')
    s = re.sub(r'(<a [^>]*class="section-cta-btn[^"]*"[^>]*>)Enroll now', r'\1Enroll Now', s)
    # Round 26 (Omri: no long cards on phones): review quotes trimmed from the end, unchanged words
    for a, b in [
        ('So happy finding eTeacher Group. They are genuinely concerned that you learn what you want to learn. They listen to what you want to learn and why, and then give thoughtful recommendations. Excellent classes and teachers.',
         'So happy finding eTeacher Group. They are genuinely concerned that you learn what you want to learn.'),
        ("Our teacher is patient and kind. She does great. Even when I can't attend a session, the recording helps me catch up, and the materials mean I can learn at a time that's convenient.",
         "Our teacher is patient and kind. She does great. Even when I can't attend a session, the recording helps me catch up."),
        ('At first I was finding logistics difficult, but I got a phone call from a staff member checking in on me and she opened up a clear path forward. I really appreciate that personal touch, staff who stay with students to keep their learning moving.',
         'At first I was finding logistics difficult, but I got a phone call from a staff member checking in on me and she opened up a clear path forward.'),
    ]:
        if a in s: s = s.replace(a, b)
        else: print('note: review not found:', a[:50])
    s = must(s, '<h2 class="section-title">Learn to Master<br><span class="mf-acc">Six Pillars of a Longer, Better Life.</span></h2>', '<h2 class="section-title">Learn to Master<br class="mf-mbr"> <span class="mf-acc">Six Pillars</span><br>for a Longer, Better Life.</h2>')
    s = r39(s)
    s = no_orphans(s)
    s = re.sub(r'(<span class="phase-block-name">[^<]*?)&nbsp;([^<]*</span>)', r'\1 \2', s)  # phase names may wrap freely
    css = open(os.path.join(HERE, 'meta_final.css'), encoding='utf-8').read().replace('/*%%HERO_CSS%%*/', '').replace('/*%%NEW_FOLDS%%*/', open(os.path.join(HERE, 'meta_final_newfolds.css'), encoding='utf-8').read()).replace('/*%%JULIE_CSS%%*/', open(os.path.join(HERE, 'masterclass_julie.css'), encoding='utf-8').read()).replace('/*%%BRAND%%*/', open(os.path.join(HERE, 'meta_final_fix.css'), encoding='utf-8').read() + '\n' + open(os.path.join(HERE, 'meta_final_pricing_big.css'), encoding='utf-8').read() + '\n' + open(os.path.join(HERE, 'meta_final_r39.css'), encoding='utf-8').read().replace('#syllabus', '#mf-retired-syllabus') + '\n' + open(os.path.join(HERE, 'meta_final_syllabus_com.css'), encoding='utf-8').read())
    css += '\n' + open(os.path.join(HERE, 'meta_final_r57.css'), encoding='utf-8').read()
    css += '\n' + open(os.path.join(HERE, 'meta_final_r60.css'), encoding='utf-8').read()
    css = widen_palette(css)
    s = s.replace('</head>', '<style id="meta-final">\n' + css + '\n</style>\n</head>', 1)
    s = no_royal_blue(s)
    # Omri 6 Nov (real Android phone at about 320px wide: text outside buttons, broken folds): phones narrower than 390px
    # get the checked 390px layout scaled to fit their screen, so nothing spills out of a box.
    s = must(s, '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
             '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n' + FIT_VIEWPORT_JS)
    js = open(os.path.join(HERE, 'meta_final.js'), encoding='utf-8').read()
    s = s.replace('</body>', AUTOPLAY_JS + '\n<script>\n' + js + '\n</script>\n</body>', 1)
    return s



def widen_palette(css):
    """Omri 6 Nov: card colours too similar. Five clearly different brand steps for every card group:
    clean white, bright sky, steel, navy, black-navy (with its light-blue neon edge)."""
    for a, b in [('#E4F3FF 0%,#BBDEFF 100%', '#FFFFFF 0%,#E2EFFF 100%'),
                 ('#AEDAFF 0%,#7BBEF6 100%', '#9ED8FF 0%,#58A8E8 100%'),
                 ('#1A3A75 0%,#0C2150 100%', '#2A4E8A 0%,#122A5A 100%'),
                 ('#0C1733 0%,#040A1B 100%', '#070C1A 0%,#000207 100%'),
                 ('#4C84CA 0%,#2C61A4 100%', '#5A86BE 0%,#2F5487 100%')]:
        css = css.replace(a, b)
    return css

FIT_VIEWPORT_JS = """<script>(function(){var m=document.querySelector('meta[name="viewport"]');if(!m)return;var D='width=device-width, initial-scale=1.0',cur=D;function fit(){var a=screen.width,b=screen.height,land=window.matchMedia&&window.matchMedia('(orientation: landscape)').matches,w=land?Math.max(a,b):Math.min(a,b),want=(w&&w<390)?'width=390':D;if(want!==cur){m.setAttribute('content',want);cur=want;}}fit();window.addEventListener('orientationchange',function(){setTimeout(fit,250);});})();</script>"""


def _royal_fix(r, g, b):
    """Omri: no royal blue. Saturated mid blues become brand steel (darker) or light blue (lighter)."""
    import colorsys
    h, l, sat = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
    hd = h * 360
    if not (205 <= hd <= 235 and sat >= .55 and .32 <= l <= .62):
        return None
    if l >= .55:
        sat, l = min(sat, .75), max(l, .74)
    else:
        sat, l = min(sat, .42), l * .82
    rr, gg, bb = colorsys.hls_to_rgb(h, l, sat)
    return round(rr * 255), round(gg * 255), round(bb * 255)


def no_royal_blue(s):
    def hexsub(m):
        hx = m.group(1)
        if len(hx) == 3:
            hx = ''.join(c * 2 for c in hx)
        f = _royal_fix(int(hx[0:2], 16), int(hx[2:4], 16), int(hx[4:6], 16))
        return m.group(0) if f is None else '#%02X%02X%02X' % f

    def rgbsub(m):
        f = _royal_fix(float(m.group(2)), float(m.group(3)), float(m.group(4)))
        if f is None:
            return m.group(0)
        return '%s(%d,%d,%d%s)' % (m.group(1), f[0], f[1], f[2], m.group(5) or '')

    def fix(css):
        css = re.sub(r'#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b', hexsub, css)
        return re.sub(r'\b(rgba?)\(\s*([\d.]+)\s*,\s*([\d.]+)\s*,\s*([\d.]+)\s*(,\s*[\d.]+%?\s*)?\)', rgbsub, css)
    s = re.sub(r'(<style\b[^>]*>)(.*?)(</style>)', lambda m: m.group(1) + fix(m.group(2)) + m.group(3), s, flags=re.S)
    s = re.sub(r'(\sstyle=")([^"]*)(")', lambda m: m.group(1) + fix(m.group(2)) + m.group(3), s)
    s = re.sub(r'(\s(?:fill|stroke|stop-color)=")(#[0-9a-fA-F]{3,6})(")', lambda m: m.group(1) + fix(m.group(2)) + m.group(3), s)
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
    s = must(s, '<p class="pk-foot">', '<p class="pk-previewnote" hidden>Preview. On longevitylifeacademy.com this button opens eTeacher\'s checkout, unchanged.</p><p class="pk-foot">')

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

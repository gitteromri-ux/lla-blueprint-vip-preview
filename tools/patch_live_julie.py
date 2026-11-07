#!/usr/bin/env python3
"""Apply the glass VIP fold (round 69) to the LIVE .com index.html. Only two changes:
   1. section#julie is replaced (same copy, same animation markup and classes, new layout wrapper);
   2. one <link> to assets/lla-julie-vip-glass.css after lla-julie-vip-motion.css.
Usage: patch_live_julie.py <live index.html> <out>"""
import sys, re
src, out = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
i = s.find('<section class="mf-julie mf-julie-bonus" id="julie">')
if i < 0 or s.count('id="julie"') != 1: sys.exit('julie section not found exactly once')
j = s.find('</section>', i) + len('</section>')
old = s[i:j]
m = re.search(r'<div class="jb4-motion".*?<button class="jb4-motion-toggle"[^>]*>[^<]*</button>\s*</div>', old, flags=re.S)
if not m: sys.exit('motion block not found')
motion = m.group(0)
for need in ('The Longevity Masterclass', 'Exclusive VIP Access', 'Learn to age&nbsp;slower', 'Sat,&nbsp;Nov&nbsp;14', '12:00 PM ET', '90&nbsp;min with live&nbsp;Q&amp;A', 'data-checkout-open'):
    if need not in old: sys.exit('live copy changed, stop: ' + need)
arts = re.findall(r'<article class="jb4-animation">.*?</article>', motion, flags=re.S)
if len(arts) != 2: sys.exit('expected two animations')
photo = '<figure class="jv5-photo"><span class="jv5-halo" aria-hidden="true"></span><img src="assets/mf/julie-face.jpg" alt="Julie Gibson Clark" width="600" height="600" loading="lazy"><span class="jv5-rim" aria-hidden="true"></span></figure>'
stage = motion.replace(arts[0], arts[0] + '\n        ' + photo, 1).replace('<div class="jb4-motion"', '<div class="jb4-motion jv5-stage"', 1)
new = '''<section class="mf-julie mf-julie-bonus jv5-sec" id="julie">
  <div class="container">
    <article class="jv5">
      <span class="jv5-sheen" aria-hidden="true"></span>
      <header class="jv5-head">
        <p class="jv5-kick">Exclusive VIP Access ·&nbsp;<strong>Included</strong></p>
        <h2 class="jb4-title jv5-title"><span class="jb4-masterclass">The Longevity Masterclass</span> <em>Julie Gibson&nbsp;Clark</em></h2>
        <p class="jv5-msg"><b>Learn to age&nbsp;slower</b> from the 2nd slowest&#8209;aging woman on&nbsp;Earth</p>
      </header>
      ''' + stage + '''
      <div class="jv5-ticket">
        <p class="jv5-date"><span>Sat</span><b>Nov&nbsp;14</b></p>
        <p class="jv5-when"><b>12:00 PM ET</b><span>90&nbsp;min with live&nbsp;Q&amp;A</span></p>
        <a class="jv5-btn" href="#lead-gen" data-checkout-open>Join&nbsp;us<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14M13 5l7 7-7 7"/></svg></a>
      </div>
    </article>
  </div>
</section>'''
s = s[:i] + new + s[j:]
link = re.search(r'<link rel="stylesheet" href="assets/lla-julie-vip-motion\.css\?v=[^"]*">', s)
if not link: sys.exit('motion css link not found')
s = s[:link.end()] + '\n<link rel="stylesheet" href="assets/lla-julie-vip-glass.css?v=20261107-3">' + s[link.end():]
open(out, 'w', encoding='utf-8').write(s)
print('patched', out)

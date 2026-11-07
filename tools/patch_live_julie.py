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
for need in ('The Longevity Masterclass', 'Exclusive VIP Access', 'Learn to age&nbsp;slower', 'Sat,&nbsp;Nov&nbsp;14', '12:00 PM ET', '90&nbsp;min with live&nbsp;Q&amp;A', 'data-checkout-open'):
    if need not in old: sys.exit('live copy changed, stop: ' + need)
clips = dict((m.group(1), m.group(0)) for m in re.finditer(r'<div class="jb4-clip"[^>]*data-motion-src="([^"]+)"[^>]*>\s*<img[^>]*>\s*</div>', old))
pace = [v for k, v in clips.items() if 'ANIM_PACE' in k]; curve = [v for k, v in clips.items() if 'ANIM_CURVE' in k]
if len(pace) != 1 or len(curve) != 1: sys.exit('animation clips not found')
if '<button class="jb4-motion-toggle"' not in old: sys.exit('toggle not found')
VARIANT = ' jv13-black' if '--black' in sys.argv else ''
cal = '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3.5" y="5" width="17" height="15" rx="3"/><path d="M3.5 10h17M8 3v4M16 3v4"/></svg>'
chk = '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M8 12.5l2.6 2.6L16 9.8"/></svg>'
new = """<section class="mf-julie mf-julie-bonus jv13""" + VARIANT + """" id="julie">
  <div class="container">
    <div class="jv13-in">
      <header class="jv13-head">
        <p class="jv13-eyebrow">The Longevity Masterclass<i aria-hidden="true"></i><br class="jv13-br">Exclusive VIP Access, <b>included</b></p>
        <h2 class="jv13-h">Learn to <em>age slower</em> from the 2nd slowest&#8209;aging woman on&nbsp;Earth.</h2>
      </header>
      <figure class="jv13-portrait"><img src="assets/mf/julie-face.jpg" alt="Julie Gibson Clark" width="600" height="600" loading="lazy"><figcaption><b>Julie Gibson Clark</b><span>2nd slowest-aging woman on Earth</span></figcaption></figure>
      <div class="jv13-side">
        <div class="jb4-motion jv13-proof" role="group" aria-label="Julie&rsquo;s Masterclass animations">
          <div class="jv13-stat"><p class="jv13-num">33<small>%</small></p><p class="jv13-lbl">slower aging than the average&nbsp;human</p>""" + curve[0] + """</div>
          <div class="jv13-stat"><p class="jv13-num">6.7</p><p class="jv13-lbl">years of aging per&nbsp;decade</p>""" + pace[0] + """</div>
          <button class="jb4-motion-toggle" type="button" aria-pressed="false">Pause animations</button>
        </div>
        <p class="jv13-when">""" + cal + """<b>Sat, Nov&nbsp;14</b><span>12:00 PM ET</span><span>90&nbsp;min live with&nbsp;Q&amp;A</span></p>
        <div class="jv13-cta"><a class="jv13-btn" href="#lead-gen" data-checkout-open>Join&nbsp;us<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14M13 5l7 7-7 7"/></svg></a><p class="jv13-incl">""" + chk + """<span>Included in your enrollment</span></p></div>
      </div>
    </div>
  </div>
</section>"""
s = s[:i] + new + s[j:]
link = re.search(r'<link rel="stylesheet" href="assets/lla-julie-vip-motion\.css\?v=[^"]*">', s)
if not link: sys.exit('motion css link not found')
s = s[:link.end()] + '\n<link rel="stylesheet" href="assets/lla-julie-vip-glass.css?v=20261107-13">' + s[link.end():]
open(out, 'w', encoding='utf-8').write(s)
print('patched', out)

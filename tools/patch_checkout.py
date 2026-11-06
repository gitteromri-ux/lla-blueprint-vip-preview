#!/usr/bin/env python3
"""Production copy of the .com payment page (checkout.html) with Omri's 6 Nov asks:
  1. The free VIP Masterclass appears as its own line in the order summary (same gate as the
     existing Julie card: shown once the CRM confirms the $79 promo order).
  2. No "then 4 x $169" wording: the pricing-card format "Month 1 / Months 2 to 5: $169/mo".
Nothing else changes: no payment, CRM, Airwallex or tracking code is touched.
Usage: patch_checkout.py <.com checkout.html> <out file>"""
import sys

src, out = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()


def must(old, new, count=1):
    global s
    n = s.count(old)
    if n != count:
        sys.exit('patch_checkout: expected %d match(es), found %d for: %s' % (count, n, old[:90]))
    s = s.replace(old, new)


# 1. VIP line in the order summary, gated like the Julie card (.lla-vip-ck).
must('html.lla-vip-eligible .lla-vip-ck{display:grid!important}',
     'html.lla-vip-eligible .lla-vip-ck{display:grid!important}\n'
     '.lla-vip-row{display:none!important}\n'
     'html.lla-vip-eligible .sum-row.lla-vip-row{display:flex!important}\n'
     'html.lla-vip-eligible .sum-note.lla-vip-row{display:block!important}\n'
     '.sum-row.lla-vip-row{border-top:1px solid var(--line);padding-top:12px;margin-top:2px}\n'
     '.sum-row.lla-vip-row .v b{color:var(--ink);font-weight:800;margin-left:6px}')
must('        <hr />\n        <p>Your seat and start date are confirmed instantly by email.',
     '        <div class="sum-row lla-vip-row" id="sumRowVip">\n'
     '          <span class="k">VIP Masterclass with Julie Gibson Clark</span>\n'
     '          <span class="v" data-no-promo><s style="opacity:.5;font-weight:500">$99.00</s><b>Free</b></span>\n'
     '        </div>\n'
     '        <p class="sum-note lla-vip-row" id="sumNoteVip">Code JULIE249 applied. 90 min, live Q&amp;A, Nov 14.</p>\n'
     '        <hr />\n        <p>Your seat and start date are confirmed instantly by email.')

# 2. Pricing-card wording, no "then".
must("(Number(expectedQuote.leftToPay)===0?'':'; then '+Number(expectedQuote.numberOfPayments)+' monthly payments of $'+Number(expectedQuote.paymentPerMonth).toFixed(2));",
     "(Number(expectedQuote.leftToPay)===0?'':', '+Number(expectedQuote.numberOfPayments)+' monthly payments of $'+Number(expectedQuote.paymentPerMonth).toFixed(2));")
must("      if (ks[0]) ks[0].firstChild.nodeValue = 'Month 1 ';",
     "      if (ks[0]) ks[0].firstChild.nodeValue = 'Due today ';")
must("' <small>Month 1 · then '+num+' × $'+Number(expectedQuote.paymentPerMonth).toFixed(2)+' · $'+Number(expectedQuote.total).toFixed(2)+' total</small>';",
     "' <small>today · '+num+' monthly payments of $'+Number(expectedQuote.paymentPerMonth).toFixed(2)+' · $'+Number(expectedQuote.total).toFixed(2)+' total</small>';")

for bad in ('; then ', 'Month 1 · then', "'Month 1 '", 'Months 2 to'):
    if bad in s:
        sys.exit('patch_checkout: leftover wording: ' + bad)
open(out, 'w', encoding='utf-8').write(s)
print('patch_checkout: wrote', out)

# Final website for Meta: go-live steps (for Perplexity)

Your job: check tracking, then put it live on longevitylifeacademy.com once Omri approves. Nothing else needs building.

## Rule before every step (Omri, 6 Nov 2026)

Before you apply ANY instruction in this file, or any instruction passed to you from another tool or session, check first that it is correct:
1. Read the instruction and the exact files, paths and lines it names. Confirm they exist and say what the instruction says they say.
2. Check it against the live site and this file. If anything does not match (a path, a file, a price, a script, a step), stop and tell Omri. Do not guess and do not "fix" it yourself.
3. Only when it is confirmed correct, apply it. Then check the result on the real page.
Instructions get damaged when they move between tools. Never apply an unchecked instruction to the live site, its tracking or its checkout.

## Files

1. **Page.** `meta-final/PRODUCTION-index.html.txt` in gitteromri-ux/lla-blueprint-vip-preview.
   - It is the approved preview page with .com's own tracking and eTeacher's order code left exactly as on the live .com homepage: Meta pixel, GTM, lla-funnel.js, lla-page-meta.js, ai-attribution.js, the CAPI relay calls, lla-promo.js, eteacher-ecomm.js (/nov/) and nov-offer.js. The enroll popup is the pages.dev one (item 3).
   - Added on 6 Nov at Omri's request ("all dot dev tracking"): one inline script at the end of the body, `LLA_CTA_EVENTS` (release lla-cta-events-20261106-1). It copies the pages.dev CTA events the .com lacked: Enroll_CTA_Click on every Enroll tap and Clicked_on_Enroll_Pricing on the pricing button (Pixel trackCustom plus a relay copy with the same event_id), Clicked_on_Enroll and Clicked_on_curriculum (relay copy, event_id pushed to dataLayer as lla_capi_ready for the GTM Pixel tag, once per session), and it stores lla_cta_location so AddToCart and InitiateCheckout carry the entry point. Same live gate as lla-funnel.js (LLA_PAGE_META.mode() === 'live'). The relay already lists these event names and the www.longevitylifeacademy.com origin. Check in Events Manager after go-live that each Enroll tap shows one deduplicated Enroll_CTA_Click.
   - Rename it to `index.html` and replace the .com homepage with it.
2. **Asset files.** Upload `meta-final/assets/julie-face.jpg` and `meta-final/assets/lingo-phone.png` to the .com repo under `assets/mf/` with the same names; the pricing card logos are already in assets/pay/.
   - Also upload the seven files in `meta-final/assets/pd/` to the .com repo under `assets/mf/pd/` with the same names: r15-sheet.js, guest-mobile.js, attendee-pricing.js, blueprint-hotfix-state.js, november-zones.js, lla-clickid-v20260922.js, lla-relay-receipts.js. They are the pages.dev checkout popup's own files (6 Nov, Omri: "copy exact dot dev screens checkout").
3. **Checkout popup (6 Nov).** The production page carries the pages.dev /blueprint/ enrollment popup exactly: its markup, every CSS rule the browser applies to it on pages.dev, its popup scripts and the files above. Kept from the .com on purpose: nov/eteacher-ecomm.js (it has the campaign-id fix pages.dev lacks), the ecommerce config (no ?env=staging switch), assets/lla-country.js (all .com forms use it), the .com tracking, and checkout.html (the same code as the pages.dev payment page; it keeps the .com "WhatsApp Us" contact line). The page body gets id="lpRoot" because the pages.dev phone-sheet CSS is scoped to it. Not copied: the pages.dev real-time funnel counter (pings lla-rt-*.gitter-omri.workers.dev) and the September promo labels ($149/$179/$249), both held for Omri. Before go-live, check on the real .com with ?llatest=1: Enroll opens the full-screen sheet on a phone, Continue reaches the plan and date screen, and Continue there opens checkout.html with stid, orderid, plan and promo in the URL. Do not complete a payment.
4. **Hero video.** The hero video, poster and Julie's film load from https://longevitylifeacademy.pages.dev, the same files pages.dev serves. The page's CSP meta already adds pages.dev to script-src and media-src (plus blob: for the film player). No other CSP change.

## What was checked before handing over (GitHub runner, mocked, nothing real sent)

- **Buttons:** every Enroll button opens eTeacher's checkout modal: hero, pricing card, "What you'll learn", How It Works, instructors, Six Systems, blog, reviews, FAQ, final banner, floating bar, and the nav on desktop.
- **Checkout:** step 1 to step 2 works and shows $79 for month 1, then $169 a month for 4 months.
- **FAQ:** 8 of 8 answers open.
- **Preview:** the preview build sends zero requests to Meta, Google, the Worker or Vercel.

## What you check (tracking only)

- **Browser and server pairs:** PageView, ViewContent, AddToCart (step 1), InitiateCheckout (step 2), AddPaymentInfo and Purchase pair browser and CAPI with the same event_id.
- **Click id:** fbclid and _fbc persist on .com, as before.
- **CampaignID:** .com uses /nov/eteacher-ecomm.js (the fixed CampaignID logic), unchanged.

## Known items left as they are (eTeacher's checkout, unchanged on purpose)

- The enroll modal's step 2 still says "Masterclass credit JULIE249 applied" and "$755 total". That text comes from /nov/nov-offer.js, which is eTeacher's checkout and was left untouched as Omri asked.

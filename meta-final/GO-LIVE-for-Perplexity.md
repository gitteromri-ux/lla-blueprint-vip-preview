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
   - Also upload these six files from `meta-final/assets/pd/` to the .com repo under `assets/mf/pd/` with the same names: r15-sheet.js, guest-mobile.js, attendee-pricing.js, november-zones.js, lla-clickid-v20260922.js, lla-relay-receipts.js. They are the pages.dev checkout popup's own files (6 Nov, Omri: "copy exact dot dev screens checkout").
   - blueprint-hotfix-state.js was removed from the folder and the page no longer loads it. Do not add it. Omri, 6 Nov: "You don't need the state". The popup has no State field. The CRM lead keeps the .com behaviour as it is today.
   - attendee-pricing.js is the pages.dev file with one change (Omri, 6 Nov: no "then $169" wording, use the pricing-card format). Step 2's tuition box now reads "Due today ~~$169~~ $79", then a separate line "Bonus VIP Masterclass Free" (Omri, 6 Nov: no "Month 1" / "Months 2 to 5" wording). JULIE249 is pre-applied in the promo field. The refund line under Continue wraps on phones instead of cutting off (tools/pagesdev_checkout/r67.css).
3. **Checkout popup (6 Nov).** The production page carries the pages.dev /blueprint/ enrollment popup exactly: its markup, every CSS rule the browser applies to it on pages.dev, its popup scripts and the files above. Kept from the .com on purpose: nov/eteacher-ecomm.js (it has the campaign-id fix pages.dev lacks), the ecommerce config (no ?env=staging switch), assets/lla-country.js (all .com forms use it), and the .com tracking. The payment page is the .com checkout.html with two small changes (item 4); it keeps the .com "WhatsApp Us" contact line. The page body gets id="lpRoot" because the pages.dev phone-sheet CSS is scoped to it. Not copied: the pages.dev real-time funnel counter (pings lla-rt-*.gitter-omri.workers.dev) and the September promo labels ($149/$179/$249), both held for Omri. Before go-live, check on the real .com with ?llatest=1: Enroll opens the full-screen sheet on a phone, Continue reaches the plan and date screen, and Continue there opens checkout.html with stid, orderid, plan and promo in the URL. Do not complete a payment.
4. **Payment page (6 Nov).** Replace the .com `checkout.html` with `meta-final/PRODUCTION-checkout.html.txt` (rename it to `checkout.html`). It is the current .com checkout.html (c320050) plus the output of `tools/patch_checkout.py`. The only changes:
   - The order summary gets a line "VIP Masterclass with Julie Gibson Clark, ~~$99.00~~ Free" and a note "Code JULIE249 applied. 90 min, live Q&A, Nov 14.". It uses the same gate as the existing Julie card: it shows once the CRM confirms the $79 promo order (class `lla-vip-eligible`).
   - The "then" wording is gone. The plan box reads "$79.00 today · 4 monthly payments of $169.00 · $755.00 total" and the tuition band reads "$755.00 total, 4 monthly payments of $169.00". In the summary, the first row is labelled "Due today" (was "Month 1"); the .com row "Monthly tuition fee 4 x $169.00" is unchanged.
   - No payment, Airwallex, CRM or tracking code changed. Check it with `diff` against the live checkout.html before you apply it. If the live file changed since c320050, stop and tell Omri.
5. **Hero video.** The hero video, poster and Julie's film load from https://longevitylifeacademy.pages.dev, the same files pages.dev serves. The page's CSP meta already adds pages.dev to script-src and media-src (plus blob: for the film player). No other CSP change.

## What was checked before handing over (GitHub runner, mocked, nothing real sent)

- **Buttons:** every Enroll button opens eTeacher's checkout modal: hero, pricing card, "What you'll learn", How It Works, instructors, Six Systems, blog, reviews, FAQ, final banner, floating bar, and the nav on desktop.
- **Checkout:** step 1 to step 2 to checkout.html works on iPhone, Android 320px and desktop: Due today ~~$169~~ $79, Bonus VIP Masterclass Free, JULIE249 pre-applied; the payment page shows the VIP line in the order summary.
- **FAQ:** 8 of 8 answers open.
- **Preview:** the preview build sends zero requests to Meta, Google, the Worker or Vercel.

## What you check (tracking only)

- **Browser and server pairs:** PageView, ViewContent, AddToCart (step 1), InitiateCheckout (step 2), AddPaymentInfo and Purchase pair browser and CAPI with the same event_id.
- **Click id:** fbclid and _fbc persist on .com, as before.
- **CampaignID:** .com uses /nov/eteacher-ecomm.js (the fixed CampaignID logic), unchanged.

## Known items

- **VIP Masterclass, second $0 enrollment in the CRM: DONE (6 Nov).** The inline script `LLA_VIP_ENROLL` (release lla-vip-enroll-20261106-1, source tools/lla_vip_enroll.js) is at the end of the page body. After the Blueprint order is created (course 258 / 1774), it sends one more order to the same endpoint for the same buyer, with ProductID 26: MainAbroadCourseId 283 / AbroadCourseId 1823, class 170142 / semester 2394 (Nov 14, the IDs the live julie-masterclass page uses), FirstPayment 0, LeftToPay 0, NumberOfPayments 0, and DynamicParameters plan=vipmasterclass&bporder=<Blueprint order>&message=VIP Masterclass with Julie Gibson Clark Sat Nov 14 12PM ET included free with Blueprint order <id>. It only runs with the JULIE249 offer active, once per order, and never changes the Blueprint order, the payment page or tracking. After go-live, check the first real enrollment in the CRM: one student with two orders, Blueprint and the Nov 14 masterclass at $0. If the CRM rejects the $0 order, the Blueprint enrollment is unaffected; tell Omri.
- The payment page still shows the total ("$755.00 total", "Total tuition: $755.00 USD") as the payment disclosure. The popup no longer shows $755.
- On desktop, the pages.dev popup script sends a browser-only Pixel custom event `LLA_Popup_ContinueVisible` / `LLA_Popup_ContinueHidden` (popup sizing check, copied from pages.dev). It has no server copy and does not affect the funnel events.

## Tracking audit (6 Nov, offline, every outside host mocked, nothing sent)

PASS for every row: PageView, ViewContent, Enroll_CTA_Click (hero, pricing, floater, Julie card), Clicked_on_Enroll_Pricing, AddToCart after screen 1, InitiateCheckout after screen 2, checkout PageView and AddPaymentInfo all send browser + server with the same event_id, each exactly once. Clicked_on_Enroll goes to the server once per session with lla_capi_ready. Purchase was checked in the code: event_id = order id on both sides. The _fbc cookie built from fbclid is in every relay payload. ?llatest=1 and tester emails are silent. No JS errors.

## 6 Nov evening changes (all in this commit)
- Homepage `<title>` back to the brand title "Longevity Life Academy, Design the Life Ahead of You" (what Google shows).
- Pricing card: "18 live sessions / 18-week course" beside the price (desktop), one line "then $169/month for 4 months", one type system for the card. FAQ price sentence without "then".
- checkout.html: Airwallex Drop-in in the site blue (`appearance.variables.colorBrand` #006EFF, a documented Airwallex option); the "This is a live payment" status line removed.
- VIP CRM order carries its own note (message) instead of repeating the Blueprint text.

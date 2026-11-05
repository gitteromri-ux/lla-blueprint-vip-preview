# Final website for Meta: go-live steps (for Perplexity)

Your job: check tracking, then put it live on longevitylifeacademy.com once Omri approves. Nothing else needs building.

## Files

1. **Page.** `meta-final/PRODUCTION-index.html.txt` in gitteromri-ux/lla-blueprint-vip-preview.
   - It is the approved preview page with .com's own tracking and eTeacher's checkout left exactly as on the live .com homepage: Meta pixel, GTM, lla-funnel.js, lla-page-meta.js, ai-attribution.js, the CAPI relay calls, lla-promo.js, eteacher-ecomm.js (/nov/), nov-offer.js and the enroll modal.
   - Rename it to `index.html` and replace the .com homepage with it.
2. **Asset files.** Upload `meta-final/assets/*` to the .com repo as `assets/mf/`:
   - `assets/mf/julie-seated.jpg`
   - `assets/mf/cgm-woman.jpg`
   - `assets/mf/anim/ANIM_PACE_1080.mp4`
   - `assets/mf/anim/ANIM_CURVE_1080.mp4`
   - `assets/mf/anim/PLAY_V6_LLA_RANK.mp4`
   - `assets/mf/anim/pace-poster.jpg`
   - `assets/mf/anim/curve-poster.jpg`
3. **Hero video.** The hero video, poster and Julie's film load from https://longevitylifeacademy.pages.dev, the same files pages.dev serves. The page's CSP meta already adds pages.dev to script-src and media-src (plus blob: for the film player). No other CSP change.

## What was checked before handing over (GitHub runner, mocked, nothing real sent)

- **Buttons:** every Enroll button opens eTeacher's checkout modal: hero, pricing card, Julie fold, "What you'll learn", final banner, floating bar, and the nav on desktop.
- **Checkout:** step 1 to step 2 works and shows $79 for month 1, then $169 a month for 4 months.
- **FAQ:** 8 of 8 answers open.
- **Preview:** the preview build sends zero requests to Meta, Google, the Worker or Vercel.

## What you check (tracking only)

- **Browser and server pairs:** PageView, ViewContent, AddToCart (step 1), InitiateCheckout (step 2), AddPaymentInfo and Purchase pair browser and CAPI with the same event_id.
- **Click id:** fbclid and _fbc persist on .com, as before.
- **CampaignID:** .com uses /nov/eteacher-ecomm.js (the fixed CampaignID logic), unchanged.

## Known items left as they are (eTeacher's checkout, unchanged on purpose)

- The enroll modal's step 2 still says "Masterclass credit JULIE249 applied" and "$755 total". That text comes from /nov/nov-offer.js, which is eTeacher's checkout and was left untouched as Omri asked.

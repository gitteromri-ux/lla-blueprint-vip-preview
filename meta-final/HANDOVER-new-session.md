# Handover: Final website for Meta (Longevity Life Academy), updated 6 Nov 2026 (round 56)

Read this file fully before touching anything. Omri has corrected the same things many times; the approved and rejected lists below are the source of truth. Latest wins.

## Where it stands
- **Current build:** branch `meta-final-wip` of gitteromri-ux/lla-blueprint-vip-preview, published to the preview link (main branch): https://gitteromri-ux.github.io/lla-blueprint-vip-preview/meta-final/
- **Not live on .com.** Production go-live waits for Omri's word, then the pull request for Perplexity (see `GO-LIVE-for-Perplexity.md`).

## How Omri wants you to work (his words, repeated many times)
1. Follow CLAUDE.md in this repo: numbered reading of his checklist, DONE / NOT DONE / ASSUMED report per item, mark any wording you wrote as UNAPPROVED, verify on the deployed URL, never write "nothing is pending".
2. Copy the longevitylifeacademy.com and Julie masterclass designs; do not invent designs or copy.
3. Look at the whole site on a phone, not fold by fold. "No code can have this type of design on mobile with huge, long cards with tiny text where you scroll a million years."
4. Short folds on phones. Card groups are sideways sliders on phones, not long stacks.
5. Large, readable text everywhere. Nothing small, nothing grey, nothing cramped, no plain white paragraphs.
6. Cards in each group in different brand colours, with depth, gradient and neon lighting on navy.
7. Symmetrical layouts, nothing wasting space, it must shine.

## Fold order (Omri's order, set 5 Nov)
1. Hero
2. Six pillars, headline "Learn to Master Six Pillars *for a Longer, Better Life.*"
3. What you'll learn (the 4-phase, 18-class syllabus)
4. CGM (Abbott Lingo)
5. Julie: VIP Masterclass bonus card
6. Pricing ("Enroll Now" opens eTeacher's ecomm checkout)
7. How It Works
8. About Longevity Life Academy
9. Client logos
10. Instructors
11. Six Systems
12. Blog (Deep Dives)

Kept after these, pending his keep or remove answer: reviews, what the course includes, Why This Course Is Different, bio-age quiz, FAQ, application form, final banner, footer.

## Approved decisions (latest wins)
- **Colours:** blue, navy/black, light blue, white only. No green, teal, violet, orange, gold or beige. Trustpilot and WhatsApp keep their own green.
- **Fonts:** Playfair Display for every header; the accent words in Playfair Display italic (light blue). No Instrument Serif, no Codec Pro.
- **Copy rules:** no em or en dashes, no all-caps words or caps labels, no pills or chips, no exclamation points, no AI-looking notes. "$100 credits back", never "cash back".
- **Hero:** .com hero layout, wordmark with "by eTeacher Group", headline "Your personal *longevity protocol,* built in 18 weeks.", calm Trustpilot line, Julie's film beside the copy on desktop and below it on phones. Logos are the .com files (nav lla-logo-no-tagline@2x.png, hero lla-wordmark-only-transparent@2x.png), unchanged.
- **CGM:** the real Abbott Lingo product shot (assets/cgm/lingo-1.jpg from .com) plus three large lines: "Minute-by-minute glucose, tracked for 2 weeks", "Lingo coaching, to build habits and adjust your nutrition", "Free, shipped to your home, full app access on iOS and Android". Fine print kept.
- **Julie fold:** a compact, symmetrical neon card about the VIP Masterclass, not about her.
  - Title "VIP Masterclass with *Julie Gibson Clark*", tag "Bonus, included".
  - Her photo (julie-face.jpg, the julie-gibson-clark.jpg image Omri sent) in a neon ring between two fact tiles: "No. 2 on Earth" and "8 months aging a year".
  - Line: "90-minute live masterclass, Q&A included, Nov 14."
  - About half a phone screen. Never her deck slides.
- **Pricing:** headline "One price. *Everything included.*" (Omri may pick one of: "Simple pricing. Everything included." / "Everything you need for 18 weeks." / "One plan for your whole protocol.").
  - Card: "55% off month one", "The Longevity *Blueprint*", $79 with $169 struck, "first month", "Then $169 a month for 4 months", "Enroll Now", "14-day try-out refund on the course.", secure checkout row with lock and card logos.
  - Tiles in this order, each a different brand gradient with neon: "18 live classes / 18 weeks, Small groups, top longevity experts"; "Your longevity protocol, Tailored to your biomarkers"; "Abbott Lingo CGM, Free, shipped to your home"; "$100 credits back, Towards your next course".
  - Then the wide neon bonus row: "Bonus VIP Masterclass. Learn to age slower from the 2nd slowest-aging human on earth. 90 min, live Q&A, Nov 14."
  - Never show $755, $845, $799, coupon codes or "you pay" lines.
- **Instructors:** one-row slider with large faces and room for text.
- **Six Systems:** each node its own brand gradient with neon; two columns on phones.
- **Blog:** videos on top of each card, text below, motion intact.
- **WhatsApp and floater:** kept, larger.

## Rejected (never reuse)
- My first custom "final-meta" design; the site-wide deck restyle.
- Julie: deck slides of any kind ("U cant show her dwcks"), the big photo, a whole-phone-long fold, the non-symmetrical strip with white text, the bento with animations on phones.
- CGM: flat white list on phones, the drawn phone app, the Lingo box image, the man-with-sensor photo, the cartoon chips.
- Pricing: hairline grid tiles, check-bullet lists, icon tiles ("robotic"), small fonts under the price.
- Compact circle teacher cards ("too small"); same-colour card groups; grey subheaders; long phone folds.
- Green, teal, violet, orange, gold, beige; Instrument Serif; Codec Pro.
- "Swipe for more" hints, pills, chips, caps eyebrows.

## Where things are
- **Build:** `python3 tools/build_meta_final.py /home/user/longevity-academy/Longevity-Academy.github.io/index.html nov14/index.html tools/pagesdev_hero.css meta-final` on `meta-final-wip`.
  - Writes `meta-final/index.html` (preview: tracking, CRM and checkout stripped, assets absolute) and `meta-final/PRODUCTION-index.html.txt` (same page with .com tracking and eTeacher checkout intact).
  - Pieces: `tools/meta_final_pricing.html`, `tools/meta_final_cgm.html`, `tools/meta_final_julie.html`.
  - CSS, in load order: `meta_final.css`, `meta_final_newfolds.css`, `masterclass_julie.css`, `meta_final_fix.css`, `meta_final_pricing_big.css` (loads last).
  - `mfasset:` in the pieces resolves to the github.io meta-final/assets URL in the preview and to `assets/mf/` in production.
- **Publishing the preview:** check out `meta-final/index.html` and `meta-final/assets` from `meta-final-wip` onto main, commit, push main. GitHub Pages redeploys in about a minute.
- **Local render:** rewrite `https://www.longevitylifeacademy.com/` to the local clone of Longevity-Academy.github.io and the github.io meta-final assets URL to the local `meta-final/assets/`, then screenshot with Playwright.
- **Device check:** gitteromri-ux/lla-julie-letter, branch `ccr-fb60a687-apnfd5`, workflow `meta-final-shots.yml` with `audit/meta-final.js`. Copy the build to `audit/fixtures/preview.html` and `production.html`, push, read `audit/out-mf/report.json`.
- **Deck slide files:** removed from the site; they remain in `meta-final-wip` history (commits c39609c, ea563bc). Purge only on Omri's word.

## Hard rules (still binding)
- No Meta, production tracking, CAPI, payment or CRM changes. Never echo the CAPI token. Never create CRM leads or AC objects. Never submit the checkout or enroll forms. Never use Vercel sandbox commands. Never spend paid credits without his word.
- No automatic mass checks that show up in the Worker.
- Never imply Julie teaches the course; she hosts the masterclass (Saturday, November 14, 12:00 PM ET).
- eTeacher's checkout is left unchanged: its step 2 still says "Masterclass credit JULIE249 applied" and "$755 total". Omri said leave it.

## Round 39 (6 Nov), from Omri's review board
- Built all 18 commented folds in one pass; Blog and FAQ approved and untouched; footer not reviewed.
- New: CSS in `tools/meta_final_r39.css` (loads last), copy changes in `r39()` and a no-one-word-last-line pass `no_orphans()` in `tools/build_meta_final.py`, the cut-out Lingo phone `meta-final/assets/lingo-phone.png`.
- Review board: https://gitteromri-ux.github.io/longevity-website-review-20261105/round39/

## Rounds 40 to 56 (6 Nov), latest wins
- **Approved as is (round 40 board):** Hero (later amended: the cells motion background is back, as on pages.dev), Blog, Reviews, FAQ, Final banner. Footer not reviewed.
- **Syllabus (round 56):** the longevitylifeacademy.com section itself (`<section class="curriculum" id="syllabus">`), with only colours and fonts optimized: "I just wanted their version in optimized coloring and fonts. That's it."
  - .com structure kept: centred phase tabs, a phase header box, one card per session that opens to Learning Goals, 50-Minute Flow and Between-Session Work.
  - Styles: `tools/meta_final_syllabus_com.css` (loads last). The old round 39 to 53 syllabus rules in `meta_final_r39.css` are switched off at build time (`#syllabus` renamed); the tap-panel JS is gone from `meta_final.js`.
  - The arrows in the 50-minute flow become full stops (the site-wide pass would make them commas).
  - Rejected for the syllabus: the pages.dev tabs restyle, stacked phases ("5 miles long"), cards of different sizes, the tap panel, the cramped desktop class list.
- **CGM (round 56):** Lingo version. Real phone cut-out `assets/lingo-phone.png` (from the .com lingo-1.jpg; 462x688 is the largest source there is), drawn 3D white sensor in front, two small dark cards with drawn graphs ("Live glucose", "After a meal").
  - Phone and sensor large, cards small ("phone and monitor larger, cards much smaller").
  - Rejected: glass or white cards, made-up looking graphs, blurry photo crops, the real sensor photo.
- **Julie (round 41):** her photo large on the left; two cards on the right: "Learn to age slower / from the 2nd slowest-aging woman on Earth" and "Sat, Nov 14 / 12:00 PM ET, 90 min with live Q&A" with "Join us" (`data-checkout-open`).
- **Device check:** `audit/live-check.js` now opens every syllabus phase and its first session on WebKit iPhone and desktop.

## Open items
1. Omri's review of the published preview, fold by fold, on his phone.
2. Keep or remove the unlisted folds (reviews, course includes, Why Different, quiz, FAQ, application form, final banner).
3. Pricing headline: keep "One price. Everything included." or pick one of the three offered.
4. Purge the deck slide files from git history, if he wants.
5. On his word only: the go-live pull request to Longevity-Academy/Longevity-Academy.github.io for Perplexity.

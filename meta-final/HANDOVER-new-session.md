# Handover: Final website for Meta (Longevity Life Academy), 5 Nov 2026

Omri wants this continued in a new session. Read this file fully before touching anything. He has corrected the same things many times; the list of what he approved and rejected below is the source of truth.

## The goal
- One final homepage for Meta ads, mobile first and perfect on desktop, in one link.
- Base: the longevitylifeacademy.com homepage.
- Approval comes from Omri on screenshots.
- After he approves, Perplexity only checks tracking and puts it live.

## How Omri wants you to work (his words, repeated many times)
1. **Base is longevitylifeacademy.com exactly as it is.** Do not change the design of any fold he did not ask about. Do not remove folds.
2. **Only apply what he writes.** No redesigns of your own, no new colours, no new graphics.
3. **No copy he did not give.** Use his wording, longevitylifeacademy.com wording, or the approved promo text only.
4. **Show before upload.** Before and after screenshots of each fold you touch, phone and desktop. Nothing goes live without his word.
5. **Don't stop to ask; work.** He gets angry when you send a message and stop. Ask only when you truly cannot proceed (the pricing content is one such case).
6. **No small text anywhere.** Never small white text on a dark background, never long white paragraphs. Reading text 19px or more, labels 15px or more.
7. **Folds must be short.** He said: "Your folds in general are too high. It's going to hurt mobile conversions." The CGM fold must be compact, not a tall fold.
8. **Read the repo rules.** See CLAUDE.md in gitteromri-ux/lla-blueprint-vip-preview (numbered checklist reading, DONE / NOT DONE / ASSUMED report, mark UNAPPROVED copy, verify on the deployed URL, never touch tracking, never submit forms).

## Approved decisions (latest wins)
- **Hero**
  - The longevitylifeacademy.com hero layout: wordmark with "by eTeacher Group", the two buttons.
  - Headline: "Your personal longevity protocol, built in 18 weeks."
  - Line under it: "Live small-group classes with certified longevity instructors. A free Abbott Lingo glucose sensor shipped to your home. You finish with a written protocol built on your own numbers."
  - Trustpilot as a clean line, **no pill** (logo, five green stars, 4.6 / 5, 600+ verified reviews).
  - Motion background: the pages.dev cells video. Julie's approved film beside the copy on desktop, below it on phones.
  - Contrast must be strong.
  - Rejected: "Slow down your pace of aging", the pages.dev italic sub, "It's Your Life. Live It Well." as the headline (he said the correct wording is the protocol-in-18-weeks line).
- **Promo strip:** removed. The offer lives in the .com floating bar (same design): "November offer", "55% off month one", "$79 Month 1".
- **Keep:** the WhatsApp button and the floater. He said both look good.
- **Six pillars:** the .com fold with its motion videos. Large on phones: each card about 72% of the screen, swipe sideways.
- **What you'll learn:** the pages.dev syllabus ("The 18 classes, week by week"), improved, a different colour per phase. No orange or green.
- **Pricing**
  - He hates every version so far: small text, weird wording, empty space, "10 million bullets".
  - His requirements: the monthly price with the big discount ($79 first month, $169 struck, 55% off month one), then $169 a month for 4 months, and everything included, in the **masterclass pricing card design, exactly** (Julie masterclass site, `#pricing` .pk-card).
  - Large text and no empty space. Never show $755, $845, $799, coupon codes or "you pay" lines.
  - **Ask him for the exact content before building it.**
- **Julie fold:** the masterclass "About Julie / VIP Masterclass included" fold with its animations ("Ten years pass. She ages six." bento with the pace and curve animations and the No.2 card). No cream background.
- **Course includes:** the .com fold, cards each a different colour (allowed colours only). The $99 tag becomes "Included".
- **CGM (Abbott Lingo)**
  - Compact, not tall, in the 3D, lighting and colour style of the deck reference slides **only** (see below).
  - Show the **real Abbott Lingo app metrics**:
    - the live glucose reading, updated every minute;
    - the day graph with spikes, and a Lingo Count number in the shaded area under each spike;
    - the daily Lingo Count total, which you aim to keep below a daily target;
    - trends over time, including the time of day with the biggest spikes;
    - food and activity logging, with Apple Health sync.
  - Sources: Abbott press release https://abbott.mediaroom.com/2024-09-05-Abbotts-Lingo-TM-Continuous-Glucose-Monitor-for-Health-and-Wellness-Now-Available-in-the-U-S , NBC/CNBC launch coverage https://www.nbcdfw.com/news/business/money-report/abbott-launches-its-first-over-the-counter-continuous-glucose-monitor-in-the-u-s/3637581/ , App Store listing https://apps.appfollow.io/ios/lingo-by-abbott/1670445335?country=us , Android launch https://www.nasdaq.com/press-release/abbotts-lingotm-now-androidtm-expanding-access-real-time-glucose-data-2025-12-08 .
  - No phone, unless shown as an app-launch moment with the real metrics popping out of it in 3D.
  - No man photo, no box, no pill or chip labels, nothing drawn that is not real.
  - Text: longevitylifeacademy.com CGM fold wording only.
- **Blog fold:** the .com "Deep Dives / What Your Doctor Doesn't Have Time to Teach You" (this is his "Longevity news"). The accent must be the hero's light blue (Instrument Serif italic, gradient #BFE2FF to #6FB6FF), not bright #006EFF.
- **About:** the .com "About Longevity Life Academy" with the eTeacher block (eTeacher's; leave it) and the client logos (.com logos only) in full colour and moving.
- **Enroll form:** the .com lead form moved up two folds from its .com position, made cleaner. eTeacher's checkout itself is left unchanged.
- **Reviews:** the .com reviews, larger text, a colour per card, more depth.
- **Other folds:** How It Works, Why This Course Is Different, Six Systems, bio-age quiz, FAQ and final banner all stay, in .com design. **No beige** anywhere.
- **Colours:** blue, navy/black, light blue, white, logo teal. Cards may differ in colour. **No orange, no green, no gold, no beige.** The deck colouring is for the CGM fold only.
- **Fonts:** .com fonts, with the italic accent as in the .com hero. He also said "our own Playfair italic"; ask once if unclear.
- **Logo and photos:** crisp nav logo (lla-logo-no-tagline@2x.png, no blur filter). Jordan Lattimore's photo cropped so his face sits higher.

## Rejected (never reuse)
- My first custom "final-meta" design.
- The site-wide deck restyle (navy glass everywhere).
- The photo of the man with the sensor.
- The cartoon phone app with orange and green chips.
- The Lingo box image.
- Pills and chips as decoration.
- The masterclass "Julie in the press" cards as Longevity news.
- "Swipe for more" hints.
- Removing folds.

## Deck reference (look, never edit)
- **Deck:** gitteromri-ux/lla-masterclass-syllabus, slide-canvas/v46 (the deck Julie presented at the masterclass event). Live: https://gitteromri-ux.github.io/lla-masterclass-syllabus/slide-canvas/v46/
- **Use only for the CGM fold's 3D and colour:**
  - n15-stress (cortisol curve, glass);
  - n11-sugar (spike, signal, scar glass chart);
  - n08-sleep (glowing timeline);
  - n09-food (four glass cards with coloured top bars);
  - n18-testing (three glass cards).

## Where things are
- **Build tool:** gitteromri-ux/lla-blueprint-vip-preview, branch `meta-final-wip`.
  - Run: `python3 tools/build_meta_final.py <Longevity-Academy.github.io/index.html> nov14/index.html tools/pagesdev_hero.css meta-final`.
  - It writes `meta-final/index.html` (preview: tracking, CRM and checkout stripped, .com assets absolute to https://www.longevitylifeacademy.com/) and `meta-final/PRODUCTION-index.html.txt` (same page with .com tracking and eTeacher checkout intact).
  - Pieces:
    - `tools/meta_final_pricing.html`, `tools/meta_final_cgm.html`, `tools/meta_final_julie.html`;
    - CSS: `tools/meta_final.css` plus `meta_final_newfolds.css` plus `meta_final_fix.css` (latest fixes);
    - JS: `tools/meta_final.js`.
  - The `meta_final_brand.css` and `meta_final_ref*.css` files are the rejected deck restyle and are no longer injected.
- **Preview link:** https://gitteromri-ux.github.io/lla-blueprint-vip-preview/meta-final/ (main branch). Main still holds an older, rejected version; the current build is only on `meta-final-wip`.
- **Local preview** (the sandbox cannot reach .com or pages.dev): rewrite `https://www.longevitylifeacademy.com/` to the local clone of Longevity-Academy.github.io and `https://longevitylifeacademy.pages.dev/assets/` to a local lla-course-checkout checkout, then screenshot with Playwright (Chromium is preinstalled).
- **Device check:** gitteromri-ux/lla-julie-letter, branch `ccr-fb60a687-apnfd5`, workflow `.github/workflows/meta-final-shots.yml` with `audit/meta-final.js`.
  - It injects `audit/fixtures/preview.html` and `production.html` with mocks, and adds an /etc/hosts block for Meta, Google, the Worker and Vercel.
  - Last result: every Enroll button opens eTeacher's checkout, the FAQ is 8 of 8, step 1 to step 2 works, zero tracking from the preview, no sideways scroll.
- **Omri's review board:** gitteromri-ux/longevity-website-review-20261105.
  - Fold screenshots of the three sites, plus `claude-selection.json` (my fold picks and comments, loaded by "Load Claude's selection").
  - His own comments there were never submitted, so ask him for them.
- **Go-live path (fastest):**
  - This account can push to Longevity-Academy/Longevity-Academy.github.io.
  - After Omri approves, open a pull request there: replace index.html with the production file and add `meta-final/assets/*` as `assets/mf/` (Julie animations, Julie photo).
  - The production file widens the CSP for the pages.dev hero video and film.
  - Perplexity checks tracking on the pull request, merges, and the site is live in about a minute.
  - See `meta-final/GO-LIVE-for-Perplexity.md`.

## Hard rules (owner handover, still binding)
- **Tracking and money systems:** no Meta changes, and no production tracking, CAPI, payment or CRM changes, without approval. Never submit the checkout or enroll forms. Never create CRM leads. Never use Vercel sandbox commands.
- **Copy:** no em dashes or en dashes, no all-caps words, no exclamation points, no emojis. Never imply Julie teaches the course (she hosts the masterclass). Masterclass: Saturday, November 14, 12:00 PM ET.
- **eTeacher's checkout:** its modal still says "Masterclass credit JULIE249 applied" and "$755 total". Omri said leave it.

## Open items right now
1. Pricing fold: get the exact content from Omri, then build it in the masterclass card design.
2. CGM fold: rebuild compact, with the real Lingo metrics above in the deck 3D style.
3. Make all folds shorter on phones; mobile conversions matter.
4. Omri's list of about 50 other mistakes: ask him to send it, then fix only those.
5. Re-run the device check on the final build. Publish to the preview link only on his word, then the pull request to .com for Perplexity.

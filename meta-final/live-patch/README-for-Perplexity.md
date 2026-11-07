# Julie VIP fold, glass design (round 69, Omri 7 Nov 2026)

Built on top of live main **6ddcb65**. Two changes only, presentation only (no tracking, CRM, checkout or network code):

1. `index.html`: replace with `meta-final/live-patch/index.html.txt`.
   - Diff vs live must show only (a) the `<section ... id="julie">` block and (b) one new line after the `lla-julie-vip-motion.css` link:
     `<link rel="stylesheet" href="assets/lla-julie-vip-glass.css?v=20261107-6">`
   - Same copy as live. Same animation markup and classes (`jb4-motion`, `jb4-motion-track`, `jb4-animation`, `jb4-clip`, `jb4-motion-toggle`), so `assets/lla-julie-vip-motion.js` keeps working. "Join us" keeps `data-checkout-open`.
2. Upload `meta-final/live-patch/lla-julie-vip-glass.css` to `assets/lla-julie-vip-glass.css`.

Before applying: confirm live main is still 6ddcb65. If index.html changed since, stop and tell Omri.
After deploy: on a phone and desktop, the VIP fold shows the glass card; both animations play; Join us opens the enrollment popup.

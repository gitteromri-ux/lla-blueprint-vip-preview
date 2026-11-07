# Julie VIP fold, cinematic v14 (Omri 7 Nov 2026)

Built on top of live main **6ddcb65**. Presentation only (no tracking, CRM, checkout or network code).

1. `index.html`: replace with `meta-final/live-patch/index.html.txt` (navy) OR `meta-final/live-patch/index-black.html.txt` (black); Omri picks one. They differ only by the class `jv14-black` on the section.
   - Diff vs live must show only (a) the `<section ... id="julie">` block and (b) one new line after the `lla-julie-vip-motion.css` link:
     `<link rel="stylesheet" href="assets/lla-julie-vip-glass.css?v=20261107-14">`
   - The two animation clips keep their markup (`jb4-clip` with `data-motion-src`, poster img) inside `.jb4-motion` with the `.jb4-motion-toggle` button, so `assets/lla-julie-vip-motion.js` keeps working. "Join us" keeps `data-checkout-open`.
2. Upload `meta-final/live-patch/lla-julie-vip-glass.css` to `assets/lla-julie-vip-glass.css`.
3. Upload `meta-final/live-patch/julie-film-still.jpg` to `assets/mf/julie-film-still.jpg` (a frame at 0:21 of Julie's approved film, 1280x720, 67 KB).

Before applying: confirm live main is still 6ddcb65. If index.html changed since, stop and tell Omri.
After deploy: on phone and desktop the fold shows Julie's film still, the two animations play, Join us opens the enrollment popup.

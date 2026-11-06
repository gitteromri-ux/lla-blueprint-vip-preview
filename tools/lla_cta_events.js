/* LLA CTA events for www.longevitylifeacademy.com, copied from the pages.dev funnel (Omri, 6 Nov 2026: "all dot dev tracking").
 * What pages.dev sends and the .com did not:
 *   Enroll_CTA_Click on every Enroll tap, plus Clicked_on_Enroll_Pricing for the pricing fold:
 *     browser Pixel trackCustom and a server copy with the same event_id (Meta dedupes the pair).
 *   Clicked_on_Enroll and Clicked_on_curriculum: server copy, with the event_id published to dataLayer
 *     (lla_capi_ready) first, so the GTM Pixel tag (same container GTM-PMRKXXJV as pages.dev) shares it.
 *   lla_cta_location is stored on the tap, so AddToCart / InitiateCheckout (lla-funnel.js) carry the entry point.
 * PageView, ViewContent, AddToCart, InitiateCheckout, AddPaymentInfo and Purchase are already sent by the .com
 * (lla-page-meta.js, lla-funnel.js, checkout.html) and are not repeated here.
 * Gate: LLA_PAGE_META.mode() === 'live' (qa=1, llatest=1, testers, staging and any other host or path stay silent).
 * No CRM, checkout, payment or AC code is touched by this file. */
(function (root) {
  'use strict';
  if (root.LLA_CTA_EVENTS) return;
  var PIXEL = '1440305917310328';
  var RELAY = 'https://lla-ac-events.vercel.app/api/meta/capi';
  var CONTENT_ID = 'lla-longevity-blueprint';
  var doc = root.document;
  function live() {
    try { return !!(root.LLA_PAGE_META && root.LLA_PAGE_META.mode() === 'live'); } catch (_) { return false; }
  }
  function staging() { return !!(root.LLA_ECOMM_CONFIG && root.LLA_ECOMM_CONFIG.env === 'staging'); }
  function ck(n) { var m = doc.cookie.match(new RegExp('(?:^|; )' + n + '=([^;]+)')); return m ? m[1] : ''; }
  function fbc() {
    var c = ck('_fbc'); if (c) return c;
    var q = (root.location.search.match(/[?&]fbclid=([^&#]+)/) || [])[1] || '';
    if (!/^[A-Za-z0-9_-]+$/.test(q)) q = '';
    var s = null; try { s = JSON.parse(root.localStorage.getItem('lla_fbc_v1') || 'null'); } catch (_) {}
    if (s && s.v && (Date.now() - (s.ts || 0)) < 7776000000 && (!q || s.raw === q)) return s.v;
    if (q) { var v = 'fb.1.' + Date.now() + '.' + q; try { root.localStorage.setItem('lla_fbc_v1', JSON.stringify({v: v, raw: q, ts: Date.now()})); } catch (_) {} return v; }
    return '';
  }
  function letters(s) { return String(s || '').toLowerCase().replace(/[^a-z]/g, ''); }
  function identity() {
    var i = null;
    try { i = JSON.parse(root.sessionStorage.getItem('lla_buyer_v1') || 'null'); } catch (_) {}
    if (!i || !i.email) { try { i = JSON.parse(root.localStorage.getItem('lla_identity_v1') || 'null'); } catch (_) {} }
    i = i || {};
    var xid = ''; try { xid = root.localStorage.getItem('lla_xid_v1') || ''; } catch (_) {}
    return {
      email: i.email ? String(i.email).trim().toLowerCase() : '',
      phone: i.phone ? String(i.phone).replace(/[^0-9]/g, '') : '',
      fn: letters(i.fn), ln: letters(i.ln),
      st: i.st ? String(i.st).trim().toLowerCase() : '',
      country: i.country ? String(i.country).trim().toLowerCase() : '',
      external_id: xid
    };
  }
  function newId(name) { return 'lla_' + String(name).toLowerCase().replace(/[^a-z0-9_]/g, '') + '_' + Date.now() + '_' + Math.random().toString(36).slice(2, 8); }
  function base(name, id) {
    var i = identity();
    return {event_name: name, event_id: id, email: i.email, phone: i.phone, fn: i.fn, ln: i.ln, st: i.st, country: i.country,
      external_id: i.external_id, event_time: Math.floor(Date.now() / 1000), user_agent: navigator.userAgent, url: root.location.href,
      fbp: ck('_fbp'), fbc: fbc()};
  }
  function post(payload) {
    try { root.fetch(RELAY, {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(payload), keepalive: true}).catch(function () {}); } catch (_) {}
  }
  /* pages.dev LLA_FUNNEL.trackCustom: custom Pixel event plus a server copy, one event_id, no session guard. */
  function trackCustom(name, extra) {
    if (!live() || staging()) return false;
    var id = newId(name);
    var data = {content_name: 'Longevity Blueprint', content_ids: [CONTENT_ID], content_type: 'product'};
    var k; for (k in extra) { if (extra.hasOwnProperty(k)) data[k] = extra[k]; }
    try { if (root.fbq) root.fbq('trackCustom', name, data, {eventID: id}); } catch (_) {}
    var p = base(name, id);
    p.value = 0; p.currency = 'USD'; p.content_name = 'Longevity Blueprint'; p.order_id = ''; p.content_type = 'product';
    p.content_ids = [CONTENT_ID]; p.contents = [];
    for (k in extra) { if (extra.hasOwnProperty(k)) p[k] = extra[k]; }
    post(p);
    return true;
  }
  /* pages.dev fire(): server copy once per session, event_id published to dataLayer first for the GTM Pixel tag. */
  function fireServer(name, key, extra) {
    if (!live() || staging()) return;
    try { var flag = 'lla_capi_' + key; if (root.sessionStorage.getItem(flag)) return; root.sessionStorage.setItem(flag, '1'); } catch (_) {}
    var id = newId(name);
    try { root.dataLayer = root.dataLayer || []; root.dataLayer.push({event: 'lla_capi_ready', lla_capi_name: name, lla_capi_event_id: id}); } catch (_) {}
    var p = base(name, id);
    if (extra) for (var k in extra) { if (extra.hasOwnProperty(k)) p[k] = extra[k]; }
    post(p);
  }
  var FOLDS = {hero: 'hero', topics: 'pillars', syllabus: 'learn', julie: 'julie', pricing: 'offer-monthly', cgm: 'cgm',
    teachers: 'teachers', how: 'how', about: 'about', skills: 'news', faq: 'faq', apply: 'final', 'lead-gen': 'form'};
  function location(el) {
    if (el.closest('#llaFloatCta')) return 'floater';
    if (el.closest('nav, .nav, .mobile-nav')) return 'nav';
    var s = el.closest('section');
    if (!s) return 'unknown';
    if (s.id && FOLDS[s.id]) return FOLDS[s.id];
    var c = String(s.className).split(' ')[0];
    return ({testimonials: 'reviews', deepdive: 'systems', value: 'why', bioquiz: 'quiz', topics: 'pillars'})[c] || c || 'section';
  }
  doc.addEventListener('click', function (ev) {
    var t = ev.target; if (!t || !t.closest) return;
    var el = t.closest('[data-checkout-open], a[href="#lead-gen"], a.lg-buy, #llaFloatCta a');
    if (el) {
      var x = {cta_location: location(el), cta_text: String(el.textContent || '').replace(/\s+/g, ' ').trim().slice(0, 80), plan: 'monthly'};
      try { root.sessionStorage.setItem('lla_cta_location', x.cta_location); } catch (_) {}
      trackCustom('Enroll_CTA_Click', x);
      if (/^offer-/.test(x.cta_location)) trackCustom('Clicked_on_Enroll_Pricing', x);
      try { root.dataLayer = root.dataLayer || []; root.dataLayer.push({event: 'enroll_cta_click', cta_location: x.cta_location, cta_text: x.cta_text, plan: x.plan}); } catch (_) {}
      fireServer('Clicked_on_Enroll', 'enroll_v1', {cta_location: x.cta_location});
    }
    if (t.closest('a[href*="#syllabus"], a[href*="#curriculum"]')) fireServer('Clicked_on_curriculum', 'curriculum_v1');
  }, true);
  root.LLA_CTA_EVENTS = {release: 'lla-cta-events-20261106-1'};
})(window);

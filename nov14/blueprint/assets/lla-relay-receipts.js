/* Receipt evidence only. No extra Meta events, identity storage, or automatic retries.
 * "accepted" means the relay reports a Meta receipt, NOT attribution or a real buyer. */
(function () {
  'use strict';
  var KEY = 'lla_delivery_receipts_v1', MAX = 100;
  function read() {
    try { var x = JSON.parse(sessionStorage.getItem(KEY) || '[]'); return Array.isArray(x) ? x : []; }
    catch (_) { return []; }
  }
  function write(row) {
    try {
      var rows = read().filter(function (x) { return x.event_id !== row.event_id; });
      rows.push(row); sessionStorage.setItem(KEY, JSON.stringify(rows.slice(-MAX)));
    } catch (_) {}
    try { window.dispatchEvent(new CustomEvent('lla:delivery-receipt', {detail: row})); } catch (_) {}
  }
  window.__llaDeliveryReceipts = read;
  window.__llaRelay = function (body) {
    if (window.LLA_LIVE === false) return;
    var payload;
    try {
      payload = JSON.parse(body);
    } catch (_) { return; }
    if (!payload.event_id || !payload.event_name) return;
    var row = {
      event_id: String(payload.event_id).slice(0, 160),
      event_name: String(payload.event_name).slice(0, 80),
      queued_at: new Date().toISOString(), status: 'queued',
      test_classification: payload.test_event_code ? 'declared_test' : 'unclassified'
    };
    write(row);
    var started = false, timer;
    function go() {
      if (started) return;
      started = true; clearTimeout(timer);
      window.removeEventListener('pagehide', go);
      if (window.LLA_LIVE === false) { row.status = 'excluded'; write(row); return; }
      row.status = 'dispatching'; row.dispatched_at = new Date().toISOString(); write(row);
      try {
        // Preserve the previous send-time cookie refresh, after Pixel initialization.
        // Historical commerce fbc has already been resolved by the caller.
        if (!['AddToCart', 'InitiateCheckout', 'Purchase'].includes(payload.event_name) && window.__llaRefreshClickPayload) body = window.__llaRefreshClickPayload(body);
        fetch('https://lla-ac-events.vercel.app/api/meta/capi', {
          method: 'POST', headers: {'Content-Type': 'text/plain'}, body: body, keepalive: true
        }).then(function (r) {
          return r.json().then(function (data) {
            row.http_status = r.status;
            row.meta_status = typeof data.meta_status === 'number' ? data.meta_status : null;
            row.events_received = typeof data.events_received === 'number' ? data.events_received : null;
            row.status = data.excluded === true ? 'excluded' :
              (r.ok && data.ok === true && data.events_received === 1 ? 'accepted' : 'rejected');
            row.responded_at = new Date().toISOString();
            write(row);
          });
        }).catch(function () { row.status = 'unconfirmed'; write(row); });
      } catch (_) { row.status = 'unconfirmed'; write(row); }
    }
    if (['AddToCart', 'InitiateCheckout', 'Purchase'].includes(payload.event_name)) { go(); return; }
    timer = setTimeout(go, 1500);
    window.addEventListener('pagehide', go, {once: true});
  };
})();

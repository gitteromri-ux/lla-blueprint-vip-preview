/* VIP Masterclass enrollment (Omri, 6 Nov 2026). Same student, same ProductID 26 (Longevity), second product:
 * after the Blueprint order is created, send one $0 order for the Julie VIP Masterclass, Sat Nov 14, to the same
 * CRM endpoint. Course and class IDs are the ones the live masterclass page uses (julie-masterclass, VP Ops):
 * MainAbroadCourseId 283 / AbroadCourseId 1823, Nov 14 1:00 PM ET -> CourseID 170142, SemesterID 2394.
 * Fire and forget: it never changes the Blueprint order, its ids, the payment page or tracking. Once per order. */
(function () {
  'use strict';
  if (window.LLA_VIP_ENROLL) return;
  var MC = {main: 283, abroad: 1823, classId: 170142, semester: 2394};
  function send(base, ids) {
    if (!base || !ids || !ids.orderid) return;
    var P = window.LLA_PROMO; if (!P || !P.active) return;            /* VIP comes with the JULIE249 offer only */
    var cfg = window.LLA_ECOMM_CONFIG || {}; if (cfg.mode && cfg.mode !== 'ecomm') return;
    var key = 'lla_vip_mc_' + ids.orderid;
    try { if (sessionStorage.getItem(key)) return; sessionStorage.setItem(key, '1'); } catch (e) {}
    var p = base;
    p.MainAbroadCourseId = MC.main; p.AbroadCourseId = MC.abroad;
    p.PrefferdCourseID = MC.classId; p.PreferredCourseId = MC.classId;
    p.ActivitySessionLevel1ID = MC.semester; p.SemesterID = MC.semester;
    p.FirstPayment = 0; p.NumberOfPayments = 0; p.LeftToPay = 0;
    p.DynamicParameters = (typeof p.DynamicParameters === 'string' && p.DynamicParameters ? p.DynamicParameters.replace(/(^|&)plan=[a-z]+/g, '') + '&' : '') +
      'plan=vipmasterclass&bporder=' + String(ids.orderid).replace(/[^0-9A-Za-z]/g, '');
    p.DynamicParameters = p.DynamicParameters.replace(/^&+/, '').replace(/&&+/g, '&').slice(0, 4000);
    var url = String(cfg.workerBase || '').replace(/\/$/, '') + (cfg.env === 'staging' ? '/staging' : '') + '/api/lead/ecomm';
    if (!/^https:\/\//.test(url)) return;
    try { fetch(url, {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(p), keepalive: true}).catch(function () {}); } catch (e) {}
  }
  function wrap() {
    var api = window.LLA_ECOMM;
    if (!api || typeof api.createStagedOrder !== 'function') return false;
    if (api.__vipWrapped) return true;
    var orig = api.createStagedOrder;
    api.createStagedOrder = function () {
      var snap = null;
      try { if (!sessionStorage.getItem('lla_ecomm_ids')) { var pd = JSON.parse(sessionStorage.getItem('lla_ecomm_pending') || 'null'); if (pd && pd.payload) snap = JSON.parse(JSON.stringify(pd.payload)); } } catch (e) {}
      var r = orig.apply(this, arguments);
      try { if (snap && r && typeof r.then === 'function') r.then(function (ids) { try { send(snap, ids); } catch (e) {} }, function () {}); } catch (e) {}
      return r;
    };
    api.__vipWrapped = true;
    return true;
  }
  window.LLA_VIP_ENROLL = {release: 'lla-vip-enroll-20261106-1', course: MC};
  if (!wrap()) { var n = 0, t = setInterval(function () { if (wrap() || ++n > 80) clearInterval(t); }, 250); }
})();

/* Sillage · bandeau de consentement de la vitrine.
   Rien n'est envoyé à Google tant que la personne n'a pas accepté. */
(function () {
  var GA_ID = 'G-3G1455E0RN';
  var KEY = 'sillage-consent';
  var MAX_AGE = 182 * 24 * 3600 * 1000; // 6 mois
  var EN = (document.documentElement.lang || 'fr').slice(0, 2) === 'en';
  var TXT = EN ? {
    t: 'Audience measurement',
    p: 'With your consent, we use Google Analytics to count visits to this website and see which pages are read. No data is sent to Google before you choose.',
    more: 'Learn more', href: '/en/privacy/#audience',
    yes: 'Accept all', no: 'Refuse all', manage: 'Manage cookies'
  } : {
    t: 'Mesure d’audience',
    p: 'Avec ton accord, on utilise Google Analytics pour compter les visites de ce site et voir quelles pages sont lues. Rien n’est envoyé à Google avant ton choix.',
    more: 'En savoir plus', href: '/confidentialite/#audience',
    yes: 'Tout accepter', no: 'Tout refuser', manage: 'Gérer mes cookies'
  };

  function read() {
    try {
      var v = JSON.parse(localStorage.getItem(KEY) || 'null');
      if (v && (v.c === 'granted' || v.c === 'denied') && Date.now() - v.t < MAX_AGE) return v.c;
    } catch (e) {}
    return null;
  }
  function write(c) { try { localStorage.setItem(KEY, JSON.stringify({ c: c, t: Date.now() })); } catch (e) {} }

  function loadGA() {
    if (window.__sillageGa) return;
    window.__sillageGa = true;
    window.dataLayer = window.dataLayer || [];
    function gtag() { window.dataLayer.push(arguments); }
    window.gtag = gtag;
    gtag('consent', 'default', { ad_storage: 'denied', ad_user_data: 'denied', ad_personalization: 'denied', analytics_storage: 'granted' });
    gtag('js', new Date());
    gtag('config', GA_ID, { allow_google_signals: false, allow_ad_personalization_signals: false });
    var s = document.createElement('script');
    s.async = true;
    s.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA_ID;
    document.head.appendChild(s);
  }

  function clearCookies() {
    var host = location.hostname.split('.');
    var domains = ['', location.hostname, '.' + host.slice(-2).join('.')];
    document.cookie.split(';').forEach(function (c) {
      var n = c.split('=')[0].trim();
      if (n === '_ga' || n.indexOf('_ga_') === 0 || n === '_gid' || n.indexOf('_gat') === 0) {
        domains.forEach(function (d) {
          document.cookie = n + '=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/' + (d ? '; domain=' + d : '');
        });
      }
    });
  }

  var box;
  function close() { if (box) { box.remove(); box = null; } }
  function choose(c) {
    write(c);
    close();
    if (c === 'granted') loadGA(); else { clearCookies(); if (window.__sillageGa) location.reload(); }
  }

  function css() {
    if (document.getElementById('sl-consent-css')) return;
    var st = document.createElement('style');
    st.id = 'sl-consent-css';
    st.textContent =
      '#sl-consent{position:fixed;left:16px;right:16px;bottom:16px;z-index:2147483000;max-width:560px;margin:0 auto;' +
      'background:#121B17;color:#EEF1EC;border-radius:16px;padding:20px 22px;box-shadow:0 10px 40px rgba(0,0,0,.35);' +
      'font:400 14px/1.5 Archivo,system-ui,sans-serif}' +
      '#sl-consent h2{margin:0 0 6px;border:0;padding:0;font-size:16px;font-weight:800;letter-spacing:-.01em}' +
      '#sl-consent p{margin:0 0 14px;color:#C9D1CC}' +
      '#sl-consent a{color:#EEF1EC;text-decoration:underline}' +
      '#sl-consent .row{display:flex;gap:10px;flex-wrap:wrap}' +
      '#sl-consent button{flex:1 1 150px;min-height:44px;border:0;border-radius:999px;font:700 15px Archivo,system-ui,sans-serif;cursor:pointer;' +
      'background:#EEF1EC;color:#14201B}' +
      '#sl-consent button:focus-visible{outline:3px solid #E0A21B;outline-offset:2px}';
    document.head.appendChild(st);
  }

  function show() {
    if (box) return;
    css();
    box = document.createElement('div');
    box.id = 'sl-consent';
    box.setAttribute('role', 'dialog');
    box.setAttribute('aria-labelledby', 'sl-consent-t');
    box.innerHTML = '<h2 id="sl-consent-t"></h2><p></p><div class="row"><button type="button" data-c="denied"></button><button type="button" data-c="granted"></button></div>';
    box.querySelector('h2').textContent = TXT.t;
    var p = box.querySelector('p');
    p.textContent = TXT.p + ' ';
    var a = document.createElement('a');
    a.href = TXT.href; a.textContent = TXT.more;
    p.appendChild(a);
    box.querySelector('[data-c=denied]').textContent = TXT.no;
    box.querySelector('[data-c=granted]').textContent = TXT.yes;
    box.addEventListener('click', function (e) {
      var c = e.target && e.target.getAttribute && e.target.getAttribute('data-c');
      if (c) choose(c);
    });
    document.body.appendChild(box);
  }

  function init() {
    var c = read();
    if (c === 'granted') loadGA(); else if (c === null) show();
    document.addEventListener('click', function (e) {
      var t = e.target && e.target.closest && e.target.closest('[data-cookies]');
      if (t) { e.preventDefault(); show(); }
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();

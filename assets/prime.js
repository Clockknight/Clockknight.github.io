/* Browser port of Clockknight/some-prime-nonsense (main.py).
 *
 * Three panels, one on screen at a time, with a sliding transition between them. Nothing needs a
 * "next" button: the page moves on by itself.
 *   1. The number   - press Generate; a composite N > 2^50 (no small odd factors) is generated and
 *                     all of its factors are found. When it's ready the page moves on.
 *   2. Say it, then check a factor
 *                   - N is shown with commas and spelled out for reading aloud. Entering a factor
 *                     moves on to the result, unless it's even or <= 31 (then it asks to confirm).
 *   3. Result       - yes/no, plus the full list of factors.
 * Restart returns to step 1 at any point and cancels any generation in progress.
 *
 * Runs on the page itself (no Web Worker). The factoring loop is time-sliced so the page stays
 * responsive and the progress bar moves.
 */
(function () {
  'use strict';

  var VERSION = '6';            // must match data-version on #prime-app in the page
  var BASE_POWER = 50;
  var MINIMUM_NONFACTOR = 31;
  var SLICE_MS = 30;            // how long the factoring loop runs before yielding to the browser
  var LEAVE_MS = 180;           // keep in sync with the CSS leave animation
  var ADVANCE_MS = 700;         // how long the new number is shown in step 1 before moving on

  var REQUIRED_IDS = [
    'prime-app', 'pn-boot', 'pn-error', 'pn-p1', 'pn-p2', 'pn-p3', 'pn-h1', 'pn-h2', 'pn-h3',
    'pn-numberbox', 'pn-n', 'pn-progress', 'pn-pct', 'pn-status', 'pn-start', 'pn-copy',
    'pn-ref-n', 'pn-say', 'pn-form', 'pn-guess', 'pn-msg', 'pn-submitrow', 'pn-submit',
    'pn-confirm', 'pn-confirm-text', 'pn-yes', 'pn-no', 'pn-answer', 'pn-result-n',
    'pn-result-guess', 'pn-count', 'pn-factors'
  ];

  var $ = function (id) { return document.getElementById(id); };
  var state = {
    step: 1, running: false, token: 0, navToken: 0,
    n: null, factorList: null, factorSet: null, guess: null
  };

  // ------------------------------------------------------- number display
  function formatNumber(value) {
    return String(value).replace(/\B(?=(\d{3})+(?!\d))/g, ',');
  }

  var ONES = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten',
    'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen'];
  var TENS = ['', '', 'twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety'];
  var SCALES = ['', 'thousand', 'million', 'billion', 'trillion', 'quadrillion', 'quintillion', 'sextillion'];

  function underThousand(n) {                     // 1..999
    var parts = [];
    var hundreds = Math.floor(n / 100), rest = n % 100;
    if (hundreds) parts.push(ONES[hundreds] + ' hundred');
    if (rest) {
      if (rest < 20) parts.push(ONES[rest]);
      else parts.push(TENS[Math.floor(rest / 10)] + (rest % 10 ? '-' + ONES[rest % 10] : ''));
    }
    return parts.join(' ');
  }

  // 1540887503630899 -> "one quadrillion, five hundred forty trillion, eight hundred eighty-seven billion, ..."
  function numberToWords(value) {
    var n = BigInt(value);
    if (n === 0n) return 'zero';
    var negative = n < 0n;
    if (negative) n = -n;
    var groups = [];
    while (n > 0n) { groups.push(Number(n % 1000n)); n /= 1000n; }
    if (groups.length > SCALES.length) return formatNumber(value);
    var parts = [];
    for (var i = groups.length - 1; i >= 0; i--) {
      if (groups[i] === 0) continue;
      parts.push(underThousand(groups[i]) + (SCALES[i] ? ' ' + SCALES[i] : ''));
    }
    return (negative ? 'negative ' : '') + parts.join(', ');
  }

  // Lets the number helpers be tested outside a browser; does nothing on the page.
  if (typeof module === 'object' && module && module.exports) {
    module.exports = { formatNumber: formatNumber, numberToWords: numberToWords };
    return;
  }

  // ---------------------------------------------------------------- maths
  function randomBits50() {
    var a = new Uint32Array(2);
    window.crypto.getRandomValues(a);
    var hi = a[0] & ((1 << (BASE_POWER - 32)) - 1);
    return BigInt(hi) * 4294967296n + BigInt(a[1]);
  }

  function modpow(b, e, m) {
    var r = 1n;
    b %= m;
    while (e > 0n) {
      if (e & 1n) r = (r * b) % m;
      b = (b * b) % m;
      e >>= 1n;
    }
    return r;
  }

  // Deterministic Miller-Rabin (these 12 bases are exact far beyond 2^64).
  var SMALL = [2n, 3n, 5n, 7n, 11n, 13n, 17n, 19n, 23n, 29n, 31n, 37n];
  function isPrime(n) {
    if (n < 2n) return false;
    for (var i = 0; i < SMALL.length; i++) {
      if (n === SMALL[i]) return true;
      if (n % SMALL[i] === 0n) return false;
    }
    var d = n - 1n, s = 0;
    while ((d & 1n) === 0n) { d >>= 1n; s++; }
    for (var j = 0; j < SMALL.length; j++) {
      var x = modpow(SMALL[j], d, n);
      if (x === 1n || x === n - 1n) continue;
      var composite = true;
      for (var r = 1; r < s; r++) {
        x = (x * x) % n;
        if (x === n - 1n) { composite = false; break; }
      }
      if (composite) return false;
    }
    return true;
  }

  function generateComposite() {
    var c = randomBits50() + (1n << BigInt(BASE_POWER));
    if (c % 2n === 0n) c += 1n;
    for (;;) {
      c += 2n;
      if (c % 5n === 0n) c += 2n;
      var easy = false;
      for (var i = 3; i < MINIMUM_NONFACTOR; i += 2) {
        if (c % BigInt(i) === 0n) { easy = true; break; }
      }
      if (easy) continue;
      if (!isPrime(c)) return c;
    }
  }

  // Give the browser a turn, then continue. MessageChannel isn't slowed down in background tabs
  // the way setTimeout is, so generation still finishes if the tab loses focus.
  function yieldThen(fn) {
    if (typeof MessageChannel !== 'undefined') {
      var ch = new MessageChannel();
      ch.port1.onmessage = function () { ch.port1.close(); fn(); };
      ch.port2.postMessage(0);
    } else {
      setTimeout(fn, 0);
    }
  }

  var now = (window.performance && performance.now) ? function () { return performance.now(); } : function () { return Date.now(); };

  // ----------------------------------------------------------- navigation
  function reducedMotion() {
    return !!(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches);
  }

  function panel(n) { return $('pn-p' + n); }

  var ALL_CLASSES = ['enter-fwd', 'enter-back', 'leave-fwd', 'leave-back'];
  function strip(el) { ALL_CLASSES.forEach(function (c) { el.classList.remove(c); }); }

  function restartButtons() { return document.querySelectorAll('#prime-app .pn-restart'); }

  function updateRestart() {
    // Nothing to restart while the page is still in its starting state.
    var pristine = (state.step === 1 && !state.running && state.n === null);
    Array.prototype.forEach.call(restartButtons(), function (b) { b.disabled = pristine; });
  }

  // Slide from the current panel to `next`. `focusId` is focused once the new panel is showing.
  function goTo(next, focusId) {
    if (next === state.step) { if (focusId) $(focusId).focus(); return; }
    var dir = next > state.step ? 'fwd' : 'back';
    var from = panel(state.step), to = panel(next);
    var token = ++state.navToken;

    // Settle any transition still in flight: only `from` and `to` may be visible.
    for (var p = 1; p <= 3; p++) {
      var el = panel(p);
      if (el !== from && el !== to) { strip(el); el.hidden = true; }
    }
    state.step = next;
    updateRestart();

    var delay = reducedMotion() ? 0 : LEAVE_MS;
    strip(from);
    if (delay) from.classList.add('leave-' + dir);

    setTimeout(function () {
      if (token !== state.navToken) return;
      strip(from);
      from.hidden = true;
      strip(to);
      to.hidden = false;
      if (!reducedMotion()) {
        to.classList.add('enter-' + dir);
        setTimeout(function () { if (token === state.navToken) strip(to); }, 400);
      }
      var focusEl = $(focusId || 'pn-h' + next);
      if (focusEl) { try { focusEl.focus({ preventScroll: true }); } catch (e) { focusEl.focus(); } }
      // Keep the whole widget on screen if the page is scrolled elsewhere.
      var app = $('prime-app');
      if (app.scrollIntoView) app.scrollIntoView({ block: 'nearest', behavior: reducedMotion() ? 'auto' : 'smooth' });
    }, delay);
  }

  // ------------------------------------------------------------------- UI
  function setProgress(pct) {
    var bar = $('pn-progress');
    bar.hidden = false;
    if (pct === null) bar.removeAttribute('value'); else bar.value = pct;
    $('pn-pct').textContent = pct === null ? '' : 'Processing factors… ' + pct + '%';
  }

  function clearCheck() {
    $('pn-guess').value = '';
    $('pn-guess').disabled = false;
    $('pn-msg').textContent = '';
    $('pn-confirm').hidden = true;
    $('pn-submitrow').hidden = false;
  }

  function showError(message) {
    var el = $('pn-error');
    if (!el) return;
    el.hidden = false;
    el.textContent = 'Something went wrong: ' + message;
  }

  function resetStepOne() {
    var btn = $('pn-start');
    btn.disabled = false;
    btn.textContent = 'Generate a number';
    btn.removeAttribute('aria-busy');
    $('pn-copy').disabled = true;
    $('pn-numberbox').classList.remove('is-fresh');
    $('pn-n').classList.add('pn-empty');
    $('pn-n').textContent = 'Not generated yet';
    $('pn-progress').hidden = true;
    $('pn-pct').textContent = '';
    $('pn-status').textContent = '';
  }

  function restart() {
    state.token++;                 // cancels any generation (or pending move-on) still running
    state.running = false;
    state.n = null; state.factorList = null; state.factorSet = null; state.guess = null;
    $('pn-error').hidden = true;
    resetStepOne();
    clearCheck();
    $('pn-factors').textContent = '';
    updateRestart();
    goTo(1, 'pn-start');
  }

  function start() {
    if (state.running) return;
    state.running = true;
    var token = ++state.token;
    try {
      $('pn-error').hidden = true;
      var btn = $('pn-start');
      btn.disabled = true;
      btn.textContent = 'Generating…';
      btn.setAttribute('aria-busy', 'true');
      $('pn-copy').disabled = true;
      $('pn-numberbox').classList.remove('is-fresh');
      $('pn-n').classList.add('pn-empty');
      $('pn-n').textContent = 'Generating…';
      $('pn-status').textContent = 'Generating composite number…';
      setProgress(null);
      state.n = null;
      clearCheck();
      updateRestart();
    } catch (e) { return finishError(e, token); }

    // Let the browser paint the "Generating" state before the number crunching starts.
    setTimeout(function () { compute(token); }, 30);
  }

  function compute(token) {
    if (token !== state.token) return;
    try {
      var n = generateComposite();
      var nNum = Number(n);                       // < 2^53, so exact
      var limit = Math.floor(Math.sqrt(nNum));
      while (limit * limit > nNum) limit--;
      while ((limit + 1) * (limit + 1) <= nNum) limit++;
      var cofactors = [nNum], small = [1], i = MINIMUM_NONFACTOR;

      $('pn-status').textContent = 'Processing the composite’s factors… (This takes the most time!)';
      setProgress(0);

      (function slice() {
        if (token !== state.token) return;
        try {
          var deadline = now() + SLICE_MS;
          while (i <= limit) {
            var stop = Math.min(limit, i + 200000);
            for (; i <= stop; i += 2) {
              if (nNum % i === 0) { cofactors.push(nNum / i); small.push(i); }
            }
            if (now() > deadline) break;
          }
          if (i <= limit) {
            setProgress(Math.min(99, Math.floor(((i - MINIMUM_NONFACTOR) / (limit - MINIMUM_NONFACTOR)) * 100)));
            yieldThen(slice);
          } else {
            setProgress(100);
            finish(n, cofactors.concat(small.reverse()), token);
          }
        } catch (e) { finishError(e, token); }
      })();
    } catch (e) { finishError(e, token); }
  }

  // Whatever goes wrong, never leave the button stuck on "Generating...".
  function finishError(e, token) {
    if (token !== state.token) return;
    state.running = false;
    try { resetStepOne(); updateRestart(); } catch (ignore) { /* page and script are out of sync */ }
    showError(e && e.message ? e.message : String(e));
  }

  function finish(n, all, token) {
    var seen = {}, list = [];
    all.forEach(function (f) { if (!seen[f]) { seen[f] = true; list.push(String(f)); } });
    state.n = n;
    state.factorList = list;
    state.factorSet = seen;
    state.running = false;

    var shown = $('pn-n');
    shown.classList.remove('pn-empty');
    shown.textContent = formatNumber(n);
    $('pn-numberbox').classList.remove('is-fresh');
    void $('pn-numberbox').offsetWidth;           // restart the highlight animation
    $('pn-numberbox').classList.add('is-fresh');
    $('pn-status').textContent = 'Number ready.';
    $('pn-progress').hidden = true;
    $('pn-pct').textContent = '';

    var btn = $('pn-start');                      // stays disabled until Restart
    btn.textContent = 'Generate a number';
    btn.removeAttribute('aria-busy');
    updateRestart();

    // Show the new number for a moment, then move on by itself.
    setTimeout(function () { if (token === state.token) showCheck(); }, ADVANCE_MS);
  }

  function showCheck() {
    if (state.n === null) return;
    $('pn-ref-n').textContent = formatNumber(state.n);
    $('pn-say').textContent = numberToWords(state.n);
    $('pn-copy').disabled = false;
    clearCheck();
    goTo(2, 'pn-guess');
  }

  // Accepts "23456231", "23,456,231" and "23 456 231".
  function parseGuess(text) {
    var t = text.replace(/[,\s]/g, '');
    return /^\d+$/.test(t) ? BigInt(t) : null;
  }

  function submitGuess(ev) {
    ev.preventDefault();
    if (state.n === null) return;
    var g = parseGuess($('pn-guess').value);
    var msg = $('pn-msg');
    if (g === null) { msg.textContent = 'Invalid formatting. Please input a whole number.'; return; }
    if (g === 0n || g === 1n || g === state.n) { msg.textContent = 'These are invalid answers, try again.'; return; }
    state.guess = g;

    // Only stop to confirm when the script has something to flag.
    if (g % 2n === 0n || g <= BigInt(MINIMUM_NONFACTOR)) {
      msg.textContent = 'Please warn the player this is a horrendous idea.';
      $('pn-confirm-text').textContent = 'The chosen factor is ' + formatNumber(g) + '. Is this correct?';
      $('pn-guess').disabled = true;
      $('pn-submitrow').hidden = true;
      $('pn-confirm').hidden = false;
      $('pn-yes').focus();
      return;
    }
    msg.textContent = '';
    showResult();
  }

  function reject() {
    $('pn-confirm').hidden = true;
    $('pn-submitrow').hidden = false;
    $('pn-guess').disabled = false;
    $('pn-msg').textContent = '';
    $('pn-guess').focus();
    $('pn-guess').select();
  }

  function showResult() {
    var guess = state.guess.toString();
    var ok = !!state.factorSet[guess];
    var answer = $('pn-answer');
    answer.textContent = ok ? 'Yes, it factored.' : 'No, it did not factor.';
    answer.className = 'pn-answer ' + (ok ? 'pn-yes' : 'pn-no');
    $('pn-result-n').textContent = formatNumber(state.n);
    $('pn-result-guess').textContent = formatNumber(guess);

    var list = $('pn-factors');
    list.textContent = '';
    state.factorList.forEach(function (f) {
      var li = document.createElement('li');
      var code = document.createElement('code');
      code.textContent = formatNumber(f);
      if (f === guess) li.className = 'pn-hit';
      li.appendChild(code);
      list.appendChild(li);
    });
    $('pn-count').textContent = state.factorList.length + ' factors in total';
    goTo(3, 'pn-answer');
  }

  function copyN() {
    var btn = $('pn-copy');
    var flash = function (text) {
      btn.textContent = text;
      setTimeout(function () { btn.textContent = 'Copy'; }, 1500);
    };
    try {
      navigator.clipboard.writeText(formatNumber(state.n)).then(
        function () { flash('Copied!'); },
        function () { flash('Copy failed'); });
    } catch (e) { flash('Copy failed'); }
  }

  function bootMessage(text) {
    var boot = $('pn-boot');
    if (!boot) return;
    boot.hidden = false;
    boot.textContent = text;
    boot.className = 'pn-error';
  }

  function init() {
    if (typeof BigInt === 'undefined' || !window.crypto || !window.crypto.getRandomValues) {
      return bootMessage('This page needs a current browser (BigInt and crypto support) to run the generator.');
    }
    var app = $('prime-app');
    var missing = REQUIRED_IDS.filter(function (id) { return !$(id); });
    if ((app && app.getAttribute('data-version') !== VERSION) || missing.length) {
      return bootMessage('This page and its script are from different versions (your browser is probably showing a cached copy). ' +
        'Please hard refresh: Ctrl+Shift+R, or Cmd+Shift+R on a Mac.');
    }

    $('pn-boot').hidden = true;
    $('pn-start').disabled = false;
    $('pn-start').addEventListener('click', start);
    $('pn-copy').addEventListener('click', copyN);
    $('pn-form').addEventListener('submit', submitGuess);
    $('pn-yes').addEventListener('click', showResult);
    $('pn-no').addEventListener('click', reject);
    Array.prototype.forEach.call(restartButtons(), function (b) { b.addEventListener('click', restart); });
    updateRestart();
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();

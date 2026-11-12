/* Browser port of Clockknight/some-prime-nonsense (main.py).
 *
 * Three steps, one panel on screen at a time, with a sliding transition between them:
 *   1. The number   - generate a composite N > 2^50 (no small odd factors) and find all its factors
 *   2. Check factor - the defending player's chosen factor is checked against that list
 *   3. Result       - yes/no, plus the full list of factors
 * A Restart button returns to step 1 at any point, cancelling any generation in progress.
 *
 * Runs on the page itself (no Web Worker): it takes well under a second, and the factoring loop
 * is split into short chunks so the page stays responsive and the progress bar moves.
 */
(function () {
  'use strict';

  var BASE_POWER = 50;
  var MINIMUM_NONFACTOR = 31;
  var CHUNK = 400000;           // loop iterations per tick while factoring
  var LEAVE_MS = 180;           // keep in sync with the CSS leave animation

  var $ = function (id) { return document.getElementById(id); };
  var state = {
    step: 1, running: false, token: 0, navToken: 0,
    n: null, factorList: null, factorSet: null, guess: null
  };

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

  // ----------------------------------------------------------- navigation
  function reducedMotion() {
    return !!(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches);
  }

  function panel(n) { return $('pn-p' + n); }

  var ALL_CLASSES = ['enter-fwd', 'enter-back', 'leave-fwd', 'leave-back'];
  function strip(el) { ALL_CLASSES.forEach(function (c) { el.classList.remove(c); }); }

  function updateSteps() {
    var items = $('pn-steps').children;
    for (var i = 0; i < items.length; i++) {
      var num = i + 1, li = items[i];
      li.classList.toggle('is-current', num === state.step);
      li.classList.toggle('is-done', num < state.step);
      if (num === state.step) li.setAttribute('aria-current', 'step'); else li.removeAttribute('aria-current');
      li.querySelector('.pn-step').textContent = num < state.step ? '✓' : String(num);
    }
    updateRestart();
  }

  function updateRestart() {
    // Nothing to restart while the page is still in its starting state.
    $('pn-restart').disabled = (state.step === 1 && !state.running && state.n === null);
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
    updateSteps();

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
    el.hidden = false;
    el.textContent = 'Something went wrong: ' + message;
  }

  function resetStepOne() {
    var btn = $('pn-start');
    btn.disabled = false;
    btn.textContent = 'Generate a number';
    btn.classList.remove('secondary');
    btn.removeAttribute('aria-busy');
    $('pn-copy').disabled = true;
    $('pn-next').hidden = true;
    $('pn-numberbox').classList.remove('is-fresh');
    $('pn-n').classList.add('pn-empty');
    $('pn-n').textContent = 'Not generated yet';
    $('pn-progress').hidden = true;
    $('pn-pct').textContent = '';
    $('pn-status').textContent = '';
  }

  function restart() {
    state.token++;                 // cancels any generation still running
    state.running = false;
    state.n = null; state.factorList = null; state.factorSet = null; state.guess = null;
    $('pn-error').hidden = true;
    resetStepOne();
    clearCheck();
    $('pn-factors').textContent = '';
    updateSteps();
    goTo(1, 'pn-start');
  }

  function start() {
    if (state.running) return;
    state.running = true;
    var token = ++state.token;

    $('pn-error').hidden = true;
    var btn = $('pn-start');
    btn.disabled = true;
    btn.textContent = 'Generating…';
    btn.setAttribute('aria-busy', 'true');
    $('pn-copy').disabled = true;
    $('pn-next').hidden = true;
    $('pn-numberbox').classList.remove('is-fresh');
    $('pn-n').classList.add('pn-empty');
    $('pn-n').textContent = 'Generating…';
    $('pn-status').textContent = 'Generating composite number…';
    setProgress(null);
    state.n = null;
    clearCheck();
    updateRestart();

    // Let the browser paint the "Generating" state before the number crunching starts.
    setTimeout(function () {
      if (token !== state.token) return;
      var n, limit, i, cofactors, small;
      try {
        n = generateComposite();
      } catch (e) { return finishError(e, token); }

      var nNum = Number(n);                       // < 2^53, so exact
      limit = Math.floor(Math.sqrt(nNum));
      while (limit * limit > nNum) limit--;
      while ((limit + 1) * (limit + 1) <= nNum) limit++;
      cofactors = [nNum];
      small = [1];
      i = MINIMUM_NONFACTOR;
      $('pn-status').textContent = 'Processing the composite’s factors… (This takes the most time!)';
      setProgress(0);

      function step() {
        if (token !== state.token) return;
        try {
          var stop = Math.min(limit, i + CHUNK * 2);
          for (; i <= stop; i += 2) {
            if (nNum % i === 0) { cofactors.push(nNum / i); small.push(i); }
          }
          if (i <= limit) {
            setProgress(Math.min(99, Math.floor(((i - MINIMUM_NONFACTOR) / (limit - MINIMUM_NONFACTOR)) * 100)));
            setTimeout(step, 0);
          } else {
            setProgress(100);
            finish(n, cofactors.concat(small.reverse()));
          }
        } catch (e) { finishError(e, token); }
      }
      step();
    }, 30);
  }

  function finishError(e, token) {
    if (token !== state.token) return;
    state.running = false;
    resetStepOne();
    updateRestart();
    showError(e && e.message ? e.message : String(e));
  }

  function finish(n, all) {
    var seen = {}, list = [];
    all.forEach(function (f) { if (!seen[f]) { seen[f] = true; list.push(String(f)); } });
    state.n = n;
    state.factorList = list;
    state.factorSet = seen;
    state.running = false;

    $('pn-n').classList.remove('pn-empty');
    $('pn-n').textContent = n.toString();
    $('pn-numberbox').classList.remove('is-fresh');
    void $('pn-numberbox').offsetWidth;           // restart the highlight animation
    $('pn-numberbox').classList.add('is-fresh');
    $('pn-status').textContent = 'Number ready.';
    $('pn-progress').hidden = true;
    $('pn-pct').textContent = '';
    $('pn-copy').disabled = false;

    var btn = $('pn-start');
    btn.disabled = false;
    btn.textContent = 'Generate another number';
    btn.classList.add('secondary');
    btn.removeAttribute('aria-busy');

    $('pn-next').hidden = false;
    $('pn-next').focus();
    updateRestart();
  }

  function toCheck() {
    if (state.n === null) return;
    $('pn-ref-n').textContent = state.n.toString();
    clearCheck();
    goTo(2, 'pn-guess');
  }

  function parseGuess(text) {
    var t = text.trim();
    return /^\d+$/.test(t) ? BigInt(t) : null;
  }

  function submitGuess(ev) {
    ev.preventDefault();
    if (state.n === null) return;
    var g = parseGuess($('pn-guess').value);
    var msg = $('pn-msg');
    if (g === null) { msg.textContent = 'Invalid formatting. Please input a whole number.'; return; }
    if (g === 0n || g === 1n || g === state.n) { msg.textContent = 'These are invalid answers, try again.'; return; }

    msg.textContent = (g % 2n === 0n || g <= BigInt(MINIMUM_NONFACTOR))
      ? 'Please warn the player this is a horrendous idea.' : '';
    state.guess = g;
    $('pn-confirm-text').textContent = 'The chosen factor is ' + g.toString() + '. Is this correct?';
    $('pn-guess').disabled = true;
    $('pn-submitrow').hidden = true;
    $('pn-confirm').hidden = false;
    $('pn-yes').focus();
  }

  function reject() {
    $('pn-confirm').hidden = true;
    $('pn-submitrow').hidden = false;
    $('pn-guess').disabled = false;
    $('pn-msg').textContent = '';
    $('pn-guess').focus();
    $('pn-guess').select();
  }

  function accept() {
    var guess = state.guess.toString();
    var ok = !!state.factorSet[guess];
    var answer = $('pn-answer');
    answer.textContent = ok ? 'Yes, it factored.' : 'No, it did not factor.';
    answer.className = 'pn-answer ' + (ok ? 'pn-yes' : 'pn-no');
    $('pn-result-n').textContent = state.n.toString();
    $('pn-result-guess').textContent = guess;

    var list = $('pn-factors');
    list.textContent = '';
    state.factorList.forEach(function (f) {
      var li = document.createElement('li');
      var code = document.createElement('code');
      code.textContent = f;
      if (f === guess) li.className = 'pn-hit';
      li.appendChild(code);
      list.appendChild(li);
    });
    $('pn-count').textContent = state.factorList.length + ' factors in total';
    goTo(3, 'pn-answer');
  }

  function retry() {
    clearCheck();
    goTo(2, 'pn-guess');
  }

  function copyN() {
    var btn = $('pn-copy');
    var flash = function (text) {
      btn.textContent = text;
      setTimeout(function () { btn.textContent = 'Copy number'; }, 1500);
    };
    try {
      navigator.clipboard.writeText(state.n.toString()).then(
        function () { flash('Copied!'); },
        function () { flash('Copy failed'); });
    } catch (e) { flash('Copy failed'); }
  }

  function init() {
    if (typeof BigInt === 'undefined' || !window.crypto || !window.crypto.getRandomValues) {
      $('pn-boot').textContent = 'This page needs a current browser (BigInt and crypto support) to run the generator.';
      $('pn-boot').className = 'pn-error';
      return;
    }
    $('pn-boot').hidden = true;
    $('pn-start').disabled = false;
    $('pn-start').addEventListener('click', start);
    $('pn-copy').addEventListener('click', copyN);
    $('pn-next').addEventListener('click', toCheck);
    $('pn-form').addEventListener('submit', submitGuess);
    $('pn-back').addEventListener('click', function () { goTo(1, 'pn-next'); });
    $('pn-yes').addEventListener('click', accept);
    $('pn-no').addEventListener('click', reject);
    $('pn-retry').addEventListener('click', retry);
    $('pn-restart').addEventListener('click', restart);
    $('pn-restart2').addEventListener('click', restart);
    updateSteps();
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();

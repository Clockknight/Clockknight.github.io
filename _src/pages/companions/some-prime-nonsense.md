---
title: Some Prime Nonsense
class: prime
---
This generates a composite number "N" for the combo in [this decklist](https://moxfield.com/decks/60C4okZqKEaREDOJ3En6AA).

N avoids the [rules of divisibility](https://en.wikipedia.org/wiki/Divisibility_rule#Divisibility_rules_for_numbers_1%E2%88%9230) and is intended to be humanly incalculable (generated numbers are larger than 2<sup>50</sup>), to make guessing a factor as difficult as possible.

Generate a number, have the defending player pick a factor of it, then check that factor. Everything runs in your browser; nothing is sent anywhere. This is a JavaScript port of [the original Python program](https://github.com/Clockknight/some-prime-nonsense).

<section class="prime-app" id="prime-app" aria-label="Number generator and factor checker">
<p class="pn-boot" id="pn-boot" role="status">Loading the generator&hellip; (if this message stays, the page's script didn't load. Try a hard refresh.)</p>
<noscript><p class="pn-error">This page needs JavaScript to run the generator.</p></noscript>
<p class="pn-error" id="pn-error" role="alert" hidden></p>
<div class="pn-bar" id="pn-bar">
<ol class="pn-steps" id="pn-steps" aria-label="Progress">
<li class="is-current" data-step="1" aria-current="step"><span class="pn-step">1</span><span class="pn-steplabel">The number</span></li>
<li data-step="2"><span class="pn-step">2</span><span class="pn-steplabel">Check a factor</span></li>
<li data-step="3"><span class="pn-step">3</span><span class="pn-steplabel">Result</span></li>
</ol>
<button class="btn secondary small" id="pn-restart" type="button" disabled>Restart</button>
</div>
<div class="pn-panels">
<div class="pn-panel" id="pn-p1">
<h2 id="pn-h1" tabindex="-1">The number</h2>
<div class="pn-numberbox" id="pn-numberbox">
<p class="pn-label">n chosen for combo is:</p>
<p class="pn-number pn-empty" id="pn-n" aria-live="polite">Not generated yet</p>
</div>
<progress id="pn-progress" max="100" hidden></progress>
<p class="pn-pct" id="pn-pct" aria-live="polite"></p>
<p class="pn-hint" id="pn-status" role="status"></p>
<div class="btn-row">
<button class="btn" id="pn-start" type="button" disabled>Generate a number</button>
<button class="btn secondary" id="pn-copy" type="button" disabled>Copy number</button>
<button class="btn" id="pn-next" type="button" hidden>Check a factor &rarr;</button>
</div>
</div>
<div class="pn-panel" id="pn-p2" hidden>
<h2 id="pn-h2" tabindex="-1">Check a factor</h2>
<div class="pn-ref">
<span class="pn-label">n</span>
<span class="pn-refnum" id="pn-ref-n"></span>
</div>
<form id="pn-form" novalidate>
<div class="field">
<label for="pn-guess">Enter the defending player's chosen factor</label>
<input id="pn-guess" type="text" inputmode="numeric" autocomplete="off">
</div>
<p class="pn-hint">Note: it is heavily recommended to input odd factors greater than 31.</p>
<p class="pn-msg" id="pn-msg" role="alert"></p>
<div class="btn-row" id="pn-submitrow">
<button class="btn" id="pn-submit" type="submit">Check this factor</button>
<button class="btn secondary" id="pn-back" type="button">&larr; Back to the number</button>
</div>
<div id="pn-confirm" hidden>
<p id="pn-confirm-text"></p>
<div class="btn-row">
<button class="btn" id="pn-yes" type="button">Yes, that's it</button>
<button class="btn secondary" id="pn-no" type="button">No, change it</button>
</div>
</div>
</form>
</div>
<div class="pn-panel" id="pn-p3" hidden>
<h2 id="pn-h3" tabindex="-1">Result</h2>
<p class="pn-answer" id="pn-answer" tabindex="-1"></p>
<div class="pn-pair">
<div><p class="pn-label">n</p><p class="pn-number" id="pn-result-n"></p></div>
<div><p class="pn-label">Chosen factor</p><p class="pn-number" id="pn-result-guess"></p></div>
</div>
<h3>List of factors</h3>
<p class="pn-hint" id="pn-count"></p>
<ul class="pn-factors" id="pn-factors"></ul>
<div class="btn-row">
<button class="btn" id="pn-restart2" type="button">Restart with a new number</button>
<button class="btn secondary" id="pn-retry" type="button">Try another factor</button>
</div>
</div>
</div>
</section>
<script src="../assets/prime.js" defer></script>

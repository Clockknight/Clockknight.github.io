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
<div class="pn-section" id="pn-sec-number">
<h2><span class="pn-step">1</span> The number</h2>
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
</div>
</div>
<div class="pn-section is-locked" id="pn-sec-check">
<h2><span class="pn-step">2</span> Check a factor</h2>
<p class="pn-hint" id="pn-locked-note">Generate a number first.</p>
<form id="pn-form" novalidate>
<fieldset id="pn-fields" disabled>
<div class="field">
<label for="pn-guess">Enter the defending player's chosen factor</label>
<input id="pn-guess" type="text" inputmode="numeric" autocomplete="off">
</div>
<p class="pn-hint">Note: it is heavily recommended to input odd factors greater than 31.</p>
<p class="pn-msg" id="pn-msg" role="alert"></p>
<button class="btn" id="pn-submit" type="submit">Check this factor</button>
<div id="pn-confirm" hidden>
<p id="pn-confirm-text"></p>
<div class="btn-row">
<button class="btn" id="pn-yes" type="button">Yes, that's it</button>
<button class="btn secondary" id="pn-no" type="button">No, change it</button>
</div>
</div>
</fieldset>
</form>
</div>
<div class="pn-section" id="pn-sec-result">
<h2><span class="pn-step">3</span> Result</h2>
<p class="pn-hint" id="pn-result-empty">Check a factor to see whether it factors the number, along with the full list of factors.</p>
<div id="pn-result-body" hidden>
<p class="pn-answer" id="pn-answer" tabindex="-1"></p>
<p class="pn-label">n</p>
<p class="pn-number" id="pn-result-n"></p>
<p class="pn-label">Chosen factor</p>
<p class="pn-number" id="pn-result-guess"></p>
<h3>List of factors</h3>
<p class="pn-hint" id="pn-count"></p>
<ul class="pn-factors" id="pn-factors"></ul>
</div>
</div>
</section>
<script src="../assets/prime.js" defer></script>

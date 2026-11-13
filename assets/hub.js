/* Tabbed "hub" boxes: a strip of names on top, one larger connected box below that shows the
 * selected item. Hovering a name selects it, and the box keeps showing whatever was hovered last.
 * Click, tap, focus and the arrow keys select too, so it works without a mouse.
 *
 * Markup (also the no-script fallback, where every item is simply shown one after another):
 *   <div class="hub" data-hub data-label="Projects">
 *     <div class="hub-panels">
 *       <article class="hub-item" data-tab="Name">...content...</article> ...
 */
(function () {
  'use strict';
  var uid = 0;

  function build(hub) {
    var items = Array.prototype.slice.call(hub.querySelectorAll('.hub-item'));
    var panels = hub.querySelector('.hub-panels');
    if (!items.length || !panels) return;
    uid++;

    var tabs = document.createElement('div');
    tabs.className = 'hub-tabs';
    tabs.setAttribute('role', 'tablist');
    if (hub.getAttribute('data-label')) tabs.setAttribute('aria-label', hub.getAttribute('data-label'));

    var buttons = items.map(function (item, i) {
      var id = 'hub' + uid + '-' + i;
      var b = document.createElement('button');
      b.type = 'button';
      b.className = 'hub-tab';
      b.id = id + '-tab';
      b.setAttribute('role', 'tab');
      b.setAttribute('aria-controls', id);
      b.textContent = item.getAttribute('data-tab') || item.querySelector('h3').textContent;
      item.id = id;
      item.setAttribute('role', 'tabpanel');
      item.setAttribute('aria-labelledby', b.id);
      b.addEventListener('mouseenter', function () { select(i, false); });
      b.addEventListener('focus', function () { select(i, false); });
      b.addEventListener('click', function () { select(i, false); });
      b.addEventListener('keydown', function (e) {
        var to = null;
        if (e.key === 'ArrowRight' || e.key === 'ArrowDown') to = (i + 1) % items.length;
        else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') to = (i + items.length - 1) % items.length;
        else if (e.key === 'Home') to = 0;
        else if (e.key === 'End') to = items.length - 1;
        if (to === null) return;
        e.preventDefault();
        select(to, true);
      });
      tabs.appendChild(b);
      return b;
    });

    var current = -1;
    function select(i, focus) {
      if (i === current) { if (focus) buttons[i].focus(); return; }
      current = i;
      items.forEach(function (item, k) {
        var on = k === i;
        item.classList.toggle('is-active', on);
        buttons[k].classList.toggle('is-active', on);
        buttons[k].setAttribute('aria-selected', on ? 'true' : 'false');
        buttons[k].tabIndex = on ? 0 : -1;
      });
      if (focus) buttons[i].focus();
    }

    hub.insertBefore(tabs, panels);
    if (items.length === 1) hub.classList.add('is-single');   // nothing to switch between: just the box
    hub.classList.add('is-live');
    select(0, false);                          // starts on the left-most item
  }

  // A cached older stylesheet would leave tabs unstyled and every panel showing, so without the
  // matching stylesheet the items are left as a plain list instead.
  function stylesMatch() {
    try { return getComputedStyle(document.documentElement).getPropertyValue('--hub-css').trim() === '1'; }
    catch (e) { return false; }
  }

  function init() {
    if (!stylesMatch()) return;
    Array.prototype.forEach.call(document.querySelectorAll('[data-hub]'), build);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();

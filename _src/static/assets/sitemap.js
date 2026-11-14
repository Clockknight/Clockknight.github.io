/* Controls for the sitemap tree: expand/collapse everything, and hide the "Hidden pages" group.
 * Each branch also folds on its own (click its row): the tree is plain <details>, so that works
 * without this script. */
(function () {
  'use strict';
  var tree = document.querySelector('.sitemap-tree');
  if (!tree) return;
  var branches = tree.querySelectorAll('details');
  var page = document.body;                       // body.sitemap is set by the page's class
  var bar = document.createElement('div');
  bar.className = 'sm-tools';

  function button(label, fn) {
    var btn = document.createElement('button');
    btn.type = 'button';
    btn.textContent = label;
    btn.addEventListener('click', fn);
    bar.appendChild(btn);
  }
  button('Expand all', function () {
    Array.prototype.forEach.call(branches, function (d) { d.open = true; });
  });
  button('Collapse all', function () {
    Array.prototype.forEach.call(branches, function (d, i) { d.open = i === 0; });   // keep the main page open
  });

  if (tree.querySelector('.hidden-group')) {
    var label = document.createElement('label');
    var box = document.createElement('input');
    box.type = 'checkbox';
    box.addEventListener('change', function () { page.classList.toggle('hide-hidden', box.checked); });
    label.appendChild(box);
    label.appendChild(document.createTextNode('Hide hidden pages'));
    bar.appendChild(label);
  }
  tree.parentNode.insertBefore(bar, tree);
})();

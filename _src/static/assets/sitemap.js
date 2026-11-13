/* Expand / collapse buttons for the sitemap tree. The tree itself is plain <details>, so
 * branches fold without this script; it only adds the two "all" buttons. */
(function () {
  'use strict';
  var tree = document.querySelector('.sitemap-tree');
  if (!tree) return;
  var branches = tree.querySelectorAll('details');
  if (!branches.length) return;
  var bar = document.createElement('div');
  bar.className = 'sm-tools';
  [['Expand all', true], ['Collapse all', false]].forEach(function (b) {
    var btn = document.createElement('button');
    btn.type = 'button';
    btn.textContent = b[0];
    btn.addEventListener('click', function () {
      Array.prototype.forEach.call(branches, function (d, i) {
        d.open = b[1] || i === 0;       // "collapse all" keeps the top level (the main page) open
      });
    });
    bar.appendChild(btn);
  });
  tree.parentNode.insertBefore(bar, tree);
})();

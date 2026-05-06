(function () {
  var selAuthor = document.getElementById('filter-author');
  var selDate   = document.getElementById('filter-date');
  var btnReset  = document.getElementById('filter-reset');
  var counter   = document.getElementById('filter-count');

  var posts = Array.from(document.querySelectorAll('article.blog-post'));

  function unique(arr) {
    return arr.filter(function(v, i, a) { return a.indexOf(v) === i; }).sort();
  }

  var authors = unique(posts.map(function(p) {
    return p.querySelector('.blog-post-author').textContent.replace('★', '').trim();
  }));
  var dates = unique(posts.map(function(p) {
    return p.querySelector('.blog-post-date').textContent.trim();
  }));

  authors.forEach(function(a) {
    var o = document.createElement('option');
    o.value = a; o.textContent = a;
    selAuthor.appendChild(o);
  });
  dates.forEach(function(d) {
    var o = document.createElement('option');
    o.value = d; o.textContent = d;
    selDate.appendChild(o);
  });

  function applyFilter() {
    var fa = selAuthor.value;
    var fd = selDate.value;
    var visible = 0;

    posts.forEach(function(article) {
      var author = article.querySelector('.blog-post-author').textContent.replace('★', '').trim();
      var date   = article.querySelector('.blog-post-date').textContent.trim();
      var show   = (!fa || author === fa) && (!fd || date === fd);

      article.style.display = show ? '' : 'none';
      var next = article.nextElementSibling;
      if (next && next.classList.contains('section-divider')) {
        next.style.display = show ? '' : 'none';
      }
      if (show) visible++;
    });

    counter.textContent = (fa || fd) ? ('показано: ' + visible + ' / ' + posts.length) : '';
  }

  selAuthor.addEventListener('change', applyFilter);
  selDate.addEventListener('change', applyFilter);
  btnReset.addEventListener('click', function() {
    selAuthor.value = '';
    selDate.value   = '';
    applyFilter();
  });
})();

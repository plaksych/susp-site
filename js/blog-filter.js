(function () {
  var selAuthor  = document.getElementById('filter-author');
  var inpFrom    = document.getElementById('filter-date-from');
  var inpTo      = document.getElementById('filter-date-to');
  var btnReset   = document.getElementById('filter-reset');
  var counter    = document.getElementById('filter-count');

  var posts = Array.from(document.querySelectorAll('article.blog-post'));

  // заполняем автора
  function unique(arr) {
    return arr.filter(function(v, i, a) { return a.indexOf(v) === i; }).sort();
  }
  unique(posts.map(function(p) {
    return p.querySelector('.blog-post-author').textContent.replace('★', '').trim();
  })).forEach(function(a) {
    var o = document.createElement('option');
    o.value = a; o.textContent = a;
    selAuthor.appendChild(o);
  });

  // дд.мм.гггг → число для сравнения (гггг*10000 + мм*100 + дд)
  function parseDate(str) {
    var parts = str.trim().split('.');
    if (parts.length !== 3) return null;
    var d = parseInt(parts[0], 10);
    var m = parseInt(parts[1], 10);
    var y = parseInt(parts[2], 10);
    if (isNaN(d) || isNaN(m) || isNaN(y)) return null;
    return y * 10000 + m * 100 + d;
  }

  // автомаска: вставляем точки при вводе
  function applyMask(e) {
    var val = e.target.value.replace(/\D/g, '');
    if (val.length > 2) val = val.slice(0, 2) + '.' + val.slice(2);
    if (val.length > 5) val = val.slice(0, 5) + '.' + val.slice(5);
    e.target.value = val.slice(0, 10);
    applyFilter();
  }

  function applyFilter() {
    var fa   = selAuthor.value;
    var from = parseDate(inpFrom.value);
    var to   = parseDate(inpTo.value);
    var visible = 0;
    var active = fa || inpFrom.value || inpTo.value;

    posts.forEach(function(article) {
      var author  = article.querySelector('.blog-post-author').textContent.replace('★', '').trim();
      var dateNum = parseDate(article.querySelector('.blog-post-date').textContent);
      var show = true;

      if (fa && author !== fa) show = false;
      if (from !== null && dateNum !== null && dateNum < from) show = false;
      if (to   !== null && dateNum !== null && dateNum > to)   show = false;

      article.style.display = show ? '' : 'none';
      var next = article.nextElementSibling;
      if (next && next.classList.contains('section-divider')) {
        next.style.display = show ? '' : 'none';
      }
      if (show) visible++;
    });

    counter.textContent = active ? ('показано: ' + visible + ' / ' + posts.length) : '';
  }

  selAuthor.addEventListener('change', applyFilter);
  inpFrom.addEventListener('input', applyMask);
  inpTo.addEventListener('input', applyMask);

  btnReset.addEventListener('click', function() {
    selAuthor.value = '';
    inpFrom.value   = '';
    inpTo.value     = '';
    applyFilter();
  });
})();

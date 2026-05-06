(function () {
  var btn = document.getElementById('sidebar-toggle');
  var sidebar = document.getElementById('sidebar');

  if (!btn || !sidebar) return;

  btn.addEventListener('click', function () {
    var isOpen = sidebar.classList.toggle('is-open');
    btn.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
    btn.textContent = isOpen
      ? '[ ✕ ЗАКРЫТЬ ]'
      : '[ ★ ИНФО / LINKS / STATUS ]';
  });
})();

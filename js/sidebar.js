(function () {
  var btn = document.getElementById('sidebar-toggle');
  var sidebar = document.getElementById('sidebar');

  if (!btn || !sidebar) return;

  btn.addEventListener('click', function () {
    var isOpen = sidebar.classList.toggle('is-open');
    btn.classList.toggle('is-open', isOpen);
    btn.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
    btn.textContent = isOpen
      ? '[ ✕ ЗАКРЫТЬ ]'
      : '[ ★ ИНФО / LINKS / STATUS ] [НАЖМИ]';
    btn.blur();

    if (!isOpen) {
      /* перезапускаем анимацию: снимаем, форсируем reflow, возвращаем */
      btn.style.animation = 'none';
      void btn.offsetWidth;
      btn.style.animation = '';
    }
  });
})();

function toggleMusic() {
  const player = document.getElementById("player");
  const btn = document.getElementById("play-btn");

  if (player.paused) {
    player.play();
    btn.textContent = "■ STOP MUSIC";
    btn.classList.add('is-playing');
    btn.style.animation = 'none';
  } else {
    player.pause();
    player.currentTime = 0;
    btn.textContent = "▶ PLAY MUSIC";
    btn.classList.remove('is-playing');
    btn.style.animation = 'none';
    void btn.offsetWidth;
    btn.style.animation = '';
  }
}

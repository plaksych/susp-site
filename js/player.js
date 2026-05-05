function toggleMusic() {
  const player = document.getElementById("player");
  const btn = document.getElementById("play-btn");

  if (player.paused) {
    player.play();
    btn.textContent = "■ STOP MUSIC";
  } else {
    player.pause();
    player.currentTime = 0;
    btn.textContent = "▶ PLAY MUSIC";
  }
}

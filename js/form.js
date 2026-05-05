document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('guestbook-form');
  const status = document.getElementById('form-status');

  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const data = new FormData(form);

    try {
      const response = await fetch(form.action, {
        method: 'POST',
        body: data,
        headers: {
          'Accept': 'application/json'
        }
      });

      if (response.ok) {
        status.textContent = "✔ Сообщение отправлено!";
        form.reset();
      } else {
        status.textContent = "✖ Ошибка отправки";
      }
    } catch (error) {
      status.textContent = "⚠ Сервер не отвечает";
    }
  });
});
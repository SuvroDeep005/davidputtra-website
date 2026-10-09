(() => {
  const launcher = document.querySelector('[data-chat-launcher]');
  const panel = document.querySelector('[data-chat-panel]');
  const close = document.querySelector('[data-chat-close]');
  const form = document.querySelector('[data-chat-form]');
  const input = document.querySelector('[data-chat-input]');
  const thread = document.querySelector('[data-chat-thread]');
  if (!launcher || !panel || !form || !input || !thread) return;

  const addMessage = (text, role) => {
    const bubble = document.createElement('p');
    bubble.className = 'dp-chat-bubble ' + role;
    bubble.textContent = text;
    thread.appendChild(bubble);
    thread.scrollTop = thread.scrollHeight;
    return bubble;
  };
  launcher.addEventListener('click', () => {
    panel.hidden = false;
    launcher.hidden = true;
    input.focus();
  });
  close?.addEventListener('click', () => {
    panel.hidden = true;
    launcher.hidden = false;
    launcher.focus();
  });
  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    const message = input.value.trim();
    if (!message) return;
    addMessage(message, 'customer');
    input.value = '';
    input.disabled = true;
    const pending = addMessage('One moment…', 'bot');
    try {
      const response = await fetch(form.dataset.endpoint, {
        method: 'POST',
        headers: {
          'X-CSRFToken': form.querySelector('[name=csrfmiddlewaretoken]').value,
          'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
        },
        body: new URLSearchParams({message})
      });
      const data = await response.json();
      pending.textContent = response.ok ? data.reply : (data.error || 'Please try again.');
    } catch (_) {
      pending.textContent = 'The assistant is unavailable right now. Please use the Contact page.';
    } finally {
      input.disabled = false;
      input.focus();
    }
  });
})();

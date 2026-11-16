document.querySelectorAll('[data-copy]').forEach((button) => {
  button.addEventListener('click', async () => {
    const status = document.querySelector('.copy-status');
    try {
      await navigator.clipboard.writeText(button.dataset.copy);
      status.textContent = 'Commande copiée.';
    } catch {
      status.textContent = 'Copie impossible : sélectionnez la commande manuellement.';
    }
  });
});

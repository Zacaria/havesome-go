(() => {
  const token =
    /(\/\/[^\n]*|\/\*[\s\S]*?\*\/|"(?:\\.|[^"\\])*"|`[^`]*`|'(?:\\.|[^'\\])*'|\b(?:package|import|func|var|const|type|struct|interface|return|if|else|for|range|switch|case|default|select|go|defer|chan|map|break|continue|nil|true|false)\b|\b\d+(?:\.\d+)?\b)/g;
  function highlight(source, target) {
    target.replaceChildren();
    let previous = 0;
    for (const match of source.matchAll(token)) {
      target.append(document.createTextNode(source.slice(previous, match.index)));
      const span = document.createElement('span');
      const value = match[0];
      span.className =
        value.startsWith('//') || value.startsWith('/*')
          ? 'comment'
          : /^["'`]/.test(value)
          ? 'string'
          : /^\d/.test(value)
          ? 'number'
          : 'keyword';
      span.textContent = value;
      target.append(span);
      previous = match.index + value.length;
    }
    target.append(document.createTextNode(source.slice(previous) + '\n'));
  }
  document.querySelectorAll('.playground').forEach(playground => {
    const editor = playground.querySelector('textarea');
    const colors = playground.querySelector('.editor-colors');
    const run = playground.querySelector('button');
    const output = playground.querySelector('output');
    function render() {
      highlight(editor.value, colors);
    }
    editor.addEventListener('input', render);
    editor.addEventListener('scroll', () => {
      colors.parentElement.scrollTop = editor.scrollTop;
      colors.parentElement.scrollLeft = editor.scrollLeft;
    });
    render();
    playground.classList.add('highlight-ready');
    run.addEventListener('click', () => {
      if (editor.value.length > 30000) {
        output.textContent = 'Programme trop long : maximum 30 000 caractères.';
        return;
      }
      run.disabled = true;
      output.textContent = 'Chargement et exécution…';
      let worker;
      let timer;
      function finish(message) {
        clearTimeout(timer);
        if (worker) worker.terminate();
        output.textContent = message;
        run.disabled = false;
      }
      try {
        worker = new Worker('worker.js');
        worker.onmessage = ({ data }) =>
          finish(data.error ? 'Impossible d’exécuter : ' + data.error : data.output || '(aucune sortie)');
        worker.onerror = () => finish('Impossible de charger le moteur. Vérifiez votre connexion et réessayez.');
        timer = setTimeout(() => finish('Temps limite atteint : exécution interrompue.'), 30000);
        worker.postMessage({ source: editor.value });
      } catch (error) {
        finish('Impossible de démarrer le moteur : ' + error.message);
      }
    });
  });
})();

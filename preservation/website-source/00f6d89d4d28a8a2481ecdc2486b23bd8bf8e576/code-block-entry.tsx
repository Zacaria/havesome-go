import * as React from 'react';
import { createRoot } from 'react-dom/client';

import { CodeBlock, CodeBlockActions, CodeBlockContent, CodeBlockCopyButton } from './code-block';

const tokens =
  /(\/\/[^\n]*|\/\*[\s\S]*?\*\/|"(?:\\.|[^"\\])*"|`[^`]*`|'(?:\\.|[^'\\])*'|\b(?:package|import|func|var|const|type|struct|interface|return|if|else|for|range|switch|case|default|select|go|defer|chan|map|break|continue|nil|true|false)\b|\b\d+(?:\.\d+)?\b)/g;
function colored(source: string) {
  const nodes: React.ReactNode[] = [];
  let previous = 0;
  for (const match of source.matchAll(tokens)) {
    nodes.push(source.slice(previous, match.index));
    const value = match[0];
    const name =
      value.startsWith('//') || value.startsWith('/*')
        ? 'comment'
        : /^["'`]/.test(value)
        ? 'string'
        : /^\d/.test(value)
        ? 'number'
        : 'keyword';
    nodes.push(
      <span key={match.index} className={name}>
        {value}
      </span>
    );
    previous = match.index! + value.length;
  }
  nodes.push(source.slice(previous));
  return nodes;
}

document.querySelectorAll('article pre:not(.editor pre)').forEach(pre => {
  const source = pre.querySelector('code')?.textContent;
  if (source === undefined || source === null) return;
  const tree = pre.classList.contains('tree');
  const container = document.createElement('div');
  pre.replaceWith(container);
  createRoot(container).render(
    <CodeBlock className={tree ? 'tree' : ''}>
      <CodeBlockActions>
        <CodeBlockCopyButton value={source} />
      </CodeBlockActions>
      <CodeBlockContent>{tree ? source : colored(source)}</CodeBlockContent>
    </CodeBlock>
  );
});

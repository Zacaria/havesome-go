import * as React from "react";
import { createRoot } from "react-dom/client";
import { flushSync } from "react-dom";
import { Button } from "./button";
import "./ui.css";

import {
  CodeBlock,
  CodeBlockActions,
  CodeBlockContent,
  CodeBlockCopyButton,
  CodeBlockHeader,
  CodeBlockTitle,
  CodeBlockLine,
} from "./code-block";

const tokens =
  /(\/\/[^\n]*|\/\*[\s\S]*?\*\/|"(?:\\.|[^"\\])*"|`[^`]*`|'(?:\\.|[^'\\])*'|\b(?:package|import|func|var|const|type|struct|interface|return|if|else|for|range|switch|case|default|select|go|defer|chan|map|break|continue|nil|true|false)\b|\b\d+(?:\.\d+)?\b)/g;
function colored(source: string) {
  const nodes: React.ReactNode[] = [];
  let previous = 0;
  for (const match of source.matchAll(tokens)) {
    nodes.push(source.slice(previous, match.index));
    const value = match[0];
    const name =
      value.startsWith("//") || value.startsWith("/*")
        ? "comment"
        : /^["'`]/.test(value)
          ? "string"
          : /^\d/.test(value)
            ? "number"
            : "keyword";
    nodes.push(
      <span key={match.index} className={name}>
        {value}
      </span>,
    );
    previous = match.index! + value.length;
  }
  nodes.push(source.slice(previous));
  return nodes;
}

document.querySelectorAll("article pre:not(.editor pre)").forEach((pre) => {
  const source = pre.querySelector("code")?.textContent;
  if (source === undefined || source === null) return;
  const tree = pre.classList.contains("tree");
  const container = document.createElement("div");
  pre.replaceWith(container);
  flushSync(() =>
    createRoot(container).render(
      <CodeBlock className={tree ? "tree" : ""}>
        <CodeBlockActions>
          <CodeBlockCopyButton value={source} />
        </CodeBlockActions>
        <CodeBlockContent>{tree ? source : colored(source)}</CodeBlockContent>
      </CodeBlock>,
    ),
  );
});

function Playground({ initial, id, label }: { initial: string; id: string; label: string }) {
  const [source, setSource] = React.useState(initial);
  const [output, setOutput] = React.useState("Le résultat apparaîtra ici.");
  const [running, setRunning] = React.useState(false);
  const mirror = React.useRef<HTMLPreElement>(null);
  const worker = React.useRef<Worker | null>(null);
  const timer = React.useRef<ReturnType<typeof setTimeout> | null>(null);
  React.useEffect(
    () => () => {
      if (timer.current) clearTimeout(timer.current);
      worker.current?.terminate();
    },
    [],
  );
  function run() {
    if (source.length > 30000) {
      setOutput("Programme trop long : maximum 30 000 caractères.");
      return;
    }
    setRunning(true);
    setOutput("Chargement et exécution…");
    function finish(message: string) {
      if (timer.current) clearTimeout(timer.current);
      worker.current?.terminate();
      worker.current = null;
      setOutput(message);
      setRunning(false);
    }
    try {
      worker.current = new Worker("worker.js");
      worker.current.onmessage = ({ data }) =>
        finish(
          data.error ? "Impossible d’exécuter : " + data.error : data.output || "(aucune sortie)",
        );
      worker.current.onerror = () =>
        finish("Impossible de charger le moteur. Vérifiez votre connexion et réessayez.");
      timer.current = setTimeout(
        () => finish("Temps limite atteint : exécution interrompue."),
        30000,
      );
      worker.current.postMessage({ source });
    } catch (error) {
      finish("Impossible de démarrer le moteur : " + (error as Error).message);
    }
  }
  return (
    <CodeBlock className="playground-block" size="sm">
      <CodeBlockHeader>
        <CodeBlockTitle>main.go</CodeBlockTitle>
        <CodeBlockActions>
          <CodeBlockCopyButton value={source} />
          <Button className="run-button" type="button" disabled={running} onClick={run}>
            Exécuter
          </Button>
        </CodeBlockActions>
      </CodeBlockHeader>
      <div className="playground-editor">
        <CodeBlockContent ref={mirror} lineNumbers aria-hidden="true" tabIndex={-1}>
          {source.split("\n").map((line, index) => (
            <CodeBlockLine key={index}>{line ? colored(line) : "\u200b"}</CodeBlockLine>
          ))}
        </CodeBlockContent>
        <textarea
          id={id}
          aria-label={label}
          spellCheck={false}
          autoCapitalize="off"
          autoComplete="off"
          wrap="off"
          value={source}
          onChange={(event) => setSource(event.currentTarget.value)}
          onScroll={(event) => {
            if (mirror.current) {
              mirror.current.scrollTop = event.currentTarget.scrollTop;
              mirror.current.scrollLeft = event.currentTarget.scrollLeft;
            }
          }}
        />
      </div>
      <output aria-live="polite" aria-label="Résultat du programme">
        {output}
      </output>
    </CodeBlock>
  );
}

document.querySelectorAll(".playground").forEach((container) => {
  const textarea = container.querySelector("textarea");
  const label = container.querySelector("label");
  if (!textarea || !label) return;
  const initial = textarea.value,
    id = textarea.id,
    text = label.textContent || "Programme Go modifiable";
  flushSync(() =>
    createRoot(container).render(<Playground initial={initial} id={id} label={text} />),
  );
});

import * as React from "react";
import { createRoot } from "react-dom/client";
import { Button } from "./button";
import { CodeBlock, CodeBlockActions, CodeBlockContent, CodeBlockCopyButton } from "./code-block";
import "./ui.css";

document.querySelectorAll<HTMLButtonElement>("[data-copy]").forEach((button) => {
  const value = button.dataset.copy!;
  const label = button.getAttribute("aria-label") || "Copier";
  const host = document.createElement("span");
  button.replaceWith(host);
  createRoot(host).render(
    <Button
      type="button"
      variant="outline"
      data-copy={value}
      aria-label={label}
      onClick={async () => {
        const status = document.querySelector(".copy-status")!;
        try {
          await navigator.clipboard.writeText(value);
          status.textContent = "Commande copiée.";
        } catch {
          status.textContent = "Copie impossible : sélectionnez la commande manuellement.";
        }
      }}
    >
      Copier
    </Button>,
  );
});

document.querySelectorAll<HTMLPreElement>("pre[data-go-example]").forEach((pre) => {
  const source = pre.querySelector("code")?.textContent;
  if (source == null) return;
  const host = document.createElement("div");
  host.dataset.example = pre.dataset.goExample;
  pre.replaceWith(host);
  createRoot(host).render(
    <CodeBlock>
      <CodeBlockActions>
        <CodeBlockCopyButton value={source} />
      </CodeBlockActions>
      <CodeBlockContent>{source}</CodeBlockContent>
    </CodeBlock>,
  );
});

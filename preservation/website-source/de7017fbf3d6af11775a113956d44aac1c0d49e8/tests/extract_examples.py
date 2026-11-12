"""Compile the exact Go snippets shown to readers, not parallel copies."""
from html import unescape
from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
html = (root / 'index.html').read_text(encoding='utf8')
snippets = re.findall(r'<pre><code>(.*?)</code></pre>', html, re.S)
if len(snippets) != 3:
    raise SystemExit(f'Expected three Go examples, got {len(snippets)}')
source = 'package examples\n\nimport ("context"; "fmt"; "io")\n\n' + '\n\n'.join(map(unescape, snippets)) + '\n'
(root / 'examples' / 'snippets.go').write_text(source, encoding='utf8')

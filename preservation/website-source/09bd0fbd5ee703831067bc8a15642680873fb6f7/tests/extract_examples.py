"""Compile the exact Go snippets shown to readers, not parallel copies."""
from html import unescape
from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
html = (root / 'index.html').read_text(encoding='utf8')
snippets = re.findall(r'<pre><code>(.*?)</code></pre>', html, re.S)
if len(snippets) != 5:
    raise SystemExit(f'Expected five Go examples, got {len(snippets)}')
source = 'package examples\n\nimport ("context"; "fmt"; "io"; "net/http")\n\n' + '\n\n'.join(unescape(snippets[i]) for i in (0, 1, 2, 4)) + '\n'
test = 'package examples\n\nimport ("net/http"; "net/http/httptest"; "testing")\n\n' + unescape(snippets[3]) + '\n'
(root / 'examples' / 'http_snippet_test.go').write_text(test, encoding='utf8')
(root / 'examples' / 'snippets.go').write_text(source, encoding='utf8')

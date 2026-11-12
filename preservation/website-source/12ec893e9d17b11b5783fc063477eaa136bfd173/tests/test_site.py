import unittest
from pathlib import Path
from html.parser import HTMLParser

ROOT = Path(__file__).resolve().parents[1]

class Document(HTMLParser):
    def __init__(self):
        super().__init__(); self.ids = []; self.links = []; self.lang = None
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a: self.ids.append(a['id'])
        if tag == 'a' and 'href' in a: self.links.append(a['href'])
        if tag == 'html': self.lang = a.get('lang')

class SiteTest(unittest.TestCase):
    def test_complete_french_document_and_navigation(self):
        page = ROOT / 'index.html'
        self.assertTrue(page.exists(), 'Le guide doit exister')
        d = Document(); d.feed(page.read_text(encoding='utf-8'))
        self.assertEqual(d.lang, 'fr')
        self.assertEqual(len(d.ids), len(set(d.ids)))
        for section in ('philosophie', 'valeurs', 'api', 'concurrence', 'outils', 'production', 'senior', 'sources'):
            self.assertIn(section, d.ids)
            self.assertIn('#' + section, d.links)
        for href in d.links:
            if href.startswith('#'): self.assertIn(href[1:], d.ids)
        for concept in ('defer', 'append', 'interface nil', 'http.HandlerFunc', 'go test', 'switch'):
            self.assertIn(concept, page.read_text(encoding='utf-8'))
        self.assertGreaterEqual(sum(h.startswith('https://go.dev/') or h.startswith('https://pkg.go.dev/') for h in d.links), 8)

    def test_practice_and_architecture_are_navigable(self):
        page = (ROOT / 'index.html').read_text(encoding='utf8')
        d = Document(); d.feed(page)
        for section in ('atelier', 'architecture', 'ecosysteme'):
            self.assertIn(section, d.ids)
            self.assertIn('#' + section, d.links)
        for text in ('WebAssembly', 'interpréteur', 'application/', 'domain/', 'infrastructure/', 'TDD'):
            self.assertIn(text, page)
        self.assertTrue((ROOT / 'playground' / 'go.mod').exists())
        self.assertTrue((ROOT / 'playground.js').exists())

    def test_examples_match_reader_visible_snippets(self):
        import re
        from html import unescape
        html = (ROOT / 'index.html').read_text(encoding='utf8')
        snippets = re.findall(r'<pre><code>(.*?)</code></pre>', html, re.S)
        self.assertEqual(len(snippets), 5)
        expected = 'package examples\n\nimport ("context"; "fmt"; "io"; "net/http")\n\n' + '\n\n'.join(unescape(snippets[i]) for i in (0, 1, 2, 4)) + '\n'
        expected_test = 'package examples\n\nimport ("net/http"; "net/http/httptest"; "testing")\n\n' + unescape(snippets[3]) + '\n'
        self.assertEqual((ROOT / 'examples/http_snippet_test.go').read_text(encoding='utf8'), expected_test)
        self.assertEqual((ROOT / 'examples/snippets.go').read_text(encoding='utf8'), expected)

if __name__ == '__main__': unittest.main()

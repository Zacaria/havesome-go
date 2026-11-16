import unittest
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = 'https://github.com/Zacaria/havesome-go'

class Links(HTMLParser):
    def __init__(self):
        super().__init__(); self.region = None; self.links = {}; self.ids = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ('header', 'footer'): self.region = tag
        if 'id' in a: self.ids.append(a['id'])
        if tag == 'a' and self.region: self.links.setdefault(self.region, []).append(a.get('href'))
    def handle_endtag(self, tag):
        if tag == self.region: self.region = None

class CheatSheetTest(unittest.TestCase):
    def test_guide_links_and_accessible_reference(self):
        guide = Links(); guide.feed((ROOT / 'index.html').read_text())
        for region in ('header', 'footer'):
            self.assertIn('fiche.html', guide.links[region])
            self.assertIn(REPO, guide.links[region])
        sheet = (ROOT / 'fiche.html').read_text()
        doc = Links(); doc.feed(sheet)
        self.assertEqual(len(doc.ids), len(set(doc.ids)))
        for word in ('lang="fr"', 'go test ./...', 'go vet ./...', 'go build ./...', 'go.dev', 'erreur', 'goroutine'):
            self.assertIn(word, sheet)
        self.assertIn('cheatsheet-art.png', sheet)
        self.assertTrue((ROOT / 'cheatsheet-art.png').is_file())

if __name__ == '__main__': unittest.main()

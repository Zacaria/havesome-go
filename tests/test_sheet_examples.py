"""Execute the exact, reader-visible, self-contained Go examples."""
import os
import shutil
import subprocess
import tempfile
import unittest
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class Examples(HTMLParser):
    def __init__(self):
        super().__init__()
        self.items = []
        self.current = None
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'pre' and 'data-go-example' in a:
            self.current = [a['data-go-example'], a['data-output'], '']
    def handle_data(self, data):
        if self.current is not None:
            self.current[2] += data
    def handle_endtag(self, tag):
        if tag == 'pre' and self.current is not None:
            self.items.append(self.current)
            self.current = None

class SheetExamplesTest(unittest.TestCase):
    def test_topics_and_reader_visible_programs(self):
        parser = Examples()
        parser.feed((ROOT / 'fiche.html').read_text(encoding='utf-8'))
        self.assertEqual(len(parser.items), 7)
        self.assertEqual({x[0] for x in parser.items}, {'declarations', 'fonctions', 'collections', 'flux', 'types', 'erreurs', 'concurrence'})
        go = shutil.which('go')
        if go is None:
            self.fail('Go est nécessaire pour vérifier les exemples de la fiche')
        assert go is not None
        with tempfile.TemporaryDirectory() as directory:
            program = Path(directory) / 'main.go'
            for name, expected, code in parser.items:
                with self.subTest(name=name):
                    program.write_text(code, encoding='utf-8')
                    result = subprocess.run([go, 'run', str(program)], capture_output=True, text=True, timeout=90, env={**os.environ, 'GOTOOLCHAIN': 'local'})
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertEqual(result.stdout, expected)

if __name__ == '__main__': unittest.main()

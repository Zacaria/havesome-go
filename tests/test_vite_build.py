import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class ViteBuildTest(unittest.TestCase):
    def test_site_build_has_both_pages_and_playground_assets(self):
        manifest = json.loads((ROOT / 'package.json').read_text())
        self.assertEqual(manifest['scripts']['build'], 'vp build')
        for name in ('index.html', 'fiche.html', 'worker.js', 'wasm_exec.js', 'engine.wasm', 'licenses/GO-LICENSE.txt'):
            self.assertTrue((ROOT / 'dist' / name).is_file(), name)
        self.assertIn('Fiche mémo Go', (ROOT / 'dist' / 'fiche.html').read_text())

if __name__ == '__main__':
    unittest.main()

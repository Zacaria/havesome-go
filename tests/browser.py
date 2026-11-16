from playwright.sync_api import sync_playwright
from pathlib import Path
import sys

url = sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:18765/'
with sync_playwright() as p:
    browser = p.chromium.launch(executable_path='/usr/bin/brave-browser', headless=True, args=['--no-sandbox'])
    for width in (1440, 390, 320):
        page = browser.new_page(viewport={'width': width, 'height': 900 if width == 1440 else 844}, java_script_enabled=False, reduced_motion='reduce')
        response = page.goto(url, wait_until='networkidle')
        assert response and response.status == 200
        assert page.locator('html').get_attribute('lang') == 'fr'
        assert page.locator('h1').inner_text().startswith('Go, sans')
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), f'overflow {width}'
        for anchor in ('philosophie', 'valeurs', 'api', 'concurrence', 'outils', 'production', 'senior', 'sources'):
            page.locator('aside nav a[href="#' + anchor + '"]').click()
            assert page.evaluate('location.hash') == '#' + anchor
            box = page.locator('#' + anchor).bounding_box()
            assert box is not None and box['y'] < page.viewport_size['height'], (width, anchor, box)
        page.goto(url); page.screenshot(path=str(Path('/home/hermes/.hermes/profiles/builder/cache/scratch') / f'havesome-go-{width}.png'), full_page=True)
        print(f'PASS: {width}px, lecture sans JavaScript, huit liens et aucun débordement')
        page.close()
    browser.close()

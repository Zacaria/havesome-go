from playwright.sync_api import sync_playwright
import sys

url = sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:18765/'
with sync_playwright() as p:
    browser = p.chromium.launch(executable_path='/usr/bin/brave-browser', headless=True, args=['--no-sandbox'])
    for width in (1440, 390, 320):
        page = browser.new_page(viewport={'width': width, 'height': 844}, reduced_motion='reduce', permissions=['clipboard-read', 'clipboard-write'])
        page.goto(url, wait_until='networkidle')
        sections = page.locator('article > section')
        ids = sections.evaluate_all('(ss) => ss.map(s => s.id)')
        for ident in ids + list(reversed(ids)):
            page.evaluate('(id) => document.getElementById(id).scrollIntoView()', ident)
            page.wait_for_timeout(80)
            current = page.locator('aside [aria-current="location"]')
            assert current.count() == 1 and current.get_attribute('href') == '#' + ident, (width, ident, current.all_text_contents())
        page.evaluate('window.scrollTo(0, document.documentElement.scrollHeight)')
        page.wait_for_timeout(80)
        assert page.locator('aside [aria-current="location"]').get_attribute('href') == '#sources'
        assert page.locator('aside').bounding_box()['y'] < 844
        page.goto(url + '#api', wait_until='networkidle')
        page.wait_for_function('document.querySelector(\'aside [aria-current="location"]\')?.getAttribute("href") === "#api"')
        page.locator('aside a[href="#concurrence"]').focus()
        page.keyboard.press('Enter')
        page.wait_for_timeout(100)
        assert page.locator('aside [aria-current="location"]').get_attribute('href') == '#concurrence'
        assert page.locator('article [data-slot="code-block"]:not(.playground-block)').count() == 6
        assert page.locator('.playground textarea').count() == 2
        static_block = page.locator('article [data-slot="code-block"]:not(.playground-block)').first
        button = static_block.locator('[data-slot="code-block-copy-button"]')
        expected = static_block.locator('[data-slot="code-block-content"]').inner_text()
        button.click()
        assert page.evaluate('navigator.clipboard.readText()') == expected
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
        print(f'PASS {width}px: scroll, ancres, clavier, blocs, copie, ateliers')
        page.close()
    browser.close()

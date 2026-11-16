"""Brave regression for the editable shadcn code block."""
import sys
from playwright.sync_api import sync_playwright

url = sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:18979/'
with sync_playwright() as p:
    browser = p.chromium.launch(executable_path='/usr/bin/brave-browser', headless=True, chromium_sandbox=True)
    for width in (320, 390, 800, 1440):
        page = browser.new_page(viewport={'width': width, 'height': 844}, reduced_motion='reduce', permissions=['clipboard-read', 'clipboard-write'])
        page.goto(url, wait_until='load')
        page.locator('.playground [data-slot="code-block-header"]').first.wait_for()
        for block in page.locator('.playground').all():
            editor = block.locator('textarea')
            content = block.locator('[data-slot="code-block-content"]')
            copy = block.locator('[data-slot="code-block-header"] [data-slot="code-block-copy-button"]')
            assert copy.count() == 1
            assert copy.evaluate('e => e.scrollWidth <= e.clientWidth'), 'Le bouton Copier est tronqué'
            assert block.locator('[data-slot="code-block-header"]').get_by_role('button', name='Exécuter').count() == 1
            editor.fill('package main\n' + '\n'.join('line%02d abcdefghijklmnopqrstuvwxyz 0123456789' % i for i in range(35)))
            content.locator('[data-slot="code-block-line"]').last.wait_for()
            assert content.locator('[data-slot="code-block-line"]').count() == 36
            geometry = block.evaluate('''b => {
              const e=b.querySelector('textarea'), c=b.querySelector('[data-slot="code-block-content"] code');
              let a=getComputedStyle(e), z=getComputedStyle(c);
              return ['fontFamily','fontSize','fontWeight','lineHeight','letterSpacing','tabSize'].map(k => [k,a[k],z[k]]);
            }''')
            assert all(a == b for _, a, b in geometry), geometry
            editor.evaluate('e => {e.scrollTop=250; e.scrollLeft=120; e.dispatchEvent(new Event("scroll"))}')
            scroll = block.evaluate('''b => {let e=b.querySelector('textarea'), p=b.querySelector('[data-slot="code-block-content"]'); return [e.scrollTop,p.scrollTop,e.scrollLeft,p.scrollLeft]}''')
            assert abs(scroll[0]-scroll[1]) < 1 and abs(scroll[2]-scroll[3]) < 1, scroll
            editor.scroll_into_view_if_needed()
            editor.evaluate('e => {e.scrollTop=0; e.scrollLeft=0; e.dispatchEvent(new Event("scroll"))}')
            page.wait_for_timeout(100)
            # Click after a known visible glyph in the rendered mirror. The native
            # textarea must put its insertion point at the same source offset.
            line = content.locator('[data-slot="code-block-line"]').nth(1).locator('[data-slot="code-block-line-content"]')
            rect = line.evaluate('''e => {const r=document.createRange(); r.setStart(e.firstChild, 6); r.setEnd(e.firstChild, 7); const b=r.getBoundingClientRect(); return {x:b.right-0.2,y:(b.top+b.bottom)/2}}''')
            page.mouse.click(rect['x'], rect['y'])
            assert editor.evaluate('e => e.selectionStart') == len('package main\n') + 7
            if width in (390, 1440):
                source = 'package main\nimport "fmt"\nfunc main() { fmt.Println(42) }'
                editor.fill(source)
                block.get_by_role('button', name='Copier le code').click()
                assert page.evaluate('navigator.clipboard.readText()') == source
                block.get_by_role('button', name='Exécuter').click()
                block.locator('output').get_by_text('42', exact=True).wait_for(timeout=45000)
        page.close()
        print('PASS editor geometry and scrolling', width)
    browser.close()

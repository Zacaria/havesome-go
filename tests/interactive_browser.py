"""Real browser checks for the local Wasm exercises and responsive guide."""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

url = sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:18768/'
with sync_playwright() as p:
    browser = p.chromium.launch(executable_path='/usr/bin/brave-browser', headless=True, args=['--no-sandbox'])
    for width in (320, 390, 800, 1440):
        page = browser.new_page(viewport={'width': width, 'height': 900}, reduced_motion='reduce')
        errors = []
        page.on('pageerror', lambda error: errors.append(str(error)))
        assert page.goto(url, wait_until='load').status == 200
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), f'overflow {width}'
        for name in ('atelier', 'architecture', 'ecosysteme', 'senior'):
            page.locator('nav a[href="#' + name + '"]').click()
            assert page.evaluate('location.hash') == '#' + name
        assert page.locator('pre code .keyword').count() > 0
        page.locator('.playground [data-slot=code-block-header]').first.wait_for()
        assert page.locator('.playground [data-slot=code-block-content] .keyword').count() > 0
        if width == 390:
            page.goto(url + '#atelier')
            editor = page.locator('#code-valeur')
            editor.focus()
            assert page.evaluate('document.activeElement.id') == 'code-valeur'
            editor.fill('package main\nimport "fmt"\nfunc main() { fmt.Println(7 * 6) }')
            page.locator('.playground').first.get_by_role('button', name='Exécuter').click()
            page.locator('.playground').first.locator('output').get_by_text('42', exact=True).wait_for(timeout=45000)
            editor.fill('package main\nfunc main() { x := }')
            page.locator('.playground').first.get_by_role('button', name='Exécuter').click()
            page.locator('.playground').first.locator('output').get_by_text('Erreur :', exact=False).wait_for(timeout=45000)
            other = page.locator('.playground').nth(1)
            other.get_by_role('button', name='Exécuter').click()
            other.locator('output').get_by_text('Erreur : nom requis', exact=False).wait_for(timeout=45000)
            other.locator('textarea').fill('package main\nimport "fmt"\nfunc main() { fmt.Println("modifié") }')
            other.get_by_role('button', name='Exécuter').focus()
            page.keyboard.press('Enter')
            other.locator('output').get_by_text('modifié', exact=True).wait_for(timeout=45000)
            editor.fill('package main\nimport "net/http"\nfunc main() { _, _ = http.Get("https://example.com") }')
            page.locator('.playground').first.get_by_role('button', name='Exécuter').click()
            page.locator('.playground').first.locator('output').get_by_text('Erreur :', exact=False).wait_for(timeout=45000)
            editor.fill('package main\nfunc main() { for {} }')
            page.locator('.playground').first.get_by_role('button', name='Exécuter').click()
            page.locator('.playground').first.locator('output').get_by_text('Temps limite atteint', exact=False).wait_for(timeout=45000)
            assert page.locator('.playground').first.get_by_role('button', name='Exécuter').is_enabled()
            page.screenshot(path=str(Path.home() / '.hermes/profiles/builder/cache/scratch/hsg-interactive-mobile.png'))
        assert not errors, errors
        print(f'PASS {width}px : navigation, coloration, absence de débordement' + (', exécution éditée, erreur et clavier' if width == 390 else ''))
        page.close()
    fallback = browser.new_page(java_script_enabled=False)
    fallback.goto(url)
    assert fallback.locator('#code-valeur').evaluate("e => getComputedStyle(e).webkitTextFillColor") != 'rgba(0, 0, 0, 0)'
    fallback.close()
    fallback = browser.new_page()
    fallback.route('**/code-block.bundle.js', lambda route: route.abort())
    fallback.goto(url)
    assert fallback.locator('#code-valeur').evaluate("e => getComputedStyle(e).webkitTextFillColor") != 'rgba(0, 0, 0, 0)'
    fallback.close()
    failure = browser.new_page()
    failure.route('**/engine.wasm', lambda route: route.abort())
    failure.goto(url)
    failure.locator('.playground').first.get_by_role('button', name='Exécuter').click()
    failure.locator('.playground').first.locator('output').get_by_text('Impossible d’exécuter', exact=False).wait_for(timeout=15000)
    assert failure.locator('.playground').first.get_by_role('button', name='Exécuter').is_enabled()
    failure.close()
    print('PASS fallback : code visible sans JavaScript ou si le script échoue ; échec de téléchargement signalé')
    browser.close()

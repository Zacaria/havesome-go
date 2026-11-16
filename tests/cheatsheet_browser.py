from playwright.sync_api import sync_playwright, expect
import sys
url = sys.argv[1].rstrip('/') if len(sys.argv) > 1 else 'http://127.0.0.1:18766'
with sync_playwright() as p:
    browser = p.chromium.launch(executable_path='/usr/bin/brave-browser',headless=True,chromium_sandbox=True)
    for width in (320,390,700,701,800,1440):
        context=browser.new_context(viewport={'width':width,'height':900},permissions=['clipboard-read','clipboard-write'])
        page=context.new_page()
        errors=[]
        page.on('pageerror',lambda e:errors.append(str(e)))
        for path in ('/','/fiche.html'):
            response=page.goto(url+path,wait_until='networkidle')
            assert response.status==200
            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), (width,path,page.evaluate('document.documentElement.scrollWidth'))
            for region in ('header','footer'):
                assert page.locator(region+' a[href="https://github.com/Zacaria/havesome-go"]').count()==1
            if path=='/':
                assert page.locator('header a[href="fiche.html"]').is_visible()
                assert page.locator('footer a[href="fiche.html"]').count()==1
            else:
                assert page.locator('.sheet-hero img').evaluate('(i) => i.complete && i.naturalWidth > 0')
                for ident in ('declarations', 'fonctions', 'collections', 'flux', 'types', 'erreurs', 'concurrence-syntaxe'):
                    assert page.locator('.sheet-index a[href="#' + ident + '"]').count() == 1
                    block = page.locator('#' + ident + ' [data-slot="code-block"]')
                    assert block.count() == 1
                    content = block.locator('[data-slot="code-block-content"]')
                    assert content.evaluate('e => e.scrollWidth <= e.clientWidth'), (width, ident)
                    copy = block.get_by_role('button', name='Copier le code')
                    assert copy.evaluate('e => e.scrollWidth <= e.clientWidth')
                    copy.click()
                    assert page.evaluate('navigator.clipboard.readText()') == block.locator('[data-slot="code-block-content"]').inner_text()
                for command in ('go run .', 'go fmt ./...', 'go mod tidy', 'go doc fmt.Println', 'go test ./...', 'go test -race ./...', 'go vet ./...', 'go build ./...'):
                    button = page.locator('button[data-copy="' + command + '"]')
                    button.focus()
                    page.keyboard.press('Enter')
                    expect(page.locator('[role=status]')).to_have_text('Commande copiée.')
                    assert page.evaluate('navigator.clipboard.readText()') == command
                page.screenshot(path='/home/hermes/.hermes/profiles/builder/cache/scratch/go-sheet-%s.png'%width,full_page=True)
        assert not errors,errors
        print('PASS',width,'guide + fiche, no overflow, links, image and clipboard')
        context.close()
    fallback = browser.new_page(java_script_enabled=False, viewport={'width': 320, 'height': 900})
    fallback.goto(url + '/fiche.html')
    assert fallback.locator('pre[data-go-example]').count() == 7
    assert fallback.evaluate('document.documentElement.scrollWidth <= innerWidth')
    assert fallback.locator('#collections pre').evaluate('e => e.scrollWidth <= e.clientWidth')
    fallback.close()
    browser.close()

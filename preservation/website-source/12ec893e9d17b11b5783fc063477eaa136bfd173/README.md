# HaveSome Go

Guide francophone pour développeurs expérimentés : notions, choix de conception, écosystème et pratiques junior/senior. Les explications restent consultables sans JavaScript.

## Expérience et exécution

La navigation, les cartes et les schémas privilégient des parcours courts ; les détails restent dans le guide. Les exemples interactifs utilisent Yaegi, un interpréteur Go exécuté dans un Web Worker local avec WebAssembly : il ne s’agit pas du compilateur officiel et il ne prend pas en charge tout Go. Aucun code n’est envoyé à un serveur pour être exécuté ; les ressources du site sont toutefois téléchargées à l’ouverture. Le worker est interrompu après un délai limité. N’exécutez que du code de confiance.

Le gopher et son icône sont des illustrations de Renee French, non modifiées, issues de `https://go.dev/doc/gopher/frontpage.png` et `https://go.dev/doc/gopher/favicon.svg` et distribuée sous CC BY 4.0 (`https://go.dev/doc/gopher/README`). Les licences de Yaegi et Go sont dans `licenses/` ; les sources techniques sont liées depuis le guide. Le site est publié sur https://havesome-go.vercel.app/ par déploiement Vercel manuel ; la branche n’est pas reliée automatiquement à la production.

## Vérifier localement

Depuis ce dossier : `python3 -m unittest discover -s tests`, puis `python3 -m http.server`. Régénérer les extraits depuis la page avec `python3 tests/extract_examples.py`, puis exécuter `go -C examples test -race ./...`, `go -C examples vet ./...` et `go -C examples build ./...`.

Le moteur WebAssembly est généré à partir des sources épinglées du dossier `playground` avec `go -C playground generate ./...` ; il faut une installation Go et un accès au proxy de modules pour la première compilation. Les artefacts générés ne sont pas suivis par Git et doivent être reconstruits avant la vérification navigateur et le déploiement.

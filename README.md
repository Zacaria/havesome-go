# HaveSome Go

Guide francophone pour développeurs expérimentés : notions, choix de conception, écosystème et pratiques junior/senior. Les explications restent consultables sans JavaScript.

## Expérience et exécution

La navigation, les cartes et les schémas privilégient des parcours courts ; les détails restent dans le guide. Les exemples interactifs utilisent Yaegi, un interpréteur Go exécuté dans un Web Worker local avec WebAssembly : il ne s’agit pas du compilateur officiel et il ne prend pas en charge tout Go. Aucun code n’est envoyé à un serveur pour être exécuté ; les ressources du site sont toutefois téléchargées à l’ouverture. Le worker est interrompu après un délai limité. N’exécutez que du code de confiance.

Le gopher et son icône sont des illustrations de Renee French, non modifiées, issues de `https://go.dev/doc/gopher/frontpage.png` et `https://go.dev/doc/gopher/favicon.svg` et distribuée sous CC BY 4.0 (`https://go.dev/doc/gopher/README`). Le logo Gin-Gonic non modifié est de Javier Provecho, avec les yeux du gopher de Renee French : source `https://github.com/gin-gonic/logo`, licence CC BY 4.0 pour le logo (yeux : CC BY 3.0 selon la source). Il identifie le framework Gin sans suggérer une affiliation. Les licences de Yaegi et Go sont dans `licenses/` ; les sources techniques sont liées depuis le guide. Le site est publié sur https://havesome-go.vercel.app/ par déploiement Vercel statique manuel. Ce dépôt dédié n’est pas relié au projet Vercel : y pousser du code ne met pas le site à jour. Un nouveau déploiement exige une action explicite sur le projet existant.

La navigation indique la dernière section ayant atteint la ligne de lecture et reste accessible pendant le défilement sur mobile. Les exemples statiques utilisent le composant React Code Block officiel de shadcn/ui, adapté aux couleurs du guide ; les ateliers Yaegi restent modifiables et exécutables. Sans JavaScript, les exemples restent lisibles et le sommaire reste utilisable.

Pour construire les blocs : `npm ci --workspaces=false && npm run build --workspaces=false` dans ce dossier. Le composant est issu du registre officiel shadcn/ui (base-nova) ; ses imports et libellés ont été adaptés à cette page statique sans Tailwind. Le fichier construit `code-block.bundle.js` est un artefact non suivi et doit être présent pour le déploiement.

## Vérifier localement

Depuis ce dossier : `python3 -m unittest discover -s tests`, puis `python3 -m http.server`. Régénérer les extraits depuis la page avec `python3 tests/extract_examples.py`, puis exécuter `go -C examples test -race ./...`, `go -C examples vet ./...` et `go -C examples build ./...`.

Le moteur WebAssembly est généré à partir des sources épinglées du dossier `playground` avec `GOFLAGS=-buildvcs=false go -C playground generate ./...` ; il faut Go 1.27.4 et un accès au proxy de modules pour la première compilation. L’option désactive l’inclusion des métadonnées Git et permet de reproduire les octets du moteur actuellement publié. Les artefacts générés ne sont pas suivis par Git et doivent être reconstruits avant la vérification navigateur et le déploiement.

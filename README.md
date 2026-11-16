# HaveSome Go

Guide francophone pour développeurs expérimentés : notions, choix de conception, écosystème et pratiques junior/senior. Les explications et le code initial restent consultables sans JavaScript. La fiche `fiche.html` réunit les principes, des exemples de syntaxe Go autonomes et les commandes courantes en texte sélectionnable. Ses exemples sont extraits et exécutés par les tests ; les sorties attendues sont vérifiées avec Go.

## Développement

Prérequis : Node.js 24.11 ou plus récent, npm et Go 1.27.4. Depuis la racine :

```sh
npm ci --workspaces=false
GOFLAGS=-buildvcs=false go -C playground generate ./...
npm run dev
```

Ouvrez l'URL locale affichée par Vite+. Le moteur est généré depuis les sources épinglées de `playground` ; la première compilation nécessite l'accès au proxy Go. `GOFLAGS` évite d'inclure les métadonnées Git dans le binaire. Les fichiers `engine.wasm` et `wasm_exec.js` sont générés, non suivis ; ils sont indispensables aux ateliers et au build.

Vite+ est installé localement, sans modifier la CLI ou le runtime globaux. Les overrides npm suivent ses versions de Vite et Vitest ; les maintenir alignées avec `npm exec -- vp toolchain vitest` lors d'une mise à jour. Les composants Code Block et Button proviennent du registre officiel shadcn/ui, style base-nova ; leurs imports, libellés et styles ont été adaptés à l'identité du guide. Code Block affiche le code coloré ; un textarea natif accessible superposé permet l'édition. Il ne s'agit pas d'un éditeur shadcn prêt à l'emploi.

## Construire et vérifier

```sh
npm run build
npm run check
python3 -m unittest discover -s tests
python3 -m http.server 39523 --bind 127.0.0.1 --directory dist
```

Dans un autre terminal, avec Brave et Playwright Python installés :

```sh
for test in browser progress_browser cheatsheet_browser editor_browser interactive_browser; do
  python3 "tests/$test.py" http://127.0.0.1:39523/
done
```

Les scripts utilisent Brave en mode headless avec son sandbox. Adapter le chemin `/usr/bin/brave-browser` dans les scripts si nécessaire. Pour vérifier les exemples Go, régénérer les extraits avec `python3 tests/extract_examples.py`, puis lancer `go -C examples test -race ./...`, `go -C examples vet ./...` et `go -C examples build ./...`. Les tests du moteur se lancent avec `go -C playground test ./...`.

## Contribuer et publier

Proposez une modification dans une branche et une pull request sur [le dépôt HaveSome Go](https://github.com/Zacaria/havesome-go). Vérifiez les commandes ci-dessus et les parcours concernés, notamment la navigation, la copie et les deux ateliers sur mobile et ordinateur. Les commandes de la fiche s'exécutent dans un module Go de confiance et peuvent lancer du code de test.

Le site existant est publié sur https://havesome-go.vercel.app/ par déploiement Vercel statique manuel ; ce dépôt n'est pas relié au projet Vercel, donc un push ne publie pas le site. Après revue et vérification de l'absence de publication concurrente, publier le contenu complet de `dist/` sur le projet existant, puis contrôler les pages, liens et ateliers publics. Ne pas publier les sources ou un build sans moteur WebAssembly.

## Exécution et crédits

Les exemples interactifs utilisent Yaegi, interpréteur Go exécuté dans un Web Worker local avec WebAssembly : ce n'est pas le compilateur officiel et tout Go n'est pas pris en charge. Aucun code n'est envoyé à un serveur pour être exécuté ; les ressources du site sont téléchargées à l'ouverture. Le worker est interrompu après un délai limité. N'exécutez que du code de confiance. La copie de la fiche nécessite l'accès au presse-papiers ; sinon, sélectionnez le texte.

Le gopher et son icône sont des illustrations non modifiées de Renee French, issues de https://go.dev/doc/gopher/frontpage.png et https://go.dev/doc/gopher/favicon.svg et distribuées sous CC BY 4.0 (https://go.dev/doc/gopher/README). Le logo Gin-Gonic non modifié est de Javier Provecho, avec les yeux du gopher de Renee French : source https://github.com/gin-gonic/logo, licence CC BY 4.0 pour le logo (yeux : CC BY 3.0 selon la source). Il identifie Gin sans suggérer une affiliation. Les licences de Yaegi et Go sont dans `licenses/`.

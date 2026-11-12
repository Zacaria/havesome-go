# HaveSome Go

Guide francophone autonome pour développeurs expérimentés. La lecture suit une requête de service : philosophie, valeurs et types, API et erreurs, concurrence, outils, production et choix de conception. Chaque chapitre relie les décisions à des sources officielles ; les contrastes junior/senior décrivent des pratiques, pas des personnes.

## Choix

- HaveSome TOML et OIDC sont des applications statiques Vite publiées sur GitHub Pages après vérification. HaveSome Memory est une lecture native statique, publiée de la même manière. HaveSome Rust est une présentation Reveal publiée avec Surge.
- Ce guide privilégie une lecture native et séquentielle sans JavaScript ni installation côté lecteur ; navigation par ancres, exemples lisibles et sources directement liées. Palette papier/encre et bleu Go, sans reprendre les mécanismes interactifs propres aux autres sujets.
- Code conservé comme application autonome dans le dépôt HaveSomeCode existant sur une branche de travail. Le site public est disponible sur https://havesome-go.vercel.app/ : il est publié sur Vercel par déploiement statique manuel. La branche n'est pas reliée automatiquement à la production ; toute mise à jour du site nécessite un nouveau déploiement explicite.

## Vérifier localement

Depuis ce dossier : `python3 -m unittest discover -s tests`, puis servir le dossier avec `python3 -m http.server`. Régénérer les extraits exacts depuis la page avec `python3 tests/extract_examples.py`, puis exécuter `go -C examples test -race ./...`, `go -C examples vet ./...` et `go -C examples build ./...`. La page est elle-même le livrable statique : aucune compilation n'est nécessaire.

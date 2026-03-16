# Guide pour l'Assistant Visuel (Visual Companion)

Ceci est l'outil visuel basé sur un navigateur permettant de générer en direct et d'exposer des maquettes, des schémas interactifs et des options esthétiques durant la phase de Brainstorming.

## Quand l'utiliser

Il convient de prendre la décision de l'utiliser **pour chaque question individuellement** et non pas globalement pour la session.
La question clé à se poser : **L'utilisateur comprendra-t-il mieux cette alternative en la voyant plutôt qu'en la lisant ?**

**Utilise le navigateur web** lorsque le contenu à valider est intrinsèquement purement visuel :
- **Maquettes UI (Mockups)** — wireframes, de positionnements, l'architecture UI (Navbar, fil d'Ariane, disposition en grille) 
- **Diagrammes architecturaux** — flux et cycles de données, composant systèmes, relationnels DB
- **Comparatifs visuels** — faire le choix direct entre deux approches de colorimétrie, deux styles esthétiques ou UX
- **Affinement de design (Polish)** — positionnement subtile, espaces (paddings/margins), hiérarchie visuelle
- **Statuts Spatiaux complexes** — organigrammes visuels.

**Utilise le terminal classique** si le contenu est textuel, factuel ou tabulaire :
- **Périmètres et concepts de demande** — "Est-ce que cette fonctionnalité est à faire ?" ou questions descriptives
- **Choix Conceptuels (A/B/C)** — choisir la méthode d'approche qui se décrit avec des mots et de la logique pure
- **Tableaux et liste "Avantages / Inconvénients"** — les compromis se lisent très bien pour un développeur.
- **Toute décision technique pure** — Modélisation API, base de données, langage à utiliser...

## Comment fonctionne l'outil ?

Le composant technique est un serveur local embarqué dans les scripts locaux (`../scripts/`) qui boucle l'observation d'un dossier racine où les fichiers `HTML` fraîchement créés par toi-même (agent) seront instantanément actualisés sur le navigateur ouvert par l'utilisateur. Lors des interactivités (clics, séléctions d'options générées), une trace est laissée sous forme JSON et tu récupère l'information dans ton prochain tour.

**Important (Fragments vs Documents complets) :**
Dès que tu écris dans le fichier HTML servi quelques bribes HTML basiques (ex: `<h2>Option A</h2>`), le système du serveur enveloppe automatiquement avec toutes les dépendances standards, CSS global et mécanismes JS ("Frame template"). Écris donc UNIQUEMENT ce que veut cibler ton choix. Produit un document brut (avec `<html` ou `<!DOCTYPE`) **exclusivement** si tu as expressément la nécessité d'assumer tout le contexte CSS absolu de la page.

## Démarrer une session (le Serveur)

**Via les scripts copiés dans `../scripts/` de la compétence :**

Lance une commande avec ton outil système (Bash / Terminal).

```bash
# Lance le service en persistant la vue vers le projet souhaité:
../scripts/start-server.sh --project-dir /chemin/absolu/vers/le/projet
```

**Retour attendu:**
Il te délivrera une connexion formattée en JSON (Port Web, URI, Dossier Ecran cible). Demande vite à l'utilisateur d'ouvrir le lien. C'est l'URI locale.

- Si lancé en arrière-plan, tu as une copie Json d'état de vie disponible dans le dossier de rendu (`.superpowers/brainstorm/`).
- Attention pour les environnements qui forcent l'extinction, utilise `--foreground` lors de la commande de démarrage.

## La Boucle d'action de l'Agent

1. **Vérifie la vitalité du serveur** :
   Le fichier statut doit exister. Sinon, relance. Crée ou modifie un fichier HTML qui ira dans le dossier d'observation (la propriété "Screen Dir" donnée par l'outil server). Par ex `layout-v1.html`, modifie-le **uniquement** avec un outil de type `write_to_file`. **Evite à tout prix les redirections lourdes par des "écho" shell qui embourbent le terminal d'inutilités visuelles**. Ne nomme jamais plusieurs fois les fichiers pareils dans le cycle (laisse exister `v2`, `v3`, `v4`... en créant des nouveaux et non remplaçant un acquis).

2. **Délivre la balle au répondant** :
   Dis simplement "Je vous montre 3 options d'ergonomie, jetez un oeil sur le navigateur. (Rappel lien). Validez le choix qui vous intéresse ou commentez ici."

3. **Ton prochain tour de boucle** :
   Check le fichier `.events` généré en cache. C'est du JSON, parsé à la volée. Ajoute cette logique aux requêtes tapées par l'humain dans son chat.

4. **Itère jusqu'aux validations adéquates de chaque étape.**

## Exemples HTML Rapides (CSS Inclus par défaut)

Tu as des options prédéfinies :

**Options QCM à cliquer (Options Multiples si l'attribut `data-multiselect` est lié à `.options` ) :**
```html
<div class="options">
  <div class="option" data-choice="a" onclick="toggleSelect(this)">
    <div class="letter">A</div>
    <div class="content"><h3>Super Option A</h3><p>C'est cool</p></div>
  </div>
</div>
```

**Maquettes (Split 50/50 possible via `.split` global)*:**
```html
<div class="mockup">
  <div class="mockup-header">Aperçu Footer</div>
  <div class="mockup-body">
    <!-- ton code HTML imbriqué visuellement ici -->
  </div>
</div>
```

**Eléments d'interface fictifs préconçus** :
- `<div class="mock-nav"></div>` : NavBar rapide
- `<div class="mock-sidebar"></div>` : Sidebar
- `<div class="mock-content"></div>` : Body
- `<button class="mock-button"></button>`
- `<input class="mock-input">`
- `<div class="placeholder"></div>`

## Clôturer la Session (Clean Up)

Stoppe le processus du serveur quand le brainstorming du composant nécessite d'être totalement clôturé via ton exécuteur shell `stop-server.sh`.

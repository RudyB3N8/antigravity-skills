# Aura.build Assistant Skill 🚀

Cette compétence permet d'automatiser le flux de travail avec l'IA de conception web **Aura.build** au sein de Google Antigravity. Elle vous aide à rédiger des prompts parfaitement alignés avec la charte graphique de votre projet et à nettoyer/convertir le code exporté.

## 📁 Structure de la compétence

```text
aura-build-assistant/
├── SKILL.md                 # Instructions de la compétence pour Antigravity
├── README.md                # Cette documentation humaine
└── scripts/
    └── import-code.py       # Script d'extraction, nettoyage et structuration
```

## 🛠️ Installation et Prérequis

Le script d'importation utilise uniquement les bibliothèques standard de **Python 3** (`html.parser`, `re`, `zipfile`, `urllib`, etc.). Il n'y a donc aucune dépendance externe à installer.

Le dossier temporaire `./aura-imports/` sera créé automatiquement à la racine de votre projet lors du premier import.

## 💡 Utilisation

### 1. Générer le fichier `DESIGN.md` pour Aura.build
Demandez simplement à Antigravity :
> *"Génère un fichier DESIGN.md pour mon projet."*
L'IA analysera vos fichiers de style locaux et créera un document résumant vos polices, couleurs et espacements. Vous pourrez le copier et le charger dans Aura.build, puis le référencer via `@DESIGN.md` pour forcer la cohérence visuelle.

### 2. Importer du code exporté (HTML ou ZIP)
1. Téléchargez votre page ou composant depuis Aura.build.
2. Renommez le fichier selon son rôle (ex : `contact-form.html` ou `landing-page.zip`).
3. Glissez-déposez le fichier dans le dossier `./aura-imports/` à la racine de votre projet.
4. Demandez à Antigravity :
   > *"Importe le fichier contact-form.html en mode SCSS"* (ou Tailwind).
5. Vos fichiers propres et convertis seront générés sous `./aura-imports/output/<nom-du-composant>/`.

## ⚙️ Détail du script d'importation

Le script effectue automatiquement les actions suivantes :
- **Extraction des ZIP** : Décompresse les packages multi-pages ou de composants.
- **Nettoyage HTML** : Supprime les scripts de tracking, les éditeurs interactifs injectés par Aura et les commentaires inutiles.
- **Mode Tailwind** : Sauvegarde le HTML épuré avec ses classes utilitaires intactes.
- **Mode SCSS** :
  - Analyse toutes les classes Tailwind et les styles en ligne.
  - Génère un fichier HTML propre avec des classes sémantiques.
  - Crée une feuille de style `.scss` structurée avec les sélecteurs correspondants prêts à être personnalisés.
- **Nettoyage du workspace** : Supprime automatiquement le fichier d'origine de `./aura-imports/` après traitement.

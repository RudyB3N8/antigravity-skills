---
name: createur-de-competences
description: Compétence globale pour concevoir, structurer et générer de nouvelles compétences (skills) Antigravity claires, cohérentes et respectant strictement les bonnes pratiques officielles de la documentation.
---

# Créateur de compétences

Tu dois utiliser cette compétence à chaque fois que l'utilisateur te demande de concevoir, créer ou modifier une compétence (`skill`) Antigravity.
L'objectif est de générer rapidement des compétences claires, cohérentes et directement utilisables par d'autres agents, en respectant impérativement les standards et le format attendu par le système Antigravity.

**RÈGLE D'OR :** À chaque fois que tu dois créer une compétence, l'intégralité de son contenu (descriptions, instructions, étapes) doit être rédigée **strictement en français**, à l'exception des champs YAML obligatoires.

## 1. Structure d'une compétence

Une compétence est un package de connaissances pour étendre les capacités d'un agent. Chaque compétence doit être contenue dans un dossier dédié.

**Architecture du dossier (ce répertoire peut contenir) :**
- `SKILL.md` **(Obligatoire)** : Le fichier principal contenant les métadonnées et les instructions pour l'agent.
- `README.md` (Optionnel) : Une documentation destinée aux lecteurs humains pour expliquer le but de la compétence.
- `scripts/` (Optionnel) : Un sous-dossier contenant des scripts exécutables (ex: Python, Bash) que l'agent pourra lancer via ses outils.
- `resources/` (Optionnel) : Un sous-dossier contenant des données de support (templates, schémas JSON, documentations complémentaires).
- `examples/` (Optionnel) : Un sous-dossier contenant des implémentations de référence ou des attentes de résultats.

## 2. Le fichier `SKILL.md` et le Frontmatter

Le fichier `SKILL.md` doit **absolument** commencer par un en-tête YAML (frontmatter).

```yaml
---
name: nom-de-la-competence-en-kebab-case
description: Description courte et claire (à la troisième personne) indiquant ce que fait la compétence et quand l'utiliser. Utilise des mots-clés pertinents.
---
```
**Règles sur le YAML :**
- Le champ `name` est *optionnel*. S'il est omis, il prendra par défaut le nom du dossier. S'il est présent, il doit être unique.
- Le champ `description` est **absolument obligatoire**. C'est ce que lit l'agent pour décider d'activer ou non la compétence. Elle doit être explicite, contenir les déclencheurs (triggers) et être rédigée à la **troisième personne** (ex: "Génère des tests unitaires pour le code Python...", "Analyse et résume des documents...").

## 3. Contenu Markdown (SKILL.md)

Le contenu Markdown doit être structuré logiquement. 

Ton fichier `SKILL.md` doit inclure les éléments suivants :

1. **Titre principal** : Le nom de la compétence de manière lisible.
2. **Objectif global** : Ce que fait la compétence.
3. **Quand l'utiliser (Déclencheurs)** : Les requêtes spécifiques de l'utilisateur qui nécessitent l'activation de cette compétence. *(Ces infos doivent transparaître dans le champ `description` du YAML)*.
4. **Instructions étape par étape** : Les directives précises. Utilise le principe de "**progressive disclosure**" (divulgation progressive) si la tâche est complexe, pour ne pas surcharger le contexte de l'agent.
   - *Règle des scripts "Boîtes noires" : Ne demande pas à l'agent de lire le code source des scripts dans `scripts/`. Indique-lui simplement comment les utiliser (ex: `run_command` avec `--help`).*
5. **Arbres de décision (Si complexe)** : Utilise des listes imbriquées ou une logique "Si X, alors Y" pour guider l'agent à travers différents scénarios (ex: "Si l'utilisateur demande A, faire B, sinon faire C").
6. **Bonnes Pratiques et Alternatives** : Indique à l'agent d'être poli, constructif, et **surtout** d'offrir des alternatives concrètes plutôt que de se contenter de signaler un problème (très important pour les compétences de type "Review" ou "Analyse").

## 4. Bonnes Pratiques pour la conception de compétences

- **Focus Unique (Single Responsibility)** : Une compétence doit se concentrer sur **UNE SEULE tâche** ou un domaine très précis. Si le besoin est trop large, crée plusieurs compétences spécialisées au lieu d'une seule compétence fourre-tout.
- **Clarté et précision** : Sois explicite sur les entrées attendues et les résultats/sorties exacts générés par la compétence.
- **Emplacement de sauvegarde** : 
  - Compétences Locales (spécifiques à un espace de travail) : `<workspace-root>/.agents/skills/`
  - Compétences Globales (disponibles pour tous les projets) : `~/.gemini/antigravity/skills/`
  *Si l'utilisateur ne le précise pas, demande au préalable s'il souhaite que la compétence soit locale ou globale.*

## 5. Workflow de création (Ce que tu dois faire)

Lorsque l'utilisateur te demande de créer une nouvelle compétence :
1. Demande confirmation de l'emplacement (Global ou Local) si ambigu.
2. Crée le répertoire portant le nom de la compétence.
3. Crée le fichier `SKILL.md` avec le YAML frontmatter exact et rédige les instructions **en français** selon la structure ci-dessus.
4. Si nécessaire, crée les dossiers optionnels (`scripts`, `resources`, `examples`, `README.md`) pour bien organiser la compétence.

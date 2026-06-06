---
name: planification
description: "Conçoit un plan d'implémentation détaillé pour une tâche complexe en plusieurs étapes, en générant les artefacts natifs d'Antigravity 2.0 (implementation_plan.md, task.md) avant d'écrire ou de modifier du code."
---

# Écriture de Plans ("Planification")

## Vue d'ensemble

Rédige des plans d'implémentation exhaustifs en partant du principe que le développeur qui exécutera le plan n'a aucun contexte préalable de la base de code. Tu dois absolument tout documenter pour lui de manière granulaire et méthodique : quels fichiers toucher pour chaque tâche exacte, quel code écrire, quelles commandes de test lancer, comment vérifier que cela fonctionne.

Le plan d'implémentation sous Antigravity 2.0 s'appuie sur la génération et la gestion des artefacts de planification natifs situés dans le répertoire de la conversation :
1. `<appDataDir>/brain/<conversation-id>/implementation_plan.md` : Document d'architecture et de conception globale soumis à validation.
2. `<appDataDir>/brain/<conversation-id>/task.md` : Liste de tâches (TODO) granulaires pour suivre la progression de l'implémentation.
3. `<appDataDir>/brain/<conversation-id>/walkthrough.md` : Document de synthèse récapitulant les changements effectués et les validations après exécution.

Pratiques de développement à imposer dans tout plan :
- **DRY (Don't Repeat Yourself)** : Pas de duplication inutile.
- **YAGNI (You Aren't Gonna Need It)** : Ne pas coder de fonctionnalités superflues ou non demandées.
- **TDD (Test Driven Development)** : Écrire d'abord le test unitaire ou d'intégration, vérifier son échec, implémenter le minimum de code requis pour le faire passer au vert, puis committer.
- **Commits fréquents et granulaires** : Committer après chaque sous-étape validée.

**Annonce de démarrage :**
> "J'utilise la compétence de `planification` pour initialiser le plan d'implémentation natif d'Antigravity 2.0."

---

## 1. Vérification du périmètre (Scope Check)

Si la demande initiale couvre plusieurs sous-systèmes indépendants et massifs, propose de diviser le travail en plusieurs plans distincts (un plan par sous-système). Chaque plan doit aboutir à un composant logiciel fonctionnel et testable individuellement.

---

## 2. Structure et rédaction de `implementation_plan.md`

Crée le fichier `<appDataDir>/brain/<conversation-id>/implementation_plan.md` en utilisant obligatoirement le format d'artefact natif suivant :

```markdown
# [Description globale de l'Objectif]

[Description textuelle claire du problème, contexte et de ce que la modification va accomplir]

## User Review Required

[Décisions d'architecture critiques, dépendances à introduire, ou changements cassants qui nécessitent l'attention de l'utilisateur. Utiliser des alertes GitHub de type > [!IMPORTANT], > [!WARNING] ou > [!CAUTION]]

## Open Questions

[Questions en suspens influençant la conception ou l'implémentation. Utiliser des alertes GitHub pour les points bloquants]

## Proposed Changes

[Grouper les fichiers à modifier par composant (package, zone fonctionnelle) et séparer les composants par des lignes de séparation `---`. Utiliser la scheme `file:///` pour rendre tous les liens vers les fichiers cliquables dans l'IDE]

### [Nom du Composant]

#### [NEW / MODIFY / DELETE] [nom_du_fichier](file:///chemin/absolu/vers/fichier)
[Résumé précis et détaillé des modifications qui seront apportées à ce fichier]

## Verification Plan

### Automated Tests
- Commandes exactes pour exécuter les tests automatisés (ex: `pytest tests/path/test_file.py`, `npm run test`, etc.)

### Manual Verification
- Instructions détaillées pour que l'utilisateur ou l'agent vérifie manuellement le comportement (ex: déploiement en local, navigation sur une page spécifique, saisie de données de test, etc.)
```

---

## 3. Décomposition des tâches dans `task.md`

Crée le fichier de suivi `<appDataDir>/brain/<conversation-id>/task.md` avec une liste de tâches élémentaires (représentant chacune 2 à 5 minutes de développement pour un humain ou un prompt pour un agent).
Utilise la syntaxe standard :
- `- [ ]` pour les tâches non commencées
- `- [/]` pour les tâches en cours
- `- [x]` pour les tâches terminées

### Modèle de tâche TDD
Pour chaque tâche impliquant l'écriture ou la modification de logique de code, structure-la de la manière suivante dans `task.md` :

```markdown
- [ ] Tâche N : [Nom du composant cible]
  - Fichiers impactés : [chemin_fichier](file:///chemin/absolu)
  - [ ] Étape 1 : Écrire le test unitaire/intégration qui doit échouer
  - [ ] Étape 2 : Lancer le test pour valider l'échec (Commande : `...` -> Sortie attendue : `...`)
  - [ ] Étape 3 : Écrire l'implémentation minimale requise pour faire passer le test
  - [ ] Étape 4 : Relancer le test pour valider le succès (Commande : `...` -> Sortie attendue : `...`)
  - [ ] Étape 5 : Effectuer le commit Git (`git commit -m "..."`)
```

---

## 4. Choix de l'approche et boucle de révision

Avant de soumettre le plan finalisé à la validation de l'utilisateur, tu DOIS lui demander s'il souhaite activer la vérification automatisée par un sous-agent IA :

1. **Poser la question :**
   > "Souhaitez-vous activer la révision automatisée du plan par un sous-agent IA ? (Par défaut, le plan sera soumis directement à votre validation humaine)."
   
2. **Si l'utilisateur accepte la révision automatisée :**
   - Délègue la vérification de `implementation_plan.md` et `task.md` à un sous-agent de relecture en lui passant le prompt défini dans [plan-document-reviewer-prompt.md](file:///home/rudybn/.gemini/config/skills/planification/resources/plan-document-reviewer-prompt.md).
   - Si le sous-agent retourne des problèmes (❌), corrige-les directement dans les fichiers d'artefacts puis relance l'évaluation jusqu'à obtenir la mention "✅ Validé".
   - Limite : Ne dépasse pas 5 boucles d'erreurs enchaînées avant de demander de l'aide à l'humain.
   
3. **Si l'utilisateur refuse ou par défaut (validation directe) :**
   - Présente le plan en activant l'attribut `request_feedback = true` dans les métadonnées de l'artefact `implementation_plan.md` pour déclencher le processus natif de validation d'Antigravity 2.0.

---

## 5. Transition vers l'exécution

Une fois le plan d'implémentation validé par l'utilisateur (humainement ou après révision IA) :
- Initialise la phase d'exécution.
- Indique à l'utilisateur :
  > "Le plan d'implémentation est approuvé. Je démarre l'exécution des tâches détaillées dans `task.md`."
- Mets à jour rigoureusement `task.md` au fil de tes modifications (en passant les statuts à `[/]` puis `[x]`).
- Rédige et mets à jour `walkthrough.md` une fois l'implémentation achevée pour consigner les résultats des validations.

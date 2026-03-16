---
name: planification
description: "À utiliser lorsque tu disposes d'une spécification ou des exigences pour une tâche complexe en plusieurs étapes, AVANT de toucher au moindre code ou fichier."
---

# Écriture de Plans ("Planification")

## Vue d'ensemble

Rédige des plans d'implémentation exhaustifs en partant du principe que le développeur qui exécutera le plan n'a absolument **aucun contexte** de la base de code, ni un bon "flair" naturel. Tu dois absolument tout documenter pour lui de manière granulaire et méthodique : quels fichiers toucher pour chaque tâche exacte, quel code écrire, quels tests, comment vérifier que cela fonctionne, quelle documentation lire.

Sers-lui le plan complet découpé en toutes petites tâches (Bite-Sized Tasks).
Pratiques à imposer : DRY (Don't Repeat Yourself), YAGNI (You Aren't Gonna Need It), TDD (Test Driven Development) et Commits fréquents.
Assume qu'il est un développeur chevronné mais qu'il ne sait rien de notre conception de tests, de notre domaine d'application ou de nos bibliothèques.

**Annonce de démarrage :** "J'utilise la compétence de `planification` pour créer le plan d'implémentation."

**Où sauvegarder :** Les plans doivent être sauvegardés dans `docs/superpowers/plans/AAAA-MM-JJ-<nom-fonctionnalite>.md`
- (Sauf indication contraire et préférences explicites de l'utilisateur).

## Vérification du périmètre (Scope Check)

Si la spécification initiale couvre plusieurs sous-systèmes indépendants et énormes, le Brainstorming aurait dû les séparer. Si ce n'est pas le cas, propose ici de diviser la demande en **plusieurs plans distincts** — un par sous-système. Chaque plan doit aboutir à un composant logiciel fonctionnel et testable par lui-même, pas la moitié d'un tout inutilisable.

## Structure de fichiers (Verrouillage)

Avant de lister les tâches, indique d'abord quels fichiers seront créés ou modifiés et quelle sera la responsabilité de chacun. C'est ici que l'architecture et la décomposition se figent.

- Conçois des unités avec des frontières claires et des interfaces définies. Chaque fichier doit répondre d'une **seule** responsabilité.
- Privilégie les petits fichiers précis plutôt que les énormes monstres inmaintenables. Il vaut mieux de petites unités.
- Les fichiers modifiés conjointement doivent habiter ensemble, par fonctionnalité et non par calque technique pur si possible.
- Sur du code existant, respecte les normes en place, mais propose une cassure (refactor par extraction) si le fichier devient horriblement long.

## Granularité des Tâches (Bite-Sized Tasks)

**Chaque étape est UNE action (2 à 5 minutes humaines / 1 prompt IA) :**
- "Écrire le test unitaire qui échoue" - étape 1
- "Lancer le test pour voir qu'il échoue (TDD)" - étape 2
- "Écrire l'implémentation minimale requise pour faire passer ce test" - étape 3
- "Relancer le/les tests pour vérifier le vert" - étape 4
- "Committer" - étape 5

## En-tête du Plan (Header obligatoire)

**CHAQUE plan DOIT obligatoirement commencer par cet en-tête exact :**

```markdown
# Plan d'Implémentation : [Nom de la fonctionnalité]

> **Pour l'Exécuteur :** REQUIS : Utilisez des listes de cases à cocher (`- [ ]`) pour valider les étapes sans brûler les étapes.

**Objectif :** [Une seule phrase qui décrit le but de cette construction]

**Architecture :** [2 ou 3 phrases sur l'approche technique exacte choisie]

**Stack / Technos :** [Librairies et/ou conventions à utiliser impérativement]

---
```

## Structure d'une Tâche

````markdown
### Tâche N : [Nom du composant cible]

**Fichiers impactés :**
- Création : `chemin/exact/vers/fichier.py`
- Modification : `chemin/exact/existant.js:123-145`
- Test : `tests/chemin/exact/vers/test.py`

- [ ] **Étape 1 : Écrire le test qui doit échouer**

```python
def test_specific_behavior():
    result = function(input)
    assert result == expected
```

- [ ] **Étape 2 : Lancer le test pour validation d'échec**

Action : `pytest tests/path/test.py::test_name -v`
Résultat attendu : ÉCHEC "function not defined"

- [ ] **Étape 3 : Écrire l'implémentation minimale**

```python
def function(input):
    return expected
```

- [ ] **Étape 4 : Lancer le test pour validation du succès**

Action : `pytest tests/path/test.py::test_name -v`
Résultat attendu : SUCCÈS (PASS)

- [ ] **Étape 5 : Effectuer le Commit**

```bash
git add tests/path/test.py src/path/fichier.py
git commit -m "feat: ajout de la fonctionnalité specifique"
```
````

## Mémos obligatoires
- Spécifie systématiquement les **chemins exacts et absolus/relatifs pertinents**.
- Rédige le code COMPLET nécessaire de l'étape dans le plan (Évite le "Ajoute une validation ici").
- Donne les commandes exactes de terminal pour valider (avec le retour shell attendu).
- N'oublie pas : DRY, YAGNI, TDD, Commits rapides.

## Boucle de révision du plan (Examen)

Après avoir rédigé chaque grand bloc ou bloc complet (Chunk) de plan :

1. Délègue le sous-agent de vérification du plan fourni dans `resources/plan-document-reviewer-prompt.md`. Fixe bien le contexte du document de base et de ton plan, pas ton esprit de fonctionnement (session data).
   - Fournir : Contenu du Chunk et chemin vers la Spec validée en amont.
2. S'il y a des ❌ "Problèmes Constatés" :
   - Corrige les soucis directement dans ce chunk spécifique.
   - Relance le délégataire d'examen sur le même bloc.
   - Boucle jusqu'à "✅ Validé".
3. Si c'est "✅ Validé" : Passe à la rédaction du chunk suivant, ou finalise si c'était le dernier.

**Limites de "Chunk" :** Un bloc (`## Chunk N`) ne doit jamais faire plus de 1000 lignes.
**Guide de révision :** L'agent qui écrit est celui qui corrige. Au bout de 5 boucles d'erreurs enchaînées ou de désaccords de l'expert, demande de l'aide à l'humain. Sois capable d'expliquer pourquoi tu ignores un faux positif s'il te l'impose.

## Transition / Fin (Prêt à l'exécution)

Après la sauvegarde confirmée du document de plan parfait :

**"Le plan d'implémentation est achevé, vérifié et sauvegardé au chemin `docs/superpowers/plans/<filename>.md`. Êtes-vous prêt pour l'exécution ?"**

L'utilisateur devra prendre le relais avec la compétence appropriée ou te donner le feu vert pour entrer en Phase d'Éxécution de Plan (`EXECUTION`) avec son accord implicite.

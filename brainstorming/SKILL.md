---
name: brainstorming
description: "À utiliser obligatoirement AVANT tout travail créatif - création de fonctionnalités, construction de composants, ajout de logiques, ou modification de comportements. Permet d'explorer l'intention de l'utilisateur, les exigences et le design avant l'implémentation."
---

# Générer des idées vers des Designs (Brainstorming)

Cette compétence permet de transformer des idées vagues en designs complets et en spécifications grâce à un dialogue collaboratif naturel avec l'utilisateur.

Commence par assimiler le contexte actuel du projet, puis pose des questions une par une pour affiner l'idée. Une fois que tu as compris ce que tu vas construire, présente le design et obtiens la validation de l'utilisateur.

**HARD-GATE / LIMITE STRICTE :**
N'invoque ABSOLUMENT AUCUNE compétence d'implémentation, n'écris SURTOUT PAS de code, ne mets en place aucun système et ne prends STRICTEMENT AUCUNE action d'implémentation AVANT d'avoir présenté un design complet et obtenu la validation claire de l'utilisateur. Cela s'applique à CHAQUE projet, quelle que soit son apparente simplicité.

## Anti-Pattern : "C'est trop simple pour nécessiter un design"

Tout projet doit passer par ce processus. Une liste de tâches à faire, un utilitaire ne nécessitant qu'une fonction, un changement de configuration — tous y passent. "Les petits projets simples" sont ceux où les hypothèses non examinées causent le plus de perte de temps. Le design peut être court (quelques phrases pour un sujet très basique), mais tu DOIS le présenter et obtenir une validation de l'utilisateur.

## Checklist (Étapes obligatoires)

Tu DOIS créer une tâche (`task.md`) comportant chacun des points suivants et les compléter séquentiellement :

1. **Explorer le contexte du projet** — lis les fichiers, la documentation, les commits récents.
2. **Proposer l'assistant visuel (Visual Companion)** — (si la discussion portera sur des notions visuelles) : tu dois faire ton offre dans un message isolé, non combiné avec des questions de clarification. Voir la section « Assistant Visuel » plus bas.
3. **Poser des questions de clarification** — une question à la fois, pour comprendre l'objectif, les contraintes et les critères de succès.
4. **Proposer 2 à 3 approches possibles** — avec leurs avantages, inconvénients (trade-offs) et ta propre recommandation.
5. **Présenter le design finalisé** — section par section selon la complexité ; obtiens l'approbation de l'utilisateur après chaque section.
6. **Rédiger le document de conception (Spec)** — sauvegarde sous `docs/superpowers/specs/AAAA-MM-JJ-<sujet>-design.md` et commit.
7. **Boucle de révision de la spécification** — délègue un sous-agent de révision avec un contexte précis (jamais tout ton historique de session) ; corrige les problèmes remontés et boucle (max 5 fois, au-delà, demande l'intervention humaine). Utilise les directives fournies dans `resources/spec-document-reviewer-prompt.md`.
8. **Révision humaine** — demande à l'utilisateur de valider le fichier de spécification écrit avant de passer à l'étape finale.
9. **Transition vers l'implémentation** — active obligatoirement la compétence de planification (`planification`) pour générer le plan basé sur la spécification.

## Arbre de Décision Global

- **SI** la demande décrit plusieurs sous-systèmes indépendants (ex: "un site e-commerce avec chat, stockage web, paiement direct et analytique") : **ALORS** arrête immédiatement et aide l'utilisateur à découper ce vaste objectif en plusieurs sous-projets indépendants. Réalisez un brainstorming focalisé sur le PREMIER sous-projet.
- **SI** la demande évoque des options visuelles (UI, maquettes, schémas) : **ALORS** tu dois demander à l'utilisateur s'il accepte d'utiliser l'outil `Visual Companion` (une demande seule, attendre sa réponse). Voir le guide complet dans `resources/visual-companion.md`.
- **SI** l'utilisateur a approuvé l'approche finale : **ALORS** rédige la Spécification et lance la boucle de révision par l'agent de test.
- **SI** l'utilisateur rejette une idée : **ALORS** demande plus de contexte, propose d'autres alternatives.
- **SI** le fichier de spec est final et validé par l'utilisateur : **ALORS** utilise la compétence de `planification` exclusivement.

## Bonnes Pratiques

**Compréhension fine de l'idée** :
- Pose une question à la fois.
- Préfère proposer des choix multiples / QCM quand c'est possible.
- Focalise sur les éléments de définition cruciaux : Pourquoi ? Quelles contraintes ? Quel critère de réussite définitif ?

**Exploration d'approches technologiques et design** :
- Propose systématiquement 2 à 3 options.
- Argumente pour chacune d'elle.
- Donne ton avis d'expert et oriente l'utilisateur avec ta recommandation.

**Isoler et structurer proprement** :
- Divise le système en petites unités qui ont chacune un but unique et clair.
- Pour chaque sous-ensemble du design, on doit pouvoir répondre à : "Que fait-il ?", "Comment l'utilise-t-on ?" et "De quoi dépend-il ?".
- Évite les gros blocs "fourre-tout".

**Réécriture en bases de code pré-existantes** :
- Explore toujours d'abord l'architecture existante.
- Inclus dans ton design les petites refactorisations structurelles qui sont logiquement liées à la nouvelle mise en place, mais ne propose PAS de refactorisation globale sans rapport.

## Assistant Visuel (Visual Companion)

Cet outil (un serveur de rendu Web) aide pour tous les cas de figure nécessitant une projection en interface (Mockups, wireframes, architectures...).

**Offrir l'assistant :**
> "Une partie de ce que nous concevons pourrait être plus simple à comprendre si je vous le montre dans un navigateur web. Je peux vous créer des maquettes et des diagrammes à la volée. Voulez-vous utiliser ce système ? (Cela demandera d'ouvrir une URL locale)"

**ATTENTION :** Ce message DOIT être posé SEUL. Ne le combine pas avec des descriptions ou d'autres questions. Attends l'accord. Si l’utilisateur refuse, reste dans le terminal.
Lis attentivement le manuel `resources/visual-companion.md` avant de lancer ou manipuler le serveur.

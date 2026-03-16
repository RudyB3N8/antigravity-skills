# Antigravity Skills

Bienvenue dans mon dépôt de compétences (skills) personnalisées pour **Google Antigravity**, l'assistant IA de codage.

Ce dépôt sert à stocker, versionner et partager les différentes compétences que je crée pour étendre les capacités d'Antigravity.

## 🚀 Compétences disponibles

*   **[Créateur de compétences (`createur-de-competences`)](./createur-de-competences/SKILL.md)** : Une compétence globale (méta-compétence) conçue pour aider Antigravity à concevoir, structurer et générer de nouvelles compétences de manière claire, cohérente et en respectant strictement les bonnes pratiques officielles de la documentation.

## 🛠️ Structure d'une compétence

Chaque compétence (skill) est stockée dans son propre dossier et contient au minimum :

*   `SKILL.md` : Le fichier principal contenant les instructions, le frontmatter YAML (nom, description) et le comportement attendu de l'agent.
*   (Optionnel) `scripts/` : Des scripts utilitaires pour étendre les capacités de la compétence.
*   (Optionnel) `examples/` : Des exemples d'implémentation ou de modèles pour guider l'agent (comme le `code-reviewer` dans le créateur de compétences).
*   (Optionnel) `resources/` : Des ressources supplémentaires (fichiers de configuration, templates, etc.).

## 💡 Comment utiliser ces compétences

Pour utiliser ces compétences avec votre propre instance d'Antigravity :

1.  Clonez ce dépôt dans votre dossier de compétences Antigravity (par défaut, il s'agit souvent de `<chemin_vers_appDataDir>/skills`).
2.  Assurez-vous qu'Antigravity a accès en lecture à ce dossier.
3.  Antigravity détectera automatiquement les dossiers contenant un fichier `SKILL.md` valide et pourra s'en servir lorsque le contexte de votre tâche s'y prêtera.

---
*Dépôt généré et maintenu avec l'aide d'Antigravity.*

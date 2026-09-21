# Git — règles globales

## A propos des commits

- Fait des Conventional Commits.
- Ne commit pas sans mon autorisation.

## ⛔️ Merge = accord explicite OBLIGATOIRE

**Ne JAMAIS merger une PR (ou une branche) vers `main` sans l'accord explicite de l'utilisateur, donné pour CETTE PR précise.**

- Un « push et merge » donné pour une PR ne vaut PAS autorisation pour les suivantes. Une autorisation de merge est **ponctuelle**, jamais permanente.
- Le workflow par défaut s'arrête à : commit → push (si autorisé) → ouvrir la PR → **STOP**. L'utilisateur review et décide du merge.
- Même pour une retouche d'une ligne, même si ça semble évident : la PR attend.

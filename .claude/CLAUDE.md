# kommit-perso

Ce dossier n'est pas un projet applicatif. Il existe pour héberger **ma configuration Claude Code personnelle** et englober les 2 repos du projet.

## Pourquoi il existe

Kommit est un projet **multi-repo** : le backend et le frontend sont deux repos totalement indépendants, avec des stacks différentes. Il ne s'agit pas d'un projet full-stack unique type Next.js.

Ma config Claude Code n'a pas sa place dans leurs repos : ce sont ceux de l'équipe, et mes préférences de travail ne les regardent pas. Elle vit donc ici, à l'échelle du projet, plutôt que dans `~/.claude` où elle s'appliquerait à tout le reste de la machine.

## Ce qui va dedans, et ce qui n'y va pas

**Y va** ce qui resterait vrai si je changeais de projet demain : la façon dont je veux qu'on me réponde, mes raccourcis, mes conventions d'écriture.

**N'y va pas** ce qui décrit ce code-là : la structure du backend, les conventions de nommage, les règles d'UI. Tout ça appartient à l'équipe et vit dans ses repos.

## Arborescence

```
kommit-perso/
├── .claude/
│   ├── CLAUDE.md      # ce fichier
│   ├── rules/         # mes règles de comportement
│   └── skills/        # mes skills
├── .vscode/
├── kommit-backend/    # repo de l'équipe
└── kommit-frontend/   # repo de l'équipe
```

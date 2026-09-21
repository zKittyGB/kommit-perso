---
name: recap
description: Re-place the user back into this repo's context by reading the latest handoff(s). Use when the user says "recap", "remets-moi dans le contexte", "où on en était", "reprends le contexte", "catch me up", or starts a fresh session and wants to resume where they left off.
---

## Entrée

- Les **derniers handoffs** du dossier `handoffs/` du repo courant.
- L'**état git réel** du repo : branche, `git status`, commits depuis le dernier handoff.

## Sortie

- Un **rappel de contexte** à l'écran : ticket actif, où on en était, état réel maintenant, prochaine action.
- La **liste des divergences** entre ce que le handoff annonçait et ce que le repo contient réellement.

---

Lis les derniers handoffs dans `handoffs/` (tri alpha = chronologique, pars du plus récent et remonte autant que nécessaire pour reconstituer le fil), puis **confronte-les à l'état git réel** avant de restituer. Si aucun handoff → propose les commits récents.

**Signale les vraies divergences** : travail décrit dans le handoff mais introuvable, branche inattendue, conflit, état contradictoire avec ce qui était annoncé. Une seule exception explicite : du travail « non commité » au moment du handoff qui est désormais commité est la **progression normale et attendue** entre deux sessions — **ne le mentionne JAMAIS comme un écart.** Tout le reste qui cloche, signale-le.

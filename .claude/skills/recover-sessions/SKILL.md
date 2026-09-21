---
name: recover-sessions
description: Restaure une ou plusieurs sessions Claude Code supprimées via le skill delete-sessions (elles sont dans ~/.Trash, pas perdues). Utiliser quand l'utilisateur veut récupérer, restaurer ou annuler la suppression d'une conversation : "récupère cette session", "restaure la conversation que j'ai supprimée", "annule la suppression".
---

## Entrée
Un mot-clé optionnel pour filtrer les sessions présentes dans la corbeille (nom de projet, ou texte présent dans l'aperçu). Sans rien fourni, propose toutes les sessions actuellement dans `~/.Trash`.

## Sortie
Confirmation des session(s) restaurée(s) (aperçu + chemin de destination), ou le menu si aucune sélection n'a encore été validée par l'utilisateur.

---

## Comment faire

**Règle bloquante** : ne jamais exécuter le `mv` de restauration (étape 3) pour un fichier sans un appel `AskUserQuestion` **résolu dans ce même tour**, dont le résultat désigne explicitement ce fichier. Une confirmation donnée plus tôt dans la conversation — sur un autre sujet, un autre fichier, ou même « oui » à une proposition générale — ne vaut jamais validation ici. Aucune inférence, aucune extrapolation d'une intention passée. Sans résultat frais et explicite du menu, ne rien restaurer.

1. **Lister les sessions présentes dans la corbeille** en réutilisant le script du skill `delete-sessions` (ne pas le dupliquer), avec `--use-ctime` pour que le temps relatif reflète le moment de la suppression (et non l'activité de la conversation elle-même). Le script est à `../delete-sessions/scripts/list_sessions.py` **relativement au dossier de base de ce skill**, celui donné au chargement — ne jamais coder ce chemin en dur, le skill peut être installé ailleurs que dans `~/.claude/skills/` :
   ```bash
   python3 <dossier-de-base-du-skill>/../delete-sessions/scripts/list_sessions.py --use-ctime ~/.Trash
   ```
   Sortie : une ligne par fichier `<temps relatif>\t<taille>\t<nb messages user>\t<chemin>\t<aperçu>\t<ACTIVE ou vide>`, triée de la plus récente à la plus ancienne. Ignorer la colonne `ACTIVE` ici (sans objet dans la corbeille).

2. **Toujours présenter la liste via l'outil `AskUserQuestion`** (menu à choix, jamais une question en texte libre), avec `multiSelect: true` pour permettre de restaurer plusieurs sessions d'un coup. Une option par fichier : label = temps relatif (supprimé il y a X) + intitulé court, description = aperçu + taille + nombre de messages + nom de fichier.
   - Minimum 2 options exigé par l'outil : s'il ne reste qu'un seul fichier, ajouter une option factice « Aucune, ne rien restaurer ».
   - Si la corbeille ne contient aucun `.jsonl`, le dire directement sans ouvrir de menu.

3. **Pour chaque fichier sélectionné, retrouver son dossier projet d'origine** via le champ `cwd` enregistré dans les lignes de la conversation :
   ```bash
   grep -o '"cwd":"[^"]*"' "<fichier>" | head -1 | sed -E 's/"cwd":"(.*)"/\1/'
   ```
   Convertir ce chemin en nom de dossier mangled (remplacer `/` par `-`), recréer le dossier `~/.claude/projects/<mangled>/` s'il n'existe plus, puis déplacer le fichier avec `mv` (pas `cp`) de `~/.Trash` vers ce dossier, en conservant son nom actuel.
   - Si aucun `cwd` n'est trouvable (fichier stub sans conversation réelle), le signaler à l'utilisateur et ne pas deviner une destination.

4. **Restaurer directement** dès la sélection dans le menu, et seulement à ce moment-là — pas besoin de redemander une seconde confirmation après coup, mais la sélection fraîche du menu (étape 2) reste un préalable obligatoire, jamais optionnel. Puis confirmer ce qui a été restauré (aperçu + chemin de destination final).

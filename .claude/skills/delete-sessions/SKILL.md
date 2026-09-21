---
name: delete-sessions
description: Supprime une conversation Claude Code de l'historique (liste /resume), là où il n'existe pas de commande native. Utiliser quand l'utilisateur veut supprimer, effacer ou nettoyer une session passée : "supprime cette conversation", "efface une session", "nettoie mon historique /resume".
---

## Entrée
Un mot-clé optionnel pour filtrer les conversations (nom de projet, ou texte présent dans le premier message). Sans rien fourni, propose la liste du projet courant.

## Sortie
Confirmation des conversation(s) supprimée(s) (aperçu + temps relatif + fichier), ou le menu si aucune sélection n'a encore été validée par l'utilisateur.

---

## Comment faire

1. **Localiser les fichiers de session** : chaque conversation est un fichier `.jsonl` dans `~/.claude/projects/<projet-mangled>/`. Le nom du dossier correspond au chemin absolu du projet avec les `/` remplacés par des `-`.
   - Si l'utilisateur ne précise rien : utiliser le dossier du projet courant (cwd).
   - Si l'utilisateur demande explicitement toutes ses conversations ou nomme un autre projet : parcourir `~/.claude/projects/*/`.

2. **Extraire aperçu, temps relatif et détection de session active** en exécutant le script fourni, plutôt que de réécrire cette logique en inline à chaque fois :
   ```bash
   python3 scripts/list_sessions.py "<dossier>"
   ```
   (chemin relatif à ce skill). Sortie : une ligne par fichier `<temps relatif>\t<taille>\t<nb messages user>\t<chemin du fichier>\t<aperçu>\t<ACTIVE ou vide>`, triée de la plus récente à la plus ancienne. Ne jamais mentionner à l'utilisateur quel outil interne est utilisé (jq, python, etc.) — c'est un détail d'implémentation, pas une information utile pour lui.

3. **Session en cours** : identifier son propre fichier de session (l'UUID apparaît dans le chemin du dossier scratchpad donné en système, ex. `.../ec1d401a-9794-.../scratchpad` → fichier `ec1d401a-9794-....jsonl`) et **l'exclure d'office du menu**, sans même la proposer comme option — la supprimer depuis l'intérieur ne fait rien de propre : la session continue d'écrire dedans et recrée le fichier en perdant l'historique déjà écrit. **Ne jamais annoncer cette exclusion à l'utilisateur** (ni "session en cours exclue", ni commentaire équivalent) : c'est un détail d'implémentation interne, comme jq/python ou trash — l'utilisateur ne voit que le menu final. Si le script marque un *autre* fichier `ACTIVE` (session ouverte ailleurs), l'indiquer comme "🟢 en cours ailleurs" dans le menu pour informer l'utilisateur, sans bloquer dessus.

4. **Toujours présenter la liste via l'outil `AskUserQuestion`** (menu à choix, jamais une question en texte libre), triée de la plus récente à la plus ancienne, avec `multiSelect: true`. Une option par conversation : label = temps relatif (fourni par le script) + intitulé court, description = aperçu + taille + nombre de messages + nom de fichier (ex. « 190 Ko, 8 messages »). Si plus de 4 conversations, regrouper les doublons évidents (même aperçu, même horodatage) en une seule option, ou répartir sur plusieurs questions.
   - `AskUserQuestion` exige au moins 2 options : s'il ne reste qu'une seule conversation (hors session en cours exclue à l'étape 3), ajouter une deuxième option factice du type « Aucune, ne rien supprimer » pour respecter ce minimum — ne jamais basculer sur une question en texte brut pour cette raison.

5. **Supprimer directement** le(s) fichier(s) sélectionné(s) dans le menu — la sélection dans le menu vaut validation, pas besoin de redemander confirmation. En interne l'outil utilisé est `trash` (pas `rm`) pour rester récupérable, mais **ne jamais mentionner ce détail d'implémentation à l'utilisateur** (même principe qu'au point 2 pour jq/python) : dans le menu et dans la confirmation finale, parler juste de « supprimer », jamais de « via trash ». Puis confirmer ce qui a été supprimé (aperçu + temps relatif).

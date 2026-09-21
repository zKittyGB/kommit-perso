#!/usr/bin/env bash
# Supprime des sessions Claude Code (.jsonl) sans passer par Claude Code.
# Usage:
#   delete-sessions            -> sessions du projet courant (dossier courant)
#   delete-sessions <dossier>  -> sessions d'un projet précis (chemin absolu du projet, pas le dossier ~/.claude/projects/...)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECTS_ROOT="$HOME/.claude/projects"

mangle() {
  echo "$1" | sed 's/\//-/g'
}

if [ -n "${1:-}" ]; then
  DIRS=("$PROJECTS_ROOT/$(mangle "$1")/")
else
  DIRS=("$PROJECTS_ROOT/$(mangle "$PWD")/")
fi

MAPFILE_OUT=$(python3 "$SCRIPT_DIR/list_sessions.py" "${DIRS[@]}")

if [ -z "$MAPFILE_OUT" ]; then
  echo "Aucune session trouvée."
  exit 0
fi

declare -a REL_TIMES
declare -a SIZES
declare -a COUNTS
declare -a PATHS
declare -a PREVIEWS
declare -a ACTIVES

i=0
while IFS=$'\t' read -r rel size count path preview active; do
  REL_TIMES[$i]="$rel"
  SIZES[$i]="$size"
  COUNTS[$i]="$count"
  PATHS[$i]="$path"
  PREVIEWS[$i]="$preview"
  ACTIVES[$i]="$active"
  i=$((i+1))
done <<< "$MAPFILE_OUT"

echo "Sessions trouvées :"
echo
for idx in "${!PATHS[@]}"; do
  n=$((idx+1))
  marker=""
  [ "${ACTIVES[$idx]}" = "ACTIVE" ] && marker=" 🟢 en cours"
  fname=$(basename "${PATHS[$idx]}")
  printf "%2d) %-14s %-8s %-4s msg  %s%s\n" "$n" "${REL_TIMES[$idx]}" "${SIZES[$idx]}" "${COUNTS[$idx]}" "${PREVIEWS[$idx]:-(sans apercu)}" "$marker"
  printf "     %s\n" "$fname"
done

echo
read -rp "Numéros à supprimer (ex: 1 3 5), vide pour annuler : " -a CHOICES

if [ "${#CHOICES[@]}" -eq 0 ]; then
  echo "Annulé."
  exit 0
fi

TO_DELETE=()
for c in "${CHOICES[@]}"; do
  if ! [[ "$c" =~ ^[0-9]+$ ]] || [ "$c" -lt 1 ] || [ "$c" -gt "${#PATHS[@]}" ]; then
    echo "Numéro invalide ignoré : $c"
    continue
  fi
  idx=$((c-1))
  if [ "${ACTIVES[$idx]}" = "ACTIVE" ]; then
    read -rp "⚠️  ${PATHS[$idx]} est une session en cours. Confirmer la suppression ? (o/N) " confirm
    [[ "$confirm" =~ ^[oOyY]$ ]] || { echo "Ignoré : ${PATHS[$idx]}"; continue; }
  fi
  TO_DELETE+=("${PATHS[$idx]}")
done

if [ "${#TO_DELETE[@]}" -eq 0 ]; then
  echo "Rien à supprimer."
  exit 0
fi

for f in "${TO_DELETE[@]}"; do
  trash "$f"
  echo "Supprimé : $(basename "$f")"
done

#!/usr/bin/env python3
"""Liste les sessions Claude Code (.jsonl) d'un ou plusieurs dossiers projet, triées de la plus récente à la plus ancienne.

Usage: list_sessions.py [--limit N] [--use-ctime] <dossier> [<dossier> ...]

--use-ctime : le temps relatif est calculé sur la date de dernier changement du
fichier (ctime) plutôt que sur le timestamp de la conversation elle-même.
Utile pour lister une corbeille : ctime y reflète le moment où le fichier y a
été déplacé (donc le moment de la suppression), pas l'activité de la
conversation.

Sortie (une ligne par fichier, colonnes séparées par des tabulations) :
  <temps relatif>\t<taille>\t<nb messages user>\t<chemin complet du fichier>\t<aperçu du premier message user>\t<ACTIVE ou vide>
"""
import json
import os
import subprocess
import sys
import time


def relative_time(epoch, now):
    delta = now - epoch
    if delta < 60:
        return "à l'instant"
    if delta < 3600:
        return f"il y a {int(delta // 60)} min"
    if delta < 86400:
        return f"il y a {int(delta // 3600)} h"
    return f"il y a {int(delta // 86400)} j"


def format_size(num_bytes):
    if num_bytes < 1024:
        return f"{num_bytes} o"
    kb = num_bytes / 1024
    if kb < 1024:
        return f"{kb:.0f} Ko"
    return f"{kb / 1024:.1f} Mo"


def collect_dir(directory, use_ctime=False):
    entries = []
    for fname in os.listdir(directory):
        if not fname.endswith(".jsonl"):
            continue
        path = os.path.join(directory, fname)
        preview = None
        epoch = None
        message_count = 0

        with open(path, "r", errors="ignore") as fh:
            for line in fh:
                try:
                    obj = json.loads(line)
                except (json.JSONDecodeError, ValueError):
                    continue
                if obj.get("type") == "user" and obj.get("message", {}).get("role") == "user":
                    content = obj["message"].get("content")
                    if isinstance(content, str):
                        text = content
                    elif isinstance(content, list):
                        text = " ".join(
                            c.get("text", "") for c in content
                            if isinstance(c, dict) and c.get("type") == "text"
                        )
                    else:
                        text = ""
                    text = text.strip()
                    if text:
                        message_count += 1
                        if preview is None:
                            preview = text.replace("\n", " ")[:80]
                            ts = obj.get("timestamp")
                            if ts:
                                try:
                                    epoch = time.mktime(
                                        time.strptime(ts.split(".")[0], "%Y-%m-%dT%H:%M:%S")
                                    ) - time.timezone
                                except ValueError:
                                    epoch = None

        try:
            size = os.path.getsize(path)
        except OSError:
            size = 0

        if use_ctime:
            try:
                epoch = os.stat(path).st_ctime
            except OSError:
                epoch = None

        try:
            lsof_out = subprocess.run(
                ["lsof", path], capture_output=True, text=True
            ).stdout
            active = bool(lsof_out.strip())
        except (OSError, subprocess.SubprocessError):
            active = False

        entries.append((epoch, path, preview, active, size, message_count))
    return entries


def main():
    args = sys.argv[1:]
    limit = None
    use_ctime = False
    while args and args[0].startswith("--"):
        if args[0] == "--limit":
            limit = int(args[1])
            args = args[2:]
        elif args[0] == "--use-ctime":
            use_ctime = True
            args = args[1:]
        else:
            break
    directories = args or ["."]

    now = time.time()
    results = []
    for directory in directories:
        results.extend(collect_dir(directory, use_ctime=use_ctime))

    results.sort(key=lambda x: (x[0] is not None, x[0] or 0), reverse=True)
    if limit:
        results = results[:limit]

    for epoch, path, preview, active, size, message_count in results:
        rel = relative_time(epoch, now) if epoch else "date inconnue"
        marker = "ACTIVE" if active else ""
        print(f"{rel}\t{format_size(size)}\t{message_count}\t{path}\t{preview}\t{marker}")


if __name__ == "__main__":
    main()

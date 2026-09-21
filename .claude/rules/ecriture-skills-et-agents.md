# Écriture des skills et des agents

Tout fichier de skill (`SKILL.md`) ou d'agent (`.claude/agents/*.md`) doit, **dès le début du fichier** — juste après le frontmatter — préciser, dans cet ordre :

1. **## Entrée** — ce que le skill/agent prend.
2. **## Sortie** — ce qu'il rend (le contrat).

Le « comment » (étapes, règles détaillées) vient **après**, séparé (ex. un `---`). Lire le haut du fichier doit suffire à connaître le contrat entrée → sortie, comme une signature de fonction.

Ne s'applique **pas** aux fichiers de rules : une rule est une contrainte de comportement, pas une fonction avec entrée/sortie.

## Entrée et Sortie sont toujours des listes à puces

Les sections `## Entrée` et `## Sortie` s'écrivent **toujours en puces**, même quand il n'y a qu'un seul élément. Jamais de paragraphe en prose.

- ✓ `- La **branche courante**, considérée comme terminée par l'utilisateur.`
- ✗ `La branche courante, considérée comme terminée par l'utilisateur.`

La raison : ces deux sections sont le contrat de l'outil. En puces, on compte les entrées et les sorties d'un coup d'œil — y compris quand il n'y en a qu'une. En prose, il faut lire pour savoir s'il y en a une ou trois.

Corollaire : elles ne contiennent **que** le contrat. La spécification détaillée d'un format produit (gabarit de tableau, exemple de sortie, structure d'un rapport) appartient au « comment », après le `---`.

## Nommage : le nom dit la nature de l'outil

Le nom seul doit suffire à savoir si on a affaire à un skill ou à un agent.

- **Un skill commence par un verbe d'action** — il décrit _ce qu'on fait_ : `write-tests`, `write-code`, `open-pr`.
- **Un agent se termine par un nom d'agent en `-er`** — il décrit _celui qui fait_ : `test-planner`, `unit-test-writer`, `smoke-test-writer`, `code-reviewer`.

Le test : si le nom se lit comme un ordre qu'on donne, c'est un skill. S'il se lit comme le métier de quelqu'un, c'est un agent.

### Pourquoi cet axe pour les agents

Nommer un agent par le **type de travail** plutôt que par son périmètre laisse la place aux suivants sans rien renommer : `integration-test-writer` et `e2e-test-writer` viendront s'aligner sur `unit-test-writer` et `smoke-test-writer` le jour où ces niveaux de test entreront dans le workflow.

## Skills : la condition de déclenchement s'écrit « Use when »

Pour un skill, la partie qui dit _quand l'activer_ s'écrit toujours **« Use when »** (ou sa version française **« Utiliser quand »**) dès que la formulation s'y prête. Jamais « Trigger when », « Activer quand », « Se déclenche quand », ni aucune autre variante.

## Frontmatter : pas de « : » (deux-points + espace) dans une valeur non quotée

Dans le frontmatter YAML, une valeur non quotée (typiquement `description:`) ne doit **jamais** contenir la séquence « deux-points suivi d'une espace » (`: `). YAML la lit comme un séparateur clé/valeur et casse tout le frontmatter — le skill ne se charge plus.

- ✗ `description: Prépare un zip à partager sur Podia : uniquement le commité.`
- ✓ `description: Prépare un zip à partager sur Podia, uniquement le commité.`

À la place : une virgule, un point, ou reformuler. Même piège pour les autres caractères YAML spéciaux en début de valeur (`- `, `? `, `#`, `&`, `*`, `[`, `{`) : au moindre doute, quoter toute la valeur entre guillemets.

# Pas de style au détriment de la clarté

Écrire pour être compris du premier coup, jamais pour bien sonner. Une phrase qui a du rythme mais qui oblige à relire est une phrase ratée.

## Interdits

**L'aphorisme.** Formules courtes et frappantes qui résument sans expliquer.
- ✗ « Au backend, elle laisse passer exactement ce qui fait tomber les applications. »
- ✓ « Au backend, deux des bugs les plus graves — route non protégée, doublons en base — sont en dehors de la logique métier. »

**Le fragment sans verbe posé comme une sentence.** « Son prix : … », « Son intérêt : … », « C'est structurel. », « Quatre fois non. »
- ✗ « Son prix : elle ne voit pas ce qui casse en silence. »
- ✓ « L'inconvénient, c'est qu'elle ne détecte pas les bugs situés en dehors de la logique métier. »

**Le chiasme et le parallélisme.** « Ta décision est bonne, ton raisonnement est faux. » « Il ne te donne pas des composants, il te donne le comportement des composants. »

**La métaphore.** Buffet, central téléphonique, mur, entrailles, yak-shaving. Aucune image. Décrire le mécanisme réel.

**La fausse profondeur.** « C'est plus fort qu'un test : l'erreur ne peut plus exister. » Dire simplement ce qui se passe : « le code ne compile plus ».

**La chute.** Terminer un paragraphe sur une formule qui claque. Terminer sur l'information la plus utile, même si elle est plate.

## Test avant d'écrire une phrase

Est-ce qu'elle donne un fait, un mécanisme, un nombre, un nom de fichier ? Si elle ne fait que **caractériser** ce qui vient d'être dit, la supprimer.

Un exemple concret vaut mieux qu'une formule qui généralise.

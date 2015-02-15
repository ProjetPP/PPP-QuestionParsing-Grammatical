renommer fichiers/fonctions (simplify, 

revoir l'ajout d'info selon qw:
  - seul le verbe peut déjà contenir l'info ?
  - on peut référencer les verbs qui contiennent l'info
  - il faut ajouter un nouveau triplet parfois (how fast ??)
  - comment faire cette opération alors qu'on veut éviter les alternatives ?

Algo de nounification:
  - lors de analyse de l'arbre avec R0, R1...
  - fonction buildPredicate qui prend une liste de Word en entrée : 
   > si la liste contient un seul mot + verbe : utiliser les maps de double nounification (et lemmatization)
   > sinon : buildValue habituel après lemmatization
  - Renvoie une liste l à 2 éléments : l[0]: predicates, l[1] : reverse predicates

------------

les positions 1000, 1001 n'ont plus lieu d'être

processQuestionInfo : gestion des reverse, perte d'infos sur les triplets

fusions des prep : conserver Words distincts

enlever les règles qui produisent des prédicats arbres !

Who is Homer J. Simpson? > prq une liste dans prédicat

nettoyer les en-têtes

cf ex de https://github.com/ProjetPP/PPP-QuestionParsing-Grammatical/pull/106

What did Richard Feynman say upon hearing he would receive the Nobel Prize in Physics? >>> prep pas fusionnée définitivement

Where is Inoco based?

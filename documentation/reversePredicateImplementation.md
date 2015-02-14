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

-------------------------------------

(enlever tous les asserts inutiles à la fin)

dependencyTreeCorrection.py :
 - inchangé

dependencyTree.py : 
 - classe Word
 - classe DependenciesTree + ses fonctions de construction
 > fonction computeTree qui produit l'arbre identique au stanford parser (juste correctTree en +)
 >> QuotationHandler prend fin ici

preprocessingMerge.py : 
 - quotationHandler
 - merge sister-brother
 > fonction merge (pas quotation, donc seulement sister-brother pour l'instant)

dependencyAnalysis.py :
 - inchangé

questionWordProcessing.py :
 - une fonction qui extrait le qw (agit dans dependencyAnalysis.py)
 - une fonction qui place les types (agit dans dependencyAnalysis.py)
 - une fonction qui ajoute les infos (agit dans normalization.py) __TODO__

normalization.py :
 - buildPredicate cf ci-dessus (verbe -> renvoie 2 listes)
 - buildValue (list de Words -> renvoie
 - construction de l'arbre à la volée, en utilisant nounDB.py pour nounification (lemmatization aussi appliquée) __TODO__
 - enrichissement de l'arbre produit grâce au qw __TODO__
 - master fonction : normalFormProduction

------------

Quotation Start -> computeTree -> Quotation End -> preprocessingMerge -> simplify

les positions 1000, 1001 n'ont plus lieu d'être

processQuestionInfo : gestion des reverse, perte d'infos sur les triplets

fusions des prep : conserver Words distincts

enlever les règles qui produisent des prédicats arbres !

General
=======

* Yes/no question: product dobj relation?
* verb+ing: do sthg special (look POS tag)? : What did Richard Feynman say upon hearing he would receive the Nobel Prize in Physics?
* If nounification becomes powerful enough: use it to analyse superlative (biggest > size...)
* Multiple words : Where is Inoco based? > base + place = base place :(
* exists : is there -> idem au traitement des mots interrogatifs
* booléen : comment gérer les noeuds contenant plusieurs mots (synonymes)
* Article : enlever numéro apparaissant dans noeud (et idem pour arbre) / enlever encadrement
* data model : autoriser des listes de prédicats dans les sort ?
* réecrire demo3 pour le rendre dépendant de DependencyTree
* t5 peut être enlevé ?
* prepMerge: plus de merge parent/fils si conj dependency
* processQuestionWord doit être exécuter en dernier car ...
* les mots de position 1000 sont les connecteurs
* les mots de position 1001 sont les mots propagés/ajoutés par le qw
* Traiter "does" comme "be" (descendre dans l'arbre pour l'éviter) : Where does the prime minister of united kingdom live
* Dans le question word processing (et plus généralement) : les connecteurs ne sont pas uniquement les 1000. Les 1000 prennent les conj mais pas le superlatives.
* Traiter question word sur forme normalisée ? 
    >> garantir qu'en entrée de normalize chaque noeud contient une seule alternative
    >> ajout des infos sur les premières feuilles / prédicats / ...
    >> seul les prédicats peuvent contenir des alternatives > le garantir
* Vérifier que les positions/tag sont bien gérées (en particulier sur les alternatives)
* Ecrire des Readme ('bla bla'.split(' '))

Gestion des prep(c)_x
=====================

go -prep_to-> ... = go to -prep->
What is Frozen based on?

* What two US biochemists won the Nobel Prize in medicine in 1992?

https://github.com/ProjetPP/PPP-QuestionParsing-Grammatical/issues/72

Analyse du question word
========================

How many : placer en tête un opérateur de comptage
  > généraliser à tout les qw = juste ajouter un opérateur en tête
      who : identity
      when : date
      cas particulier de "be" > on ajoute l'info directement dans le noeud

Recherche de wexcept/id... : uniquement prefixe/suffixe (sunday ?)

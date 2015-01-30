General
=======

* Yes/no question: product dobj relation?
* verb+ing: do sthg special (look POS tag)? : What did Richard Feynman say upon hearing he would receive the Nobel Prize in Physics?
* If nounification becomes powerful enough: use it to analyse superlative (biggest > size...)
* Multiple words : Where is Inoco based? > base + place = base place :( >> en fait "base" se nounifie en "place" ?
* Article : enlever numéro apparaissant dans noeud (et idem pour arbre) / enlever encadrement
* data model : autoriser des listes de prédicats dans les sort ?
* réecrire demo3 pour le rendre dépendant de DependencyTree
* t5 peut être enlevé ?
* Dans le question word processing (et plus généralement) : les connecteurs ne sont pas uniquement les 1000. Les 1000 prennent les conj mais pas le superlatives.
* Travailler sur la forme normalisée? 
    >> garantir qu'en entrée de normalize chaque noeud contient une seule alternative
    >> ajout des infos sur les premières feuilles / prédicats / ...
    >> traiter les mots interrogatifs (ajout d'infos...)
    >> seul les prédicats peuvent contenir des alternatives > le garantir
* Recherche de wexcept/id... : uniquement prefixe/suffixe (sunday ?)
* Vérifier que les positions/tag sont bien gérées (en particulier sur les alternatives)

Remarks
=======

* prepMerge: plus de merge parent/fils si conj dependency
* les mots de position 1000 sont les connecteurs
* les mots de position 1001 sont les mots propagés/ajoutés par le qw
* "Is there a pink bird" may be formalized as ∃ (?, instance of, bird) ∩ (?, color, pink)

Gestion des prep(c)_x
=====================

go -prep_to-> ... = go to -prep->
What is Frozen based on?

* What two US biochemists won the Nobel Prize in medicine in 1992?

https://github.com/ProjetPP/PPP-QuestionParsing-Grammatical/issues/72

Superlative
===========

* What is the most easily identifiable tree
* What is the most advanced technology ?
* http://dictionary.cambridge.org/fr/grammaire/grammaire-britannique/most-the-most-mostly

Yes/No questions
================

Exists
======

* Is there a ghost in my house
* Is there a pilot in the plane
* Is there a capital in France
* Is there a king of england > https://www.wikidata.org/wiki/Q18810062
* http://english.stackexchange.com/questions/34353/is-there-versus-are-there
* Are there any articles available on the subject?
* Are there computers in your room
* Does a king of England exist?

Racine à fils multiples
=======================

* nsubjpass + prep_in               : What language is spoken in Argentina?     > (Argentina, language, ?)
* prep_from + prep_to + prep_on     : carpool from Lyon to Paris on December 31 > (?, instance of, carpool) ∩ (?, from, Paris) ∩ (?, to, Lyon) ∩ (?,day, December 31st)
* nsubj + dobj                      : Which books did Suzanne Collins write?    > (Suzanne Collins, author, ?) + typage "book" sur ?
* nsubj + dobj (+ do)               : What albums did Pearl Jam record?
* nsubj + prep_from                 : Are you from Germany?                     > (you,origin,Germany) > yes/no : (subj | pred:be from, do..live | cpt)
* nsubj + prep_by                   : List movies directed by Spielberg
* prep_of + prep_of                 : list of president of usa
* nsubj + prep_by                   : List movies directed by Spielberg

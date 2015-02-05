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
* Multiple predicates pour les sort
* Tell me where the DuPont company is located. Name the Ranger who was always after Yogi Bear.
* How do you solve "Rubik's Cube"? > en quoi est transformé how
* réduire le nb de map, ajouter + d'infos
* How many : opérateur de comptage 
    >> How many films did Ingmar Bergman make?
    >> How many children does Barack Obama have?
* nounificatin : Which books did Suzanne Collins write? > author n'est pas un prédicat de Suzanne C. ?
    >> http://www.wikidata.org/wiki/Q33977
    >> http://www.wikidata.org/wiki/Property:P800 notable works, literary works, bibliography work, works

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

Semi question words
===================

* Show me Star Wars movies
* List movies directed by Spielberg
* List books by Roald Dahl
* List albums of Pink Floyd
* List films with Jack Nicholson
* List of US presidents
* List of presidents of France
* Give me the capital of France
* Give the capital of France
* Give us the capital of France
* list of president of usa (mal parsé)

Racine à fils multiples
=======================

* nsubj + prep_from                 : Are you from Germany?                     > (you,origin,Germany) > yes/no : (subj | pred:be from, do..live | cpt)
* dobj + prep_for                   : Who held the endurance record for women pilots in 1929?


#### instance_of

Mot interrogatif dans un sous-arbre nsubj
position(verbe) > position(nsubj)

* nsubjpass + prep_in               : What language is spoken in Argentina? 
* nsubj + dobj                      : What dictator has the nickname "El Maximo"?
* nsubj + dobj                      : What actor married John F. Kennedy's sister? > (?, instance of, actor) ∩ (?, wife, (John F. Kennedy, sister, ?))
* nsubj + prep_by                   : List movies directed by Spielberg
* nsubjpass                         : Which president has been killed by Oswald? > remove nsubjpass
* What actor married John F. Kennedy's sister
* nsubjpass                         : which books were written by Victor Hugo

#### instance_of exception

position(verbe) > position(nsubj) mais pas d'instance_of

* nsubj + dobj                      : Which books did Suzanne Collins write?    > (Suzanne Collins, author, ?) ∩ (books, typage "book" sur ?
* nsubj + prep_in                   : How many gas stations are there in the United States?
* What did John Hinckley do to impress Jodie Foster?

#### nsubj avec verbe nécessaire

Mot interrogatif est dobj

* Is there a ghost in my house
* Are there computers in your room
* What is the most beautiful country in Europe?
* Who was the first Taiwanese President?
* What was the monetary value of the Nobel Peace Prize in 1989? 
* When was Benjamin Disraeli prime minister?
* nsubjpass : Where was Ulysses S. Grant born?
* nsubjpass : Where is Inoco based?
* What was the first Gilbert and Sullivan opera?
* Where is the ENS of Lyon?
* What did Bob write ?
* Who is the author of Sea and Sky?

#### Question word nsubj

No subject after preprocessing

* Who wrote the song, "Stardust"?
* Who invented the hula hoop?
* nsubjpass : Who was killed by Oswald?
* Who elected the president ?

#### ???

* nsubj + dobj (+ do)               : What albums did Pearl Jam record? (cf parsing de: Which books did Suzanne Collins write)
* How many films did Ingmar Bergman make?
* Who Clinton defeated?

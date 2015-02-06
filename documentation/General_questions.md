General
=======

* verb+ing: do sthg special (look POS tag)? : What did Richard Feynman say upon hearing he would receive the Nobel Prize in Physics?
* If nounification becomes powerful enough: use it to analyse superlative (biggest > size...)
* Multiple words : Where is Inoco based? > base + place = base place :( >> en fait "base" se nounifie en "place" ?
* Article : enlever numéro apparaissant dans noeud (et idem pour arbre) / enlever encadrement
* data model : autoriser des listes de prédicats dans les sort ?
* réecrire demo3 pour le rendre dépendant de DependencyTree
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

* Yes/no question: product dobj relation?

Conjonction
===========

Mauvais : 
  * What was the first Gilbert and Sullivan opera?

Exemples :
----------
* Who makes and distributes bells?
* Who is the author of Sea and Sky?
* What percentage of the world's plant and animal species can be found in the Amazon forests?
* Good: Who is section manager for guidance and control systems at JPL?
* Bad: How many people did the United Nations commit to help restore order and distribute humanitarian relief in Somalia in September 1992?
* Bad: Which Italian city is home to the Cathedral of Santa Maria del Fiore or the Duomo?

Problem with merging:
---------------------
* What is the length of border between the Ukraine and Russia?

Comment construire les sous arbres
----------------------------------
* What was the first Gilbert and Sullivan opera?
* When was General Manuel Noriega ousted as the leader of Panama and turned over to U.S. authorities?
* When did Princess Diana and Prince Charles get married?
* When did the royal wedding of Prince Andrew and Fergie take place?
* ++ How many people did the United Nations commit to help restore order and distribute humanitarian relief in Somalia in September 1992?
    >> peut être propager les prep après ?
    >> même problème que pour les nn

Merge nn with the 2 nodes if nn above them:
 - When did Princess Diana and Charles get married?
 - When did Princess Diana and Prince Charles get married?
 - Who is section manager for guidance and control systems at JPL?

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

* Show me Star Wars movies > mal parsé
* List movies directed by Spielberg
* List books by Roald Dahl
* List albums of Pink Floyd
* List films with Jack Nicholson
* List of US presidents
* List of presidents of France
* Give me the capital of France
* Give the capital of France
* Give us the capital of France
* list of president of usa > mal parsé

Racine à fils multiples
=======================

* nsubj + prep_from                 : Are you from Germany?                     > (you,origin,Germany) > yes/no : (subj | pred:be from, do..live | cpt)
* dobj + prep_for                   : Who held the endurance record for women pilots in 1929?
_________________________________________________________________________________________________________________________________
_________________________________________________________________________________________________________________________________

Améliorer le MWE recognition
============================

Rattraper un mauvais parsing:
  * who is the president of the United states of america
  * Where is the ENS of Lyon? (merge car majuscule?)

Tag "S." car index entre les 2 + relation nn: 
  * Where was Ulysses S. Grant born?
  * What actor married John F. Kennedy's sister?

Good:
  * Who is the United States president
  * What was the first Gilbert and Sullivan opera?
  * Obama is the United States president.

Amod:
  * Who is the French president? >> nécessite avant de transformer French en France

Plus généralement : avoir une fonction de preprocessing qui applique des corrections sur l'arbre de dépendances dès le début (ajout de tags,...)
_________________________________________________________________________________________________________________________________

Nounification et inversion de triplets
======================================

Which books did Suzanne Collins write? > author n'est pas un prédicat de Suzanne C. ?
  >> http://www.wikidata.org/wiki/Q33977
  >> http://www.wikidata.org/wiki/Property:P800 notable works, literary works, bibliography work, works

Same problem : 
  * which book was authored by Victor Hugo
  * List movies directed by Spielberg
  * Which president has been killed by Oswald
  * List books by Roald Dahl

Contre-ex : 
  * who is the author of Narnia
  * capital of France

Good (?): 
  * Who elected the president of France?

Solutions (?):
  * ça n'arrive que dans certains cas (prep_by, agent...) > inverser ces règles
  * dans la nounification, prévoir les cas symétriques > authored = [works,author,...]
  * voir ce qui est fait pour la nn rule

R7 : nécessaire ou se rapproche du problème nounification/triplet inverse ???
_________________________________________________________________________________________________________________________________

Amélioration de nsubj avec instance_of
======================================

#### instance_of

Mot interrogatif dans un sous-arbre nsubj
position(verbe) > position(nsubj)

* nsubjpass + prep_in               : What language is spoken in Argentina? 
* nsubj + dobj                      : -What dictator has the nickname "El Maximo"?
* nsubj + dobj                      : -What actor married John F. Kennedy's sister?
* nsubj + prep_by                   : List movies directed by Spielberg
* nsubjpass                         : Which president has been killed by Oswald?
* nsubjpass                         : which book was authored by Victor Hugo

#### instance_of exception

position(verbe) > position(nsubj) mais pas d'instance_of

* nsubj + dobj                      : -Which books did Suzanne Collins write? 
* When was the president of the United States born
* nsubj + prep_in                   : -How many gas stations are there in the United States?
* What did John Hinckley do to impress Jodie Foster?

#### nsubj avec verbe nécessaire

Mot interrogatif est relié directement au verbe + pas dans un sous arbre sujet (souvent dep)

* What is the most beautiful country in Europe?
* -Who was the first Taiwanese President? > problème fusion
* What was the monetary value of the Nobel Peace Prize in 1989? 
* When was Benjamin Disraeli prime minister? > -advmod-> When
* nsubjpass : Where was Ulysses S. Grant born?
* nsubjpass : Where is Inoco based?
* What was the first Gilbert and Sullivan opera?
* Where is the ENS of Lyon?
* What did Bob write ? -dobj-> What
* Who is the author of Sea and Sky?
* Is there a ghost in my house -xcomp-> there
* Are there computers in your room

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

_________________________________________________________________________________________________________________________________

TODO
====

What dictator has the nickname "El Maximo"? / What albums did Pearl Jam record?                 >> traiter tous les auxiliaires comme be. Et dobj ici ? Généraliser la
                                                                                                   règle d'évitation à toutes les relations ? Uniquement sur les fils de 
                                                                                                   la racine ?
Who was the leader of the Branch Davidian Cult confronted by the FBI in Waco, Texas in 1993?    >> gros sujet
Where is Inoco based?                                                                           >> revoir la nounification associée
Who Clinton defeated?                                                                           >> prq nounification échoue ? non lemmatizé ?
Rapprocher/renommer les règles R.. similaires
R7 : nécessaire ou se rapproche du problème nounification/triplet inverse ???
instance of + tmod : which day was the president born

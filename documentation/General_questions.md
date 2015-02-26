General
=======

* verb+ing: do sthg special (look POS tag)? : What did Richard Feynman say upon hearing he would receive the Nobel Prize in Physics?
* If nounification becomes powerful enough: use it to analyse superlative (biggest > size...)
* Article : enlever numéro apparaissant dans noeud (et idem pour arbre) / enlever encadrement
* data model : autoriser des listes de prédicats dans les sort ?
* Dans le question word processing (et plus généralement) : les connecteurs ne sont pas uniquement les 1000. Les 1000 prennent les conj mais pas le superlatives.
* Recherche de wexcept/id... : uniquement prefixe/suffixe (sunday ?)
* Vérifier que les positions/tag sont bien gérées (en particulier sur les alternatives)
* Tell me where the DuPont company is located. Name the Ranger who was always after Yogi Bear.
* How do you solve "Rubik's Cube"? > en quoi est transformé how
* autres auxiliaire (have) : What dictator has the nickname "El Maximo" / What plant has the largest seed?
* Who was the leader of the Branch Davidian Cult confronted by the FBI in Waco, Texas in 1993?    >> gros sujet
* Who Clinton defeated?                                                                           >> prq nounification échoue ? non lemmatizé ?
* Typage : refaire une map complète : dependance <-> règle de typage (et pas règle Ri <-> règle de typage)
* processQuestionInfo : gestion des reverse, perte d'infos sur les triplets
* Ne plus lemmatizer les noms: What are Brazil's national colors? > garder le pluriel
* Nouveau qw : In what shows does Jennifer Aniston appears?
* How long were Tyrannosaurus Rex's teeth? > lemmatization de teeth

Remarks
=======

* prepMerge: plus de merge parent/fils si conj dependency
* les mots de position 1000 sont les connecteurs
* les mots de position 1001 sont les mots propagés/ajoutés par le qw
* "Is there a pink bird" may be formalized as ∃ (?, instance of, bird) ∩ (?, color, pink)

Gestion des prep(c)_x
=====================

go -prep_to-> ... = go to -prep->
* What is Frozen based on?
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
* nsubj + prep_from                 : Are you from Germany?                     > (you,origin,Germany) > yes/no : (subj | pred:be from, do..live | cpt)

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

Prédicat "be" inapproprié
========================

* What color is indigo?
* What nationality was Jackson Pollock?
* What is the tallest mountain?
* What tourist attractions are there in Reims?
* What do camels store in their humps?
* What color are tennis balls?
* What species is a colt?
* What animal has the biggest eyes?
* What nationality is Sean Connery?
_________________________________________________________________________________________________________________________________
_________________________________________________________________________________________________________________________________

Prédicats alternatifs
=====================

- https://github.com/json-ld/json-ld.org/issues/221

* Reconstruire map des participes passés avec le wiktionary
 > What university did Thomas Jefferson found? > found/founded/find (superlative map changée sur found)
 > https://simple.wiktionary.org/wiki/found
* Fusion des prep
 > What is Frozen based on?
 > go -prep_to-> ... = go to -prep->
 > prep_by > supprimer by et inverser le triplet
 > Mots interrogatifs : enrichir en ajoutant un mot au participe passé : When was the U.S. capitol built? > built in // ... by
 > In which country is Lake Victoria > fusion is/in car in ne peut pas être supprimé de l'arbre (prep_in). De toute façon, la suppression du qw se fait après merging
   >> solution: fusion + propre des prepositions (rajouter des Words au lieu de fusionner dans un seul word)
* Nounification map :
 > ne plus faire verbe (lemmatizé) > prédicats
 > à la place : set de sets. Chaque set = ensemble de prédicats équivalents
 > lien entre un set et son inverse
 > placer des prédicats alternatifs aussi pour les noms
* Obtenir prédicat de base (depuis verbe):
 > verbe > participe passé
 > si by > inverse sans by (et inversement)
* Trouver le bon set : 
 > si pas un verbe, le chercher directement
 > si verbe, chercher son participe passé p
* Construire les sets :
 > cf inverse : https://www.wikidata.org/wiki/User:Joshbaumgartner/property_available_summary/100-199
 > prendre les ensembles de propriétés/alias sur wikidata
* Traitement du qw : ne pas enrichir les participes passés
* Donner un score aux prédicats alternatifs > ou juste trier par ordre de pertinence ?

_________________________________________________________________________________________________________________________________

__How many__ : opérateur de comptage 
====================================

> How many films did Ingmar Bergman make?
> How many children does Barack Obama have?
> How many gas stations are there in the United States?
> cf instance_of sur dobj >> on récupère la liste produite en sortie et on renvoie sa taille
> How much did Mercury spend on advertising in 1993?
> How many stars are there on the Soviet Union's flag?
> How many Gutenberg Bibles are there?
> How many people died on D-Day?
> How many employees does Apple have
> How many people live in China
> How many episodes does Seinfeld have?
> How many people watch network television?
> How much does the human adult female brain weigh?
> How many presidents have died on the 4th of July?
> How many NFL teams are there?

_________________________________________________________________________________________________________________________________

Améliorer la MWE recognition
============================

Rattraper un mauvais parsing:
  * who is the president of the United states of america
  * Where is the ENS of Lyon? (merge car majuscule?)
  * What country made the Statue of Liberty?
  * What is the motto for the Boy Scouts? (NER)
  * Who is Vlad the Impaler?
  * date of birth

Amod:
  * Who is the French president? >> nécessite avant de transformer French en France
  * Who was the first Taiwanese President?

What organization was founded by the Rev. Jerry Falwell? >> tagger Rev car majuscule


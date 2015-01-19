# Review of the hierarchy collapsing rules

+++ : current choice is good

--- : currend choice is bad

Please, don't remove any example (they are used frequently to check the whole algorithm)

### Most problematic dependencies

* appos
* dep (no hope... the stanford parser needs to be improved/trained)
* dobj

appos
=====

Current rule: don't merge/remove appos

##### ---

* Who came up with the name, El Nino?
* Who wrote the song, "Stardust"? > (sometimes dep instead of appos) replace the father by the son || or R5 (or R2) rule?

xcomp
=====

* What did John Hinckley do to impress Jodie Foster?

amod
====

Current rule: merge if not JJS POS tag or ORDINAL NER tag

##### ---

* What is the most beautiful country in Europe?

##### +++ (superlative)
  
* What country is the biggest producer of tungsten?
* Who was the first Taiwanese President?
* Who was the first American in space?
* What is the largest city in Germany?
* Who was the 23rd president of the United States?
* Who is the tallest man in the world?

##### +++ (merging)

* What was the monetary value of the Nobel Peace Prize in 1989? 
* What is the name of the managing director of Apricot Computer?
* Who is the prime minister of Japan?
* Who is the Greek God of the Sea?
* Who invented the hula hoop? 

nn
==

Current rule: merge

##### ---
  
* How long did the Charles Manson murder trial last?
* What two US biochemists won the Nobel Prize in medicine in 1992?
* Who is the US president?

##### +++
  
* What was the monetary value of the Nobel Peace Prize in 1989? 
* Who was the leader of the Branch Davidian Cult confronted by the FBI in Waco, Texas in 1993?
* Where was Ulysses S. Grant born?

nsubjpass
=========
  
##### ---

* Which president has been killed by Oswald? > remove nsubjpass

##### +++

* Who was killed by Oswald?
* Where is Inoco based?
* Where was George Washington born?

cop
===

cop doesn't always disappear -> needs to remove it manually

##### ---

* What is the brightest star visible from Earth? >> cop not removed! change what <-> is
* Who is the president black and blue?
* What is black and white?

prep
====

##### ---

* Who was President of Afghanistan in 1994? ( of -> in)
* Who won two gold medals in skiing in the Olympic Games in Calgary?
* Who followed Willy Brandt as chancellor of the Federal Republic of Germany?
* Where does most of the marijuana entering the United States come from?
  
dobj
====

Current rule: dobj=t2

- dobj = t2 or t4?
- collapse dobj to comp ?
- different if a nsubj is present?

##### +++

* What did John Hinckley do to impress Jodie Foster?
* When did they won the lottery? >> dobj = t4
* What two US biochemists won the Nobel Prize in medicine in 1992?
* How many films did Ingmar Bergman make? >> with nsubj
* Who has written "The Hitchhiker's Guide to the Galaxy"? >> question is transformed as "(?,writer,The Hitchhiker 's Guide to the Galaxy)". The triple should be "(The Hitchhiker 's Guide to the Galaxy, author, ?)" or "(The Hitchhiker 's Guide to the Galaxy, writer, ?)"
* Who wrote "The Hitchhiker's Guide to the Galaxy"?

look at the verb ? (passive, acted ...)

##### ???

* Who killed Gandhi?
-> t4 would be better if we nounify "killed" into "killer".
For instance, Wikidata returns a good answer for the triple `(Gandhi, killer, ?)`

##### ---

* Who held the endurance record for women pilots in 1929?
* How many children does Barack Obama have? > https://github.com/ProjetPP/PPP-QuestionParsing-Grammatical/issues/75,  not do an intersection each time a node have several child.
* What did Eddy Caron write? > https://github.com/ProjetPP/PPP-QuestionParsing-Grammatical/issues/79, Should be (?, writer, Eddy Caron), not (Eddy Caron, writer, ?)


ccomp
=====

##### +++

* Who said "I am a Berliner"?

pobj
====

- map to comp temporarily
- pobj impossible ?

##### +++

* Who is the author of "Twenty Thousand Leagues Under the Sea"?

##### ---

* Who is Bob according to you?

dep
===

##### ---

* Who wrote the song, "Stardust"?
* When did Diana and Charles get married? > replace/merge the father by/with the son if dep (get -dep-> married = get married)
* What country is the biggest producer of tungsten? > idem

vmod
====

##### ---

* Who was the second man to walk on the moon?

nsubj
=====

- only if a = is/was/... ?
- when is/... is replaced, it's more relevant to produce a R5 rule

##### +++

* Who elected the president of France?
* What was the first Gilbert and Sullivan opera?
* Who Clinton defeated?
* Where is the ENS of Lyon?

num
===

Current rule: merge

##### ---

* What two US biochemists won the Nobel Prize in medicine in 1992?

rcmod
=====

* What did Richard Feynman say upon hearing he would receive the Nobel Prize in Physics? >> delete hearing et rcmod

conj
====

##### +++

* When did Rococo painting and architecture flourish?

pcomp
=====

* When did Israel begin turning the Gaza Strip and Jericho over to the PLO?


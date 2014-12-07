# Review of the hierarchy collapsing rules

+++ : current choice is good

--- : currend choice is bad

Please, don't remove any example (they are used frequently to check the whole algorithm)

appos
=====

Current rule: don't merge/remove appos

##### ---

* Who came up with the name, El Nino?

xcomp
=====

* What did John Hinckley do to impress Jodie Foster?

amod
====

Current rule: ~~don't merge~~ merge if not JJS POS tag or ORDINAL NER tag
 
##### ---

* What was the monetary value of the Nobel Peace Prize in 1989? 
* What is the name of the managing director of Apricot Computer?
* Who held the endurance record for women pilots in 1929?
* Who is the prime minister of Japan?
* Who is the Greek God of the Sea?
* Who invented the hula hoop? 

##### +++
  
* What country is the biggest producer of tungsten? <<
* Who was the first Taiwanese President?
* Who was the first American in space?
* What is the largest city in Germany?
* Who was the 23rd president of the United States?
* Who is the tallest man in the world?

nn
==

Current rule: merge

##### ---
  
* How long did the Charles Manson murder trial last?
* What two US biochemists won the Nobel Prize in medicine in 1992?

##### +++
  
* What was the monetary value of the Nobel Peace Prize in 1989? 
* Who was the leader of the Branch Davidian Cult confronted by the FBI in Waco, Texas in 1993?
* Where was Ulysses S. Grant born?

nsubjpass
=========
  
##### ---

* Where is Inoco based?
* Where was George Washington born?
* Which president has been killed by Oswald?

##### +++

* Who was killed by Oswald?

cop
===

cop doesn't always disappear -> needs to remove it manually

##### ---

* What is the brightest star visible from Earth? >> cop not removed! change what <-> is
* Who is the president black and blue?
* What is black and white?

prep
====

merge prep (when it's not prep_x) 

Level up prep_x in order not to have a -prep-> b -prep-> c
  - Who was President of Afghanistan in 1994? (juste pour of -> in)
  - Who won two gold medals in skiing in the Olympic Games in Calgary?
or not : 
  - Who followed Willy Brandt as chancellor of the Federal Republic of Germany?
  
##### ---

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

ccomp
=====

##### +++

* Who said "I am a Berliner"?

pobj
====

- map to comp temporarily
- pobj impossible ?

##### ---

* Who is the author of "Twenty Thousand Leagues Under the Sea"?
* Who is Bob according to you?

dep
===

##### ---

* Who wrote the song, "Stardust"?

vmod
====

##### ---

* Who was the second man to walk on the moon?

nsubj
=====

- only if a = is/was/... ?

##### ---

* Who Clinton defeated?

##### +++

* Who elected the president of France?

num
===

Current rule: merge

##### ---

* What two US biochemists won the Nobel Prize in medicine in 1992?

and, or
=======

Current rule: remove

##### ---

* When did Rococo painting and architecture flourish?

rcmod
=====

* What did Richard Feynman say upon hearing he would receive the Nobel Prize in Physics? >> delete hearing et rcmod

pcomp
=====

* When did Israel begin turning the Gaza Strip and Jericho over to the PLO?

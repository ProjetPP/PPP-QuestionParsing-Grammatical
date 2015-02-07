# Review of the hierarchy collapsing rules

+++ : current choice is good

--- : currend choice is bad

Please, don't remove any example (they are used frequently to check the whole algorithm)

### Most problematic dependencies

* appos
* dep (no hope... the stanford parser needs to be improved/trained)
* dobj
* nsubj

### Problematic questions

* Who won the first general election for President held in Malawi in May 1994? 
* How much did Mercury spend on advertising in 1993?
* How far is Yaroslavl from Moscow?
* What effect does a prism have on light?
* Where was the movie "Somewhere in Time" filmed? (not always the same result?)
* What country in Latin America is the largest one?
* He is the biggest and fattest man >> problem with amod and 2*conj
* Who held the endurance record for women pilots in 1929? >> problem with for
* How many people that live in China speak english?
* How many USA presidents have visited Iran?
* Which movies did Quentin Tarantino direct, but not star in?
* Who receives the Nobel Prize in Physics in 2000?
* When did Diana and Charles get married?
* Where is Mozambique located? > location/place
* Who built the first pyramid? > consider "pyramide" as (single) triple / predicate
* Who was the first Taiwanese President?
* What is the brightest star visible from Earth?

appos
=====

Current rule: don't merge/remove appos

##### ---

* Who came up with the name, El Nino?
* Who wrote the song, "Stardust"? > (sometimes dep instead of appos) replace the father by the son || or R5 (or R2) rule?
* Who wrote the book, "Huckleberry Finn"?
* Who is the author of the book, "The Iron Lady : A Biography of Margaret Thatcher"? >> problem of redundancy (book + title of the book)

prt
===

* Who came up with the name, El Nino?

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
* When was Benjamin Disraeli prime minister?
* What dictator has the nickname "El Maximo"?

##### +++
  
* What was the monetary value of the Nobel Peace Prize in 1989? 
* Who was the leader of the Branch Davidian Cult confronted by the FBI in Waco, Texas in 1993?
* Where was Ulysses S. Grant born?

nsubjpass
=========
  
##### ---

* Which president has been killed by Oswald?

##### +++

* Who was killed by Oswald?
* Where is Inoco based?
* Where was George Washington born?

agent
=====

* Which president has been killed by Oswald?
* Who was killed by Oswald?
* which book was authored by Victor Hugo

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

- collapse dobj to comp ?
- different if a nsubj is present?
- dobj rules should/can produce tripls with missing subject
- __hardcoder__ certains dobj comme des types (book, day : which day, ...)

##### +++

* What did John Hinckley do to impress Jodie Foster?
* When did they won the lottery?
* What two US biochemists won the Nobel Prize in medicine in 1992?
* How many films did Ingmar Bergman make?
* Who has written "The Hitchhiker's Guide to the Galaxy"?
* Who wrote "The Hitchhiker's Guide to the Galaxy"?
* Who invented the hula hoop?
* Who killed Gandhi?
* Who elected the president?

look at the verb ? (passive, acted ...)

##### ---

* How many children does Barack Obama have?
* Which books did Suzanne Collins write?

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
- sometimes it's relevent to produce an "instance of" triple.
- not "instance of" only if is/was/... ?
- new rules Rnsubj ????

##### +++

* Who elected the president of France?
* What was the first Gilbert and Sullivan opera?
* Who Clinton defeated?
* Where is the ENS of Lyon?
* What did Bob write ? > R3 if weak question word + not 'identity' >> problem or parsing failure ???

##### ---

* What actor married John F. Kennedy's sister

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

advmod
======

* Is there a doctor here?

npadvmod
========

* Is there a doctor here?
* Are there any articles available on the subject? > remplacer père par son fils

tmod
====

* Are there 29 days in February 
* which day was the president born

Stanford Parser fails
=====================

* What country is the biggest producer of tungsten?
* Who are the The Rolling Stones members?
* Is 42 an integer?
* Whose gender is genderqueer?
* How to get to the ENS Lyon?
* Are there pets on the farm?
* Are there geocaches in this forest?
* What albums did Pearl Jam record? (record est probablement mal taggé)
* Which movies does Quentin Tarantino star in? (idem)
* Which movies did Quentin Tarantino direct, but not star in?
* Are there beers in Germany?
* Show me Star Wars movies
* What country is the biggest producer of tungsten?
* How long did the Charles Manson murder trial last?
* What kind of animal is Babar?
* Which movies does Quentin Tarantino star in?
* What U.S. state is Fort Knox in?
* What city is Purdue University in?
* When was Benjamin Disraeli prime minister?
* list of president of usa
* Show me Star Wars movies
* Who held the endurance record for women pilots in 1929?
* What dictator has the nickname "El Maximo"?

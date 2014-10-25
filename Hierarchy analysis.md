Here we try to analyse the grammatical relations used by the Stanford Parser. The hierarchy of types dependencies below is taken from the manual ("The grammatical relations defined in the above section stand in a hierarchy. The most generic grammatical relation, dependent (dep), will be used when a more precise relation in the hierarchy does not exist or cannot be retrieved by the system.")

The elements with the symbol (-) don't appear in the hierarchy, but are explained in the part 2 of the manual (the contrary also happens). 

Some transformations need to be perform in a certain order. For example, some relations, such as "agent", must be transform in "nsubjpass". So you need to analyze nsubjpass relation after "agent" for example.

Some vocabulary:
* "Remove" means "remove the endpoint of the edge" (we assume it's a leaf, otherwise give me counterexamples). 
* "Merge" means "merge the 2 nodes of the edge" (and so destroy the edge). 
* "Collapse to x" means "replace the edge by a x-type edge". 
* "Impossible" means "this relation doesn't appear in collapse dependency" (give counterexamples otherwise).


> **root - root**

> root of the tree

> **dep - dependent**

> parser fails to find a dependency.

> merge all the subtree? (ex:  Who is the author of the book, "The Iron Lady : A Biography of Margaret Thatcher"?)

>> **aux - auxiliary**

>> remove (aux (born,was) -> born) 

>> (or merge and simplify?)

>>> **auxpass - passive auxiliary**

>> remove (to "inverse" the verb, ex: The man has been killed by the police), the "passive information" will be treat in nsubjpass

>> (or merge and simplify?)

>>> **cop - copula**

>> impossible (thanks to makeCopulaHead)

>> **arg - argument**

>> see cases below

>>> **agent - agent**

>>> always implies passive voice (?)

>>> transform the subject relation nsubj (and csubj ?) to nsubjpass (if it's not ever done)

>>> perform the things of nsubjpass

>>> **comp - complement**

>>> __*KEEP*__

>>>> **acomp - adjectival complement**

>>>> collapse to comp

>>>> **ccomp - clausal complement with internal subject**

>>>> collapse to comp

>>>> **xcomp - clausal complement with external subject**

>>>> collapse to comp

>>>> **pcomp - prepositional complement (-)**

>>>> collapse to comp

>>>> **obj - object**

>>>> impossible (always one the subcase below ?)

>>>>> **dobj - direct object**

>>>>> collapse to comp

>>>>> **iobj - indirect object**

>>>>> remove (in a first time). please give example of questions with iobj

>>>>> **pobj - object of preposition**

>>>>> impossible

>>>>> (or treat it as "prep_x" (x is "in", "on" ...))

>>> **subj - subject**

>>> __*KEEP*__

>>>> **nsubj - nominal subject**

>>>> collapse to subj

>>>>> **nsubjpass - passive nominal subject**

>>>>> passive voice, link the verb to the subject (that support the action)

>>>>> need to search somewhere else the "actor of the verb"

>>>>> we assume (need more verification to be sure) that there is always an agent ie the verb is followed by "by".

>>>>> we assume the verb has already been "inversed" (just by removing "by" or "has been" for example?)

>>>>> the agent is the "actor" of the (new) verb

>>>>> transformations to remove "agent" and "nsubjpass" (miss some of the possible cases?) :

>>>>>   - (The man has been killed by the police) `x <-nsubjpass- y -agent-> z` becomes `z <-nsubj- y -comp-> x` 

>>>>>   - (Effects caused by the protein are important) `x -vmod-> y -agent-> z` becomes `z <-nsubj- y -comp-> x` (in the example, we obtain `important -nsubj-> caused -nsubj-> protein` and `caused -comp-> effects`. The example is very important (see the graph). Here we have made transformations that product grammatical relations (`important -nsubj-> caused`) that are probably irelevant from a "grammarian point of view" but that are very close to the triple representation. Indeed, we obtain directly 2 triples: `protein <-nsubj- caused -comp-> effects` (denoted by X) and `X <-nsubj- are --> important` (need to transform the copula before).

>>>>>   - ???

>>>> **csubj - clausal subject**

>>>>> **csubjpass - passive clausal subject**

>> **cc - coordination**

>> **conj - conjunct**

>> duplicate the tree?

>> **expl - expletive (expletive “there”)**

>> **mod - modifier**

>> merge the 2 nodes 

>>> **amod - adjectival modifier**

>>> collapse to mod

>>> **appos - appositional modifier**

>>> **advcl - adverbial clause modifier**

>>> **det - determiner**

>>> could be removed in a lot of case

>>> can link a word to a "question word"

>>> ex : “Which book do you prefer?” -> det(book, which)

>>> ex: What debts did Qintex group leave?

>>> not a problem because who analyze the question word before?

>>> **predet - predeterminer**

>>> **preconj - preconjunct**

>>> **vmod - reduced, non-finite verbal modifier**

>>> **mwe - multi-word expression modifier**

>>> merge nodes

>>>> **mark - marker (word introducing an advcl or ccomp)**

>>> **advmod - adverbial modifier**

>>>> **neg - negation modifier**

>>> **rcmod - relative clause modifier**

>>>> **quantmod - quantifier modifier**

>>> **nn - noun compound modifier**

>>>  __*KEEP*__

>>> **npadvmod - noun phrase adverbial modifier**

>>>> **tmod - temporal modifier**

>>> **num - numeric modifier**

>>>  __*KEEP*__

>>> **number - element of compound number**

>>> merge and normalize (number (thousand, four) -> 400)

>>> **prep - prepositional modifier**

>>> prep_x in collapse dependency

>>> see possibility of prep_x and prepc_x in the manual

>>> ...

>>> **prepc - prepositional clausal modifier (-)**

>>> prepc_x in collapse dependency

>>> collapse to prep_x

>>> **poss - possession modifier**

>>> important! produce a triple

>>> ...

>>> **possessive - possessive modifier (’s)**

>>> impossible

>>> apparently could produce relations such that possessive(John, ’s) but I didn't an example. If this kind od relations appears, need some transformation

>>> **prt - phrasal verb particle**

>>> merge

>> **parataxis - parataxis**

>> **punct - punctuation**

>> impossible

>> **ref - referent**

>> **sdep - semantic dependent**

>>> **xsubj - controlling subject**

>> **goeswith - error space (-)**

>> merge

>> **discourse - discourse element (-)**

>> remove










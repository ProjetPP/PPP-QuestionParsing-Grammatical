Here we try to analyze the grammatical relations used by the Stanford Parser. The hierarchy of types dependencies below is taken from the manual ("The grammatical relations defined in the above section stand in a hierarchy. The most generic grammatical relation, dependent (dep), will be used when a more precise relation in the hierarchy does not exist or cannot be retrieved by the system.")

The elements with the symbol (-) don't appear in the hierarchy, but are explained in the part 2 of the manual (the contrary also happens). 

Some transformations need to be perform in a certain order. For example, some relations, such as "agent", must be transform in "nsubjpass". So you need to analyze nsubjpass relation after "agent" for example.

Some vocabulary:
* Remove: remove the endpoint of the edge (we assume it's a leaf, otherwise give me counterexamples). 
* Ignore: remove but it could be interesting to analyze it later
* Merge: merge the 2 nodes of the edge (and so destroy the edge). 
* Collapse to x: means "replace the edge by a x-type edge. 
* Impossible: means "this relation doesn't appear in collapse dependency (give counterexamples otherwise).

Restricted set of dependencies:
* dep: unknown dependency
* subj: subject
* comp: subj verb comp
* mod: modifier of an entity (adjective,...)
* conj: conjonction (conj_and, conj_or...)
* neg: negation
* num: number
* pos: possessive
* prep: preposition (prep_in,prep_on,...)
* Agent and nsubjpass could also be kept in a first time (in order not to perform the particular transformations they imply).

> **root - root**

> root of the tree

> **dep - dependent**

> __*KEEP*__

> parser fails to find a dependency.

> merge all the subtree (ex:  Who is the author of the book, "The Iron Lady : A Biography of Margaret Thatcher"?) and keep "dep"

>> **aux - auxiliary**

>> remove (aux (born,was) -> born) 

>>> **auxpass - passive auxiliary**

>> remove (in order to "inverse" the verb, ex: The man has been killed by the police), the "passive information" will be treat in nsubjpass

>>> **cop - copula**

>> impossible (thanks to makeCopulaHead)

>> counterexamples: What is the brightest star visible from Earth?

>> **arg - argument**

>> impossible (see cases below)

>>> **agent - agent**

>>> always implies passive voice (?)

>>> transform the closest nsubj to nsubjpass (if it's not ever done)

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

>>>> impossible (always one of the cases below ?)

>>>>> **dobj - direct object**

>>>>> collapse to comp

>>>>> __use it to find question word?__ (when qw is not subject)

>>>>> **iobj - indirect object**

>>>>> remove (in a first time). please give example of _questions_ with iobj

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

>>>> impossible

>>>>> **csubjpass - passive clausal subject**

>>>>> impossible

>> **cc - coordination**

>> ignore

>> **conj - conjunct**

>> __*KEEP*__

>> conj_x (conj_and, conj_or ...) in practice

>> **expl - expletive (expletive “there”)**

>> ignore

>> How many undiscovered blood groups are there?

>> How Many Undiscovered Blood Groups Are There?

>> **mod - modifier**

>> __*KEEP*__ (mod is never displayed by the parser, see subcases below)

>>> **amod - adjectival modifier**

>>> collapse to mod

>>> **appos - appositional modifier**

>>> collapse to mod

>>> **advcl - adverbial clause modifier**

>>> collapse to mod (probably too difficult to be analyzed)

>>> **det - determiner**

>>> remove

>>> can link a word to a "question word"

>>> ex : “Which book do you prefer?” -> det(book, which)

>>> ex: What debts did Qintex group leave?

>>> not a problem if we analyze/remove the question word before

>>> **predet - predeterminer**

>>> ignore

>>> **preconj - preconjunct**

>>> ignore

>>> **vmod - reduced, non-finite verbal modifier**

>>> collapse to mod (not very good...)

>>> **mwe - multi-word expression modifier**

>>> merge nodes

>>>> **mark - marker (word introducing an advcl or ccomp)**

>>>> ignore

>>> **advmod - adverbial modifier**

>>> merge __only if__ it's not the question word (question word is deleted)

>>>> **neg - negation modifier**

>>>>  __*KEEP*__

>>> **rcmod - relative clause modifier**

>>> ignore

>>>> **quantmod - quantifier modifier**

>>>> ignore

>>> **nn - noun compound modifier**

>>> merge (noun modifiers are more likely to form an entity with the NP they modified, than adjectives for ex)

>>> **npadvmod - noun phrase adverbial modifier**

>>> merge

>>>> **tmod - temporal modifier**

>>>> collapse to mod (later: keep the "temporal" info)

>>>> merge all the subtree and add TIME identifier?

>>> **num - numeric modifier**

>>>  __*KEEP*__

>>> **number - element of compound number**

>>> merge and normalize (number (thousand, four) -> 400)

>>> **prep - prepositional modifier**

>>>  __*KEEP*__

>>> prep_x in practice

>>> see prep_x and prepc_x in the manual

>>> ...

>>> **prepc - prepositional clausal modifier (-)**

>>> prepc_x in practice

>>> collapse to prep_x

>>> **poss - possession modifier**

>>> __*KEEP*__

>>> **possessive - possessive modifier (’s)**

>>> impossible

>>> apparently could produce relations such as possessive(John, ’s) but I didn't found an example. If this kind of relations appears, need some transformation

>>> **prt - phrasal verb particle**

>>> merge

>> **parataxis - parataxis**

>> ignore

>> **punct - punctuation**

>> impossible

>> **ref - referent**

>> impossible?

>> **sdep - semantic dependent**

>> impossible (see cases below)

>>> **xsubj - controlling subject**

>>> collapse to comp

>> **goeswith - error space (-)**

>> merge

>> **discourse - discourse element (-)**

>> remove



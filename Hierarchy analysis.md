Here we try to analyse the grammatical relations used by the Stanford Parser. The hierarchy of types dependencies below is taken from the manual ("The grammatical relations defined in the above section stand in a hierarchy. The most generic grammatical relation, dependent (dep), will be used when a more precise relation in the hierarchy does not exist or cannot be retrieved by the system.")

The elements with the symbol (-) don't appear in the hierarchy, but are explained in the part 2 of the manuel (the contrary also happens). 

> **root - root**

> root of the tree

> **dep - dependent**

> parser fails to find a dependency.

> remove the subtree.

>> **aux - auxiliary**

>> merge and simplify (aux (born,was) -> bear) 

>>> **auxpass - passive auxiliary**

>> merge and simplify

>> the "passive information" will be treat in nsubjpass

>>> **cop - copula**

>> **arg - argument**

>>> **agent - agent**

>>> **comp - complement**

>>>> **acomp - adjectival complement**

>>>> **ccomp - clausal complement with internal subject**

>>>> **xcomp - clausal complement with external subject**

>>>> **pcomp - prepositional complement (-)**

>>>> **obj - object**

>>>>> **dobj - direct object**

>>>>> **iobj - indirect object**

>>>>> **pobj - object of preposition**

>>> **subj - subject**

>>>> **nsubj - nominal subject**

>>>>> **nsubjpass - passive nominal subject**

>>>>> passive voice, link the verb to the subject (that support the action)

>>>>> need to search somewhere else the "actor of the verb"

>>>> **csubj - clausal subject**

>>>>> **csubjpass - passive clausal subject**

>> **cc - coordination**

>> **conj - conjunct**

>> duplicate the tree?

>> **expl - expletive (expletive “there”)**

>> **mod - modifier**

>>> **amod - adjectival modifier**

>>> **appos - appositional modifier**

>>> **advcl - adverbial clause modifier**

>>> **det - determiner**

>>> could be removed in a lot of case

>>> can link a word to a "question word"

>>> ex : “Which book do you prefer?” -> det(book, which)

>>> **predet - predeterminer**

>>> **preconj - preconjunct**

>>> **vmod - reduced, non-finite verbal modifier**

>>> **mwe - multi-word expression modifier**

>>> merge nodes

>>>> **mark - marker (word introducing an advcl or ccomp**

>>> **advmod - adverbial modifier**

>>>> **neg - negation modifier**

>>> **rcmod - relative clause modifier**

>>>> **quantmod - quantifier modifier**

>>> **nn - noun compound modifier**

>>> **npadvmod - noun phrase adverbial modifier**

>>>> **tmod - temporal modifier**

>>> **num - numeric modifier**

>>> **number - element of compound number**

>>> merge and normalize (number (thousand, four) -> 400)

>>> **prep - prepositional modifier**

>>> **prepc - prepositional clausal modifier (-)**

>>> collapsed tree only

>>> **poss - possession modifier**

>>> **possessive - possessive modifier (’s)**

>>> same as "poss"

>>> **prt - phrasal verb particle**

>>> merge nodes

>> **parataxis - parataxis**

>> **punct - punctuation**

>> can be removed, by default not output

>> **ref - referent**

>> **sdep - semantic dependent**

>>> **xsubj - controlling subject**

>> **goeswith - error space (-)**

>> concatenate the two nodes

>> **discourse - discourse element (-)**

>> remove










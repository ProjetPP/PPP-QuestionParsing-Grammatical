How to produce triples from the dependency tree
-----------------------------------------------

Generalities
============

Notation: we denote a -b-> c the dependency relation b from node a to node c.

We associate one unknown to each node. In fact, it is one node by subtree.
  a -b-> c                  : ?A = unknown of the node a

A triple is denoted predicat-///**/*/***//---e(subject,object). We give below what triple produce depending on each edge.

The final answer will be ?R of the root r.

+ comp, pos, subj, prep, dep, root

=

- mod

? conj

ignore : agent, nsubjpass, neg

Root
====

a -root-> b               : ?A = ?B

Comp
====

a -comp-> b               : a(?A,b)

Pos
===

a -pos-> b                : a(?A,b)

Mod
===

a -amod-> b               : b(?A,a)
  ok if merge is not relevant

a -vmod-> b               : ?A = ?B
  Who was the second man to walk on the moon?

a -mod-> b                : b(?A,a)
  not tested
   
Dep
===

a -dep-> b               : a(?A,b)

livre -dep-> titre

Subj
====

a -subj-> b               : ?A = ?B
  only if a = is/was/... ? (no)
  
Prep
====

a -prep-> b -prep-> c     : a(?A,b) /\ a(?A,c) ou a(?A,b) /\ b(?B,c)

a -prep_of-> b -prep_in-> c     : a(?A,b) /\ a(?A,c) ou a(?A,b) /\ b(?B,c)

a -prep-> b               : a(?A,b)
  
a -prep_x-> b          : a_x(?A_x,b) 
  --> or : replace a by a_x / or just if a_x is a verb
  --> not sooner: 
        Who is the founder of Scientology?
        Who held the endurance record for women pilots in 1929? : good not to hace held_for for record
  --> transform in a_x -comp-> b
  --> idem for prepc
  --> or a_x(?A,b) (instead of ?A_x) in order not to lose the level-unknown

Level up prep_x in order not to have a -prep-> b -prep-> c
  Who was President of Afghanistan in 1994? (juste pour of -> in)
  Who won two gold medals in skiing in the Olympic Games in Calgary?
or not : 
  Who followed Willy Brandt as chancellor of the Federal Republic of Germany?
 
Dep
===

a -b-> c -dep-> d == d <-b- a -b-> c
  Who wrote the song, "Stardust"?
  
Who
===

Who was/is
  be -subj-> a            : is(??,a)
  a=be -subj-> b          : ?A = ?B
    Who is the Queen of Holland?

Who vb (sam as above in fact ?)
  vb -comp-> a            : vb(??,a)




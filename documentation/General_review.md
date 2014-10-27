
## Preprocessing merging

* merge with wordnet (list english compound words)
* What is the name of the managing director of Apricot Computer?
* Merge amod :
    - prime minister
* Who wrote "The Pines of Rome"?
  

## Dependency restriction 

* mod is too generic
* treat nn as mod (and not merge)
* more info in Hierarchy_review.md


## General algorithm

* no merging during dependencies analysis
* initial tree -> tree with restricted dependencies -> tree with triple type annotation (T1,...) or mix of the 2
* when modules fail to find unknowns, they collapse everything:  is -subj-> voice -prep_of-> Miss Piggy : is(??,y) /\ voice(y,Miss Piggy) -> collapse to: is(??,voice Miss Piggy)


## Good examples

* Who won the first general election for President held in Malawi in May 1994? 

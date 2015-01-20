elected     : elector, election, voter
directed    : director
born        : birth, -birthday, -birthplace
wrote       : writter, author ('/r/CapableOf')
live        : residence (synonym to home that is related to live), residency
fix         : repair (biggest weight, lowest similarity)
know        : knowledge
invent      : inventor
die         :
wrote       :
play        : player (capableof)
ran         : run (limit 400)
jump        :
walk        :
hide        :
dive        :
drive       : driver (limit 250)
fall        :
climb       :
ride        :
dance       : dancer
wash        :
cook        : cook
repair      :
build       :
fly         :
buy         : buyer
manufacture
spend (on)
kill        : killer (Desires) or: http://www.wikidata.org/wiki/Property:P157
make        : directed by (http://www.wikidata.org/wiki/Property:P57)

score : 
  - si pas sous mot : inutile de regarder similarité
  - s'authoriser à augmenter la limite, mais uniquement pour récupérer des mots très similaires (runner)

Nounification: 
  killed by: http://www.wikidata.org/wiki/Property:P157
  sur prédicat uniquement, mais pas toujours nécessaire
    >> ou pas, si POS tag 'V' il faut forcèment nounifier
  president of germany > president est un prédicat mais il ne faut pas le nounifier
  effectuer nounification sur forme normalisée
  traiter également question word sur forme normalisée ? 
    >> garantir qu'en entrée de normalize chaque noeud contient une seule alternative
    >> ajout des infos sur les premières feuilles / prédicats / ...
    >> seul les prédicats peuvent contenir des alternatives < le garantir

Relacher le test sur ['identity'] (dans questionWordProcessing.py) : si présent dans la liste (et non plus égal) alors ajouter toutes les combinaisons additionelles (et même garder identity ?)

Traiter à part :
  be 
  do
  have
  go (to) How to get to the ENS Lyon?

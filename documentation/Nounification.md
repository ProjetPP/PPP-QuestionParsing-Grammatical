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
go to       : 

Score : 
  - si l'un des 2 mots n'est pas facteur de l'autre (préfixe, suffixe...) : inutile de regarder similarité car les 2 mots différent trop
  - s'autoriser à augmenter la limite de lookup, mais uniquement pour récupérer des mots très similaires (runner)

Relacher le test sur ['identity'] (dans questionWordProcessing.py) : si présent dans la liste (et non plus égal) alors ajouter toutes les combinaisons additionelles (et même garder identity ?)

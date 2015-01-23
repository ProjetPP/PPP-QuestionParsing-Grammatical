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

Score : 
  - si l'un des 2 mots n'est pas facteur de l'autre (préfixe, suffixe...) : inutile de regarder similarité car les 2 mots différent trop
  - s'autoriser à augmenter la limite de lookup, mais uniquement pour récupérer des mots très similaires (runner)

Wikidata:
  - récupérer toutes les propriétés possibles
  - essayer systématiquement de mapper les prédicats vers des propriétés existantes (pendant la nounification)
     * faire une extraction large par conceptnet, puis filtrer les prédicats présents effictement dans wikidata
     * chercher à mapper directement le verbe vers des prédicats wikidata. Regarder pour cela si une arête relie les 2 concepts dans conceptnet (et regarder les poids si trop de candidats) < trop long, comment faire une épuration préliminaire ?

Nounification: 
  killed by: http://www.wikidata.org/wiki/Property:P157
  sur prédicat uniquement, mais pas toujours nécessaire
    >> ou pas, si POS tag 'V' il faut forcèment nounifier
  president of germany > president est un prédicat mais il ne faut pas le nounifier >> mais ce n'est pas tagger verbe
  effectuer nounification sur forme normalisée
  traiter également question word sur forme normalisée ? 
    >> garantir qu'en entrée de normalize chaque noeud contient une seule alternative
    >> ajout des infos sur les premières feuilles / prédicats / ...
    >> seul les prédicats peuvent contenir des alternatives < le garantir

Relacher le test sur ['identity'] (dans questionWordProcessing.py) : si présent dans la liste (et non plus égal) alors ajouter toutes les combinaisons additionelles (et même garder identity ?)

Exception : chercher dans les exceptions avant d'essayer l'algo
 > avoir le plus d'exceptions possible et utiliser l'algo en dernier recourt
 > s'autoriser alors une limite de lookup très importante
 > 7440 verbs in ntlk

Traiter à part :
  be 
  do
  have
  go (to) How to get to the ENS Lyon?

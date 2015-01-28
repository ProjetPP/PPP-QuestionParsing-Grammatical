# Nounification

## Overview

The nounification process consists in finding nouns related to a given verb. Here we are looking especially for nouns that can be predicates of [our datamodel](https://github.com/ProjetPP/Documentation/blob/master/data-model.md). For instance, in the question `Where does the president live?` it is relevant to nounify `live` into `residence` but not into `life` (the triple `(president,residence,?)` makes more sense than `(president,life,?)`).

Since nounification is a difficult task that highly depends on the meaning of the sentence, we do not intend to find exactly the right noun. Instead, we would like to __store__ for each verb a small set of nouns (less than 100) that contains all the possible relevant ways of nounify it. For instance, we could store for the verb `speak` the nouns `language`, `official language`, `mother tongue`, `speech`, `spokesman`.

We have already implemented an algorithm (using ConceptNet) that has automatically built a database of nounifications for about 7000 verbs (see [nounificationAuto.pickle](https://github.com/ProjetPP/PPP-QuestionParsing-Grammatical/blob/master/ppp_questionparsing_grammatical/data/nounificationAuto.pickle)). This database is a temporary solution since we are filling in manually a more accurate one (see [nounificationManual.pickle](https://github.com/ProjetPP/PPP-QuestionParsing-Grammatical/blob/master/ppp_questionparsing_grammatical/data/nounificationManual.pickle)).

## Your task

If you want to help us improving [nounificationManual.pickle](https://github.com/ProjetPP/PPP-QuestionParsing-Grammatical/blob/master/ppp_questionparsing_grammatical/data/nounificationManual.pickle), here are the instructions:
  - go into the [ppp_questionparsing_grammatical](https://github.com/ProjetPP/PPP-QuestionParsing-Grammatical/tree/master/ppp_questionparsing_grammatical) folder
  - run `python3`
  - import the Nounificator class: `from nounDB import *`
  - load `nounificationManual.pickle`:

  ```python
  n = Nounificator()
  n.load('data/nounificationManual.pickle')
  ```

  - load  `nounificationAuto.pickle` (optional):

  ```python
  m = Nounificator()
  m.load('data/nounificationAuto.pickle')
  ```

Actions available (see [NounDB](https://github.com/ProjetPP/PPP-QuestionParsing-Grammatical/blob/master/ppp_questionparsing_grammatical/nounDB.py)):
  - Add the noun `author` to the verb `write`: `n.add('write','author')`
  - Add the nouns `inventor` and `invention` to the verb `invent`: `n.addList('invent',['inventor','invention'])` or `n.addList('invent','inventor invention'.split(' '))`
  - Get all the nouns related to the verb `found`: `n.toNouns('found')`
  - Remove the noun `birth` from the verb `bear`: `n.remove('bear','birth')`
  - Remove the verb `speak` from the database: `n.removeVerb('speak')`

__Do not forget__ to save the database at the end:
```python
n.save('data/nounificationAuto.pickle')
```

## Advice

Be sure to have understood what we want, it is not only nounification! In order to be sure that a noun can be added to a verb, find a question in which the verb should to be transformed into this noun. For instance, the question `Who has played Batman?` needs to be transformed into the triple `(Batman,actor,?)` and so you can add `actor` to the verb `play`.

Look into `nounificationAuto.pickle` if there are interesting results. For instance, if you do `m.toNouns('kill')` you will see that `killer` appears into the list, and it is relevant to add it into `nounificationManual.pickle`.

Our databases are stored as binary files, you cannot merge them automatically with Git. In order to avoid merge conflict, please follow these rules:
  - `nounificationManual.pickle` must only be changed in the `Master` branch of the repository
  - before making any modification, don't forget to make a `git pull`. Once you have finished, quickly `push` :)
  - in case of conflict, don't panic. The class `NounDB` has a merge method. In order to merge a Nounificator `m` into a Nounificator `n`, make: `n.merge(m)`

Finally, if you don't want to deal with our database, you can write down your ideas in the file [nounifyMe.md](https://github.com/ProjetPP/PPP-QuestionParsing-Grammatical/blob/master/nounification/nounifyMe.md). Then, we copy them into `nounificationManual.pickle` for you ;)

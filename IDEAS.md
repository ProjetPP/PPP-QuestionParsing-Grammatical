# Ideas

Some common draft of the ideas that we may have. The aim is to begin a discussion
about them.

Please have a look at the graphs generated with the Stanford library, and try
your own experimentations.

## Pre-processing

#### Tree simplification

Return the tree given by the Stanford library, with some modifications.

* To each edge, apply some function. For instance, the string `president of France`
will give two nodes under the root node, `president -> France`, with the label
`prep_of` on the edge. We shall transform it into the triple (president, qualifier, 
France). The same transformation can be applied to the parsing result of 
`George Washington` which is `Washington -> George` and label `nn`.
* Remove some nodes. For example, nodes after an edge `det`.

This gives a nice recursive function.

#### Name entity recognition

There may be a way to group "same entities" together (ex: George Washington). It's call "name entity recognition". See the pad (http://pad.aliens-lyon.fr/p/ppp-nlp) for some (basic) resources.

Name entity recognition can be useful in two ways:
  - tag and group some parts of the question (ex: name 'Barack Obama', location 'Paris').
  - replace references in sentences (ex: 'What Nadal does when he has to serve?' -> 'What Nadal does when Nadal has to serve?')
  
I made new experiments with the StanfordNLP library. All worked well for the sentence
`Barack Obama is the president of the United States.`: the `parsetree` attribute 
of the resulting object put `George` and `Washington` in a same nominal group. Idem 
for `United` and `States`. The result in the dependency tree is great too: `George` 
is a subnode of `Washington` and `United` is a subnode of `States`.

So I hoped to have a good entity recognition tool with StanfordNLP.

Then I tried `Who is the United States president?`. Big fail. In the parse tree, 
it groups `the United States president` in one nominal group, but does not make 
a subgroup with only `United States`.
The dependency tree is even worst. There is a subtree for the whole group, with 
`president` on top, with two children: `United` and `States`. Thus, these two words 
are separated, which looks pretty bad.

I will search other ways, maybe with NLTK library...

**Interesting:** StanfordNLP also provide the meaning of some words in the `words`
attribute. For instance, words `George` and `Washington` are recognized as `person`,
whereas words `United` and `States` are recognized as `location`, in the sentence
`George Washington is the president of the United States.`. It could be very
useful.
  
## Pattern recognition

We can observe some incoherencies. 
Consider the two sentences `Who is the president of France?` and `Where does the
singer of Led Zeppelin live?`. The question word is not placed at the same place 
in the obtained tree.

-> It's probably due to the specific role holding by "be" in the Stanford parser. See section 4.7 of the manual, there is a way to avoid this (and always have the verb at the top of the tree?) but I don't how adding the flag required.

A solution could be to compute these questions specifically:

For all sentence of the form `<question word> <aux> X`, only parse `X` with the 
Stanford library. Let `x` be the triple obtained after the parsing and our (classical)
transformation. Return `(X,pred,?)` where `pred` is decided in function of the 
question word (and maybe the auxiliary?). 

For example, we can have the following predicates:

* `who`: `identity` or `function`
* `where`: `location`
* `when`: `date` or `event`
* `how`: `way` or `mean`

Some common questions (from http://ailab.ijs.si/delia_rusu/Papers/www_ssws_2009.pdf):

* Yes/No questions (Do animals eat fruit?)
* list questions (What do animals eat?)
* reason questions (Why do animals eat fruit?)
* quantity questions (How much fruit do animals eat?)
* location questions (Where do animals eat?)
* time questions (When do animals eat?)

See also: http://www.aclweb.org/anthology/A00-1023.pdf

**Other solution:**

We may not care of the question word. For instance, several questions are possible
about the French revolution: `When was the French revolution?` or `Where was the 
French revolution?`. Then, either we answer precisely (e.g. `1789` for the date, 
`Paris` for the location), or we output a short summary which would be identical 
for each question word. In the later case, simply drop the question word and the 
auxiliary. This lake of precision is unsatisfying (in comparison with existing
tools), but it would be better than nothing. This can be even worst for other
questions: `Who is Washington?` and `Where is Washington?` refer to two different
things (the person or the town).

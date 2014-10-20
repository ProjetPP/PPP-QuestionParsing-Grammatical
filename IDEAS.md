# Ideas

Some common draft of the ideas that we may have. The aim is to begin a discussion about them.

Please have a look at the graphs generated with the Stanford library, and try your own experimentations.

## 1. Pre-processing

#### 1.1. Stanford's output description

###### Graph properties

The Stanford Parser can output 5 different types of dependency graph (see the manual for a description of them). It may be interesting not to work with the standard one (the collapsed tree could be useful).

-> I agree, it seems very interesting. I did not see such a representation in the wrapper written in python. 
The python wrapper seems to provide the `collapsed tree` representation. You can see it by parsing the sentence `Bell, based in Los Angeles, makes and distributes electronic, computer and building products.`: the two words `based in` are collapsed, but we keep a tree structure. The question is: is it collapsed enough for us? A
non-tree structure may be tricky to handle...

-> I think (according to some tests provided by section 4.9) it's "Collapsed dependencies preserving a tree structure" (section 4.4 of the manual). Its properties are:
  - connected
  - acyclic
  - __tree__
  - collapsed nodes
  - rooted
  - no self-loops
  - not a multigraph
  - see 4.2 to 4.4 for more properties
  
This structure seems to be the most interesting one.

###### Copula verb

Consider the two sentences `Who is the president of France?` and `Where does the singer of Led Zeppelin live?`. The question word is not placed at the same place in the obtained tree.

It's probably due to the specific role held by "be" in the Stanford parser (copula verb). See section 4.7 of the manual, there is a way to avoid this (and always have the verb at the top of the tree?): adding the flag -makeCopulaHead. I don't know if it's possible with the wrapper but it could simplify our work.

#### 1.2. Tree simplification

Return the tree given by the Stanford library, with some modifications.

* To each edge, apply some function. For instance, the string `president of France` will give two nodes under the root node, `president -> France`, with the label
`prep_of` on the edge. We shall transform it into the triple (president, qualifier, France). The same transformation can be applied to the parsing result of `George Washington` which is `Washington -> George` and label `nn`.
* Remove some nodes. For example, nodes after an edge `det`.

This gives a nice recursive function.

We must take care of the properties we want to preserve on our graph:
  - connected: before removing a node (determinant for example), be sure that it is a leaf
  - acyclic: be carefull when merging 2 nodes
  - ...
  
We could try to collapse additional elements. For instance, it would be great to have only one node for `George Washington`.
An idea could be to merge two nodes if one is the parent of the other, and they both have the same (non null) tag.
We could even merge two nodes which have the same parent and the same (non null) tag (by doing this, we would merge `United States` in the sentence `Who was the first United States president?`, which is what we want).

#### 1.3. Name entity recognition

There may be a way to group "same entities" together (ex: George Washington). It's call "name entity recognition". See the pad (http://pad.aliens-lyon.fr/p/ppp-nlp) for some (basic) resources.

Name entity recognition can be useful in two ways:
  - tag and group some parts of the question (ex: name 'Barack Obama', location 'Paris').
  - replace references in sentences (ex: 'What Nadal does when he has to serve?' -> 'What Nadal does when Nadal has to serve?')
  
I made new experiments with the StanfordNLP library. All worked well for the sentence `Barack Obama is the president of the United States.`: the `parsetree` attribute of the resulting object put `George` and `Washington` in a same nominal group. Idem for `United` and `States`. The result in the dependency tree is great too: `George` is a subnode of `Washington` and `United` is a subnode of `States`.

So I hoped to have a good entity recognition tool with StanfordNLP.

Then I tried `Who is the United States president?`. Big fail. In the parse tree, it groups `the United States president` in one nominal group, but does not make a subgroup with only `United States`.
The dependency tree is even worst. There is a subtree for the whole group, with `president` on top, with two children: `United` and `States`. Thus, these two words are separated, which looks pretty bad.

Surprisingly, the parsing of `What is John Smith hair colour?` works very well. The dependencies are correct, and it recognizes `John` and `Smith` as `person`.

I will search other ways, maybe with NLTK library...

As far as I know the NLTK library does not provide a statistical parser (= you cannot have immediately a parse tree, you must design a grammar before). However, it seems that there is a name entity recognition toolkit included in. Otherwise, you can try the online demo of the name entity recognition system provided by coreNLP (called NER, see: http://nlp.stanford.edu/software/corenlp.shtml) here : http://nlp.stanford.edu:8080/ner/process. NER claims to be able to recognize PERSON, LOCATION, ORGANIZATION, MISC, DATE, TIME, MONEY, NUMBER and it works on the example `Who is the United States president?`

**Interesting:** StanfordNLP also provide the meaning of some words in the `words`
attribute (__did you find a description of what this attribute contains ?__ -> It 
comes from the original StanfordNLP library, under the name of `NamedEntityTag`, 
you can check it by running the `corenlp.sh` script in the StanfordNLP repository,
and inputting the desired sentence. I did not find any mention of this in their
paper. I searched this term on google, and found the [Named Entity Recognizer](http://nlp.stanford.edu/software/CRF-NER.shtml).
Did not read yet, but their [online tool](http://nlp.stanford.edu:8080/ner/process)
does exactly what I said). For instance, words `George` and `Washington` are recognized as `person`,
whereas words `United` and `States` are recognized as `location`, in the sentence
`George Washington is the president of the United States.`. It could be very
useful.
-> it's exactly NER. nice.

Even more interesting, in the sentence `What is Pkofjqdaeo Zllitjtpq hair colour?` it recognizes `Pkofjqdaeo` and `Zllitjtpq` as a person (although there is certainly not these words in the dictionary).
Limit: in the sentence `What is the president of Pkofjqdaeo Zllitjtpq?`, the two last words are still considered as a person. Moreover it seems that capital letters can modify the output.
-> WolframAlpha answers: "brown" and "No president, it's a monarchy"...

The date recognition works also well. Parse the sentence `Turing was born on June 23, 1912.`.
It will recognize `June`, `23` and `1912` as a date, and for each one there is an attribute `NormalizedNamedEntityTag` with value `'1912-06-23'` and an attribute `Timex` with value `'<TIMEX3 tid="t1" type="DATE" value="1912-06-23">June 23, 1912</TIMEX3>'` (yes these values are strings, which is sad).

###### Name entity recognition and merging

If we plan to merge nodes that are of the same type, there are 2 ways of doing this from the tree:
  - merging 2 nodes when one is the descendant of the other
  - merging 2 nodes when they have the same parent

The sentence `John likes Yoko.` show that merging two nodes when they have a same 
parend and a same tag is not a good idea.
-> perhaps we must add "same dependency to their parent" (here we have nsubj et dobj)

Be sure this procedure is correct (is it always relevant to merge 2 nodes with the same parents?). An other way to proceed is:
  1. apply Name Entity Recognition
  2. in the __original sentence__ merge all consecutive words of the same type
  3. in the tree, merge the nodes that has been merged in step 2
  
## 2. Pattern recognition

A solution could be to compute questions specifically:

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

And: http://english.stackexchange.com/questions/126317/common-question-structures


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

## 3. Overall algorithm

Here is a first proposition of overall algorithm:

INPUT: question

OUTPUT: conjunction of triples, with at least one hole by triple

1. Compute the dependency tree
2. Apply name entity recognition for merging some nodes and attach description on them (location, name...)
3. Apply as many simplifications (merge, delete...) as possible on the tree. Obtain a new tree that uses a _restricted_ set of dependencies (not 50 dependencies possible, as in Stanford dependency)
4. Identify the "question word" (or type of question)
5. Produce the triples involved by the question type
6. Add the triples involved by other parts of the tree
7. Output the conjunction of all the triples

I think we cannot avoid "hardcoding" the step 5, ie determine (in advance) __all the types__ of possible questions (chat, where, how...) and what triples must be directly produced by each question. In fact, the most difficult thing is to place the "holes" in triples. Analyzing the dependency tree without pre-learned patterns will never allow us to find "from scratch" where holes must be.

_Example:_ Where is born Barack Obama's wife?

1. Parse tree
2. "Barack Obama" is recognized as a name. The 2 nodes are merged
3. Simplifications
4. Question word: where. 
  * The verb is identified ("bear") and the subject ("Barack Obama's wife")
  * The pattern attached to "where" is: `<where> <verb> <subject>` -> `verbIn(subject,x)` where x is the final answer
5. The triple `bearIn(y=Barack Obama's wife,x)` is produced
6. The system produces an extra triple:
  * "Barack Obama's wife" is recognized as a relation of possession. 
  * The triple `wifeOf(y,Barack Obama)` is produce
7. Output: `bearIn(y,x) /\ wifeOf(y,Barack Obama)`

Here we can see that "Barack Obama's wife" can be firstly not considered as an unknown (step 5, in `bearIn(Barack Obama's wife,x)`), and in a second time some additionnal information "destruct" it in a triple (`wifeOf(y,Barack Obama)`). This is interesting because we have progressively "simplified" the set of triples (it's difficult to query `bearIn(Barack Obama's wife,x)` but it's easy to query `wifeOf(y,Barack Obama)`, obtain `y=Michelle Obama` and then query `bearIn(Michelle Obama,x)`).

The big difference between the transformation in triples we perform and transformations in text simplification for example (automatic summarization: only extract triples, without holes) is the __holes__. Produce some triples without holes is much more simpler that what we do. However, I think we can say that the above algorithm places in fact only __one real hole__ (x, the answer we search). Indeed, in the example we could output `bearIn(Barack Obama's wife,x) /\ wifeOf(Barack Obama's wife,Barack Obama)` and then perform as many simplifications on triples as possible. For example:
  - we query `wifeOf(Barack Obama's wife,_)` (_ is a hole). The database gives no answer.
  - we query `wifeOf(_,Barack Obama)`. The database finds `Michelle Obama`. We replace `Barack Obama's wife` everywhere it appears
  - we continue until we success to find the really unknown x
  
Triples such as `wifeOf(Barack Obama's wife,Barack Obama)` can be found directly from the tree, but the only real hole cannot be placed from scratch. This is why we have to study all types of questions patterns.





# Ideas

Somme common draft of the ideas that we may have. The aim is to begin a discussion
about them.

Please have a look at the graphs generated with the Stanford library, and try
your own experimentations.

## First idea

Return the tree given by the Stanford library, with some modifications.

* To each edge, apply some function. For instance, the string `president of France`
will give two nodes under the root node, `president -> France`, with the label
`prep_of` on the edge. We shall transform it into the triple (president, qualifier, 
France). The same transformation can be applied to the parsing result of 
`George Washington` which is `Washington -> George` and label `nn`.
* Remove some nodes. For example, nodes after an edge `det`.

This gives a nice recursive function.

### Critics and improvement

We can observe some incoherencies. 
Consider the two sentences `Who is the president of France?` and `Where does the
singer of Led Zeppelin live?`. The question word is not placed at the same place 
in the obtained tree.

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


Parsing (loading the module)
============================

Run (example):
  `python3 demo1.py`

Launching a server
==================

May need to install [jsonrpclib](https://github.com/tcalmant/jsonrpclib) (for python3).

Go to the folder where CoreNLP is installed (usually the Scripts/ folder) and run:

  CORENLP="stanford-corenlp-full-2014-08-27" python3 -m corenlp

To remove copula relations (other flags can be passed in the same way):

  CORENLP="stanford-corenlp-full-2014-08-27" CORENLP_OPTIONS="-parse.flags \" -makeCopulaHead\"" python3 -m corenlp
     
Parsing using a server
======================

Run (example):
  python3 demo2.py
  
Using a server enables to parse quicker than loading the module each time.


Presentation of the output using dot
====================================

We assume that a server is launched.

You can have a dot file using the following: `python3 > demo.dot` (then, write
your sentence).

You can also have directly a ps file using the following: `python3 demo3.py | dot -Tps > demo.ps`

More laziness: `echo "What is the birth date of the first president of the United States?" | python3 demo3.py | dot -Tps > demo.ps`

Description of demo files
=========================

* demo1.py: parsing without a server. test1.py outputs the direct answer of CoreNLP
* demo2.py: Start server before. demo2.py outputs the dependency from CoreNLP
* demo3.py: Start server before. demo3.py outputs the graph dependency produces from CoreNLP
* demo4.py: Start server before. demo4.py uses functions defined in parsetree_to_triple



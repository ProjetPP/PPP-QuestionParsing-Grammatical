
Parsing (loading the module)
============================

Run (example):
  `python3 test1.py`

Launching a server
==================

May need to install [jsonrpclib](https://github.com/tcalmant/jsonrpclib) (for python3).

Go to the folder where CoreNLP is installed (usually the Scripts/ folder)
and run:
  CORENLP="stanford-corenlp-full-2014-08-27" python3 -m corenlp
     
Parsing using a server
======================

Run (example):
  python3 test2.py
  
Using a server enables to parse quicker (< 1s) than loading the module each time.


Presentation of the output using dot
====================================

We assume that a server is launched.

You can have a dot file using the following: `python3 > test.dot` (then, write
your sentence).

You can also have directly a ps file using the following: `python3 test3.py | dot -Tps > test.ps`

More laziness: `echo "What is the birth date of the first president of the United States?" | python3 test3.py | dot -Tps > test.ps`


Parsing (loading the module)
============================

Run (example):
  `python3 test1.py`

Launching a server
==================

Go into Scripts directory
Run:
  python corenlp-python/corenlp/corenlp.py
  
May need to install [jsonrpclib](https://github.com/tcalmant/jsonrpclib) (for python3).
  
and to replace line 47 (in Scripts/corenlp-python/corenlp/corenlp.py): 
  `DIRECTORY = "stanford-corenlp-full-2014-08-27"`
     
Parsing using a server
======================

Run (example):
  python3 test2.py
  
Using a server enables to parse quicker (< 1s) than loading the module each time.


Presentation of the output using dot
==========================

We assume that a server is launched.

You can have a dot file using the following: `python3 > test.dot` (then, write
your sentence).

You can also have directly a ps file using the following: `python3 test3.py | dot -Tps > test.ps`

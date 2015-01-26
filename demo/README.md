# How to test the Question Parsing algorithm

The files `demo*.py` enable you to test the main steps of the Question Parsing algorithm. You first need to launch a CoreNLP server, and then run a demo file.

## Launching a server

May need to install [jsonrpclib](https://github.com/tcalmant/jsonrpclib) (for python3).

Go to the folder where CoreNLP is installed (`Scripts/` folder if you have cloned the [scripts repository](https://github.com/ProjetPP/Scripts) and run `bash bootstrap_corenlp.sh`). Run:

```bash
CORENLP="stanford-corenlp-full-2014-08-27" CORENLP_OPTIONS="-parse.flags \" -makeCopulaHead\"" python3 -m corenlp
```

## Choosing a demo file

Here is a description of the demo files:

* `demo1.py`: Output the dependency relations graph from CoreNLP (this file is the only one that does not need to run a server. On the other hand, it's really slow. Moreover, copula relations are not removed)
* `demo2.py`: Output the dependency relations graph from CoreNLP
* `demo3.py`: Output the dependency relations graph from CoreNLP in dot format
* `demo4.py`: Output the dependency graph in dot format after preprocessing simplifications (merging of some nodes)
* `demo5.py`: Output the dependency graph in dot format after dependency analysis
* `demo6.py`: Full algorithm, output the final normal form from question

## Examples

Here is some examples on the input question `Where is the capital of Belgium?`.

* Save the dependency graph in dot format into `demo.dot`: 
```bash
python3 demo3.py > demo.dot
Where is the capital of Belgium?
```

* Save the dependency graph in ps format after preprocessing simplifications. Display the graph:
```bash
python3 demo4.py | dot -Tps > demo.ps
Where is the capital of Belgium?
evince demo.ps
``` 

* Save the dependency graph in ps format after preprocessing simplifications (more laziness):
```bash
echo "Where is the capital of Belgium?" | python3 demo4.py | dot -Tps > demo.ps
```

* Display the dependency graph in ps format after preprocessing simplifications (even more laziness):
```bash
bash displaygraph.sh Where is the capital of Belgium?
```

* Display the final normal form:
```bash
python3 demo6.py
Where is the capital of Belgium?
``` 

## Dataset generation

Fill in a file `dataset.in` with one question per line. Run the following code to parse each question and save its normal form into `dataset.out`:

```bash
python3 datasetGeneration.py < dataset.in > dataset.out 2> dataset.error
```

import sys
import ppp_datamodel
from .preprocessing import DependenciesTree
from ppp_datamodel import Resource, Missing, Triple, Last, First, List, Sort, Intersection, Union, Exists
from .data.conjunction import conjunctionTab
from .data.superlative import superlativeNoun, superlativeOrder
from .data.exceptions import GrammaticalError

def buildValue(tree):
    """
        Used to build the values of the normal form.
            len(tree.getWords()) = 1 -> single value, use a string
            len(tree.getWords()) > 1 -> alternatives, use a list of strings
    """
    if len(tree.getWords()) == 1:
        return tree.getWords()[0]
    else:
        return tree.getWords()

def normalizeSuperlative(tree):
    """
        Handle Rspl dependency (superlative, ordinal)
    """
    assert len(tree.getWords()) == 1 # only one possible superlative
    assert len(tree.child) == 1
    if buildValue(tree) in superlativeNoun:
        if buildValue(tree) in superlativeOrder:
            return superlativeOrder[buildValue(tree)](list=Sort(list=normalize(tree.child[0]),predicate=superlativeNoun[buildValue(tree)]))
        else:
            return First(list=Sort(list=normalize(tree.child[0]),predicate=superlativeNoun[buildValue(tree)])) # First by default
    else:
        if buildValue(tree) in superlativeOrder:
            return superlativeOrder[buildValue(tree)](list=Sort(list=normalize(tree.child[0]),predicate='default')) # default predicate
        else:
            return First(list=Sort(list=normalize(tree.child[0]),predicate='default'))

def normalizeConjunction(tree):
    """
        Handle Rconj dependency (conjunction)
    """
    result = []
    assert len(tree.getWords()) == 1
    assert len(tree.child) == 2 and tree.child[0].dependency.startswith('Rconj') and tree.child[1].dependency.startswith('Rconj')
    if tree.child[0].dependency == 'RconjT':
        result = [normalize(tree.child[0]),normalize(tree.child[1])]
    else:
        result = [normalize(tree.child[1]),normalize(tree.child[0])]    
    try:
        return conjunctionTab[buildValue(tree)](list=result)
    except KeyError:
        raise GrammaticalError(buildValue(tree),"conjunction unknown")

def normalize(tree):
    """
        Map the tree to a normal form (= final result)
    """
    if tree.child == []: # leaf
        return Resource(value=buildValue(tree))
    if tree.child[0].dependency == 'Rexist':
        return Exists(list = normalize(tree.child[0]))
    if tree.child[0].dependency == 'Rspl': # Rspl = superlative, ordinal
        return normalizeSuperlative(tree)
    if tree.child[0].dependency.startswith('Rconj'): # Rconj = conjunction
        return normalizeConjunction(tree)
    result = []
    for t in tree.child: # R0 ... R5
        assert t.dependency != 'Rspl' and not t.dependency.startswith('Rconj')
        if t.dependency == 'R0':
            result.append(normalize(t))
        if t.dependency == 'R1':
            result.append(Resource(value=buildValue(t)))
        if t.dependency == 'R2': # ou enlever la condition, ça devient R5
            if len(t.child) == 0:
                result.append(Triple(subject=Resource(value=buildValue(t)), predicate=Resource(value=buildValue(tree)), object=Missing()))
            else:
                result.append(normalize(t))
        if t.dependency == 'R3':
            result.append(Triple(subject=Missing(), predicate=Resource(value=buildValue(tree)), object=normalize(t)))
        if t.dependency == 'R4':
            result.append(Triple(subject=Missing(), predicate=normalize(t), object=Resource(value=buildValue(tree))))
        if t.dependency == 'R5' or t.dependency == 'R5s':
            result.append(Triple(subject=normalize(t), predicate=Resource(value=buildValue(tree)), object=Missing()))
        #if t.dependency == 'R6': # not use for the moment
        #   result.append(Triple(subject=Resource(value=buildValue(tree)), predicate=normalize(t), object=Missing()))
    if len(result) == 1:
        return result[0]
    else:
        return Intersection(list=result)

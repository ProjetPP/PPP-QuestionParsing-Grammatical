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
            len(tree.getWords()) = 1 -> single value -> return a resource
            len(tree.getWords()) > 1 -> multiple alternatives -> return a list of resources
    """
    if len(tree.getWords()) == 1:
        return Resource(tree.getWords()[0])
    else:
        return List([Resource(x) for x in tree.getWords()])

def normalizeSuperlative(tree):
    """
        Handle Rspl dependency (superlative, ordinal)
    """
    assert len(tree.getWords()) == 1 and len(tree.child) == 1
    superlative = tree.getWords()[0]
    if superlative in superlativeNoun:
        if superlative in superlativeOrder:
            return superlativeOrder[superlative](Sort(normalize(tree.child[0]),Resource(superlativeNoun[superlative])))
        else:
            return First(Sort(normalize(tree.child[0]),Resource(superlativeNoun[superlative]))) # First by default
    else:
        if superlative in superlativeOrder:
            return superlativeOrder[superlative](Sort(normalize(tree.child[0]),Resource('default'))) # default predicate
        else:
            return First(Sort(normalize(tree.child[0]),Resource('default')))

def normalizeConjunction(tree):
    """
        Handle Rconj dependency (conjunction)
    """
    result = []
    assert len(tree.getWords()) == 1
    assert len(tree.child) == 2 and tree.child[0].dependency.startswith('Rconj') and tree.child[1].dependency.startswith('Rconj')
    conjunction = tree.getWords()[0]
    if tree.child[0].dependency == 'RconjT':
        result = [normalize(tree.child[0]),normalize(tree.child[1])]
    else:
        result = [normalize(tree.child[1]),normalize(tree.child[0])]    
    try:
        return conjunctionTab[conjunction](result)
    except KeyError:
        raise GrammaticalError(conjunction,"conjunction unknown")

def normalize(tree):
    """
        Map the tree to a normal form (= final result)
    """
    if tree.child == []: # leaf
        return buildValue(tree)
    if tree.child[0].dependency == 'Rexist':
        return Exists(normalize(tree.child[0]))
    if tree.child[0].dependency == 'Rspl': # Rspl = superlative, ordinal
        return normalizeSuperlative(tree)
    if tree.child[0].dependency.startswith('Rconj'): # Rconj = conjunction
        return normalizeConjunction(tree)
    result = []
    for t in tree.child: # R0 ... R7
        if t.dependency == 'R0':
            result.append(normalize(t))
        if t.dependency == 'R1':
            result.append(buildValue(t))
        if t.dependency == 'R2':
            if len(t.child) == 0:
                result.append(Triple(buildValue(t),buildValue(tree),Missing()))
            else:
                result.append(normalize(t))
        if t.dependency == 'R3':
            result.append(Triple(Missing(),buildValue(tree),normalize(t)))
        if t.dependency == 'R4':
            result.append(Triple(Missing(),normalize(t),buildValue(tree)))
        if t.dependency == 'R5':
            result.append(Triple(normalize(t),buildValue(tree),Missing()))
        if t.dependency == 'R6':
           result.append(Triple(Missing(),Resource('instance of'),normalize(t)))
        if t.dependency == 'R7':
            result.append(Triple(buildValue(tree),normalize(t),Missing()))
    if len(result) == 1:
        return result[0]
    else:
        return Intersection(result)

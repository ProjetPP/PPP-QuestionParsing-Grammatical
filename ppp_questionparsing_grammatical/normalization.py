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
            len(tree.getWords()) > 1 -> alternatives, use a list of resources
    """
    if len(tree.getWords()) == 1:
        return Resource(value=tree.getWords()[0])
    else:
        return List([Resource(value=x) for x in tree.getWords()])

def normalizeSuperlative(tree):
    """
        Handle Rspl dependency (superlative, ordinal)
    """
    assert len(tree.getWords()) == 1 and len(tree.child) == 1
    superlative = tree.getWords()[0]
    if superlative in superlativeNoun:
        if superlative in superlativeOrder:
            return superlativeOrder[superlative](list=Sort(list=normalize(tree.child[0]),predicate=Resource(value=superlativeNoun[superlative])))
        else:
            return First(list=Sort(list=normalize(tree.child[0]),predicate=Resource(value=superlativeNoun[superlative]))) # First by default
    else:
        if superlative in superlativeOrder:
            return superlativeOrder[superlative](list=Sort(list=normalize(tree.child[0]),predicate=Resource(value='default'))) # default predicate
        else:
            return First(list=Sort(list=normalize(tree.child[0]),predicate=Resource(value='default')))

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
        return conjunctionTab[conjunction](list=result)
    except KeyError:
        raise GrammaticalError(conjunction,"conjunction unknown")

def normalize(tree):
    """
        Map the tree to a normal form (= final result)
    """
    if tree.child == []: # leaf
        return buildValue(tree)
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
            result.append(buildValue(t))
        if t.dependency == 'R2': # ou enlever la condition, ça devient R5
            if len(t.child) == 0:
                result.append(Triple(subject=buildValue(t), predicate=buildValue(tree), object=Missing()))
            else:
                result.append(normalize(t))
        if t.dependency == 'R3':
            result.append(Triple(subject=Missing(), predicate=buildValue(tree), object=normalize(t)))
        if t.dependency == 'R4':
            result.append(Triple(subject=Missing(), predicate=normalize(t), object=buildValue(tree)))
        if t.dependency == 'R5' or t.dependency == 'R5s':
            result.append(Triple(subject=normalize(t), predicate=buildValue(tree), object=Missing()))
        if t.dependency == 'R6':
           result.append(Triple(subject=Missing(), predicate=Resource(value='instance of'), object=normalize(t)))
        if t.dependency == 'R7':
            result.append(Triple(subject=buildValue(tree), predicate=normalize(t), object=Missing()))
    if len(result) == 1:
        return result[0]
    else:
        return Intersection(list=result)

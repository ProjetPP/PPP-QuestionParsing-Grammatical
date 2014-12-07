import sys
import ppp_datamodel
from .preprocessing import DependenciesTree
from ppp_datamodel import Resource, Missing, Triple, Last, First, List, Sort, Intersection, Union

superlativeTab = {
    # how to sort dependending on the superlative
    'biggest'   : 'size',
    'largest'   : 'width'
}

conjunctionTab = {
    'and'       : Intersection,
    'or'        : Union
}

def normalizeSuperlative(tree):
    """
        Handle Rspl dependency (superlative, ordinal)
    """
    assert len(tree.child) ==1
    try: 
        return Last(list=Sort(list=normalize(tree.child[0]),predicate=superlativeTab[tree.getWords()])) # last / first
    except KeyError:
        return First(list=Sort(list=normalize(tree.child[0]),predicate='default'))

def normalizeConjunction(tree):
    """
        Handle Rconj dependency (conjunction)
    """
    result = []
    assert len(tree.child) == 2 and tree.child[0].dependency.startswith('Rconj') and tree.child[1].dependency.startswith('Rconj')
    if tree.child[0].dependency == 'RconjT':
        result = [normalize(tree.child[0]),normalize(tree.child[1])]
    else:
        result = [normalize(tree.child[1]),normalize(tree.child[0])]    
    try:
        return conjunctionTab[tree.getWords()](list=result)
    except KeyError:
        sys.exit('conjunction unknown')

def normalize(tree):
    """
        Map the tree to a normal form (= final result)
    """
    if tree.child == []: # leaf
        return Resource(value=tree.getWords())
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
            result.append(Resource(value=t.getWords()))
        if t.dependency == 'R2': # ou enlever la condition, ça devient R5
            if len(t.child) == 0:
                result.append(Triple(subject=Resource(value=t.getWords()), predicate=Resource(value=tree.getWords()), object=Missing()))
            else:
                result.append(normalize(t))
        if t.dependency == 'R3':
            result.append(Triple(subject=Missing(), predicate=Resource(value=tree.getWords()), object=normalize(t)))
        if t.dependency == 'R4':
            result.append(Triple(subject=Missing(), predicate=normalize(t), object=Resource(value=tree.getWords())))
        if t.dependency == 'R5':
            result.append(Triple(subject=normalize(t), predicate=Resource(value=tree.getWords()), object=Missing()))
        #if t.dependency == 'R6': # not use for the moment
        #   result.append(Triple(subject=Resource(value=tree.getWords()), predicate=normalize(t), object=Missing()))
    if len(result) == 1:
        return result[0]
    else:
        return Intersection(list=result)

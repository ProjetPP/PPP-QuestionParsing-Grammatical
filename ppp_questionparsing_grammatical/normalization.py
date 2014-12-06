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
        Handle R6 dependency (superlative, ordinal)
    """
    assert len(tree.child) ==1
    try: 
        return Last(list=Sort(list=normalize(tree.child[0]),predicate=superlativeTab[tree.getWords()])) # last / first
    except KeyError:
        return First(list=Sort(list=normalize(tree.child[0]),predicate='default'))

def normalizeConjunction(tree):
    """
        Handle R7 dependency (conjunction)
    """
    result = []
    for t in tree.child:
        assert t.dependency == 'R7'
        result.append(normalize(t))
    try:
        return conjunctionTab[tree.getWords()](list=result)
    except KeyError:
        sys.exit('unknown conjunction')
    
def normalize(tree):
    """
        Map the tree to a normal form (= final result)
    """
    if tree.child == []: # leaf
        return Resource(value=tree.getWords())
    if tree.child[0].dependency == 'R6': # R6 = superlative, ordinal
        return normalizeSuperlative(tree)
    if tree.child[0].dependency == 'R7': # R7 = conjunction
        return normalizeConjunction(tree)
    result = []
    for t in tree.child: # R1 ... R5, R8
        assert t.dependency != 'R6' and t.dependency != 'R7'
        if t.dependency == 'R0':
            result.append(normalize(t))
        if t.dependency == 'R1': # ou enlever la condition, ça devient R4
            if len(t.child) == 0:
                result.append(Triple(subject=Resource(value=t.getWords()), predicate=Resource(value=tree.getWords()), object=Missing()))
            else:
                result.append(normalize(t))
        if t.dependency == 'R2':
            result.append(Triple(subject=Missing(), predicate=Resource(value=tree.getWords()), object=normalize(t)))
        if t.dependency == 'R3':
            result.append(Triple(subject=Missing(), predicate=normalize(t), object=Resource(value=tree.getWords())))
        if t.dependency == 'R4':
            result.append(Triple(subject=normalize(t), predicate=Resource(value=tree.getWords()), object=Missing()))
        if t.dependency == 'R5':
           result.append(Triple(subject=Resource(value=tree.getWords()), predicate=normalize(t), object=Missing()))
        if t.dependency == 'R8':
            result.append(Resource(value=t.getWords()))
    if len(result) == 1:
        return result[0]
    else:
        return Intersection(list=result)

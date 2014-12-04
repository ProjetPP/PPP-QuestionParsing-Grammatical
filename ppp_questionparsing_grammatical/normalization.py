import sys
import ppp_datamodel
from .preprocessing import DependenciesTree

sortTab = {
    # how to sort dependending on the superlative
    'biggest'   : 'size',
    'largest'   : 'width'
}

def normalize(tree):
    if tree.child == []: # leaf
        return ppp_datamodel.Resource(value=tree.getWords())
    if tree.child[0].dependency == 'R6': # R6 = superlative, ordinal
        assert len(tree.child) ==1
        try: # <------------------------
            return ppp_datamodel.Last(list=[ppp_datamodel.Sort(list=[normalize(tree.child[0])],predicate=sortTab[tree.getWords()])]) # last / first
        except KeyError:
            return ppp_datamodel.First(list=[ppp_datamodel.Sort(list=[normalize(tree.child[0])],predicate='default')])
    if tree.child[0].dependency == 'R7': # R7 = conjunction
        result = []
        for t in tree.child:
            assert t.dependency == 'R7'
            result.append(normalize(t))
        if tree.getWords() == 'and':
            return ppp_datamodel.Intersection(list=result)
        if tree.getWords() == 'or':
            return ppp_datamodel.Union(list=result)
    result = []
    for t in tree.child: # R1 ... R5, R8
        assert t.dependency != 'R6' and t.dependency != 'R7'
        if t.dependency == 'R0':
            result.append(normalize(t))
        if t.dependency == 'R1': # ou enlever la condition, ça devient R4
            if len(t.child) == 0:
                result.append(ppp_datamodel.Triple(subject=ppp_datamodel.Resource(value=t.getWords()), predicate=ppp_datamodel.Resource(value=tree.getWords()), object=ppp_datamodel.Missing()))
            else:
                result.append(normalize(t))
        if t.dependency == 'R2':
            result.append(ppp_datamodel.Triple(subject=ppp_datamodel.Missing(), predicate=ppp_datamodel.Resource(value=tree.getWords()), object=normalize(t)))
        if t.dependency == 'R3':
            result.append(ppp_datamodel.Triple(subject=ppp_datamodel.Missing(), predicate=normalize(t), object=ppp_datamodel.Resource(value=tree.getWords())))
        if t.dependency == 'R4':
            result.append(ppp_datamodel.Triple(subject=normalize(t), predicate=ppp_datamodel.Resource(value=tree.getWords()), object=ppp_datamodel.Missing()))
        if t.dependency == 'R5':
           result.append(ppp_datamodel.Triple(subject=ppp_datamodel.Resource(value=tree.getWords()), predicate=normalize(t), object=ppp_datamodel.Missing()))
        if t.dependency == 'R8':
            result.append(ppp_datamodel.Resource(value=t.getWords()))
    if len(result) == 1:
        return result[0]
    else:
        return ppp_datamodel.Intersection(list=result)

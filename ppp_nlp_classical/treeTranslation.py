
import sys
import ppp_datamodel
from .tripleProduction import TriplesBucket

def newNode(triplesBucket,t):
    """
        build a tree of root t, with all the triples of triplesBucket possibles
    """
    if not t:
        return ppp_datamodel.Missing()
    if isinstance(t.subjectT,int):
        sub_t = triplesBucket.extractTriple(t.subjectT)
        subj = newNode(triplesBucket,sub_t)
    else:
        subj = ppp_datamodel.Resource(value=t.subjectT)
    if isinstance(t.predicateT,int):
        sub_t = triplesBucket.extractTriple(t.predicateT)
        pred = newNode(triplesBucket,sub_t)
    else:
        pred = ppp_datamodel.Resource(value=t.predicateT)
    if isinstance(t.objectT,int):
        sub_t = triplesBucket.extractTriple(t.objectT)
        obj = newNode(triplesBucket,sub_t)
    else:
        obj = ppp_datamodel.Resource(value=t.objectT)
    return ppp_datamodel.Triple(subject=subj, predicate=pred, object=obj)

def buildTree(triplesBucket):
    """
        build a tree from a triplesBucket
    """
    t = triplesBucket.extractTriple(0) # 0 = main unknown
    assert t # != None
    return newNode(triplesBucket,t)

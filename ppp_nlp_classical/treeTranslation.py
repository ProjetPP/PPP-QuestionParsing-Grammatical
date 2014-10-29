
import sys
import ppp_datamodel
from .tripleProduction import TriplesBucket

def newNode(triplesBucket,t):
    """
        build a tree of root t, with all the triples of triplesBucket possibles
    """
    if isinstance(t.subjectT,int):
        sub_t = triplesBucket.extractTriple(t.subjectT)
        if not sub_t:
            subj = ppp_datamodel.Missing()
        else:
            subj = newNode(triplesBucket,sub_t)
    else:
        subj = ppp_datamodel.Resource(value=t.subjectT)
    if isinstance(t.predicateT,int):
        sub_t = triplesBucket.extractTriple(t.predicateT)
        if not sub_t:
            pred = ppp_datamodel.Missing()
        else:
            pred = newNode(triplesBucket,sub_t)
    else:
        pred = ppp_datamodel.Resource(value=t.predicateT)
    if isinstance(t.objectT,int):
        sub_t = triplesBucket.extractTriple(t.objectT)
        if not sub_t:
            obj = ppp_datamodel.Missing()
        else:
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


import sys
import ppp_datamodel
from .tripleProduction import TriplesBucket

def newSubNode(triplesBucket,t):
    """
        built the subtree of root t
    """
    if isinstance(t,int):
        sub_t = triplesBucket.extractTriple(t)
        return newNode(triplesBucket,sub_t)
    else:
        return ppp_datamodel.Resource(value=t)

def newNode(triplesBucket,t):
    """
        build a tree of root t, with all the triples of triplesBucket possibles
    """
    if not t:
        return ppp_datamodel.Missing()
    subj=newSubNode(triplesBucket,t.subjectT)
    pred=newSubNode(triplesBucket,t.predicateT)
    obj=newSubNode(triplesBucket,t.objectT)
    return ppp_datamodel.Triple(subject=subj, predicate=pred, object=obj)

def buildTree(triplesBucket):
    """
        build a tree from a triplesBucket
    """
    t = triplesBucket.extractTriple(0) # 0 = main unknown
    assert t # != None
    return newNode(triplesBucket,t)

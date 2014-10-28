""" Third step of the algorithm."""

import sys

# define a triple class ?
    
def getWords(t):
    """
        concatenate all strings of the node (in wordList)
    """
    l = t.wordList
    l.sort(key = lambda x: x[1]) 
    s = ''
    for w in l:
        s += ' ' + w[0]
    return s
    
def tripleProduce1(t,nodeToID,triplesBucket):
    """
        a -b-> c : ?A = ?C
    """
    assert t.parent in not None
    for tr in triplesBucket:
        for i in range(0,3):
            if tr[i] == nodeToID[t]:
                tr[i] = nodeToID[t.parent]
    nodeToID[t] = nodeToID[t.parent]
    
def tripleProduce2(t,nodeToID,triplesBucket,suffix=''):
    """
        a -b-> c : a(?A,c)
        suffix: for prep_x
    """
    assert t.parent is not None
    triplesBucket.append([nodeToID[t.parent],
                          '%s %s' % (getWords(t.parent), +suffix),
                          getWords(t)])

def tripleProduce3(t,nodeToID,triplesBucket):
    """
        a -b-> c : c(?A,a)
    """
    assert t.parent is not None
    triplesBucket.append([nodeToID[t.parent],
                          getWords(t),
                          getWords(t.parent)])
        
tripleMap = {
    'root'    : tripleProduce1,
    'subj'    : tripleProduce1,
    'comp'    : tripleProduce2,
    'pos'     : tripleProduce2,
    'mod'     : tripleProduce3,
    'amod'    : tripleProduce3,
    'vmod'    : tripleProduce1
}

def initIndexes(t,nodeToID,index):
    """
        assign a different index to each node
    """
    nodeToID[t] = index
    index += 1
    for c in t.child:
        index = initIndexes(c,nodeToID,index)
    return index

def fillBucket(t,nodeToID,triplesBucket,tmap=tripleMap):
    """
        triple analysis of node t
    """
    if t.dependency in tmap:
        tmap[t.dependency](t,nodeToID,triplesBucket)
    if t.dependency.startswith('prep'): # prep_x or prepc_x
        prep = t.dependency[t.dependency.rindex('_')+1:]
        tripleProduce2(t,nodeToID,triplesBucket,prep)
    for c in t.child:
        fillBucket(c,nodeToID,triplesBucket)

def buildBucket(t):
    """
        return a set of 3-list (made of int = unknown, or words = str) 
    """
    nodeToID = {}
    triplesBucket = []
    initIndexes(t,nodeToID,0)
    fillBucket(t,nodeToID,triplesBucket)
    return triplesBucket

def printTriple(l):
    """
        print the triple l
    """
    s = [None] * 3
    for i in range(0,3):
        if isinstance(l[i], int):
            if l[i] == 0: #root
                s[i] = '??' # the answer of the question
            else:
                s[i] = '?%s' % l[i]
        else:
            s[i] = l[i]
    print('(%s | %s | %s)' % (s[0], s[1], s[2]))
       
def printTriples(t):
    """
        print all the triples
    """
    triplesBucket = buildBucket(t)
    for l in triplesBucket:
        printTriple(l)

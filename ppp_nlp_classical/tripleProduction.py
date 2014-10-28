""" Third step of the algorithm."""

import sys

# define a triple class ?

def tripleProduce1(t,nodeToID,triplesBucket):
    """
        a -b-> c : ?A = ?C
    """
    assert t.parent != None
    for tr in triplesBucket:
        for i in range(0,3):
            if tr[i] == nodeToID[t]:
                tr[i] = nodeToID[t.parent]
    nodeToID[t] = nodeToID[t.parent]
    
def tripleProduce2(t,nodeToID,triplesBucket):
    """
        a -b-> c : a(?A,c)
    """
    assert t.parent != None
    triplesBucket.append([nodeToID[t.parent],t.parent.wordList,t.wordList])

def tripleProduce3(t,nodeToID,triplesBucket):
    """
        a -b-> c : c(?A,a)
    """
    assert t.parent != None
    triplesBucket.append([nodeToID[t.parent],t.wordList,t.parent.wordList])
        
tripleMap = {
    'root'    : tripleProduce1,
    'subj'    : tripleProduce1, # or 1
    'comp'    : tripleProduce2,
    'pos'     : tripleProduce2,
    'mod'     : tripleProduce3,
    'amod'    : tripleProduce3,
    'vmod'    : tripleProduce1
}

def giveIndexes(t,nodeToID,index):
    """
        give a different index to each node
    """
    nodeToID[t] = index
    index += 1
    for c in t.child:
        index = giveIndexes(c,nodeToID,index)
    return index

def fillBucket(t,nodeToID,triplesBucket,tmap=tripleMap):
    """
        triple analysis of node t
    """
    if t.dependency in tmap:
        tmap[t.dependency](t,nodeToID,triplesBucket)
    if t.dependency.startswith('prep'): # NO : we only merge temporarily the x of prep_x (ex: Who is the first black president of the United states)
        prep = t.dependency[t.dependency.rindex('_')+1:]
        t.parent.wordList += ([(prep,50)]) # 50 : not good, should be do during preprocessing
        tripleProduce2(t,nodeToID,triplesBucket) # produce2
    for c in t.child:
        fillBucket(c,nodeToID,triplesBucket)

def buildBucket(t):
    """
        return a set of 3-list (made of int = unknown, or words = list of str*int) 
    """
    nodeToID = {}
    triplesBucket = []
    giveIndexes(t,nodeToID,0)
    fillBucket(t,nodeToID,triplesBucket)
    return triplesBucket
    
def getWords(l):
    #l.sort(key = lambda x: x[1]) 
    s = ''
    for w in l:
        s += ' ' + w[0]
    return s

def printTriple(l):
    s = [None] * 3
    for i in range(0,3):
        if isinstance(l[i], int):
            if l[i] == 0: #root
                s[i] = '??'
            else:
                s[i] = '?' + str(l[i])
        else:
            s[i] = getWords(l[i])
    print('(%s | %s | %s)' % (s[0], s[1], s[2]))
       
def printTriples(t):
    triplesBucket = buildBucket(t)
    for l in triplesBucket:
        printTriple(l)




""" Third step of the algorithm."""

import sys

class Triple:
    """
        a triple is (subject,predicate,object)
        for x in (subject,predicate,object), x is:
            either a string (= fixed information)
            or an int (= unknown)
    """
    def __init__(self, subjectT = None, predicateT = None, objectT = None ):
        self.subjectT = subjectT
        self.predicateT = predicateT
        self.objectT = objectT

    def renameUnknown(self,x,new_x):
        """
            unknown x is replaced by new_x everywhere it appears (means that x = x_new)
        """
        if self.subjectT == x:
            self.subjectT = new_x
        if self.predicateT == x:
            self.predicateT = new_x
        if self.objectT == x:
            self.objectT = new_x

    def tripleUnit(self,t):
        """
            triple to string
        """
        if isinstance(t,int):
            if t == 0:
                return '??'
            else:
                return '?' + str(t)
        else:
            return t

    def __str__(self):
        return '(%s | %s | %s)' % (self.tripleUnit(self.subjectT),self.tripleUnit(self.predicateT),self.tripleUnit(self.objectT))

class TriplesBucket:
    """
        set of triples
    """
    def __init__(self, bucket = None):
        self.bucket = bucket or []

    def addTriple(self,t):
        self.bucket.append(t)

    def removeTriple(self,t):
        self.bucket.remove(t)
        
    def renameUnknown(self,x,new_x):
        for t in self.bucket:
            t.renameUnknown(x,new_x)

    def extractTriple(self,x): # extract a triple that contains the unknown x
        for t in self.bucket:
            if t.subjectT == x or t.predicateT == x or t.objectT == x:
                self.removeTriple(t)
                return t
        return None
    
    def __str__(self):
        return '\n'.join(str(x) for x in self.bucket)

#####################
# Triple production #
#####################

# Rules of production of triples

def tripleProduce0(t,nodeToId,triplesBucket):
    pass

def tripleProduce1(t,nodeToID,triplesBucket):
    """
        a -b-> c : ?A = ?C
    """
    assert t.parent is not None
    if not t.child: # Who is the author of the book, "The Iron Lady : A Biography of Margaret Thatcher"?
        tripleProduce2(t,nodeToID,triplesBucket)
    else:
        triplesBucket.renameUnknown(nodeToID[t],nodeToID[t.parent])
        nodeToID[t] = nodeToID[t.parent]

def tripleProduce2(t,nodeToID,triplesBucket,suffix=''):
    """
        a -b-> c : a(?A,c) if c is a leaf
                   a(?A,?C) otherwise
        suffix: for prep_x
    """
    assert t.parent is not None
    if suffix != '':
        suffix = ' %s' % suffix
    if not t.child:
        triplesBucket.addTriple(Triple(nodeToID[t.parent],
                                       '%s%s' % (t.parent.getWords(), suffix),
                                       t.getWords()))
    else:
        triplesBucket.addTriple(Triple(nodeToID[t.parent],
                                       '%s%s' % (t.parent.getWords(), suffix),
                                       nodeToID[t]))

def tripleProduce3(t,nodeToID,triplesBucket):
    """
        a -b-> c : c(?A,a)
    """
    assert t.parent is not None
    triplesBucket.addTriple(Triple(nodeToID[t.parent],
                                   t.getWords(),
                                   t.parent.getWords()))

tripleMap = {
    't0'    : tripleProduce0,
    't1'    : tripleProduce1,
    't2'    : tripleProduce2,
    't3'    : tripleProduce3
}

def initUnknowns(t,nodeToID,unknown=0):
    """
        assign a different unknown to each node
    """
    nodeToID[t] = unknown
    unknown += 1
    for c in t.child:
        unknown = initUnknowns(c,nodeToID,unknown)
    return unknown

def fillBucket(t,nodeToID,triplesBucket,tmap=tripleMap):
    """
        triple analysis of node t
    """
    if t.dependency in tmap:
        tmap[t.dependency](t,nodeToID,triplesBucket)
    if t.dependency.startswith('prep'): # prep_x or prepc_x
        prep = t.dependency[t.dependency.rindex('_')+1:]
        tripleProduce2(t,nodeToID,triplesBucket,prep)
    for c in t.child: # could become necessary to perform this step before
        fillBucket(c,nodeToID,triplesBucket)

questionMap = {
    'What'          : 'definition',
    'What kind'     : 'kind',
    'What type'     : 'type',
    'What sort'     : 'sort',
    'What time'     : 'time',
    'When'          : 'time',
    'Why'           : 'reason',
    'Where'         : 'location',
    'Who'           : 'identity',
    'How'           : 'way',
    'How much'      : 'quantity',
    'How many'      : 'number',
    'How old'       : 'age',
    'How far'       : 'distance',
    'How long'      : 'length',
    'How tall'      : 'height',
    'How deep'      : 'depth',
    'How wide'      : 'width',
    'How fast'      : 'speed',
    'How often'     : 'frequency',
    'How come'      : 'reason',
    'Which'         : 'identity',
    'Whom'          : 'identity',
    'Whose'         : 'identity'
}

def buildBucket(t,qw):
    """
        return a TriplesBucket associated to tree t and question word qw
    """
    nodeToID = {}
    triplesBucket = TriplesBucket()
    initUnknowns(t,nodeToID)
    triplesBucket.addTriple(Triple(nodeToID[t.child[0]],questionMap[qw],nodeToID[t])) # process the question word
    fillBucket(t,nodeToID,triplesBucket)
    return triplesBucket

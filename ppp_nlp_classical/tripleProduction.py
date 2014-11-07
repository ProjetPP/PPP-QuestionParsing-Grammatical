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
        
    def isEmpty(self): # true iff empty
        return not self.bucket
        
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
        a -b-> c : (c,a,?A) if c is a leaf
                   ?A = ?C otherwise
    """
    assert t.parent is not None
    if not t.child:
        tripleProduce4(t,nodeToID,triplesBucket)
    else:
        triplesBucket.renameUnknown(nodeToID[t],nodeToID[t.parent])
        nodeToID[t] = nodeToID[t.parent]

def tripleProduce2(t,nodeToID,triplesBucket,suffix=''):
    """
        a -b-> c : (?A,a,c) if c is a leaf
                   (?A,a,?C) otherwise
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
        a -b-> c : (?A,c,a) if c is a leaf
                   (?A,?C,a) otherwise
    """
    assert t.parent is not None
    if not t.child:
        triplesBucket.addTriple(Triple(nodeToID[t.parent],
                                       t.getWords(),
                                       t.parent.getWords()))
    else:
        triplesBucket.addTriple(Triple(nodeToID[t.parent],
                                       nodeToID[t],
                                       t.parent.getWords()))
                                           
def tripleProduce4(t,nodeToID,triplesBucket):
    """
        a -b-> c : (c,a,?A) if c is a leaf
                   (?C,a,?A) otherwise
    """
    assert t.parent is not None
    if not t.child:
        triplesBucket.addTriple(Triple(t.getWords(),
                                       t.parent.getWords(),
                                       nodeToID[t.parent]))
    else:
        triplesBucket.addTriple(Triple(nodeToID[t],
                                       t.parent.getWords(),
                                       nodeToID[t.parent]))

def tripleProduce5(t,nodeToID,triplesBucket):
    """
        a -b-> c : (a,c,?A) if c is a leaf
                   (a,?C,?A) otherwise <-- or exit error? because ?C is strange
    """
    assert t.parent is not None
    if not t.child:
        triplesBucket.addTriple(Triple(t.parent.getWords(),
                                       t.getWords(),
                                       nodeToID[t.parent]))
    else:
        triplesBucket.addTriple(Triple(t.parent.getWords(),
                                       nodeToID[t],
                                       nodeToID[t.parent]))
                                                                                                        
tripleMap = {
    't0'    : tripleProduce0,
    't1'    : tripleProduce1,
    't2'    : tripleProduce2,
    't3'    : tripleProduce3,
    't4'    : tripleProduce4,
    't5'    : tripleProduce5
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
        prep = t.dependency[t.dependency.index('_')+1:] #_+ could be removed
        tripleProduce4(t,nodeToID,triplesBucket) #_+ instead of tripleProduce2(t,nodeToID,triplesBucket,prep) <--- preposition always remove now
    for c in t.child: # could become necessary to perform this step before
        fillBucket(c,nodeToID,triplesBucket)

questionMap = {
    # close question word
    'is'            : 'yesno',
    'are'           : 'yesno',
    'am'            : 'yesno',
    'was'           : 'yesno',
    'were'          : 'yesno',
    'will'          : 'yesno',
    'do'            : 'yesno',
    'does'          : 'yesno',
    'did'           : 'yesno',
    'have'          : 'yesno',
    'had'           : 'yesno',
    'has'           : 'yesno',
    'can'           : 'yesno',
    'could'         : 'yesno',
    'should'        : 'yesno',
    'shall'         : 'yesno',
    'may'           : 'yesno',
    'might'         : 'yesno',
    'would'         : 'yesno',
    # open question word
    'what'          : 'definition',
    'what kind'     : 'description',
    'what type'     : 'type',
    'what sort'     : 'type',
    'what time'     : 'time',
    'when'          : 'time',
    'why'           : 'reason',
    'where'         : 'place',
    'who'           : 'person',
    'how'           : 'manner',
    'how much'      : 'amount',
    'how many'      : 'quantity',
    'how old'       : 'age',
    'how far'       : 'distance',
    'how long'      : 'length',
    'how tall'      : 'height',
    'how deep'      : 'depth',
    'how wide'      : 'width',
    'how fast'      : 'speed',
    'how often'     : 'frequency',
    'how come'      : 'reason',
    'which'         : 'choice',
    'whom'          : 'person',
    'whose'         : 'possession'
        # how big
}

def buildBucket(t,qw):
    """
        return a TriplesBucket associated to tree t and question word qw
    """
    nodeToID = {}
    triplesBucket = TriplesBucket()
    initUnknowns(t,nodeToID)
    #_+ triplesBucket.addTriple(Triple(nodeToID[t.child[0]],questionMap[qw],nodeToID[t])) # process the question word
    tripleProduce1(t.child[0],nodeToID,triplesBucket) #_+ instead of question word
    fillBucket(t,nodeToID,triplesBucket)
    return triplesBucket

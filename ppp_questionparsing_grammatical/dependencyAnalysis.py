import sys
from .questionWordProcessing import identifyQuestionWord, processQuestionWord
from .preprocessing import DependenciesTree
from .preprocessingMerge import Word
from copy import deepcopy
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
from .data.exceptions import GrammaticalError

def remove(t):
    t.parent.child.remove(t)

def impossible(t):
    raise GrammaticalError(t.dependency,"unexpected dependency")

def ignore(t):
    pass

def merge(t):
    t.parent.merge(t,True)

def amodRule(t):
    if t.namedEntityTag != 'ORDINAL' and t.wordList[0].pos != 'JJS': # [0] : must be improve (search in the whole list?)
        assert t.parent is not None
        merge(t)
    else:
        t.dependency = 'connectorUp'

def propType(t):
    """
        Propagate locally the type of the subtree
    """
    if t.parent != None:
        if t.parent.subtreeType == 'undef':
            t.parent.subtreeType = t.subtreeType
        assert t.subtreeType == 'undef' or t.subtreeType == t.parent.subtreeType
        t.subtreeType = t.parent.subtreeType

dependenciesMap1 = {
    'undef'     : 'R0', # personnal tag, should not happen?
    'root'      : 'R0',
    'dep'       : 'R8', # ? instead of R1
        'aux'       : remove,
            'auxpass'   : remove,
            'cop'       : impossible,
        'arg'       : impossible,
            'agent'     : 'R4',
            'comp'      : 'R2',
                'acomp'     : 'R2',
                'ccomp'     : 'R4',
                'xcomp'     : 'R2',
                'pcomp'     : 'R2',
                'obj'       : impossible,
                    'dobj'      : 'R4', #_+ instead of R4
                    'iobj'      : 'R2',
                    'pobj'      : 'R2', # -
            'subj'      : impossible,
                'nsubj'     : 'R1',
                    'nsubjpass'    : 'R4', #_+ ? instead of R3
                'csubj'     : impossible,
                    'csubjpass'    : impossible,
        'cc'        : impossible,
        'conj'      : 'R0',
            'conj_and'  : ignore,
            'conj_or'   : ignore,
            'conj_negcc': ignore, #?
        'expl'      : remove,
        'mod'       : 'R3',
            'amod'      : amodRule,
            'appos'     : 'R3',
            'advcl'     : 'R3',
            'det'       : remove,
            'predet'    : remove,
            'preconj'   : remove,
            'vmod'      : 'R2',
            'mwe'       : merge,
                'mark'      : remove,
            'advmod'    : merge,
                'neg'       : 'connectorUp', # need a NOT node
            'rcmod'     : 'R3', # temp, need to be analyzed
                'quantmod'  : remove,
            'nn'        : merge, # <-------
            'npadvmod'  : merge,
                'tmod'      : 'R2',
            'num'       : merge,
            'number'    : merge,
            'prep'      : 'R4', # ?
            'prepc'     : 'R4', # ?
            'poss'      : 'R4',
            'possessive': impossible,
            'prt'       : merge,
        'parataxis' : remove, #  ?
        'punct'     : impossible,
        'ref'       : impossible,
        'sdep'      : impossible,
            'xsubj'     : 'R2',
        'goeswith'  : merge,
        'discourse' : remove
}

dependenciesMap2 = {
    'R0'        : propType,
    'R1'        : propType,
    'R2'        : ignore,
    'R3'        : ignore,
    'R4'        : ignore,
    'R5'        : ignore,
    'R6'        : propType, # superlative
    'R7'        : propType, # conjunction
    'R8'        : propType
}

def collapsePrep(t):
    """
        Replace prep(c)_x by prep
    """
    temp = list(t.child) # copy, because t.child is changed while iterating
    for c in temp:
        collapsePrep(c)
    if t.dependency.startswith('prep'): # prep_x or prepc_x (others?)
        # prep = t.dependency[t.dependency.index('_')+1:] # not used for the moment
        t.dependency = 'prep' # suffix of the prep not analyzed for the moment (just removed)

def collapseMap(t,depMap,down=True):
    """
        Apply the rules of depMap to t
        If down = false, collapse from top to down
    """
    temp = list(t.child) # copy, because t.child is changed while iterating
    if down:
        for c in temp:
            collapseMap(c,depMap)
    try:
        if isinstance(depMap[t.dependency], str):
            t.dependency = depMap[t.dependency]
        else:
            depMap[t.dependency](t)
    except KeyError:
        raise GrammaticalError(t.dependency,"unknown dependency")
    if not down:
        for c in temp:
            collapseMap(c,depMap,down)

def connectorUp(t):
    """
        Move amod connectors (first, biggest...)
    """
    if t.dependency == 'connectorUp':
        assert t.parent is not None and t.child == []
        t.dependency = t.parent.dependency
        t.parent.dependency = 'R6'
        t.parent.child.remove(t)
        t.child = [t.parent]
        t.parent.parent.child.remove(t.parent)
        t.parent.parent.child.append(t)
        parentTemp = t.parent.parent
        t.parent.parent = t
        t.parent = parentTemp
    else:
        temp = list(t.child) # copy, because t.child is changed while iterating
        for c in temp:
            connectorUp(c)

def conjConnectorsUp(t):
    """
        Move conjonction connectors (and, or, neg...)
    """
    if not t.dependency.startswith('conj'):
        temp = list(t.child) # copy, because t.child is changed while iterating
        for c in temp:
            conjConnectorsUp(c)
    else:
        assert t.parent is not None
        depSave = t.dependency[t.dependency.index('_')+1:]
        parentTemp = None
        dupl = None
        newTree = None
        if len(t.parent.child) == 1:
            parentTemp = t.parent.parent # n0
            t.dependency = t.parent.dependency # dependency(n2)
            t.parent.child.remove(t) # son(n1) \= n2
            dupl = deepcopy(parentTemp) # n0'
            parentTemp.child.remove(t.parent) # son(n0) \= n1
            parentTemp.child.append(t) # son(n0)=n2
            t.parent = parentTemp # parent(n2) = n0
            newTree = DependenciesTree(depSave, 'undef', 'undef', parentTemp.dependency, [dupl,parentTemp], parentTemp.parent)
            parentTemp.dependency = 'R7'
            parentTemp.parent = newTree
        else:
            parentTemp = t.parent # n0
            parentTemp.child.remove(t) # son(n1) \= n2
            dupl = deepcopy(parentTemp) # n0'
            t.child += t.parent.child # son(n2) = son(n1)
            for n in t.child:
                n.parent = t
            newTree = DependenciesTree(depSave, 'undef', 'undef', parentTemp.dependency, [dupl,t], parentTemp.parent)
            t.dependency = 'R7'
            t.parent = newTree
        newTree.parent.child.remove(parentTemp)
        newTree.parent.child.append(newTree)
        dupl.dependency = 'R7'
        dupl.parent = newTree
        temp = list(newTree.child) # copy, because t.child is changed while iterating
        for c in temp:
            conjConnectorsUp(c)

def subNormalize(t,lmtzr,st):
    for c in t.child:
        subNormalize(c,lmtzr,st)
    if t.namedEntityTag == 'undef':
        for w in t.wordList:
            w.normalize(lmtzr,st)

def normalize(t):         
    lmtzr = WordNetLemmatizer()
    st = PorterStemmer()
    subNormalize(t,lmtzr,st)                     # normalize words (lemmatization + nounify nouns)

def simplify(t):
    """
        identify and remove question word
        collapse dependencies of tree t
    """
    s = identifyQuestionWord(t)           # identify and remove question word
    normalize(t)                          # lemmatize, nounify
    collapsePrep(t)                       # replace prep(c)_x by prep(c)
    collapseMap(t,dependenciesMap1)       # collapse the tree according to dependenciesMap1
    conjConnectorsUp(t)                   # remove conjonction connectors
    connectorUp(t)                        # remove amod connectors
    processQuestionWord(t,s)              # add info contained into the qw (type ...)
    collapseMap(t,dependenciesMap2)       # propagate types from bottom to top
    collapseMap(t,dependenciesMap2,False) # propagate types from top to bottom
    return s

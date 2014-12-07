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
    'dep'       : 'R1', # ? instead of R2
        'aux'       : remove,
            'auxpass'   : remove,
            'cop'       : impossible,
        'arg'       : impossible,
            'agent'     : 'R5',
            'comp'      : 'R3',
                'acomp'     : 'R3',
                'ccomp'     : 'R5',
                'xcomp'     : 'R3',
                'pcomp'     : 'R3',
                'obj'       : impossible,
                    'dobj'      : 'R5', #_+ instead of R5
                    'iobj'      : 'R3',
                    'pobj'      : 'R3', # -
            'subj'      : impossible,
                'nsubj'     : 'R2',
                    'nsubjpass'    : 'R5', #_+ ? instead of R4
                'csubj'     : impossible,
                    'csubjpass'    : impossible,
        'cc'        : impossible,
        'conj'      : 'R0',
            'conj_and'  : ignore,
            'conj_or'   : ignore,
            'conj_negcc': ignore, #?
        'expl'      : remove,
        'mod'       : 'R4',
            'amod'      : amodRule,
            'appos'     : 'R4',
            'advcl'     : 'R4',
            'det'       : remove,
            'predet'    : remove,
            'preconj'   : remove,
            'vmod'      : 'R3',
            'mwe'       : merge,
                'mark'      : remove,
            'advmod'    : merge,
                'neg'       : 'connectorUp', # need a NOT node
            'rcmod'     : 'R4', # temp, need to be analyzed
                'quantmod'  : remove,
            'nn'        : merge, # <-------
            'npadvmod'  : merge,
                'tmod'      : 'R3',
            'num'       : merge,
            'number'    : merge,
            'prep'      : 'R5', # ?
            'prepc'     : 'R5', # ?
            'poss'      : 'R5',
            'possessive': impossible,
            'prt'       : merge,
        'parataxis' : remove, #  ?
        'punct'     : impossible,
        'ref'       : impossible,
        'sdep'      : impossible,
            'xsubj'     : 'R3',
        'goeswith'  : merge,
        'discourse' : remove
}

dependenciesMap2 = {         # how to handle a -b-> c
    'R0'        : propType,  # normalize(c)
    'R1'        : propType,  # !c
    'R2'        : propType,  # if c is a leaf: (normalize(c),!a,?), otherwise: normalize(c)
    'R3'        : ignore,    # (?,!a,normalize(c))
    'R4'        : ignore,    # (?,normalize(c),!a)
    'R5'        : ignore,    # (normalize(c),!a,?)
     #'R6'        : ignore,    # (!a,normalize(c),?) # not use for the moment
    'Rspl'      : propType,  # superlative
    'RconjT'    : propType,  # top of a conjunction relation
    'RconjB'    : propType   # bottom of a conjunction relation

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
        If down = false, collapse from top to down, otherwise collapse from down to top
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
        Move amod connectors (superlative: first, biggest...)
    """
    if t.dependency == 'connectorUp':
        assert t.parent is not None and t.child == []
        t.dependency = t.parent.dependency
        t.parent.dependency = 'Rspl'
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
            parentTemp.dependency = 'RconjB'
            parentTemp.parent = newTree
        else:
            parentTemp = t.parent # n0
            parentTemp.child.remove(t) # son(n1) \= n2
            dupl = deepcopy(parentTemp) # n0'
            t.child += t.parent.child # son(n2) = son(n1)
            for n in t.child:
                n.parent = t
            newTree = DependenciesTree(depSave, 'undef', 'undef', parentTemp.dependency, [dupl,t], parentTemp.parent)
            t.dependency = 'RconjB'
            t.parent = newTree
        newTree.parent.child.remove(parentTemp)
        newTree.parent.child.append(newTree)
        dupl.dependency = 'RconjT'
        dupl.parent = newTree
        temp = list(newTree.child) # copy, because t.child is changed while iterating
        for c in temp:
            conjConnectorsUp(c)

def subStandardize(t,lmtzr,st):
    for c in t.child:
        subStandardize(c,lmtzr,st)
    if t.namedEntityTag == 'undef':
        for w in t.wordList:
            w.standardize(lmtzr,st)

def standardize(t):
    """
        Apply lemmatization + nounification
    """
    lmtzr = WordNetLemmatizer()
    st = PorterStemmer()
    subStandardize(t,lmtzr,st) # standardize words (lemmatization + nounify nouns)

def simplify(t):
    """
        identify and remove question word
        collapse dependencies of tree t
    """
    s = identifyQuestionWord(t)           # identify and remove question word
    standardize(t)                        # lemmatize, nounify
    collapsePrep(t)                       # replace prep(c)_x by prep(c)
    collapseMap(t,dependenciesMap1)       # collapse the tree according to dependenciesMap1
    conjConnectorsUp(t)                   # remove conjonction connectors
    connectorUp(t)                        # remove amod connectors
    processQuestionWord(t,s)              # add info contained into the qw (type ...)
    collapseMap(t,dependenciesMap2)       # propagate types from bottom to top
    collapseMap(t,dependenciesMap2,False) # propagate types from top to bottom
    return s

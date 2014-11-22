import sys
from .questionWordProcessing import identifyQuestionWord, processQuestionWord
from .preprocessing import DependenciesTree
from .preprocessingMerge import Word
from copy import deepcopy

def remove(t):
    t.parent.child.remove(t)

def impossible(t):
    sys.exit('exit: %s dependency unexpected (please, report your sentence on http://goo.gl/EkgO5l)\n' % t)

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
                
dependenciesMap1 = {
    'undef'     : 't0', # personnal tag, should not happen?
    'root'      : 't0',
    'dep'       : 't6', # ? instead of t1
        'aux'       : remove,
            'auxpass'   : remove,
            'cop'       : impossible,
        'arg'       : impossible,
            'agent'     : 't4',
            'comp'      : 't2',
                'acomp'     : 't2',
                'ccomp'     : 't2',
                'xcomp'     : 't2',
                'pcomp'     : 't2',
                'obj'       : impossible,
                    'dobj'      : 't2', #_+ instead of t4
                    'iobj'      : 't2',
                    'pobj'      : 't2', # -
            'subj'      : impossible,
                'nsubj'     : 't1',
                    'nsubjpass'    : 't4', #_+ ? instead of  t3
                'csubj'     : impossible,
                    'csubjpass'    : impossible,
        'cc'        : impossible,
        'conj'      : 't0',
            'conj_and'  : ignore,
            'conj_or'   : ignore,
            'conj_negcc': ignore, #?
        'expl'      : remove,
        'mod'       : 't3',
            'amod'      : amodRule,
            'appos'     : 't3',
            'advcl'     : 't3',
            'det'       : remove,
            'predet'    : remove,
            'preconj'   : remove,
            'vmod'      : 't2',
            'mwe'       : merge,
                'mark'      : remove,
            'advmod'    : merge,
                'neg'       : 'connectorUp', # need a NOT node
            'rcmod'     : 't3', # temp, need to be analyzed
                'quantmod'  : remove,
            'nn'        : ignore, # <-------
            'npadvmod'  : merge,
                'tmod'      : 't2',
            'num'       : merge,
            'number'    : merge,
            'prep'      : 't4', # ?
            'prepc'     : 't4', # ?
            'poss'      : 't4',
            'possessive': impossible,
            'prt'       : merge,
        'parataxis' : remove, #  ?
        'punct'     : impossible,
        'ref'       : impossible,
        'sdep'      : impossible,
            'xsubj'     : 't2',
        'goeswith'  : merge,
        'discourse' : remove
}

dependenciesMap2 = {
    't0'        : ignore,
    't1'        : ignore,
    't2'        : ignore,
    't3'        : ignore,
    't4'        : ignore,
    't5'        : ignore,
    't6'        : ignore,
    'connectorUp' : ignore,
    'connector' : ignore, 
    'nn'        : merge   
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

def collapseMap(t,depMap):
    """
        Apply the rules of depMap to t
    """
    temp = list(t.child) # copy, because t.child is changed while iterating
    for c in temp:
        collapseMap(c,depMap)
    try:
        if isinstance(depMap[t.dependency], str):
            t.dependency = depMap[t.dependency]
        else:
            depMap[t.dependency](t)
    except KeyError:
        sys.exit('exit: dependency %s unknown (please, report your sentence on http://goo.gl/EkgO5l)\n' % t.dependency)

def connectorUp(t):
    """
        Move amod connectors (first, biggest...)
    """
    if t.dependency == 'connectorUp':
        assert t.parent is not None and t.child == []
        t.dependency = t.parent.dependency
        t.parent.dependency = 'connector'
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
    if t.dependency.startswith('conj') and len(t.parent.child) == 1:
        assert t.parent is not None #and t.child == []

        depSave = t.dependency[t.dependency.index('_')+1:]
        
        parentTemp = t.parent.parent # n0
        
        t.dependency = t.parent.dependency # dependency(n2)
        t.parent.child.remove(t) # son(n1) \= n2
        
        dupl = deepcopy(parentTemp) # n0'
        
        parentTemp.child.remove(t.parent) # son(n0) \= n1
        parentTemp.child.append(t) # son(n0)=n2
        t.parent = parentTemp # parent(n2) = n0

        newTree = DependenciesTree(depSave, 'undef', parentTemp.dependency, [dupl,parentTemp], parentTemp.parent)

        parentTemp.parent.child.remove(parentTemp)
        parentTemp.parent.child.append(newTree)

        parentTemp.dependency = 'connector'
        parentTemp.parent = newTree
        dupl.dependency = 'connector'
        dupl.parent = newTree
        
        temp = list(newTree.child) # copy, because t.child is changed while iterating
        for c in temp:
            conjConnectorsUp(c)
    if t.dependency.startswith('conj') and len(t.parent.child) > 1:
        assert t.parent is not None #and t.child == []

        depSave = t.dependency[t.dependency.index('_')+1:]
        parentTemp = t.parent # n0
        
        parentTemp.child.remove(t) # son(n1) \= n2
        
        dupl = deepcopy(parentTemp) # n0'
        
        t.child += t.parent.child # son(n2) = son(n1)
        for n in t.child:
            n.parent = t

        newTree = DependenciesTree(depSave, 'undef', parentTemp.dependency, [dupl,t], parentTemp.parent)
        
        newTree.parent.child.remove(parentTemp)
        newTree.parent.child.append(newTree)
        t.dependency = 'connector'
        t.parent = newTree
        dupl.dependency = 'connector'
        dupl.parent = newTree
        
        temp = list(newTree.child) # copy, because t.child is changed while iterating
        for c in temp:
            conjConnectorsUp(c)

def simplify(t):
    """
        identify and remove question word
        collapse dependencies of tree t
    """
    s = identifyQuestionWord(t)     # identify and remove question word
    collapsePrep(t)                 # replace prep(c)_x by prep(c)
    collapseMap(t,dependenciesMap1) # collapse the tree according to dependenciesMap1
    conjConnectorsUp(t)             # remove conjonction connectors
    collapseMap(t,dependenciesMap2) # collapse the tree according to dependenciesMap2
    connectorUp(t)                  # remove amod connectors
    processQuestionWord(t,s)
    return s

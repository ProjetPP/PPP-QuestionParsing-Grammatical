import sys
from .questionIdentify import identifyQuestionWord
from .data.exceptions import GrammaticalError

def remove(t):
    t.parent.child.remove(t)

def impossible(t):
    raise GrammaticalError(t.dependency,"unexpected dependency")

def ignore(t):
    remove(t)

def merge(t):
    t.parent.merge(t,True)

def amodRule(t):
    if t.namedEntityTag != 'ORDINAL' and t.wordList[0].pos != 'JJS': # [0] : must be improve (search in the whole list?)
        assert t.parent is not None
        merge(t)
    else:
        t.dependency = 't5'
                
dependenciesMap = {
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
        'expl'      : ignore,
        'mod'       : 't3',
            'amod'      : amodRule,
            'appos'     : 't3',
            'advcl'     : 't3',
            'det'       : remove,
            'predet'    : ignore,
            'preconj'   : ignore,
            'vmod'      : 't2',
            'mwe'       : merge,
                'mark'      : ignore,
            'advmod'    : merge,
                'neg'       : 't0', # need a NOT node
            'rcmod'     : ignore,
                'quantmod'  : ignore,
            'nn'        : merge,
            'npadvmod'  : merge,
                'tmod'      : 't2',
            'num'       : merge,
            'number'    : merge,
            'prep'      : 't4', # ?
            'prepc'     : 't4', # ?
            'poss'      : 't4',
            'possessive': impossible,
            'prt'       : merge,
        'parataxis' : ignore, #  ?
        'punct'     : impossible,
        'ref'       : impossible,
        'sdep'      : impossible,
            'xsubj'     : 't2',
        'goeswith'  : merge,
        'discourse' : remove
}

def collapseDependency(t,depMap=dependenciesMap):
    """
        Apply the rules of depMap to t
    """
    temp = list(t.child) # copy, because t.child is changed while iterating
    for c in temp:
        collapseDependency(c,depMap)
    if t.dependency.startswith('prep'): # prep_x or prepc_x (others?)
        # prep = t.dependency[t.dependency.index('_')+1:] # not used for the moment
        t.dependency = 'prep' # suffix of the prep not analyzed for the moment (just removed)
    try:
        if isinstance(depMap[t.dependency], str):
            t.dependency = depMap[t.dependency]
        else:
            depMap[t.dependency](t)
    except KeyError:
        raise GrammaticalError(t.dependency,"unknown dependency")

def simplify(t):
    """
            identify and remove question word
            collapse dependencies of tree t
    """
    s = identifyQuestionWord(t) # identify and remove question word
    collapseDependency(t) # collapse the tree according to collapsing rules
    return s

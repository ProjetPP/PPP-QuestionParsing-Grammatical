""" Second step of the algorithm."""

import sys
from .questionIdentify import identifyQuestionWord

def remove(t):
    t.parent.child.remove(t)

def impossible(t):
    sys.exit('exit: %s dependency unexpected (please, report your sentence on http://goo.gl/EkgO5l)\n' % t)
    #remove(t)

def ignore(t):
    remove(t)

def merge(t):
    t.parent.merge(t,True)

dependenciesMap = {
    'undef'     : 't0', # personnal tag, should not happen?
    'root'      : 't0',
    'dep'       : 't1',
        'aux'       : remove,
            'auxpass'   : remove,
            'cop'       : impossible,
        'arg'       : impossible,
            'agent'     : 't2',
            'comp'      : 't2',
                'acomp'     : 't2',
                'ccomp'     : 't2',
                'xcomp'     : 't2',
                'pcomp'     : 't2',
                'obj'       : impossible,
                    'dobj'      : 't2',
                    'iobj'      : impossible,
                    'pobj'      : 't2',
            'subj'      : 't1',
                'nsubj'     : 't1',
                    'nsubjpass'    : 't1',
                'csubj'     : impossible,
                    'csubjpass'    : impossible,
        'cc'        : ignore,
        'conj'      : 't0',
        'expl'      : ignore,
        'mod'       : 't3',
            'amod'      : 't3',
            'appos'     : 't3',
            'advcl'     : 't3',
            'det'       : remove,
            'predet'    : ignore,
            'preconj'   : ignore,
            'vmod'      : 't2',
            'mwe'       : merge,
                'mark'      : ignore,
            'advmod'    : merge,
                'neg'       : 't0',
            'rcmod'     : ignore,
                'quantmod'  : ignore,
            'nn'        : merge,
            'npadvmod'  : merge,
                'tmod'      : 't3',
            'num'       : merge,
            'number'    : merge,
            'prep'      : 't2',
            'prepc'     : 't2',
            'poss'      : 't2',
            'possessive': impossible,
            'prt'       : merge,
        'parataxis' : ignore,
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
    temp = list(t.child) # copy, t.child is changed while iterating
    for c in temp:
        collapseDependency(c,depMap)
    try:
        if isinstance(depMap[t.dependency], str):
            t.dependency = depMap[t.dependency]
        else:
            depMap[t.dependency](t)
    except KeyError: # prep_x, prepc_x
        if (t.dependency[:t.dependency.rindex('_')] not in {'prep','prepc'}):
            sys.exit('exit: dependency unknown (please, report your sentence on http://goo.gl/EkgO5l)\n')
        pass


def simplify(t):
    """
            identify and remove question word
            collapse dependencies of tree t
    """
    s = identifyQuestionWord(t) # identify and remove question word
    #sys.stderr.write('question word is: %s\n' % s)
    collapseDependency(t) # apply dependency rules of collapsing
    return s

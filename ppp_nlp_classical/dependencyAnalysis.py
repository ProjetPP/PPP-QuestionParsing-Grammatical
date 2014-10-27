""" Second step of the algorithm."""

import sys
from .preprocessing import mergeNamedEntityTagChildParent, mergeNamedEntityTagSisterBrother

def removeWord(t,word):
    """
        Remove word (of type str*int = word*position_in_sentence) in t
        Assume word has no child
    """
    if word in t.wordList:
        if not t.child:
            t.parent.child.remove(t) 
        else:
            sys.stderr.write('exit: question word has child (please, report your sentence)\n')
            sys.exit() 
    else:
        for c in t.child:
            removeWord(c,word)

def remove(t):
    t.parent.child.remove(t)

def impossible(t):
    sys.stderr.write('exit: %s dependency is possible (please, report your sentence)\n' % t)
    sys.exit() 
    #remove(t)

def ignore(t):
    remove(t)

def merge(t):
    t.parent.merge(t,True)

dependenciesMap2 = {
    'undef'     : 'undef',
    'root'      : 'root',
    'dep'       : 'dep',
        'aux'       : remove,
            'auxpass'   : remove,
            'cop'       : impossible,
        'arg'       : impossible,
            'agent'     : 'agent',
            'comp'      : 'comp',
                'acomp'     : 'comp',
                'ccomp'     : 'comp',
                'xcomp'     : 'comp',
                'pcomp'     : 'comp',
                'obj'       : impossible,
                    'dobj'      : 'comp',
                    'iobj'      : impossible,
                    'pobj'      : 'comp',
            'subj'      : 'subj',
                'nsubj'     : 'subj',
                    'nsubjpass'    : 'nsubjpass',
                'csubj'     : impossible,
                    'csubjpass'    : impossible,
        'cc'        : ignore,
        'conj'      : 'conj',
        'expl'      : ignore,
        'mod'       : 'mod',
            'amod'      : 'mod',
            'appos'     : 'mod',
            'advcl'     : 'mod',
            'det'       : remove,
            'predet'    : ignore,
            'preconj'   : ignore,
            'vmod'      : 'mod',
            'mwe'       : merge,
                'mark'      : ignore,
            'advmod'    : merge,
                'neg'       : 'neg',
            'rcmod'     : ignore,
                'quantmod'  : ignore,
            'nn'        : merge,
            'npadvmod'  : merge,
                'tmod'      : 'mod',
            'num'       : merge,
            'number'    : merge,
            'prep'      : 'prep',
            'prepc'     : 'prep',
            'poss'      : 'poss',
            'possessive': impossible,
            'prt'       : merge,
        'parataxis' : ignore,
        'punct'     : impossible,
        'ref'       : impossible,
        'sdep'      : impossible,
            'xsubj'     : 'comp',
        'goeswith'  : merge,
        'discourse' : remove
}

questionWord = [
    """
        Taken from: http://www.interopia.com/education/all-question-words-in-english/
        Rarely used: Wherefore, Whatever, Wherewith, Whither, Whence, However
    """
    # Yes/no question
    'Is', 'Are', 'Am', 'Was', 'Were', 'Will', 'Do', 'Does', 'Did', 'Have', 'Had', 'Has', 'Can', 'Could', 'Should', 'Shall', 'May', 'Might', 'Would',
    # Open-ended questions 
    'What', 'What kind', 'What type', 'What sort', 'What time', 'When', 'Why', 'Where', 'Who', 'How', 'How much', 'How many', 'How old', 'How far', 'How long', 'How tall', 'How deep', 'How wide', 'How fast', 'How often', 'How come', 'Which', 'Whom', 'Whose'
      # + What... for, What... like, Why don't
]

def firstWords(t,start):
    """
        Put the 2 first words of the sentence in start (list of size 2)
    """
    for n in t.wordList:
        if n[1] == 1:
            start[0] = n
        elif n[1] == 2:
            start[1] =n
    for c in t.child:
        firstWords(c,start)

def identifyQuestionWord(t):
    """
        Identify, remove and return the question word
    """
    start = [None,None]
    firstWords(t,start)   
    if start[0][0] + ' ' + start[1][0] in questionWord:
        removeWord(t,start[0])
        removeWord(t,start[1])
        return start[0][0] + ' ' + start[1][0]
    elif start[0][0] in questionWord: 
        removeWord(t,start[0])
        return start[0][0]
    else:
        sys.stderr.write('exit: question word not found (please, report your sentence)\n')

def collapseDependency2(t,depMap=dependenciesMap2):
    """
        Apply the rules of depMap to t
    """
    temp = list(t.child) # copy, t.child is changed while iterating
    for c in temp:
        collapseDependency2(c,depMap)
    try:
        if isinstance(depMap[t.dependency], str):
            t.dependency = depMap[t.dependency]
        else:
            depMap[t.dependency](t)
    except KeyError: # prep_x, prepc_x
        pass

def simplify2(t):
    s = identifyQuestionWord(t) # identify and remove question word
    sys.stderr.write('question word is: %s\n' % s)
    mergeNamedEntityTagChildParent(t) # NER merging
    mergeNamedEntityTagSisterBrother(t) # NER merging
    collapseDependency2(t) # apply dependency rules of collapsing

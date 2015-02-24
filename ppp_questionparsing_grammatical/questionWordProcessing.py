import sys
from .dependencyTree import Word, DependenciesTree
from .data.questionWord import closeQuestionWord, openQuestionWord, strongQuestionWord, questionAdd, questionWIs, questionType, existQuestionWord, semiQuestionWord
from ppp_datamodel import Resource, Triple, Missing, Intersection, List, Union, And, Or, Exists, First, Last, Sort

#####################################
# Identify and remove question word #
#####################################

def prepareInstanceOf(t):
    """
        Replace by 'inst_of' the highest dependency that appears on a path from the root of t to the root of the whole tree
    """
    if t.parent and t.parent.dependency == 'root':
        t.dependency = 'inst_of'
        return
    elif t.parent:
        prepareInstanceOf(t.parent)

def removeWord(t, word):
    """
        Remove word (of type str*int = s*position_of_s_in_sentence) from tree t
    """
    if word in t.wordList:
        prepareInstanceOf(t) # <<<
        for u in t.child: # the word is in the middle of the tree
            u.dependency = t.dependency
            u.parent = t.parent
            t.parent.child.append(u)
        t.parent.child.remove(t)
    else:
        for c in t.child:
            removeWord(c, word)

def firstWords(t, start):
    """
        Put the 2 first words of the sentence (if they are in the tree) in start (list of size 2)
    """
    for n in t.wordList:
        if n.index == 1:
            start[0] = n
        elif n.index == 2:
            start[1] = n
    for c in t.child:
        firstWords(c, start)

def identifyQuestionWord(t):
    """
        Identify, remove (if necessary) and return the question word.
        If there is no question word, return None.
    """
    start = [None, None]
    firstWords(t, start)
    try: # the first words are not in the tree, we extract them directly from the sentence
        start[0] = start[0] or Word(t.text.split(' ', 1)[0], 1)
        start[1] = start[1] or Word(t.text.split(' ', 1)[1], 2)
    except IndexError:
        pass
    if start[1]:
        w = start[0].word.lower() + ' ' + start[1].word.lower()
        if w in openQuestionWord or w in semiQuestionWord or w in existQuestionWord:
            removeWord(t, start[0])
            removeWord(t, start[1])
            return w
    w = start[0].word.lower()
    if w in openQuestionWord or w in semiQuestionWord:
        removeWord(t, start[0])
        return w
    if w in closeQuestionWord:
        return w
    return None

########################################################
# Process question word to improve the dependency tree #
########################################################

def processQuestionType(t, w, typeMap=questionType):
    """
        Add a type to the root of the tree (= type of the answer) depending on the question word
    """
    try:
        t.subtreeType = typeMap[w]
    except KeyError:
        pass

def questionWordDependencyTree(t, w):
    processQuestionType(t, w)  # type the ROOT according to the question word
    if w in existQuestionWord: # prepare the production of an Exists node
        t.child[0].dependency = 'Rexist'

####################################################
# Process question word to improve the normal form #
####################################################

def extractPredicates(nf):
    """
        Assume that nf is a triple
        Returns the lists of strings (values) that are predicates of the triple
    """
    if isinstance(nf.predicate, Resource):
        return [nf.predicate.value]
    else:
        return [x.value for x in nf.predicate.list]

def enhanceTriple(nf, w, addMap=questionAdd, wisMap=questionWIs):
    """
        Add info into the triple depending on the question word
    """
    predList = extractPredicates(nf)
    try:
        if 'identity' in predList:
             if w in strongQuestionWord or isinstance(nf.subject, Resource) or isinstance(nf.object, Resource): # strong qw or triple of depth 1
                 return Triple(nf.subject, List([Resource(x) for x in wisMap[w]]), nf.object) # !! Other info lost (type...) (inverse_predicate: not relevant)
             else: # delete the first level
                if isinstance(nf.subject, Missing):
                    return nf.object
                else:
                    return nf.subject
        elif not 'instance of' in predList: # add info into the predicates list (except for instance_of predicate)
             return Triple(nf.subject, List([Resource(x) for x in predList] + [Resource(x+' '+y) for x in predList for y in addMap[w]]), nf.object, nf.inverse_predicate) # !! Other info lost (type...) (reverse_predicate not enhance?)
        else:
            return nf
    except KeyError:
         return nf

def processQuestionInfo(nf, w):
    """
        Add info into the first triples depending on the question word
    """
    if isinstance(nf, (List, Intersection, Union, And, Or)):
        result = []
        for u in nf.list:
            result.append(processQuestionInfo(u, w))
        return type(nf)(result)
    elif isinstance(nf, (Last, First, Exists)):
        return type(nf)(processQuestionInfo(nf.list, w))
    elif isinstance(nf, Sort) or isinstance(nf, Resource):
        return nf
    elif isinstance(nf, Triple):
        return enhanceTriple(nf, w)
    else:
        assert False

def questionWordNormalForm(nf, w):
    """
        Improve the normal form using the question word
    """
    if w in openQuestionWord:
        return processQuestionInfo(nf, w)
    return nf

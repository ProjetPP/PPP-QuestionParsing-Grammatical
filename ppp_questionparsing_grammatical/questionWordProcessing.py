import sys
from .dependencyTree import Word, DependenciesTree
from .data.questionWord import closeQuestionWord, openQuestionWord, questionAdd, questionWIs, questionType, questionExcept, existQuestionWord, semiQuestionWord
from ppp_datamodel import Resource, Triple, Missing, Intersection, List, Union, And, Or, Exists, First, Last, Sort

#####################################
# Identify and remove question word #
#####################################

def prepareInstanceOf(t):
    """
        Replace by 'inst_of' the dependencies that appears on a path from the root of t to the root of the whole tree
    """
    if t.dependency == 'root':
        return
    else:
        t.dependency = 'inst_of'
        if t.parent:
            prepareInstanceOf(t.parent)

def removeWord(t,word):
    """
        Remove word (of type str*int = s*position_of_s_in_sentence) from tree t
    """
    if word in t.wordList:
        prepareInstanceOf(t) # <<<
        for u in t.child: # the question is in the middle of the tree
            u.dependency = t.dependency
            u.parent = t.parent
            t.parent.child.append(u)
        t.parent.child.remove(t)
    else:
        for c in t.child:
            removeWord(c,word)

def firstWords(t,start):
    """
        Put the 2 first words of the sentence (if they are in the tree) in start (list of size 2)
    """
    for n in t.wordList:
        if n.index == 1:
            start[0] = n
        elif n.index == 2:
            start[1] = n
    for c in t.child:
        firstWords(c,start)

def identifyQuestionWord(t):
    """
        Identify, remove (if necessary) and return the question word.
        If there is no question word, return None.
    """
    start = [None,None]
    firstWords(t,start)
    if not start[0]: # the first word is not in the tree, we extract it directly from the sentence    
        start[0] = Word(t.text.split(' ',1)[0],1)
    if not start[1]:
        try:
            start[1] = Word(t.text.split(' ',1)[1],2)
        except IndexError:
            pass
    if start[1]:
        w = start[0].word.lower() + ' ' + start[1].word.lower()
        if w in openQuestionWord or w in semiQuestionWord:
            removeWord(t,start[0])
            removeWord(t,start[1])
            return w
        if w in existQuestionWord:
            removeWord(t,start[1])
            return w
    w = start[0].word.lower()
    if w in openQuestionWord or w in semiQuestionWord:
        removeWord(t,start[0])
        return w
    if w in closeQuestionWord:
        return w
    return None

########################################################
# Process question word to improve the dependency tree #
########################################################

def processQuestionType(t,w,typeMap=questionType):
    """
        Add a type to the root of the tree (= type of the answer) depending on the question word
    """
    try:
        t.subtreeType = typeMap[w]
    except KeyError:
        pass

def questionWordDependencyTree(t,w):
    processQuestionType(t,w)  # type the ROOT according to the question word 
    if w in existQuestionWord:
        t.child[0].dependency = 'Rexist'

####################################################
# Process question word to improve the normal form #
####################################################

def extractPredicates(nf):
    """
        Assume that nf is a triple
        Returns the lists of strings (values) that are predicates of the triple
    """
    assert isinstance(nf,Triple) and (isinstance(nf.predicate,Resource) or isinstance(nf.predicate,List))
    if isinstance(nf.predicate,Resource):
        return [nf.predicate.value]
    else:
        return [x.value for x in nf.predicate.list]

def processQuestionInfo(nf,w,excMap=questionExcept,addMap=questionAdd,wisMap=questionWIs):
    """
        Add info into the first triples depending on the question word
    """
    if isinstance(nf, (List,Intersection,Union,And,Or,Last,First,Exists)):
        result = []
        for u in nf.list:
            result.append(processQuestionInfo(u,w))
        return type(nf)(result)
    if isinstance(nf, Sort):
        result = []
        for u in nf.list:
            result.append(processQuestionInfo(u,w))
        return Sort(result,nf.predicate)
    if isinstance(nf,Triple):
        predList = extractPredicates(nf)
        try:
            if 'identity' in predList:
                return Triple(nf.subject,List([Resource(x) for x in wisMap[w]]),nf.object) # perte des autres infos (types, ...)
            elif (set(predList) & set(excMap[w])) == set() and not 'instance of' in predList: # intersection not empty
                return Triple(nf.subject,List([Resource(x) for x in predList] + [Resource(x+' '+y) for x in predList for y in addMap[w]]),nf.object) # perte des autres infos (types, ...) !!!!
            else:
                return nf
        except KeyError:
            return nf

def questionWordNormalForm(nf,w):
    """
        Try to include the info contained in the question word
          into the sons of ROOT (ex: When -> add "date")
    """
    if w in openQuestionWord:
        return processQuestionInfo(nf,w)
    else:
        return nf

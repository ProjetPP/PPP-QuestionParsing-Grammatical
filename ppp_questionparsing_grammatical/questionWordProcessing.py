import sys
from .preprocessingMerge import Word
from .preprocessing import DependenciesTree
from .data.questionWord import closeQuestionWord, openQuestionWord, questionAdd, questionWIs, questionType, questionExcept, existQuestionWord, semiQuestionWord

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
    assert len(t.wordList) == 1 # no possible alternatives in the tree at this moment
    if word in t.wordList[0]:
        prepareInstanceOf(t) # <<<
        if t.child != []: # the question is in the middle of the tree
            for u in t.child:
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
    assert len(t.wordList) == 1
    for n in t.wordList[0]:
        if n.index == 1:
            start[0] = n
        elif n.index == 2:
            start[1] =n
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
        start[0] = Word(t.text.split(' ')[0],1)
    if not start[1]:
        try:
            start[1] = Word(t.text.split(' ')[1],2)
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

#############################################
# Process question word to improve the tree #
#############################################

def processQuestionType(t,w,typeMap=questionType):
    """
        Add a type to the root of the tree (= type of the answer) depending on the question word
    """
    try:
        t.subtreeType = typeMap[w]
    except KeyError:
        pass

def checkLists(l1,l2):
    """
        l1 is a list of lists of Words
        l2 is a list of strings
        Determine whether a string of l2 appears into at least one word of l1, or not (ex: day appears in birthday)
    """
    for s in l2:
        for l in l1:
            for w in l:
                if w.word.find(s) != -1:
                    return True
    return False

def checkSub(t,w,excMap=questionExcept):
    if t.wordList[0][0].index == 1000: # connector
        assert len(t.wordList) == 1 and len(t.wordList[0]) == 1
        res = True
        for n in t.child:
            if n.dependency != 'R6': # don't go through "instance of" edges
                res = res and checkSub(n,w)
        return res
    else:
        try:
            return not checkLists(t.wordList,excMap[w])
        except KeyError:
            return True

def checkSubInfo(t,w,excMap=questionExcept):
    """
        return false if one of the __sons__ of t contains the information related to w in excMap, otherwise true
        pass the connectors
    """
    res = True
    for n in t.child:
        if n.dependency != 'R6': # don't go through "instance of" edges
            res = res and checkSub(n,w,excMap)
    return res

def processQuestionInfo(t,w,excMap=questionExcept,addMap=questionAdd,wisMap=questionWIs): # TO IMPROVE
    """
        Add info to the first sons of ROOT that are not connectors (ie index != 1000) depending on:
          - the question word
          - whether the nodes contain 'identity' (nounification of verb be) or not
    """
    try:
        if t.wordList[0][0].index == 1000: # connector
            assert len(t.wordList) == 1 and len(t.wordList[0]) == 1
            for n in t.child:
                processQuestionInfo(n,w)
        elif t.getWords() == ['identity']:
            if checkSubInfo(t,w): # identity (be) + no info about w in the sons of the root
                t.wordList = [[Word(s,1001)] for s in wisMap[w]] # replace wordList according to the question word
            else: # do not take the root of t into account into the normalized form
                for n in t.child:
                    n.dependency = 'R0' # !!!!!!!
        elif not checkLists(t.wordList,excMap[w]): # doesn't contain 'identity' + no info about w
            t.wordList = [l + [Word(s,1001)] for l in t.wordList for s in addMap[w]]
    except KeyError:
        pass

def processQuestionWord(t,w):
    """
        Type the root
        Try to include the info contained in the question word
          into the sons of ROOT (ex: When -> add "date")
    """
    processQuestionType(t,w)  # type the ROOT according to the question word
    if w in existQuestionWord:
        t.child[0].dependency = 'Rexist'
    if w in openQuestionWord:
        processQuestionInfo(t.child[0],w)

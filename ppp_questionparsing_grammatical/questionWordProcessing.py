import sys
from .preprocessingMerge import Word
from .preprocessing import DependenciesTree
from .data.exceptions import QuestionWordError
from .data.questionWord import closeQuestionWord, openQuestionWord, questionAdd, questionWIs, questionType, questionExcept

#####################################
# Identify and remove question word #
#####################################

def removeWord(t,word):
    """
        Remove word (of type str*int = s*position_of_s_in_sentence) in t
        Assume word has no child
    """
    assert len(t.wordList) == 1
    if word in t.wordList[0]:
        if t.child != []:
            raise QuestionWordError(word,"question word has child")
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
        Identify, remove (if open qw) and return the question word.
        If there is no question word, return None.
    """
    start = [None,None]
    firstWords(t,start)
    if not start[0]: # the first word is not in the tree, we extract it directly from the sentence
        start[0] = Word(t.text.split(' ', 1)[0],1)
    if not start[1]:
        try:
            start[1] = Word(t.text.split(' ', 1)[1],2)
        except IndexError:
            pass
    if start[1] and start[0].word.lower() + ' ' + start[1].word.lower() in openQuestionWord:
        removeWord(t,start[0])
        removeWord(t,start[1])
        return start[0].word.lower() + ' ' + start[1].word.lower()
    if start[0].word.lower() in openQuestionWord: 
        removeWord(t,start[0])
        return start[0].word.lower()
    if start[0].word.lower() in closeQuestionWord: 
        return start[0].word.lower()
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
        Determine wether a string of l2 appears in at least one word of l1, or not
    """
    for s in l2:
        for l in l1:
            for w in l:
                if w.word == s:
                    return True
    return False

def processQuestionInfo(t,w,excMap=questionExcept,addMap=questionAdd,wisMap=questionWIs): # TO IMPROVE
    """
        Add info to the first sons of ROOT that are not connectors (ie index != 1000) depending on:
            - the question word
            - whether the nodes contain 'identity' (comes from verb be) or not
    """
    try:
        if t.wordList[0][0].index == 1000: # connector so [0][0] is enough
            assert len(t.wordList) == 1 and len(t.wordList[0]) == 1
            for n in t.child:
                processQuestionInfo(n,w)
        elif t.getWords() == ['identity']: # nounification of verb be
            t.wordList = [[Word(s,1001)] for s in wisMap[w]] # replace wordList according to the question word
        elif not checkLists(t.wordList,excMap[w]):   # doesn't contain 'identity' but also doesn't contain the words associated to w in excMap
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
    processQuestionInfo(t.child[0],w)

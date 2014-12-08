import sys
from .preprocessingMerge import Word
from .preprocessing import DependenciesTree
from .data.exceptions import QuestionWordError
from .data.questionWord import closeQuestionWord, openQuestionWord, questionAdd, questionWIs, questionType

def removeWord(t,word):
    """
        Remove word (of type str*int = word*position_in_sentence) in t
        Assume word has no child
    """
    if word in t.wordList:
        if not t.child:
            t.parent.child.remove(t) 
        else:
            raise QuestionWordError(word,"question word has child")
    else:
        for c in t.child:
            removeWord(c,word)

def firstWords(t,start):
    """
        Put the 2 first words of the sentence in start (list of size 2)
    """
    for n in t.wordList:
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
    if not start[0]:
        raise QuestionWordError(t,"do not understand")
    if start[1] and start[0].word.lower() + ' ' + start[1].word.lower() in openQuestionWord:
        removeWord(t,start[0])
        removeWord(t,start[1])
        return start[0].word.lower() + ' ' + start[1].word.lower()
    if start[0].word.lower() in openQuestionWord: 
        removeWord(t,start[0])
        return start[0].word.lower()
    #print(start[0].word.lower())
    if start[0].word.lower() in closeQuestionWord: 
        return start[0].word.lower()
    return None

def processQuestionType(t,w,typeMap=questionType):
    """
        Add a type to the root of the tree (= type of the answer) depending on the question word
    """
    try:
        t.subtreeType = typeMap[w]
    except KeyError:
        pass

def processQuestionInfo(t,w,addMap=questionAdd,wisMap=questionWIs):
    """
        Add info to the first sons of ROOT that are not connectors (ie index < 1000) depending on:
            - the question word
            - whether nodes contain 'identity' (comes from verb be) or not
    """
    try:
        if t.wordList[0].index >= 1000:
            for n in t.child:
                processQuestionInfo(n,w)
        elif t.getWords() == 'identity':
            t.wordList[0].word = wisMap[w] # contains 'identity', replace it according to the question word
        elif t.getWords().find(addMap[w]) == -1: # doesn't contain 'identity' and doesn't contain the word associated to w in addMap
            t.wordList.append(Word(addMap[w],1001))
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

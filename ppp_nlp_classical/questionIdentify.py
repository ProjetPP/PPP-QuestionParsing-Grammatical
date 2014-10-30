import sys

# Taken from: http://www.interopia.com/education/all-question-words-in-english/

closeQuestionWord = [
    # Yes/no question
    'is', 'are', 'am', 'was', 'were', 'will', 'do', 'does', 'did', 'have', 'had', 'has', 'can', 'could', 'should', 'shall', 'may', 'might', 'would'
]

openQuestionWord = [
    # Open-ended questions 
    'what', 'what kind', 'what type', 'what sort', 'what time', 'when', 'why', 'where', 'who', 'how', 'how much', 'how many', 'how old', 'how far', 'how long', 'how tall', 'how deep', 'how wide', 'how fast', 'how often', 'how come', 'which', 'whom', 'whose'
    # + What... for, What... like, Why don't, Where from?
    # Rarely used: Wherefore, Whatever, Wherewith, Whither, Whence, However
]

def removeWord(t,word):
    """
        Remove word (of type str*int = word*position_in_sentence) in t
        Assume word has no child
    """
    if word in t.wordList:
        if not t.child:
            t.parent.child.remove(t) 
        else:
            sys.exit('exit: question word has child (please, report your sentence on http://goo.gl/EkgO5l)\n')
    else:
        for c in t.child:
            removeWord(c,word)

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
        Identify, remove (if open qw) and return the question word
    """
    start = [None,None]
    firstWords(t,start)
    if not start[0]:
        sys.exit('exit: i don\'t understand (please, report your sentence on http://goo.gl/EkgO5l)')
    if start[1] and start[0][0].lower() + ' ' + start[1][0].lower() in openQuestionWord:
        removeWord(t,start[0])
        removeWord(t,start[1])
        return start[0][0].lower() + ' ' + start[1][0].lower()
    if start[0][0].lower() in openQuestionWord: 
        removeWord(t,start[0])
        return start[0][0].lower()
    if start[0][0].lower() in closeQuestionWord: 
        return start[0][0].lower()
    sys.exit('exit: question word not found (please, report your sentence on http://goo.gl/EkgO5l)')

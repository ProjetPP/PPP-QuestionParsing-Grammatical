import sys

# Taken from: http://www.interopia.com/education/all-question-words-in-english/
# Rarely used: Wherefore, Whatever, Wherewith, Whither, Whence, However
questionWord = [
    # Yes/no question
    'Is', 'Are', 'Am', 'Was', 'Were', 'Will', 'Do', 'Does', 'Did', 'Have', 'Had', 'Has', 'Can', 'Could', 'Should', 'Shall', 'May', 'Might', 'Would',
    # Open-ended questions 
    'What', 'What kind', 'What type', 'What sort', 'What time', 'When', 'Why', 'Where', 'Who', 'How', 'How much', 'How many', 'How old', 'How far', 'How long', 'How tall', 'How deep', 'How wide', 'How fast', 'How often', 'How come', 'Which', 'Whom', 'Whose'
      # + What... for, What... like, Why don't, Where from?
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
        Identify, remove and return the question word
    """
    start = [None,None]
    firstWords(t,start)   
    if not start[0]:
        sys.exit('only questions starting by a question word can be processed for the time')
    if start[1] and start[0][0] + ' ' + start[1][0] in questionWord:
        removeWord(t,start[0])
        removeWord(t,start[1])
        return start[0][0] + ' ' + start[1][0]
    if start[0][0] in questionWord: 
        removeWord(t,start[0])
        return start[0][0]
    sys.exit('exit: question word not found (please, report your sentence on http://goo.gl/EkgO5l)')

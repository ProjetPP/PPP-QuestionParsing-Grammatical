"""
    Taken from: http://www.interopia.com/education/all-question-words-in-english/
    Yes/no question
"""
closeQuestionWord = [
    'is', 'are', 'am', 'was', 'were', 'will', 'do', 'does', 'did', 'have', 'had', 'has', 'can', 'could', 'should', 'shall', 'may', 'might', 'would'
]

"""
    Open-ended questions
    + What... for, What... like, Why don't, Where from
    Rarely used: Wherefore, Whatever, Wherewith, Whither, Whence, However
"""
openQuestionWord = [
    'what', 'what kind', 'what type', 'what sort', 'what time', 'when', 'why', 'where', 'who', 'how', 'how much', 'how many', 'how old', 'how far', 'how long', 'how tall', 'how deep', 'how wide', 'how fast', 'how often', 'how come', 'which', 'whom', 'whose', 'how big'
]

# question word that implies to add an extra triple (ex: where is the capital of france : (france,capital,?) --> ((france,capital,?),location,?)
strongQuestionWord = [
    'what kind', 'what type', 'what sort', 'what time', 'when', 'why', 'where', 'how', 'how much', 'how many', 'how old', 'how far', 'how long', 'how tall', 'how deep', 'how wide', 'how fast', 'how often', 'how come', 'whose', 'how big'
]

questionExcept = {
    # words that already contain the info of the question word
    'what type'     : ['type','sort'],
    'what sort'     : ['type','sort'],
    'what time'     : ['time','date','day','month','year'],
    'when'          : ['time','date','day','month','year'],
    'why'           : ['reason','cause','origin'],
    'where'         : ['place','location','residence'],
    'how'           : ['manner','way'],
    'how much'      : ['amount','quantity','number'],
    'how many'      : ['amount','quantity','number'],
    'how old'       : ['age'],
    'how far'       : ['distance'],
    'how long'      : ['length'],
    'how tall'      : ['height'],
    'how deep'      : ['depth'],
    'how wide'      : ['width'],
    'how fast'      : ['speed','velocity'],
    'how often'     : ['frequency'],
    'how come'      : ['reason'],
    'whose'         : ['owner'],
    'how big'       : ['size']
}

questionAdd = {
    # how to add info into the son of ROOT (ex: when + birth = birth date) if it doesn't contain a word of questionExcept
    'what type'     : 'type',
    'what sort'     : 'type',
    'what time'     : 'time',
    'when'          : 'date',
    'why'           : 'reason',
    'where'         : 'place',
    'how'           : 'manner',
    'how much'      : 'amount',
    'how many'      : 'quantity',
    'how old'       : 'age',
    'how far'       : 'distance',
    'how long'      : 'length',
    'how tall'      : 'height',
    'how deep'      : 'depth',
    'how wide'      : 'width',
    'how fast'      : 'speed',
    'how often'     : 'frequency',
    'how come'      : 'reason',
    #'which'         : 'choice',
    'whose'         : 'owner',
    'how big'       : 'size'
}

questionWIs = {
    # how to replace the son of ROOT when it's "is" (nounified into identity) (ex : where + is = location)
    'what'          : 'definition',
    'what kind'     : 'description',
    'what type'     : 'type',
    'what sort'     : 'type',
    'what time'     : 'time',
    'when'          : 'date',
    'why'           : 'reason',
    'where'         : 'location', # != place
    'who'           : 'identity',
    'how'           : 'manner',
    'how much'      : 'amount',
    'how many'      : 'quantity',
    'how old'       : 'age',
    'how far'       : 'distance',
    'how long'      : 'length',
    'how tall'      : 'height',
    'how deep'      : 'depth',
    'how wide'      : 'width',
    'how fast'      : 'speed',
    'how often'     : 'frequency',
    'how come'      : 'reason',
    'which'         : 'choice', # ?
    'whom'          : 'identity',
    'whose'         : 'owner',
    'how big'       : 'size'
}

questionType = {
    # how to type ROOT
    'what time'     : 'DATE',
    'when'          : 'DATE',
    'where'         : 'LOCATION',
    'who'           : 'PERSON',
    'how much'      : 'NUMBER',
    'how many'      : 'quantity',
    'how old'       : 'NUMBER',
    'how far'       : 'NUMBER',
    'how long'      : 'NUMBER',
    'how tall'      : 'NUMBER',
    'how deep'      : 'NUMBER',
    'how wide'      : 'NUMBER',
    'how fast'      : 'NUMBER',
    'how often'     : 'NUMBER',
    'whom'          : 'PERSON',
    'whose'         : 'PERSON',
    'how big'       : 'NUMBER'
}

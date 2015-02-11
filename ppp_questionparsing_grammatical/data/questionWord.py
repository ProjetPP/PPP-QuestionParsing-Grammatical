
###########################
# Possible question words #
###########################

# Open-ended questions + What... for, What... like, Why don't, Where from + Rarely used: Wherefore, Whatever, Wherewith, Whither, Whence, However
openQuestionWord = [
    'list', 'what', 'what kind', 'what type', 'what sort', 'what time', 'when', 'why', 'where', 'who', 'how', 'how much', 'how many', 'how old', 'how far', 'how long', 'how tall', 'how deep', 'how wide', 'how fast', 'how often', 'how come', 'which', 'whom', 'whose', 'how big', 'of which', 'in which', 'from which'
]

# Yes/no questions
closeQuestionWord = [
    'is', 'are', 'am', 'was', 'were', 'will', 'do', 'does', 'did', 'have', 'had', 'has', 'can', 'could', 'should', 'shall', 'may', 'might', 'would'
]

# Exists questions
existQuestionWord = [
    'is there', 'are there'
]

# Other questions
semiQuestionWord = [
    'show me', 'show them', 'show us', 'show him', 'show her', 'give me', 'give them', 'give us', 'give him', 'give her', 'list of', 'give', 'show'
]

#########################
# Other classifications #
#########################

# question word that implies to add an extra triple (in practice: rule R2 vs R5) (ex: where is the capital of france : (france,capital,?) --> ((france,capital,?),location,?)
strongQuestionWord = [
    'what kind', 'what type', 'what sort', 'what time', 'when', 'why', 'where', 'how', 'how much', 'how many', 'how old', 'how far', 'how long', 'how tall', 'how deep', 'how wide', 'how fast', 'how often', 'how come', 'whose', 'how big', 'in which', 'from which'
]

#######################
# Question words maps #
#######################

questionExcept = {
    # words that already contain the info of the question word
    'what type'     : ['type','sort'],
    'what sort'     : ['type','sort'],
    'what time'     : ['time','date','day','month','year'],
    'when'          : ['time','date','day','month','year'],
    'why'           : ['reason','cause','origin'],
    'where'         : ['place','location','residence','site','country'],
    'how'           : ['manner','way'],
    'how much'      : ['amount','quantity','number'],
    'how many'      : ['amount','quantity','number'],
    'how old'       : ['age'],
    'how far'       : ['distance'],
    'how long'      : ['length','runtime'],
    'how tall'      : ['height'],
    'how deep'      : ['depth'],
    'how wide'      : ['width'],
    'how fast'      : ['speed','velocity'],
    'how often'     : ['frequency'],
    'how come'      : ['reason'],
    'whose'         : ['owner'],
    'how big'       : ['size'],
    'in which'      : ['place','location','residence','site','country'],
    'from which'    : ['place','location','residence','site','citizenship','nationality','country of citizenship','country'],
}

questionAdd = {
    # how to add info into the son of ROOT (ex: when + birth = birth date) if it doesn't already contain a word of questionExcept
    'what type'     : ['type','sort'],
    'what sort'     : ['type','sort'],
    'what time'     : ['time','date'],
    'when'          : ['time','date'],
    'why'           : ['reason','cause','origin'],
    'where'         : ['place','location','residence','country'],
    'how'           : ['manner'],
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
    #'which'         : ['choice'],
    'whose'         : ['owner'],
    'how big'       : ['size'],
    'in which'      : ['place','location','residence','country'],
    'from which'    : ['place','location','residence','origin','citizenship','nationality','country of citizenship','country']
}


questionWIs = {
    # how to replace the son of ROOT when it's "is" (nounified into identity) (ex : where + is = location)
    'what'          : ['definition'],
    'what kind'     : ['description'],
    'what type'     : ['type'],
    'what sort'     : ['type'],
    'what time'     : ['time'],
    'when'          : ['date'],
    'why'           : ['reason'],
    'where'         : ['place','location','residence','country'],
    'who'           : ['identity'],
    'how'           : ['manner'],
    'how much'      : ['amount'],
    'how many'      : ['quantity'],
    'how old'       : ['age'],
    'how far'       : ['distance'],
    'how long'      : ['length','runtime'],
    'how tall'      : ['height'],
    'how deep'      : ['depth'],
    'how wide'      : ['width'],
    'how fast'      : ['speed'],
    'how often'     : ['frequency'],
    'how come'      : ['reason'],
    'which'         : ['choice'], # ?
    'whom'          : ['identity'],
    'whose'         : ['owner'],
    'how big'       : ['size'],
    'in which'      : ['place','location','residence','country'],
    'from which'    : ['place','location','residence','origin','citizenship','nationality','country of citizenship','country']
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
    'how big'       : 'NUMBER',
    'in which'      : 'LOCATION',
    'from which'    : 'LOCATION',
}

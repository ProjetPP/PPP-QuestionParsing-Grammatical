import sys
import ppp_datamodel
from ppp_datamodel import Resource, Missing, Triple, Last, First, List, Sort, Intersection, Union, Exists
from .questionWordProcessing import questionWordNormalForm
from .data.conjunction import conjunctionTab
from .data.superlative import superlativeNoun, superlativeOrder
from .data.exceptions import GrammaticalError
from nltk.stem.wordnet import WordNetLemmatizer
from pkg_resources import resource_filename
from .nounDB import Nounificator
import pickle

nManual = Nounificator()
nManual.load(resource_filename('ppp_questionparsing_grammatical', 'data/nounificationManual.txt'))
nAuto = Nounificator()
nAuto.load(resource_filename('ppp_questionparsing_grammatical', 'data/nounificationAuto.pickle'))

file = open(resource_filename('ppp_questionparsing_grammatical', 'data/pastParticiple.pickle'), 'rb')
pastPartDict = pickle.load(file) # verb to past participle
file.close()

lemmatizer = WordNetLemmatizer()

########################
# Build resource nodes #
########################

def lemmatize(s, pos, lmtzr=lemmatizer):
    """
        Lemmatize the string s depending on its part of speech tag
    """
    if s.lower() in ('\'s', '\'re', '\'m'):
        return 'be'
    if s.lower() in ('\'ve', '\'d'): # 's : conflict between be/have
        return 'have'
    elif pos in ('NN', 'NNS'): # noun
        return lmtzr.lemmatize(s.lower(), 'n')
    elif pos and pos[0] == 'V': # verb
        return lmtzr.lemmatize(s.lower(), 'v')
    else:
        return s

def buildValue(tree):
    """
        Lemmatize the wordList and build a Resource from it
    """
    if tree.namedEntityTag == 'undef':
        for w in tree.wordList:
            w.word = lemmatize(w.word, w.pos)
    return Resource(tree.printWordList())

def verbStandardize(tree):
    """
        Assume that tree.wordList is a verb v
        Produce (v1, v2) where v1=lemmatize(v) and v2 is the past participle of v
    """
    w = tree.printWordList().lower()
    wSplit = w.split()
    wSplit[0] = lemmatize(wSplit[0], 'V')
    if tree.wordList[0].pos == 'VBN':
        pastPart = w
    elif wSplit[0] in pastPartDict:
        pastPart = ' '.join([pastPartDict[wSplit[0]]]+wSplit[1:])
    else:
        if wSplit[0].endswith('e'):
            pastPart = ' '.join([wSplit[0]+'d']+wSplit[1:])
        else:
            pastPart = ' '.join([wSplit[0]+'ed']+wSplit[1:])
    return (' '.join(wSplit), pastPart)

def buildPredicateVerb(tree):
    """
        Produce a predicate from the root of tree, assume that wordList is a verb v
        Return a couple (a, b) where a must be the predicate, and b the inverse predicate
        (b = None if there is no inverse predicate)
    """
    lem = verbStandardize(tree) # (v1, v2) where v1=lemmatize(v) and v2 is the past participle of v (v = verb of wordList)
    lDirect = [lem[1]] # the past participle is always a predicate
    lInverse = []
    if nManual.exists(lem[0]): # try to nounify the whole verb v...
        lDirect += nManual.directNouns(lem[0])
        lInverse += nManual.inverseNouns(lem[0])
    elif len(lem[0].split()) > 1 and nManual.exists(lem[0].split()[0]): # ...otherwise, try to nounify the verb withouts its particles...
        lDirect += nManual.directNouns(lem[0].split()[0])
        lInverse += nManual.inverseNouns(lem[0].split()[0])
    elif nAuto.exists(lem[0].split()[0]): # ...otherwise use the automatic nounification
        lDirect += nAuto.directNouns(lem[0].split()[0])
    # Production of the resource
    if len(lDirect) == 1: # at least 1 predicate (past part always added)
        if len(lInverse) == 0: # no inverse predicate
            return (Resource(lDirect[0]), None)
        elif len(lInverse) == 1: # 1 inverse predicate
            return (Resource(lDirect[0]), Resource(lInverse[0]))
        else:  # >1 inverse predicates
            return (Resource(lDirect[0]), List([Resource(x) for x in lInverse]))
    else: # len(lDirect) > 1
        if len(lInverse) == 0:
            return (List([Resource(x) for x in lDirect]), None)
        elif len(lInverse) == 1:
            return (List([Resource(x) for x in lDirect]), Resource(lInverse[0]))
        else:
            return (List([Resource(x) for x in lDirect]), List([Resource(x) for x in lInverse]))

def buildPredicate(tree):
    """
        Produce a predicate from the root of tree
        Return a couple (a, b) where a must be the predicate, and b the inverse predicate
        (b = None if there is no inverse predicate)
    """
    if tree.wordList[0].pos[0] == 'V':
        return buildPredicateVerb(tree)
    else:
        return (buildValue(tree), None)

###########################################
# Recursive production of the normal form #
###########################################

def normalizeSuperlative(tree):
    """
        Handle Rspl dependency (superlative, ordinal)
    """
    order = buildValue(tree).value.split(' ',1)[0] # most important > most, deepest > deepest
    predicate = buildValue(tree).value.split(' ',1)[-1] # most important > important, deepest > deepest
    if predicate in superlativeNoun:
        if order in superlativeOrder:
            return superlativeOrder[order](Sort(normalize(tree.child[0]), Resource(superlativeNoun[predicate])))
        else:
            return First(Sort(normalize(tree.child[0]), Resource(superlativeNoun[predicate]))) # First by default
    else:
        if order in superlativeOrder:
            return superlativeOrder[order](Sort(normalize(tree.child[0]), Resource('default'))) # default predicate
        else:
            return First(Sort(normalize(tree.child[0]), Resource('default')))

def normalizeConjunction(tree):
    """
        Handle Rconj dependency (conjunction)
    """
    result = []
    assert len(tree.child) == 2 and tree.child[0].dependency.startswith('Rconj') and tree.child[1].dependency.startswith('Rconj')
    conjunction = buildValue(tree).value
    if tree.child[0].dependency == 'RconjT':
        result = [normalize(tree.child[0]), normalize(tree.child[1])]
    else:
        result = [normalize(tree.child[1]), normalize(tree.child[0])]
    try:
        return conjunctionTab[conjunction](result)
    except KeyError:
        raise GrammaticalError(conjunction, "conjunction unknown")

def normalize(tree):
    """
        Map the tree to a normal form
    """
    if tree.child == []: # leaf
        return buildValue(tree)
    if tree.child[0].dependency == 'Rexist':
        return Exists(normalize(tree.child[0]))
    if tree.child[0].dependency == 'Rspl':
        return normalizeSuperlative(tree)
    if tree.child[0].dependency.startswith('Rconj'):
        return normalizeConjunction(tree)
    result = []
    for t in tree.child:
        if t.dependency == 'R0':
            result.append(normalize(t))
        if t.dependency == 'R1':
            result.append(buildValue(t))
        if t.dependency == 'R2':
            pred = buildPredicate(tree)
            if pred[1]:
                result.append(Triple(normalize(t), pred[0], Missing(), pred[1]))
            else:
                result.append(Triple(normalize(t), pred[0], Missing()))
        if t.dependency == 'R3':
            pred = buildPredicate(tree)
            if pred[1]:
                result.append(Triple(Missing(), pred[0], normalize(t), pred[1]))
            else:
                result.append(Triple(Missing(), pred[0], normalize(t)))
        if t.dependency == 'RinstOf':
           result.append(Triple(Missing(), Resource('instance of'), normalize(t)))
    if len(result) == 1:
        return result[0]
    else:
        return Intersection(result)

###################
# Global function #
###################

def normalFormProduction(tree, qw):
    nf = normalize(tree)
    return questionWordNormalForm(nf, qw)

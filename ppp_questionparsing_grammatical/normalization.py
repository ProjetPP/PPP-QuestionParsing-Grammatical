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
nManual.load(resource_filename('ppp_questionparsing_grammatical', 'data/nounificationManual.pickle'))
nAuto = Nounificator()
nAuto.load(resource_filename('ppp_questionparsing_grammatical', 'data/nounificationAuto.pickle'))

file = open(resource_filename('ppp_questionparsing_grammatical', 'data/pastParticiple.pickle'), 'rb')
pastPartDict = pickle.load(file)
file.close()

lemmatizer = WordNetLemmatizer()

########################
# Build resource nodes #
########################

def lemmatize(tree,lmtzr=lemmatizer):
    """
        Apply lemmatization to the word, using the given lemmatizer
    """
    if tree.namedEntityTag == 'undef':
        for w in tree.wordList:
            if w.pos in ('NN','NNS'):
                w.word = lmtzr.lemmatize(w.word.lower(),'n')
            elif w.pos and w.pos[0] == 'V':
                w.word = lmtzr.lemmatize(w.word.lower(),'v')

def buildValue(tree):
    """
        Used to build the values of the normal form (except for predicates)
    """
    lemmatize(tree)
    return Resource(tree.printWordList())

def verbStandardize(tree,lmtzr=lemmatizer):
    """
        Assume that tree.wordList is a verb v
        Produce (v1,v2) where v1=lemmatize(v) and v2 is the past participle of v
    """
    w = tree.printWordList().lower() # rules on / ruled on
    wSplit = w.split() # [rules,on] / [ruled,on]
    wSplit[0] = lmtzr.lemmatize(wSplit[0],'v') # [rule,on] / [rule,on]
    if tree.wordList[0].pos == 'VBN':
        pastPart = w # .. / ruled on
    elif wSplit[0] in pastPartDict: # ICI : map des participes passés
        pastPart = ' '.join([pastPartDict[wSplit[0]]]+wSplit[1:]) # ruled on / ..
    else:
        pastPart = ' '.join([wSplit[0]+'ed']+wSplit[1:])
    return (' '.join(wSplit),pastPart)

def buildPredicateVerb(tree,n):
    """
        n=0 : direct triple, n=1 : reverse triple
    """
    lem = verbStandardize(tree)
    lDirect = [lem[1]]
    lReverse = []
    if nManual.exists(lem[0]):
        lDirect += nManual.toNouns(lem[0],0)
        lReverse += nManual.toNouns(lem[0],1)
    elif len(lem[0].split()) > 1 and nManual.exists(lem[0].split()[0]):
        lDirect += nManual.toNouns(lem[0].split()[0],0)
        lReverse += nManual.toNouns(lem[0].split()[0],1)
    elif nAuto.exists(lem[0].split()[0]):
        lDirect += nAuto.toNouns(lem[0].split()[0],0)
    # Production of the resource
    if len(lDirect) == 1: # at least 1 (past part always added)
        if len(lReverse) == 0:
            return Resource(lDirect[0])
        elif len(lReverse) == 1:
            return Resource(lDirect[0]) ## value/reverse_value : lReserve[0]
        else:
            return List([Resource(lDirect[0]) for x in lReverse]) ## value/reverse_value : lReserve
    else: # len(lDirect) > 1
        if len(lReverse) == 0:
            return List([Resource(x) for x in lDirect])
        elif len(lReverse) == 1:
            return List([Resource(x) for x in lDirect]) ## value/reverse_value : lReserve[0]
        else:
            return List([Resource(x) for x in lDirect for y in lReverse]) ## value/reverse_value : lReserve

def buildPredicate(tree,n):
    """
        n=0 : direct triple, n=1 : reverse triple
    """
    if tree.wordList[0].pos[0] == 'V':
        return buildPredicateVerb(tree,n)
    else:
        return buildValue(tree)

###########################################
# Recursive production of the normal form #
###########################################

def normalizeSuperlative(tree):
    """
        Handle Rspl dependency (superlative, ordinal)
    """
    superlative = buildValue(tree).value
    if superlative in superlativeNoun:
        if superlative in superlativeOrder:
            return superlativeOrder[superlative](Sort(normalize(tree.child[0]),Resource(superlativeNoun[superlative])))
        else:
            return First(Sort(normalize(tree.child[0]),Resource(superlativeNoun[superlative]))) # First by default
    else:
        if superlative in superlativeOrder:
            return superlativeOrder[superlative](Sort(normalize(tree.child[0]),Resource('default'))) # default predicate
        else:
            return First(Sort(normalize(tree.child[0]),Resource('default')))

def normalizeConjunction(tree):
    """
        Handle Rconj dependency (conjunction)
    """
    result = []
    assert len(tree.child) == 2 and tree.child[0].dependency.startswith('Rconj') and tree.child[1].dependency.startswith('Rconj')
    conjunction = buildValue(tree).value
    if tree.child[0].dependency == 'RconjT':
        result = [normalize(tree.child[0]),normalize(tree.child[1])]
    else:
        result = [normalize(tree.child[1]),normalize(tree.child[0])]    
    try:
        return conjunctionTab[conjunction](result)
    except KeyError:
        raise GrammaticalError(conjunction,"conjunction unknown")

def normalize(tree):
    """
        Map the tree to a normal form (= final result)
    """
    if tree.child == []: # leaf
        return buildValue(tree)
    if tree.child[0].dependency == 'Rexist':
        return Exists(normalize(tree.child[0]))
    if tree.child[0].dependency == 'Rspl': # Rspl = superlative, ordinal
        return normalizeSuperlative(tree)
    if tree.child[0].dependency.startswith('Rconj'): # Rconj = conjunction
        return normalizeConjunction(tree)
    result = []
    for t in tree.child: # R0 ... R7
        if t.dependency == 'R0':
            result.append(normalize(t))
        if t.dependency == 'R1':
            result.append(buildValue(t))
        #if t.dependency == 'R2':
        #    if len(t.child) == 0:
        #        result.append(Triple(buildValue(t),buildPredicate(tree,0),Missing()))
        #    else:
        #        result.append(normalize(t))
        if t.dependency == 'R3':
            result.append(Triple(Missing(),buildPredicate(tree,1),normalize(t)))
        #if t.dependency == 'R4':
        #    result.append(Triple(Missing(),normalize(t),buildValue(tree))) ## normalize dans prédicat ????
        if t.dependency == 'R5':
            result.append(Triple(normalize(t),buildPredicate(tree,0),Missing()))
        if t.dependency == 'R6':
           result.append(Triple(Missing(),Resource('instance of'),normalize(t)))
        #if t.dependency == 'R7':
        #    result.append(Triple(buildValue(tree),normalize(t),Missing())) ## normalize dans prédicat ???? << plus utilisé ?
    if len(result) == 1:
        return result[0]
    else:
        return Intersection(result)

###################
# Global function #
###################

def normalFormProduction(tree,qw):
    nf = normalize(tree)
    return questionWordNormalForm(nf,qw)

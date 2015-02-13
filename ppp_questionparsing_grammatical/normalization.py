import sys
import ppp_datamodel
from .preprocessing import DependenciesTree
from ppp_datamodel import Resource, Missing, Triple, Last, First, List, Sort, Intersection, Union, Exists
from .data.conjunction import conjunctionTab
from .data.superlative import superlativeNoun, superlativeOrder
from .data.exceptions import GrammaticalError
from nltk.stem.wordnet import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()

################
# Build values #
################

def lemmatize(tree,lmtzr=lemmatizer):
    """
        Apply lemmatization to the word, using the given lemmatizer
        This function is not suppposed to be applied on future predicates
    """
    if t.namedEntityTag == 'undef':
        for w in t.wordList:
            if w.pos and w.pos[0] == 'N':
                w.word = lmtzr.lemmatize(w.word.lower(),'n')
            elif w.pos and w.pos[0] == 'V':
                w.word = lmtzr.lemmatize(w.word.lower(),'v')

def buildValue(tree):
    """
        Used to build the values of the normal form (except for predicates)
    """
    lemmatize(tree)
    return Resource(tree.printWordList())

def buildPredicate(tree):
    lDirect = []
    lReverse = []
    if tree.wordList[0].pos[0] == 'V':
        assert (len(tree.wordList)==1)
        w = tree.printWordList().lower()
        wLem = lmtzr.lemmatize(w.split()[0],'v') # only the first word (based on -> base)
        if nManual.exists(wLem):
            lDirect = nManual.toNouns(wLem,0)
            lReverse = nManual.toNouns(wLem,1)
        elif nAuto.exists(wLem):
            lDirect += nAuto.toNouns(wLem) # 0 par défaut
        if self.pos == 'VBN':
            lDirect.append(w)
            wLem = lmtzr.lemmatize(w,'v') # whole word (based on -> base on)
            if nManual.exists(wLem):
                lDirect += nManual.toNouns(wLem,0)
                lReverse += nManual.toNouns(wLem,1)
            elif nAuto.exists(wLem):
                lDirect += nAuto.toNouns(wLem) # 0 par défaut           
        if len(lDirect) == 0:
            if len(lReverse) == 0:
                return Resource(wLem)
            elif len(lReverse) == 1:
                return Resource(wLem) ## value/reverse_value : lReserve[0]
            else:
                return List([Resource(wLem) for x in lReverse]) ## value/reverse_value : lReserve
        elif len(lDirect) == 1:
            if len(lReverse) == 0:
                return Resource(lDirect[0])
            elif len(lReverse) == 1:
                return Resource(lDirect[0]) ## value/reverse_value : lReserve[0]
            else:
                return List([Resource(lDirect[0]) for x in lReverse]) ## value/reverse_value : lReserve
        else:
            if len(lReverse) == 0:
                return List([Resource(x) for x in lDirect])
            elif len(lReverse) == 1:
                return List([Resource(x) for x in lDirect]) ## value/reverse_value : lReserve[0]
            else:
                return List([Resource(x) for x in lDirect for y in lReverse])## value/reverse_value : lReserve
    else:
        return buildValue(tree)

###########################################
# Recursive production of the normal form #
###########################################

def normalizeSuperlative(tree):
    """
        Handle Rspl dependency (superlative, ordinal)
    """
    superlative = buildValue(tree)
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
    conjunction = buildValue(tree)
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
        if t.dependency == 'R2':
            if len(t.child) == 0:
                result.append(Triple(buildValue(t),buildPredicate(tree),Missing()))
            else:
                result.append(normalize(t))
        if t.dependency == 'R3':
            result.append(Triple(Missing(),buildPredicate(tree),normalize(t)))
        if t.dependency == 'R4':
            result.append(Triple(Missing(),normalize(t),buildValue(tree)))
        if t.dependency == 'R5':
            result.append(Triple(normalize(t),buildPredicate(tree),Missing()))
        if t.dependency == 'R6':
           result.append(Triple(Missing(),Resource('instance of'),normalize(t)))
        if t.dependency == 'R7':
            result.append(Triple(buildValue(tree),normalize(t),Missing())) ## normalize dans prédicat ????
    if len(result) == 1:
        return result[0]
    else:
        return Intersection(result)

###############################################
# Improve the normal form depending on the qw #
###############################################

def questionWordEnhancement(tree,qw):

###################
# Global function #
###################

def normalFormProduction(tree,qw):

######################


from pkg_resources import resource_filename
from .nounDB import Nounificator

nManual = Nounificator()
nManual.load(resource_filename('ppp_questionparsing_grammatical', 'data/nounificationManual.pickle'))
nAuto = Nounificator()
nAuto.load(resource_filename('ppp_questionparsing_grammatical', 'data/nounificationAuto.pickle'))

def nounify(s):
    """
        Return the string list of the closest nouns to s (die -> death)
        Replace by hard-coded exceptions if they exist (e.g. be, have, do, bear...)
    """
    if nManual.exists(s):
        return nManual.toNouns(s)
    if nAuto.exists(s):
        return nAuto.toNouns(s)
    return []

def standardize(self,lmtzr):
        """
            Apply lemmatization to the word, using the given lemmatizer
            Return the list of strings that must replaced self.word if nounification is necessary (ie if the word is a verb), [] otherwise
        """
        if self.pos and self.pos[0] == 'N':
            self.word=lmtzr.lemmatize(self.word.lower(),'n')
        elif self.pos and self.pos[0] == 'V':
            s = lmtzr.lemmatize(self.word.lower().split()[0],'v')
            if self.pos != 'VBN':
                return list(set(nounify(s))) # + [s] ??? list(set) ???
            else:
                return list(set(nounify(s) + nounify(self.word.lower()))) # + [self.word.lower()]
        return []

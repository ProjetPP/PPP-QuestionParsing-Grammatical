import sys
import ppp_datamodel
from .preprocessing import DependenciesTree
from ppp_datamodel import Resource, Missing, Triple, Last, First, List, Sort, Intersection, Union, Exists
from .data.conjunction import conjunctionTab
from .data.superlative import superlativeNoun, superlativeOrder
from .data.exceptions import GrammaticalError

def buildValue(tree):
    """
        Used to build the values of the normal form.
            len(tree.getWords()) = 1 -> single value -> return a resource
            len(tree.getWords()) > 1 -> multiple alternatives -> return a list of resources
    """
    if len(tree.getWords()) == 1:
        return Resource(tree.getWords()[0])
    else:
        return List([Resource(x) for x in tree.getWords()])

def normalizeSuperlative(tree):
    """
        Handle Rspl dependency (superlative, ordinal)
    """
    assert len(tree.getWords()) == 1 and len(tree.child) == 1
    superlative = tree.getWords()[0]
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
    assert len(tree.getWords()) == 1
    assert len(tree.child) == 2 and tree.child[0].dependency.startswith('Rconj') and tree.child[1].dependency.startswith('Rconj')
    conjunction = tree.getWords()[0]
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
                result.append(Triple(buildValue(t),buildValue(tree),Missing()))
            else:
                result.append(normalize(t))
        if t.dependency == 'R3':
            result.append(Triple(Missing(),buildValue(tree),normalize(t)))
        if t.dependency == 'R4':
            result.append(Triple(Missing(),normalize(t),buildValue(tree)))
        if t.dependency == 'R5':
            result.append(Triple(normalize(t),buildValue(tree),Missing()))
        if t.dependency == 'R6':
           result.append(Triple(Missing(),Resource('instance of'),normalize(t)))
        if t.dependency == 'R7':
            result.append(Triple(buildValue(tree),normalize(t),Missing()))
    if len(result) == 1:
        return result[0]
    else:
        return Intersection(result)

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

#Word:
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
                return list(set(nounify(s) + nounify(self.word.lower()))) #+ + [self.word.lower()]
        return []

#########################

from nltk.stem.wordnet import WordNetLemmatizer
from .data.exceptions import GrammaticalError
from .data.questionWord import strongQuestionWord

def subStandardize(t,lmtzr):
    for c in t.child:
        subStandardize(c,lmtzr)
    if t.namedEntityTag == 'undef':
        assert len(t.wordList) == 1 and len(t.wordList[0]) == 1 # len(t.wordList[0])=1 because the wordList of size>1 have been built by NER merging
        w = t.wordList[0][0]
        l = w.standardize(lmtzr)
        if l !=[]:
            t.wordList = [[Word(x,w.index,w.pos)] for x in l]

def standardize(t):
    """
        Apply lemmatization + nounification
    """
    lmtzr = WordNetLemmatizer()
    subStandardize(t,lmtzr) # standardize words (lemmatization + nounify nouns)

import sys
import os
from pkg_resources import resource_filename
from .data.exceptions import NounificationError
from .nounDB import Nounificator

########################################
# Word lemmatization and nounification #
########################################

nManual = Nounificator()
nManual.load(resource_filename('ppp_questionparsing_grammatical', 'data/nounificationManual.pickle'))
nAuto = Nounificator()
nAuto.load(resource_filename('ppp_questionparsing_grammatical', 'data/nounificationAuto.pickle'))

class Word:
    """
        One word of the sentence
    """
    def __init__(self, word, index, pos=None):
        self.word = word    # string that represents the word
        self.index = index  # position in the sentence
        self.pos = pos      # Part Of Speech tag (verb, noun, ...)

    def __str__(self):
        return "({0},{1},{2})".format(str(self.word),str(self.index),str(self.pos))

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __lt__(self, other):
        assert isinstance(other,Word)
        return (self.index,self.word,self.pos) < (other.index,other.word,other.pos)
       
    def nounify(self):
        """
            Return the string list of the closest nouns to self (die -> death)
            Replace by hard-coded exceptions if they exist (e.g. be, have, do, bear...)
        """
        if nManual.exists(self.word):
            return nManual.toNouns(self.word)
        if nAuto.exists(self.word):
            return nAuto.toNouns(self.word)
        raise NounificationError(self.word,"cannot nounify this word")

    def standardize(self,lmtzr):
        """
            Apply lemmatization to the word, using the given lemmatizer
            Return the list of strings that must replaced self.word if nounification is necessary (ie if the word is a verb), [] otherwise
        """
        if self.pos and self.pos[0] == 'N':
            self.word=lmtzr.lemmatize(self.word.lower(),'n')
        elif self.pos and self.pos[0] == 'V':
            self.word=lmtzr.lemmatize(self.word.lower(),'v')
            return self.nounify()
        return []

###################
# NER recognition #
###################

def mergeNamedEntityTagChildParent(t):
    """
        Merge all nodes n1, n2 such that:
            * n1 is parent of n2
            * n1 and n2 have a same namedEntityTag
        Don't merge if the 2 words are linked by a conjonction
    """
    for c in t.child:
        mergeNamedEntityTagChildParent(c)
    sameTagChild = set()
    if t.namedEntityTag == 'undef':
        return
    for c in t.child:
        if c.namedEntityTag == t.namedEntityTag and not c.dependency.startswith('conj'):
            sameTagChild.add(c)
    for c in sameTagChild:
        t.merge(c,True)

def mergeNamedEntityTagSisterBrother(t):
    """
        Merge all nodes n1, n2 such that:
            * n1 and n2 have a same parent
            * n1 and n2 have a same namedEntityTag
            * n1 and n2 have a same dependency
    """
    for c in t.child:
        mergeNamedEntityTagSisterBrother(c)
    tagToNodes = {}
    for c in t.child:
        if c.namedEntityTag == 'undef' or c.dependency.startswith('conj'):
            continue
        try:
            tagToNodes[c.namedEntityTag+c.dependency].add(c)
        except KeyError:
            tagToNodes[c.namedEntityTag+c.dependency] = set([c])
    for sameTag in tagToNodes.values():
        x = sameTag.pop()
        for other in sameTag:
            x.merge(other,True)

def mergeNamedEntityTag(t):
    mergeNamedEntityTagChildParent(t)
    mergeNamedEntityTagSisterBrother(t)

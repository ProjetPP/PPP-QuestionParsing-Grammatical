import sys
import os
import random
import string
from .data.exceptions import QuotationError
from .dependencyTree import DependenciesTree

#####################
# Quotation merging #
#####################

def index(l, pred):
    """
        Return the index of the first element of l which is in pred.
        Raise ValueError if there is not such an element.
    """
    for (i, x) in enumerate(l):
        if x in pred:
            return i
    raise ValueError

class QuotationHandler:
    """
        An object to handle quotations in the sentences.
    """
    __slots__ = ('replacement', 'replacementIndex', 'quotations')
    quotationList = ['“', '”', '"']
    def __init__(self, replacement=None):
        self.replacement = replacement
        self.replacementIndex = 0
        self.quotations = {}
        random.seed()

    def checkQuotation(self, sentence):
        """
            Check that there is an even number of quotation marks.
            Raise QuotationError otherwise.
        """
        if len([c for c in sentence if c in self.quotationList]) % 2 == 1:
            raise QuotationError(sentence, "Odd number of quotation marks.")

    def getReplacement(self, sentence):
        """
            Return a random string which does not appear in the sentence.
        """
        sep = "".join(random.sample(string.ascii_uppercase, 3))
        while sep in sentence:
            sep = "".join(random.sample(string.ascii_uppercase, 3))
        return sep

    def pull(self, sentence):
        """
            Remove/pull the quotations from the sentence, and replace them.
        """
        if not self.replacement:
            self.replacement = self.getReplacement(sentence)
        if self.replacementIndex == 0:
            self.checkQuotation(sentence)
        try:
            indexBegin = index(sentence, self.quotationList)
            indexEnd = indexBegin+index(sentence[indexBegin+1:], self.quotationList)+1
        except ValueError:
            return sentence
        replacement = self.replacement+str(self.replacementIndex)
        self.replacementIndex += 1
        self.quotations[replacement] = sentence[indexBegin+1:indexEnd]
        return self.pull(sentence[0:indexBegin]+replacement+sentence[indexEnd+1:])

    def push(self, tree):
        """
            Replace/push the spaces in the nodes of the tree.
        """
        for c in tree.child:
            self.push(c)
        replaced = False
        for w in tree.wordList:
            try:
                w.word = self.quotations[w.word]
                w.pos = 'QUOTE'
                replaced = True
            except KeyError:
                continue
        if replaced:
            tree.namedEntityTag = 'QUOTATION'
        for key in self.quotations.keys():
            tree.text = tree.text.replace(key, "``"+self.quotations[key]+"''")

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
        t.merge(c, True)

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
            x.merge(other, True)

def mergeNamedEntityTag(t):
    mergeNamedEntityTagChildParent(t)
    mergeNamedEntityTagSisterBrother(t)

##########################
# Preposition processing #
##########################

prepSet = ['in', 'for', 'to', 'with', 'about', 'at', 'of', 'on', 'from', 'between', 'against']

def mergePrepNode(t):
    """
        Merge x -> y into 'x y' if y is a preposition
    """
    temp = list(t.child) # copy, because t.child is changed while iterating
    for c in temp:
        mergePrepNode(c)
    if t.printWordList() in prepSet:
        t.parent.merge(t, True)

def mergePrepEdge(t):
    """
        Replace a -prep_x-> b by 'a x' -prep-> b if a is a verb, a -prep-> b otherwise
        Replace a -agent-> b by 'a by' -agent-> b
    """
    temp = list(t.child) # copy, because t.child is changed while iterating
    for c in temp:
        mergePrepEdge(c)
    if t.dependency.startswith('prep'): # prep_x or prepc_x
        prep = ' '.join(t.dependency.split('_')[1:]) # type of the prep (of, in, ...)
        if t.parent.wordList[0].pos[0] == 'V':
            t.parent.wordList[0].word += ' ' + prep
        t.dependency = 'prep'
    if t.dependency == 'agent':
        assert t.parent.wordList[0].pos[0] == 'V'
        t.parent.wordList[0].word += ' by'

###################
# Global function #
###################

def preprocessingMerge(t):
    mergeNamedEntityTag(t)
    mergePrepNode(t)
    mergePrepEdge(t)

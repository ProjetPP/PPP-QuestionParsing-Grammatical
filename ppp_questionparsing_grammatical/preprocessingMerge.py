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

    @classmethod
    def checkQuotation(cls, sentence):
        """
            Check that there is an even number of quotation marks.
            Raise QuotationError otherwise.
        """
        if len([c for c in sentence if c in cls.quotationList]) % 2 == 1:
            raise QuotationError(sentence, "Odd number of quotation marks.")

    @staticmethod
    def getReplacement(sentence):
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
        return self.pull("%s%s%s" % (sentence[0:indexBegin], replacement, sentence[indexEnd+1:]))

    def push(self, tree):
        """
            Replace/push the spaces in the nodes of the tree.
        """
        for child in tree.child:
            self.push(child)
        replaced = False
        for word in tree.wordList:
            try:
                word.word = self.quotations[word.word]
                word.pos = 'QUOTE'
                replaced = True
            except KeyError:
                continue
        if replaced:
            tree.namedEntityTag = 'QUOTATION'
        for (replacement, original) in self.quotations.items():
            tree.text = tree.text.replace(replacement, "``%s''" % original)

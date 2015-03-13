import sys
import os
import random
import string
import re
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
    quotationRegexp = '|'.join(r'{0}(?:\.|[^{0}{1}\\])*{1}'.format(quote[0], quote[1])
        for quote in ['""', '“”', '‘’', '«»']
    )

    def __init__(self, replacement=None):
        self.replacement = replacement
        self.replacementIndex = 0
        self.quotations = {}
        random.seed()

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
        self.replacement = self.replacement or self.getReplacement(sentence)
        for quote in re.finditer(self.quotationRegexp, sentence):
            self.quotations[self.replacement+str(quote.start())] = sentence[quote.start()+1 : quote.end()-1]
        return re.subn(self.quotationRegexp, lambda quote: self.replacement+str(quote.start()), sentence)[0]

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

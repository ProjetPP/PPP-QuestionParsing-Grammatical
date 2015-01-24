import sys
from nltk.corpus import wordnet as wn
from .data.exceptions import GrammaticalError, QuotationError
from .data.nounification import nounificationDict

########################################
# Word lemmatization and nounification #
########################################

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

    def nounifyScratch(self):
        """ 
            Return the string list of the closest nouns to self (die -> death)
            Assume that the POS tag of self is verb
            From George-Bogdan Ivanov on StackOverflow: http://stackoverflow.com/a/16752477/4110059
        """
        synsets = wn.synsets(self.word, pos="v")
        if not synsets: # Word not found
            return []
        # Get all lemmas of the word (consider 'a'and 's' equivalent)
        for s in synsets:
            lemmas = [l for l in s.lemmas() if s.name().split('.')[1] == "v"]
        # Get related forms
        derivationally_related_forms = [(l, l.derivationally_related_forms()) for l in lemmas]
        # filter only the desired pos (consider 'a' and 's' equivalent)
        related_noun_lemmas = [l for drf in derivationally_related_forms
                                 for l in drf[1] 
                                 if l.synset().name().split('.')[1] == "n"]
        # Extract the words from the lemmas
        words = [l.name() for l in related_noun_lemmas]
        len_words = len(words)
        # Build the result in the form of a list containing tuples (word, probability)
        result = [(w, float(words.count(w))/len_words) for w in set(words)]
        result.sort(key=lambda w: -w[1]) # sorted by probability
        # return the x most relevant nouns
        len_min = min(20,len(result))
        return [result[i][0] for i in range(0,len_min)]
       
    def nounify(self):
        """
            Return the string list of the closest nouns to self (die -> death)
            Replace by hard-coded exceptions if they exist (e.g. be, have, do, bear...)
        """
        if self.word in nounificationDict:
            return nounificationDict[self.word]
        else:
            return self.nounifyScratch()

    def standardize(self,lmtzr):
        """
            Apply lemmatization to the word, using the given lemmatizer
            Return the list of strings that must replaced self.word if nounification is necessary (ie if the word is a verb), [] otherwise
        """
        if self.pos and self.pos[0] == 'N':
            self.word=lmtzr.lemmatize(self.word,'n')
        elif self.pos and self.pos[0] == 'V':
            self.word=lmtzr.lemmatize(self.word,'v')
            return self.nounify()
        return []

def buildWord(s):
    """
        if string s is of type:
          s'-number : build Word(s',number)
          otherwise : build Word(s,1000)
    """
    if s.find('-') != -1:
        return Word(s[:s.rindex('-')],int(s[s.rindex('-')+1:]))
    else:
        return Word(s,1000)

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
        if c.namedEntityTag == 'undef':
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

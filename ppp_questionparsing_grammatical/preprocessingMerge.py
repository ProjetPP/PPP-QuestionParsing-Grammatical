import sys
from nltk.corpus import wordnet
from .data.exceptions import GrammaticalError, QuotationError
from .data.nounification import nounificationExceptions

########################################
# Word lemmatization and nounification #
########################################

class Word:
    """
    One word of the sentence.
    """
    def __init__(self, word, index, pos=None):
        self.word = word    # strings that represents the word
        self.index = index  # position in the sentence
        self.pos = pos      # Part Of Speech tag
        
    def __str__(self):
        return "({0},{1},{2})".format(str(self.word),str(self.index),str(self.pos))

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def verbToRelatedForms(self):
        """
            Return the lemmas associated to the given verb.
            Useful for nounification.
        """
        assert self.pos[0] == 'V'
        verb_synsets = wordnet.synsets(self.word, pos="v")
        # Get all verb lemmas of the word
        verb_lemmas=[]
        for s in verb_synsets:
            verb_lemmas += [l for l in s.lemmas() if s.name().split('.')[1] == 'v']
        # Return related forms
        return [(l, l.derivationally_related_forms()) for l in verb_lemmas]

    def verbToRelatedNouns(self):
        """
            Return the nouns associated to the given verb.
            Useful for nounification.
        """
        derivationally_related_forms = self.verbToRelatedForms()
        # Filter only the nouns
        related_noun_lemmas = []
        for drf in derivationally_related_forms:
            related_noun_lemmas += [l for l in drf[1] if l.synset().name().split('.')[1] == 'n']
        # Extract the words from the lemmas
        return [l.name() for l in related_noun_lemmas]

    def mostRelevantStem(self,words,st):
        """
            Return the most occuring stem of the given list of words."
        """
        stems = [st.stem(w) for w in words]
        len_stems = len(stems)
        result = [(w, float(stems.count(w))/len_stems) for w in set(stems)]
        result.sort(key=lambda w: -w[1])
        return result[0][0]

    def mostRelevantNouns(self,st):
        """
            Return the nouns associated to the given verb, which have the stem occuring the most.
        """
        words = self.verbToRelatedNouns()
        if not words:
            return []
        stem = self.mostRelevantStem(words,st)
        return [w for w in words if st.stem(w) == stem]

    def nounify(self,st):
        """ 
            Transform a verb to the closest noun: die -> death
            From George-Bogdan Ivanov on StackOverflow: http://stackoverflow.com/a/16752477/4110059
        """
        words = self.mostRelevantNouns(st)
        if not words:
            return
        len_words = len(words)
        # Build the result in the form of a list containing tuples (word, probability)
        result = [(w, float(words.count(w))/len_words) for w in set(words)]
        result.sort(key=lambda w: -w[1])
        # take the word with highest probability
        self.word = result[0][0]

    def nounifyExcept(self,st):
        """
            Transform a verb to the closest noun: die -> death
            Hard-coded exceptions (e.g. be, have, do, bear...)
        """
        try:
            self.word = nounificationExceptions[self.word]
        except KeyError:
            self.nounify(st)

    def standardize(self,lmtzr,st):
        """
            Apply lemmatization to the word, using the given lemmatizer and stemmer.
        """
        if(self.pos and self.pos[0] == 'N'):
            self.word=lmtzr.lemmatize(self.word,'n')
            return
        if(self.pos and self.pos[0] == 'V'):
            self.word=lmtzr.lemmatize(self.word,'v')
            self.nounifyExcept(st)
            return

def buildWord(word):
    """
        if word is of type:
          word'-number : build Word(word',number)
          otherwise    : build Word(word,-1)
    """
    if word.find('-') != -1:
        return Word(word[:word.rindex('-')],int(word[word.rindex('-')+1:]))
    else:
        return Word(word,1000)

###################
# NER recognition #
###################

def mergeNamedEntityTagChildParent(t):
    """
        Merge all nodes n1,n2 such that:
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
        Merge all nodes n1,n2 such that:
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

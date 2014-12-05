import sys
from .data.nounification import nounificationExceptions
from nltk.corpus import wordnet
from .data.exceptions import GrammaticalError, QuotationError

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

#########################
# Quotation recognition #
#########################

def findQuotations(r):
    """
        Return a list of elements of the form (begin,end,set of integers).
        Each set is a set of words index belonging to a same quotation.
        Begin and end are the index of the quotations marks
    """
    index=0
    inQuote=False
    quotationList=[]
    quotationSet = set()
    for word in r['words']:
        index+=1
        if word[0] == "``":
            if inQuote:
                raise QuotationError(r,"begin a quotatin inside a quotation")
            inQuote = True
            begin=index
            continue
        if word[0] == "''":
            if not inQuote:
                raise QuotationError(r,"end a quotation not inside a quotation")
            inQuote=False
            quotationList+=[(begin,index,quotationSet)]
            quotationSet = set()
            continue
        if inQuote:
            quotationSet.add(index)
    if inQuote:
        raise QuotationError(r,"quotation not terminated")
    return quotationList

def matchingQuoteWord(w,quotationList):
    """
        Return the quotation set in which belong the word (None otherwise).
        w must be of the form (word,index)
    """
    for quote in quotationList:
        if w.index in quote[2]:
            return quote
    return None

def matchingQuote(wlist,quotationList):
    """
        Return the quotation set in which belong all the words of the list (None otherwise).
        If two words does not belong to the same quotation, error.
    """
    quote=matchingQuoteWord(wlist[0],quotationList)
    for w in wlist:
        if matchingQuoteWord(w,quotationList) != quote:
            raise GrammaticalError(w,"node belong to several quotations")
    return quote

def quotationTraversal(t,quotationList,quoteIndexToNode):
    """
        Traverse the tree to merge quotations, given a quotationList (computed
            with findQuotation).
        Fill quoteIndexToNode (map from the index of the beginning of the quote to the node.
    """
    childCopy = list(t.child)
    for c in childCopy:
        quotationTraversal(c,quotationList,quoteIndexToNode)
    quote = matchingQuote(t.wordList,quotationList)
    if not quote:
        return
    if not quote[0] in quoteIndexToNode: 
        quoteIndexToNode[quote[0]] = t
    childCopy = list(t.child)
    for c in childCopy:
        if matchingQuote(c.wordList,quotationList) == quote:
            t.merge(c,True)
            quoteIndexToNode[quote[0]] = t

def handleLostQuotationWords(r,quoteIndexToNode):
    """
        Add quotation words deleted by Stanford CoreNLP, such as "in" or "of".
    """
    inQuote=False
    quoteNode=None
    index=0
    # Add words which are not nodes
    for word in r['words']:
        index+=1
        if word[0] == "``":
            inQuote = True
            quoteNode=quoteIndexToNode[index]
            indexBegin = index
            continue
        if word[0] == "''":
            inQuote = False
            characterOffsetEnd = int(word[1]['CharacterOffsetBegin'])
            quoteNode.wordList = [Word(r['text'][int(r['words'][indexBegin-1][1]['CharacterOffsetEnd']):int(r['words'][index-1][1]['CharacterOffsetEnd'])-1],indexBegin+1,'QUOTE')]
            continue

def addQuotationTag(quoteIndexToNode):
    """
        Add the tag "QUOTATION" to all nodes in quoteIndexToNode.
    """
    for c in quoteIndexToNode.values():
        c.namedEntityTag="QUOTATION"

def mergeQuotations(t,r):
    """
        Merge all nodes corresponding to quotations.
    """
    quotationList = findQuotations(r)
    quoteIndexToNode = {}
    # Merge existing nodes belonging to quotations.
    quotationTraversal(t,quotationList,quoteIndexToNode)
    handleLostQuotationWords(r,quoteIndexToNode)
    addQuotationTag(quoteIndexToNode)

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

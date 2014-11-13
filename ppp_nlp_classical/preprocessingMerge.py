import sys

#########################
# Quotation recognition #
#########################

class Word:
    """
    One word of the sentence.
    """
    def __init__(self, word, index, pos=None):
        self.word = word
        self.index = index
        self.pos = pos
    def __str__(self):
        return "({0},{1},{2})".format(str(self.word),str(self.index),str(self.pos))
    def __eq__(self, other): 
        return self.__dict__ == other.__dict__

def findQuotations(r):
    """
        Return a list of elements of the form (begin,end,set of integers).
        Each set is a set of words index belonging to a same quotation.
        Begin and end are the index of the quotations marks
    """
    index=0
    (inQuote,quotationList,quotationSet)=(False,[],set())
    for word in r['words']:
        index+=1
        if word[0] == "``":
            assert not inQuote
            (inQuote,begin) = (True,index)
            continue
        if word[0] == "''":
            assert inQuote
            quotationList+=[(begin,index,quotationSet)]
            (inQuote,quotationSet)=(False,set())
            continue
        if inQuote:
            quotationSet.add(index)
    assert not inQuote
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
            sys.exit('exit: node belong to several quotations (please, report your sentence on http://goo.gl/EkgO5l)\n')
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
    (inQuote,quoteNode)=(False,None)
    index=0
    # Add words which are not nodes
    for word in r['words']:
        index+=1
        if word[0] == "``":
            (inQuote,quoteNode) = (True,quoteIndexToNode[index])
            continue
        if word[0] == "''":
            inQuote = False
            quoteNode.wordList.sort(key = lambda x: x.index)
            continue
        if inQuote and index not in [w.index for w in quoteNode.wordList]:
            quoteNode.wordList += [Word(word[0],index,word[1]['PartOfSpeech'])]

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
    """
    for c in t.child:
        mergeNamedEntityTagChildParent(c)
    sameTagChild = set()
    if t.namedEntityTag == 'undef':
        return
    for c in t.child:
        if c.namedEntityTag == t.namedEntityTag:
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

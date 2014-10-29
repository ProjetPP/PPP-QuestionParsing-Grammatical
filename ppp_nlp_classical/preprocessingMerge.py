import sys

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
            assert not inQuote
            inQuote = True
            begin=index
            continue
        if word[0] == "''":
            assert inQuote
            inQuote=False
            quotationList+=[(begin,index,quotationSet)]
            quotationSet = set()
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
        if w[1] in quote[2]:
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
            sys.exit('exit: node belong to several quotations (please, report your sentence on http://goo.gl/EkgO5l)\n%s\n' % self.getWords())
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

def mergeQuotations(t,r,nameToNodes):
    """
        Merge all nodes corresponding to quotations.
    """
    quotationList = findQuotations(r)
    quoteIndexToNode = {}
    # Merge existing nodes belonging to quotations.
    quotationTraversal(t,quotationList,quoteIndexToNode)
    inQuote=False
    quoteNode=None
    index=0
    # Add words which are not nodes
    for word in r['words']:
        index+=1
        if word[0] == "``":
            inQuote = True
            quoteNode=quoteIndexToNode[index]
            continue
        if word[0] == "''":
            inQuote = False
            quoteNode.wordList.sort(key = lambda x: x[1])
            continue
        if inQuote and (word[0],index) not in quoteNode.wordList:
            quoteNode.wordList += [(word[0],index)]

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

""" First step of the algorithm."""

import sys

class DependenciesTree:
    """
        One node of the parse tree.
        It is a group of words of the initial sentence.
    """
    def __init__(self, word, namedentitytag='undef', dependency='undef', child=None):
        self.wordList = [(word[:word.rindex('-')],int(word[word.rindex('-')+1:]))] # words of the node
        self.namedEntityTag = namedentitytag 
        self.dependency = dependency # dependency from self to its parent
        self.child = child or [] # children of self
        self.text = "" # each node contains whole sentence
        self.parent=None # parent of self

    def string(self):
        # Concatenation of the words of the root
        w = ' '.join(x[0] for x in self.wordList)
        s=''
        # Adding the definition of the root (dot format)
        t=''
        if(self.namedEntityTag != 'O' and self.namedEntityTag != 'undef'):
            t+= " [{0}]".format(self.namedEntityTag)
        s+="\t\"{0}\"[label=\"{1}{2}\",shape=box];\n".format(self.wordList[0][0]+str(self.wordList[0][1]),w,t)
        # Adding definitions of the edges
        for n in self.child:
            s+="\t\"{0}\" -> \"{1}\"[label=\"{2}\"];\n".format(self.wordList[0][0]+str(self.wordList[0][1]),n.wordList[0][0]+str(n.wordList[0][1]),n.dependency)
        # Recursive calls
        for n in self.child:
            s+=n.string()
        return s

    def __str__(self):
        """
            Print dependency graph in dot format
        """
        return "digraph relations {"+"\n{0}\tlabelloc=\"t\"\tlabel=\"{1}\";\n".format(self.string(),self.text)+"}"

    def merge(self,other,mergeWords):
        """
            Merge the root of the two given trees into one single node.
            Merge the two wordList if mergeWords=True (otherwise only keep the WordList of self).
            The result is stored in node 'self'.
        """
        self.child += other.child
        for c in other.child:
            c.parent = self
        if mergeWords:
          self.wordList = other.wordList + self.wordList
          self.wordList.sort(key = lambda x: x[1])
        if other.parent:
            other.parent.child.remove(other)
        other.wordList = [("merged",0)]

def computeEdges(r,nameToNodes):
    """
        Compute the edges of the dependence tree.
        Take in input a piece of the result produced by StanfordNLP, and the
        map from names to nodes.
    """
    for edge in r['indexeddependencies']:
        try:
            n1 = nameToNodes[edge[1]]
        except KeyError:
            n1 = DependenciesTree(edge[1])
            nameToNodes[edge[1]] = n1
        try:
            n2 = nameToNodes[edge[2]]
        except KeyError:
            n2 = DependenciesTree(edge[2])
            nameToNodes[edge[2]] = n2
        # n1 is the parent of n2
        n1.child = n1.child+[n2]
        n2.parent = n1
        n2.dependency = edge[0]

def computeTags(r,nameToNodes):
    """
        Compute the tags of the dependence tree nodes.
        Take in input a piece of the result produced by StanfordNLP, and the
        map from names to nodes.
    """
    index=1
    # Computation of the tags of the nodes
    for word in r['words']:
        if word[0].isalnum() or word[0] == '$' or  word[0] == '%':
            w=word[0]+'-'+str(index) # key in the nameToNodes map
            index+=1
            try:
                n = nameToNodes[w]
                if word[1]['NamedEntityTag'] != 'O':
                    n.namedEntityTag = word[1]['NamedEntityTag']
            except KeyError:        # this node does not exists (e.g. 'of' preposition)
                pass

def findQuotations(r):
    """
        Return a list of elements of the form (begin,end,set of integers).
        Each set is a set of words index belonging to a same quotation.
        Begin and end are the index of the quotations marks
    """
    index=1
    inQuote=False
    quotationList=[]
    quotationSet = set()
    for word in r['words']:
        if word[0] == "``":
            assert not inQuote
            inQuote = True
            begin=index
        elif word[0] == "''":
            assert inQuote
            inQuote=False
            quotationList+=[(begin,index,quotationSet)]
            quotationSet = set()
        elif inQuote:
            quotationSet.add(index)
        index+=1
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
            sys.stderr.write('exit: node belong to several quotations (please, report your sentence)\n')
            sys.stderr.write(' '.join(x[0] for x in self.wordList)+"\n")
            sys.exit()
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
    index=1
    # Add words which are not nodes
    for word in r['words']:
        if word[0] == "``":
            inQuote = True
            quoteNode=quoteIndexToNode[index]
        elif word[0] == "''":
            inQuote = False
            quoteNode.wordList.sort(key = lambda x: x[1])
        elif inQuote:
            if (word[0],index) not in quoteNode.wordList:
                quoteNode.wordList += [(word[0],index)]
        index+=1

def initText(t,s):
    """
        Set text attribute for all nodes, with string s.
    """
    t.text = s
    for c in t.child:
        initText(c,s)

def computeTree(r):
    """
        Compute the dependence tree.
        Take in input a piece of the result produced by StanfordNLP.
        If foo is this result, then r = foo['sentences'][0]
        Return the root of the tree (word 'ROOT-0').
    """
    nameToNodes = {} # map from the original string to the node
    computeEdges(r,nameToNodes)
    computeTags(r,nameToNodes)
    initText(nameToNodes['ROOT-0'],r['text'].replace('"','\\\"'))
    mergeQuotations(nameToNodes['ROOT-0'],r,nameToNodes)
    return nameToNodes['ROOT-0']

def mergeNamedEntityTagChildParent(t):
    """
        Merge all nodes n1,n2 such that:
            * n1 is parent of n2
            * n1 and n2 have a same namedEntityTag
    """
    for c in t.child:
        mergeNamedEntityTagChildParent(c)
    sameTagChild = set()
    if t.namedEntityTag != 'undef':
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
        if c.namedEntityTag != 'undef':
            try:
                tagToNodes[c.namedEntityTag+c.dependency].add(c)
            except KeyError:
                tagToNodes[c.namedEntityTag+c.dependency] = set([c])
    for sameTag in tagToNodes.values():
        x = sameTag.pop()
        for other in sameTag:
            x.merge(other,True)

import sys


class DependenciesTree:
    """
        One node of the parse tree.
        It is a group of words of same NamedEntityTag (e.g. George Washington).
    """
    def __init__(self, word, namedentitytag='undef', dependency='undef', child=None):
        self.wordList = [(word[:word.rindex('-')],int(word[word.rindex('-')+1:]))]
        self.namedEntityTag = namedentitytag
        self.dependency = dependency
        self.child = child or []
        self.text = "" # whole sentence
        self.parent=None

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
            s+=n.string()+'\n'
        return s

    def __str__(self):
        return "digraph relations {"+"\n{0}\tlabelloc=\"t\"\tlabel=\"{1}\";\n".format(self.string(),self.text)+"}\n"

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

def mergeDependencies(t,dep):
    """
        Merge all nodes which have a dependency in dep.
        Do not keep their list of words.
    """
    for c in t.child:
        mergeDependencies(c,dep)
    for c in t.child:
      if c.dependency in dep:
        t.merge(c,False)

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

def simplify(t):
    mergeDependencies(t,{'det'})
    mergeNamedEntityTagChildParent(t)
    mergeNamedEntityTagSisterBrother(t)

# The following maps all dependencies to their direct more general dependency.
# Taken from StanfordDependenciesManual.pdf
dependenciesMap = {
    'root'      : 'root',
    'dep'       : 'dep',
        'aux'       : 'dep',
            'auxpass'   : 'aux',
            'cop'       : 'aux',
        'arg'       : 'dep',
            'agent'     : 'arg',
            'comp'      : 'arg',
                'acomp'     : 'comp',
                'ccomp'     : 'comp',
                'xcomp'     : 'comp',
                'obj'       : 'comp',
                    'dobj'      : 'obj',
                    'iobj'      : 'obj',
                    'pobj'      : 'obj',
            'subj'      : 'arg',
                'nsubj'     : 'subj',
                'csubj'     : 'subj',
        'cc'        : 'dep',
        'conj'      : 'dep',
        'expl'      : 'dep',
        'mod'       : 'dep',
            'amod'      : 'mod',
            'appos'     : 'mod',
            'advcl'     : 'mod',
            'det'       : 'mod',
            'predet'    : 'mod',
            'preconj'   : 'mod',
            'vmod'      : 'mod',
            'mwe'       : 'mod',
                'mark'      : 'mwe',
            'advmod'    : 'mod',
                'neg'       : 'advmod',
            'rcmod'     : 'mod',
            'quantmod'  : 'mod',
            'nn'        : 'mod',
            'npadvmod'  : 'mod',
                'tmod'      : 'npadvmod',
            'num'       : 'mod',
            'number'    : 'mod',
            'prep'      : 'mod',
            'poss'      : 'mod',
            'possessive': 'mod',
            'prt'       : 'mod',
        'parataxis' : 'dep',
        'punct'     : 'dep',
        'ref'       : 'dep',
        'sdep'      : 'dep',
            'xsubj'     : 'sdep'
}

allowed = { 'undef', 'root', 'dep', 'aux', 'agent', 'comp', 'subj', 'cc', 'conj',
'expl', 'mod', 'prep_of', 'prep_in' }

def collapseDependency(dep,depMap,allowedDep):
    """
        Return the first dependency in allowedDep which is a result of the 
        application of depMap on dep.
        Pre-condition: this first dependency exists.
    """
    if dep in allowedDep:
        return dep
    return collapseDependency(depMap[dep],depMap,allowedDep)
    
def collapseAllDependencies(t,depMap=dependenciesMap,allowedDep=allowed):
    """
        Apply collapseDependency on all nodes of the tree t.
    """
    t.dependency = collapseDependency(t.dependency,depMap,allowedDep)
    for c in t.child:
        collapseAllDependencies(c,depMap,allowedDep)

##################################################################

def removeWord(t,word):
    """
        Remove word (of type str*int = word*position_in_sentence) in t
        Assume word has no child
    """
    if word in t.wordList:
        if not t.child:
            t.parent.child.remove(t) 
        else:
            sys.stderr.write('exit: question word has child (please, report your sentence)\n')
            sys.exit() 
    else:
        for c in t.child:
            removeWord(c,word)
  
def remove(t):
    t.parent.child.remove(t)

def impossible(t):
    sys.stderr.write('exit: %s dependency is possible (please, report your sentence)\n' % t)
    sys.exit() 
    #remove(t)

def ignore(t):
    remove(t)

def merge(t):
    t.parent.merge(t,True)
       
dependenciesMap2 = {
    'undef'     : 'undef',
    'root'      : 'root',
    'dep'       : 'dep',
        'aux'       : remove,
            'auxpass'   : remove,
            'cop'       : impossible,
        'arg'       : impossible,
            'agent'     : 'agent',
            'comp'      : 'comp',
                'acomp'     : 'comp',
                'ccomp'     : 'comp',
                'xcomp'     : 'comp',
                'pcomp'     : 'comp',
                'obj'       : impossible,
                    'dobj'      : 'comp',
                    'iobj'      : impossible,
                    'pobj'      : 'comp',
            'subj'      : 'subj',
                'nsubj'     : 'subj',
                    'nsubjpass'    : 'nsubjpass',
                'csubj'     : impossible,
                    'csubjpass'    : impossible,
        'cc'        : ignore,
        'conj'      : 'conj',
        'expl'      : ignore,
        'mod'       : 'mod',
            'amod'      : 'mod',
            'appos'     : 'mod',
            'advcl'     : 'mod',
            'det'       : remove,
            'predet'    : ignore,
            'preconj'   : ignore,
            'vmod'      : 'mod',
            'mwe'       : merge,
                'mark'      : ignore,
            'advmod'    : merge,
                'neg'       : 'neg',
            'rcmod'     : ignore,
                'quantmod'  : ignore,
            'nn'        : merge,
            'npadvmod'  : merge,
                'tmod'      : 'mod',
            'num'       : merge,
            'number'    : merge,
            'prep'      : 'prep',
            'prepc'     : 'prep',
            'poss'      : 'poss',
            'possessive': impossible,
            'prt'       : merge,
        'parataxis' : ignore,
        'punct'     : impossible,
        'ref'       : impossible,
        'sdep'      : impossible,
            'xsubj'     : 'comp',
        'goeswith'  : merge,
        'discourse' : remove
}

questionWord = [
    """
        Taken from: http://www.interopia.com/education/all-question-words-in-english/
        Rarely used: Wherefore, Whatever, Wherewith, Whither, Whence, However
    """
    # Yes/no question
    'Is', 'Are', 'Am', 'Was', 'Were', 'Will', 'Do', 'Does', 'Did', 'Have', 'Had', 'Has', 'Can', 'Could', 'Should', 'Shall', 'May', 'Might', 'Would',
    # Open-ended questions 
    'What', 'What kind', 'What type', 'What sort', 'What time', 'When', 'Why', 'Where', 'Who', 'How', 'How much', 'How many', 'How old', 'How far', 'How long', 'How tall', 'How deep', 'How wide', 'How fast', 'How often', 'How come', 'Which', 'Whom', 'Whose'
      # + What... for, What... like, Why don't
]

def firstWords(t,start):
    """
        Put the 2 first words of the sentence in start (list of size 2)
    """
    for n in t.wordList:
        if n[1] == 1:
            start[0] = n
        elif n[1] == 2:
            start[1] =n
    for c in t.child:
        firstWords(c,start)

def identifyQuestionWord(t):
    """
        Identify, remove and return the question word
    """
    start = [None,None]
    firstWords(t,start)   
    if start[0][0] + ' ' + start[1][0] in questionWord:
        removeWord(t,start[0])
        removeWord(t,start[1])
        return start[0][0] + ' ' + start[1][0]
    elif start[0][0] in questionWord: 
        removeWord(t,start[0])
        return start[0][0]
    else:
        sys.stderr.write('exit: question word not found (please, report your sentence)\n')

def collapseDependency2(t,depMap=dependenciesMap2):
    """
        Apply the rules of depMap to t
    """
    temp = list(t.child) # copy, t.child is changed while iterating
    for c in temp:
        collapseDependency2(c,depMap)
    try:
        if isinstance(depMap[t.dependency], str):
            t.dependency = depMap[t.dependency]
        else:
            depMap[t.dependency](t)
    except KeyError: # prep_x, prepc_x
        pass

def simplify2(t):
    s = identifyQuestionWord(t) # identify and remove question word
    sys.stderr.write('question word is: %s\n' % s)
    mergeNamedEntityTagChildParent(t) # NER merging
    mergeNamedEntityTagSisterBrother(t) # NER merging
    collapseDependency2(t) # apply dependency rules of collapsing
    

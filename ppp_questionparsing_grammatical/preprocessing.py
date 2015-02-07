import sys
from .preprocessingMerge import Word, mergeNamedEntityTag
from .data.exceptions import QuotationError
from .dependencyTreeCorrection import correctTree
from copy import deepcopy
import random
import string

class DependenciesTree:
    """
        One node of the parse tree.
        It is a group of words of the initial sentence.
    """
    def __init__(self, word, start=1000, namedEntityTag='undef', subtreeType='undef', dependency='undef', child=None, parent=None):
        self.wordList = [[Word(word,start)]]  # list of the expressions/alternatives contained into the node. Each sub-list is a list of Words
        self.namedEntityTag = namedEntityTag  # NER tag (location, ...)
        self.subtreeType = subtreeType        # type of the info represented by the subtree
        self.dependency = dependency          # dependency from self to its parent
        self.child = child or []              # children of self
        self.text = ""                        # each node contains the initial whole sentence
        self.parent = parent                  # parent of self
        self.dfsTag = 0                       # number attributed by a dfs

    def dfsAnnotate(self,n):
        """
            Build a dfs annotation on the tree
            Useful to distinguish (in printing) nodes that are different but contain the same wordList
        """
        if self.child == []:
            self.dfsTag = n
            return n+1
        else:
            for t in self.child:
                n = t.dfsAnnotate(n)
            self.dfsTag = n
            return n+1

    def sort(self):
        """
            Sorting the wordLists of the tree
        """
        for t in self.child:
            t.sort()
        self.wordList.sort()
        for alt in self.wordList:
            alt.sort(key = lambda x: x.index)

    def string(self):
        # Concatenation of the words of the root
        w = self.printWords()
        s=''
        # Adding the definition of the root (dot format)
        t=''
        if(self.namedEntityTag != 'O' and self.namedEntityTag != 'undef'):
            t+= " [{0}]".format(self.namedEntityTag)
        if self.subtreeType != 'undef':
            t+= " [$ {0}]".format(self.subtreeType)
        s+="\t\"{0}\"[label=\"{1}{2}\",shape=box];\n".format(str(self.dfsTag),w,t)
        # Adding definitions of the edges
        for n in self.child:
            s+="\t\"{0}\" -> \"{1}\"[label=\"{2}\"];\n".format(str(self.dfsTag),str(n.dfsTag),n.dependency)
        # Recursive calls
        for n in self.child:
            assert n.parent == self
            s+=n.string()
        return s

    def __str__(self):
        """
            Print dependency graph in dot format
        """
        self.dfsAnnotate(0)
        return "digraph relations {"+"\n{0}\tlabelloc=\"t\"\tlabel=\"{1}\";\n".format(self.string(),self.text)+"}"

    def merge(self,other,mergeWords):
        """
            Merge the root of the two given trees into one single node.
            Merge the two wordList if mergeWords=True (otherwise only keep the wordList of self).
            The result is stored in node 'self'.
        """
        self.child += other.child
        for c in other.child:
            c.parent = self
        if mergeWords:
            self.wordList = [w+v for w in self.wordList for v in other.wordList] # ??? is it ok ???
        if other.parent:
            other.parent.child.remove(other)
        other.wordList = None

    def getWords(self):
        """
            List of alternatives strings contained into wordList
        """
        l = []
        for alt in self.wordList:
            alt.sort(key = lambda x: x.index)
            result = alt[0].word
            for i in range(1,len(alt)):
                if alt[i].pos != 'POS':
                    result += " "
                result += alt[i].word
            l.append(result)
        return l

    def printWords(self):
        """
            Concatenation of all the alternatives strings contained into wordList, separated by |
        """
        return ' | '.join(self.getWords())

def index(l,pred):
    """
        Return the index of the first element of l which is in pred.
        Raise ValueError if there is not such an element.
    """
    for i in range(0,len(l)):
        if l[i] in pred:
            return i
    raise ValueError

class QuotationHandler:
    """
        An object to handle quotations in the sentences.
    """
    quotationList = ['“','”','"']
    def __init__(self,replacement=None):
        self.replacement = replacement
        self.replacementIndex = 0
        self.quotations = {}
        random.seed()

    def checkQuotation(self,sentence):
        """
            Check that there is an even number of quotation marks.
            Raise QuotationError otherwise.
        """
        if len([c for c in sentence if c in self.quotationList]) % 2 == 1:
            raise QuotationError(sentence,"Odd number of quotation marks.")

    def getReplacement(self,sentence):
        """
            Return a random string which does not appear in the sentence.
        """
        sep = "".join(random.sample(string.ascii_uppercase,3))
        while sep in sentence:
            sep = "".join(random.sample(string.ascii_uppercase,3))
        return sep

    def pull(self,sentence):
        """
            Remove/pull the quotations from the sentence, and replace them.
        """
        if not self.replacement:
            self.replacement = self.getReplacement(sentence)
        if self.replacementIndex == 0:
            self.checkQuotation(sentence)
        try:
            indexBegin = index(sentence,self.quotationList)
            indexEnd = indexBegin+index(sentence[indexBegin+1:],self.quotationList)+1
        except ValueError:
            return sentence
        replacement = self.replacement+str(self.replacementIndex)
        self.replacementIndex += 1
        self.quotations[replacement] = sentence[indexBegin+1:indexEnd]
        return self.pull(sentence[0:indexBegin]+replacement+sentence[indexEnd+1:])

    def push(self,tree):
        """
            Replace/push the spaces in the nodes of the tree.
        """
        for c in tree.child:
            self.push(c)
        assert len(tree.wordList) == 1
        replaced = False
        for w in tree.wordList:
            for i in range(0,len(w)):
                try:
                    w[i].word = self.quotations[w[i].word]
                    w[i].pos = 'QUOTE'
                    replaced = True
                except KeyError:
                    continue
        if replaced:
            tree.namedEntityTag = 'QUOTATION'
        for key in self.quotations.keys():
            tree.text = tree.text.replace(key,"``"+self.quotations[key]+"''")

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
            n1 = DependenciesTree(edge[1][:edge[1].rindex('-')],int(edge[1][edge[1].rindex('-')+1:]))
            nameToNodes[edge[1]] = n1
        try:
            n2 = nameToNodes[edge[2]]
        except KeyError:
            n2 = DependenciesTree(edge[2][:edge[2].rindex('-')],int(edge[2][edge[2].rindex('-')+1:]))
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
    index=0
    # Computation of the tags of the nodes
    for word in r['words']:
        index+=1
        if word[0].isalnum() or word[0] == '$' or  word[0] == '%':
            w=word[0]+'-'+str(index) # key in the nameToNodes map
            try:
                n = nameToNodes[w]
                assert len(n.wordList) == 1 and len(n.wordList[0]) == 1
                n.wordList[0][0].pos = word[1]['PartOfSpeech']
                if word[1]['NamedEntityTag'] != 'O':
                    n.namedEntityTag = word[1]['NamedEntityTag']
            except KeyError:        # this node does not exists (e.g. 'of' preposition)
                pass

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
        Take in input a piece of the result produced by StanfordNLP (if foo is this result, then r = foo['sentences'][0])
        Apply quotation and NER merging
        Return the root of the tree (word 'ROOT-0').
    """
    nameToNodes = {}                             # map from the original string to the node
    computeEdges(r,nameToNodes)
    computeTags(r,nameToNodes)
    tree = nameToNodes['ROOT-0']                 # the tree is built
    correctTree(tree, nameToNodes, r)
    initText(tree,r['text'].replace('"','\\\"'))
    mergeNamedEntityTag(tree)                    # NER merging
    return tree

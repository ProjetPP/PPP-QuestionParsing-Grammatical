import sys
import os
import string
from .dependencyTreeCorrection import correctTree

########
# Word #
########

class Word:
    """
        One word of the sentence
    """
    __slots__ = ('word', 'index', 'pos')
    def __init__(self, word, index, pos=None):
        self.word = word    # string that represents the word
        self.index = index  # position in the sentence
        self.pos = pos      # Part Of Speech tag (verb, noun, ...)

    def __str__(self):
        return "({0}, {1}, {2})".format(str(self.word), str(self.index), str(self.pos))

    def __eq__(self, other):
        return self.word == other.word and \
                self.index == other.index and \
                self.pos == other.pos

###################
# Dependency tree #
###################

class DependenciesTree:
    """
        One node of the parse tree.
        It is a group of words of the initial sentence.
    """
    __slots__ = ('wordList', 'namedEntityTag', 'subtreeType', 'dependency', 'child', 'text', 'parent', 'dfsTag')
    def __init__(self, word, start=1000, namedEntityTag='undef', subtreeType='undef', dependency='undef', child=None, parent=None):
        self.wordList = [Word(word, start)]    # list of the words contained into the node
        self.namedEntityTag = namedEntityTag  # NER tag (location, ...)
        self.subtreeType = subtreeType        # type of the info represented by the subtree
        self.dependency = dependency          # dependency from self to its parent
        self.child = child or []              # children list of self
        self.text = ""                        # each node contains the initial whole sentence
        self.parent = parent                  # parent of self
        self.dfsTag = 0                       # number attributed by a dfs

    def dfsAnnotate(self, n):
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
        self.wordList.sort(key = lambda x: x.index)

    def printWordList(self):
        """
            List of strings contained into wordList
        """
        self.wordList.sort(key = lambda x: x.index)
        return ' '.join([x.word for x in self.wordList if x.pos != 'POS']) # don't print punctiation (?, !, ...)

    def string(self):
        # Concatenation of the words of the root
        w = self.printWordList()
        s=''
        # Adding the definition of the root (dot format)
        t=''
        if(self.namedEntityTag != 'O' and self.namedEntityTag != 'undef'):
            t+= " [{0}]".format(self.namedEntityTag)
        if self.subtreeType != 'undef':
            t+= " [$ {0}]".format(self.subtreeType)
        s+="\t\"{0}\"[label=\"{1}{2}\", shape=box];\n".format(str(self.dfsTag), w, t)
        # Adding definitions of the edges
        for n in self.child:
            s+="\t\"{0}\" -> \"{1}\"[label=\"{2}\"];\n".format(str(self.dfsTag), str(n.dfsTag), n.dependency)
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
        return "digraph relations {"+"\n{0}\tlabelloc=\"t\"\tlabel=\"{1}\";\n".format(self.string(), self.text)+"}"

    def merge(self, other, mergeWords):
        """
            Merge the root of the two given trees into one single node.
            Merge the two wordList if mergeWords=True (otherwise only keep the wordList of self).
            The result is stored in node 'self'.
        """
        self.child += other.child
        for c in other.child:
            c.parent = self
        if mergeWords:
            self.wordList += other.wordList
        if other.parent:
            other.parent.child.remove(other)
        other.wordList = None

def computeEdges(r, nameToNodes):
    """
        Compute the edges of the dependence tree.
        Take in input a piece of the result produced by StanfordNLP, and the
        map from names to nodes.
    """
    for edge in r['indexeddependencies']:
        try:
            n1 = nameToNodes[edge[1]]
        except KeyError:
            t = edge[1].rsplit('-', 1)
            n1 = DependenciesTree(t[0], int(t[1]))
            nameToNodes[edge[1]] = n1
        try:
            n2 = nameToNodes[edge[2]]
        except KeyError:
            t = edge[2].rsplit('-', 1)
            n2 = DependenciesTree(t[0], int(t[1]))
            nameToNodes[edge[2]] = n2
        # n1 is the parent of n2
        n1.child.append(n2)
        n2.parent = n1
        n2.dependency = edge[0]

def computeTags(r, nameToNodes):
    """
        Compute the tags of the dependence tree nodes.
        Take in input a piece of the result produced by StanfordNLP, and the
        map from names to nodes.
    """
    index=0
    # Computation of the tags of the nodes
    for word in r['words']:
        index+=1
        if word[0].isalnum() or word[0] == '$' or word[0] == '%' or word[0][0] == '\'': # \' for 's, 're, ...
            w=word[0]+'-'+str(index) # key in the nameToNodes map
            try:
                n = nameToNodes[w]
                assert len(n.wordList) == 1
                n.wordList[0].pos = word[1]['PartOfSpeech']
                if word[1]['NamedEntityTag'] != 'O':
                    n.namedEntityTag = word[1]['NamedEntityTag']
            except KeyError:        # this node does not exists (e.g. 'of' preposition)
                pass

def initText(t, s):
    """
        Set text attribute for all nodes, with string s.
    """
    t.text = s
    for c in t.child:
        initText(c, s)

###################
# Global function #
###################

def computeTree(r):
    """
        Compute the dependence tree.
        Take in input a piece of the result produced by StanfordNLP (if foo is this result, then r = foo['sentences'][0])
        Apply quotation and NER merging
        Return the root of the tree (word 'ROOT-0').
    """
    nameToNodes = {}                             # map from the original string to the node
    computeEdges(r, nameToNodes)
    computeTags(r, nameToNodes)
    tree = nameToNodes['ROOT-0']                 # the tree is built
    correctTree(tree, nameToNodes, r)            # some obvious corrections on the tree produced by the stanford parser
    initText(tree, r['text'].replace('"', '\\\"')) # each node contains the input question
    return tree

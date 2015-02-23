import sys
import os
import string

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

    def isNoun(self):
        """
            Return True if and only if the word is a verb (according to its POS tag).
        """
        return self.pos is not None and self.pos.startswith('N')

    def isVerb(self):
        """
            Return True if and onlf if the word is a noun (according to its POS tag).
        """
        return self.pos is not None and self.pos.startswith('V')

    def append(self, other):
        """
            Append the given string at the end of the word.
        """
        self.word += " " + other

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
        self.wordList = [Word(word, start)]   # list of the words contained into the node
        self.namedEntityTag = namedEntityTag  # NER tag (location, ...)
        self.subtreeType = subtreeType        # type of the info represented by the subtree
        self.dependency = dependency          # dependency from self to its parent
        self.child = child or []              # children list of self
        self.text = ""                        # each node contains the initial whole sentence
        self.parent = parent                  # parent of self
        self.dfsTag = 0                       # number attributed by a dfs

    def isVerb(self):
        """
            Return True if and only if one word of wordList is a verb (according to its POS tag).
        """
        return any(word.isVerb() for word in self.wordList)

    def isNoun(self):
        """
            Return True if and only if one word of wordList is a noun (according to its POS tag).
        """
        return any(word.isNoun() for word in self.wordList)

    def appendWord(self, word):
        """
            Assume the wordList contains only one element.
            Append the given string at the end of the word of the wordList.
        """
        assert len(self.wordList) == 1
        self.wordList[0].append(word)

    def dfsAnnotate(self, n):
        """
            Build a dfs annotation on the tree.
            Useful to distinguish (in printing) nodes that are different but contain the same wordList.
        """
        if self.child == []:
            self.dfsTag = n
            return n+1
        else:
            for child in self.child:
                n = child.dfsAnnotate(n)
            self.dfsTag = n
            return n+1

    def initText(self, text):
        """
            Set text attribute for all nodes, with string s.
        """
        self.text = text
        for child in self.child:
            child.initText(text)

    def sort(self):
        """
            Sort the wordLists of the tree.
        """
        for child in self.child:
            child.sort()
        self.wordList.sort(key = lambda x: x.index)

    def getWords(self):
        """
            Return the string represented by wordList.
        """
        self.wordList.sort(key = lambda x: x.index)
        return ' '.join([x.word for x in self.wordList if x.pos != 'POS']) # don't print punctiation (?, !, ...)

    def string(self):
        # Concatenation of the words of the root
        w = self.getWords()
        s=''
        # Adding the definition of the root (dot format)
        t=''
        if(self.namedEntityTag != 'O' and self.namedEntityTag != 'undef'):
            t+= " [{0}]".format(self.namedEntityTag)
        if self.subtreeType != 'undef':
            t+= " [$ {0}]".format(self.subtreeType)
        s+='\t"{0}"[label="{1}{2}", shape=box];\n'.format(str(self.dfsTag), w, t)
        # Adding definitions of the edges
        for n in self.child:
            s+='\t"{0}" -> "{1}"[label="{2}"];\n'.format(str(self.dfsTag), str(n.dfsTag), n.dependency)
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
        return 'digraph relations {' + '\n{0}\tlabelloc="t"\tlabel="{1}";\n'.format(self.string(), self.text)+'}'

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

#############################
# Dependency tree generator #
#############################

class TreeGenerator:
    """
        A class to generate a dependency tree given the result of the Stanford parser.
    """
    def __init__(self, stanfordResult):
        self.stanfordResult = stanfordResult
        self.nameToNodes = {}

    def _getNode(self, nodeName):
        try:
            node = self.nameToNodes[nodeName]
        except KeyError:
            (word,index) = nodeName.rsplit('-', 1)
            node = DependenciesTree(word, int(index))
            self.nameToNodes[nodeName] = node
        return node

    def _computeEdges(self):
        """
            Compute the edges of the dependency tree.
        """
        for edge in self.stanfordResult['indexeddependencies']:
            node1 = self._getNode(edge[1])
            node2 = self._getNode(edge[2])
            # n1 is the parent of n2
            node1.child.append(node2)
            node2.parent = node1
            node2.dependency = edge[0]

    def _computeTags(self):
        """
            Compute the tags of the dependency tree nodes.
        """
        index=0
        # Computation of the tags of the nodes
        for word in self.stanfordResult['words']:
            index+=1
            if word[0].isalnum() or word[0] == '$' or word[0] == '%' or word[0][0] == '\'': # \' for 's, 're, ...
                w=word[0]+'-'+str(index) # key in the nameToNodes map
                try:
                    n = self.nameToNodes[w]
                    assert len(n.wordList) == 1
                    n.wordList[0].pos = word[1]['PartOfSpeech']
                    if word[1]['NamedEntityTag'] != 'O':
                        n.namedEntityTag = word[1]['NamedEntityTag']
                except KeyError:        # this node does not exists (e.g. 'of' preposition)
                    pass

    def _addNamedEntityTag(self, tree, words):
        """
            If a word v is between 2 words u and w that have the same NER tag,
               and v is linked to u or w by a nn relation,
            then add the tag of u and w to v
        """
        def nnDependent(n1, n2):
            return (n1.parent == n2 and n1.dependency == 'nn')\
                or (n2.parent == n1 and n2.dependency == 'nn')
        for i in range(1, len(words)-1):
            previous = self.nameToNodes[words[i-1]]
            current = self.nameToNodes[words[i]]
            next = self.nameToNodes[words[i+1]]
            if current.namedEntityTag == 'undef' and previous.namedEntityTag != 'undef' and previous.namedEntityTag == next.namedEntityTag:
                if nnDependent(previous, current) or nnDependent(next, current):
                    current.namedEntityTag = previous.namedEntityTag

    def _correctTree(self, tree):
        """
            Correct the tree returned by the Stanford Parser, according to several heuristics.
        """
        words = sorted(self.nameToNodes.keys(), key = lambda x: int(x.split('-')[-1]))
        self._addNamedEntityTag(tree, words)


    def _getTree(self):
        return self.nameToNodes['ROOT-0']

    def computeTree(self):
        """
            Generate the tree and return it.
        """
        self._computeEdges()
        self._computeTags()
        tree = self._getTree()
        self._correctTree(tree)
        return tree

###################
# Global function #
###################

def computeTree(stanfordResult):
    """
        Compute the dependence tree.
        Take in input a piece of the result produced by StanfordNLP (if foo is this result, then stanfordResult = foo['sentences'][0])
        Apply quotation and NER merging
        Return the root of the tree (word 'ROOT-0').
    """
    generator = TreeGenerator(stanfordResult)
    tree = generator.computeTree()
    tree.initText(stanfordResult['text'].replace('"', '\\"')) # each node contains the input question
    return tree

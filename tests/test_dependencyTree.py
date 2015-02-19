import json
from nltk.stem.wordnet import WordNetLemmatizer
from ppp_questionparsing_grammatical import Word, DependenciesTree, computeTree
import data

from unittest import TestCase

class DependenciesTreeTests(TestCase):

    ########
    # Word #
    ########

    def testBasicWordConstructor1(self):
        w=Word('foo',1,'bar')
        self.assertEqual(w.word,'foo')
        self.assertEqual(w.index,1)
        self.assertEqual(w.pos,'bar')
        self.assertEqual(str(w),"(foo,1,bar)")

    ###################
    # Dependency tree #
    ###################

    def testBasicTreeConstructor(self):
        n = DependenciesTree('foo',1)
        self.assertEqual(n.wordList, [Word('foo',1)])
        self.assertEqual(n.namedEntityTag, 'undef')
        self.assertEqual(n.dependency, 'undef')
        self.assertEqual(n.child, [])
        self.assertEqual(n.text,"")
        self.assertEqual(n.parent,None)
        self.assertEqual(n.subtreeType,'undef')
        self.assertEqual(n.dfsTag,0)

    ###############
    # computeTree #
    ###############

    def testStr(self):
        tree=computeTree(data.give_john_smith()['sentences'][0])
        self.maxDiff=None
        tree.sort()
        self.assertEqual(str(tree),data.give_john_smith_string())

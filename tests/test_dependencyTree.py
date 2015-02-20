import json
from nltk.stem.wordnet import WordNetLemmatizer
from ppp_questionparsing_grammatical import Word, DependenciesTree, TreeGenerator, computeTree
import data

from unittest import TestCase

class DependenciesTreeTests(TestCase):

    ########
    # Word #
    ########

    def testBasicWordConstructor1(self):
        w=Word('foo', 1, 'bar')
        self.assertEqual(w.word, 'foo')
        self.assertEqual(w.index, 1)
        self.assertEqual(w.pos, 'bar')
        self.assertEqual(str(w), "(foo, 1, bar)")

    ###################
    # Dependency tree #
    ###################

    def testBasicTreeConstructor(self):
        n = DependenciesTree('foo', 1)
        self.assertEqual(n.wordList, [Word('foo', 1)])
        self.assertEqual(n.namedEntityTag, 'undef')
        self.assertEqual(n.dependency, 'undef')
        self.assertEqual(n.child, [])
        self.assertEqual(n.text, "")
        self.assertEqual(n.parent, None)
        self.assertEqual(n.subtreeType, 'undef')
        self.assertEqual(n.dfsTag, 0)

    ###############
    # computeTree #
    ###############

    def testStr(self):
        tree=computeTree(data.give_john_smith()['sentences'][0])
        self.maxDiff=None
        tree.sort()
        self.assertEqual(str(tree), data.give_john_smith_string())

    ###############
    # correctTree #
    ###############

    def testAddNamedEntityTag1(self):
        foo1 = DependenciesTree('foo1', 1, namedEntityTag='42')
        foo2 = DependenciesTree('foo2', 3, namedEntityTag='42')
        bar = DependenciesTree('bar', 2, namedEntityTag='undef', dependency = 'nn', parent = foo1)
        generator = TreeGenerator(None)
        generator.nameToNodes = {'foo1-1' : foo1, 'bar-2' : bar, 'foo2-3' : foo2}
        generator._correctTree(foo1)
        self.assertEqual(bar.namedEntityTag, '42')

    def testAddNamedEntityTag2(self):
        foo1 = DependenciesTree('foo1', 1, namedEntityTag='42')
        foo2 = DependenciesTree('foo2', 3, namedEntityTag='42')
        bar = DependenciesTree('bar', 2, namedEntityTag='27', dependency = 'nn', parent = foo1)
        generator = TreeGenerator(None)
        generator.nameToNodes = {'foo1-1' : foo1, 'bar-2' : bar, 'foo2-3' : foo2}
        generator._correctTree(foo1)
        self.assertEqual(bar.namedEntityTag, '27')

    def testAddNamedEntityTag3(self):
        foo1 = DependenciesTree('foo1', 1, namedEntityTag='42')
        foo2 = DependenciesTree('foo2', 3, namedEntityTag='42')
        bar = DependenciesTree('bar', 2, namedEntityTag='undef', dependency = 'amod', parent = foo1)
        generator = TreeGenerator(None)
        generator.nameToNodes = {'foo1-1' : foo1, 'bar-2' : bar, 'foo2-3' : foo2}
        generator._correctTree(foo1)
        self.assertEqual(bar.namedEntityTag, 'undef')

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
        w.append('aaa')
        self.assertEqual(Word('foo aaa', 1, 'bar'), w)

    def testPOS(self):
        for pos in {'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ'}:
            w = Word('foo', 1, pos)
            self.assertTrue(w.isVerb())
            self.assertFalse(w.isNoun())
        for pos in {'NN', 'NNS', 'NNP', 'NNPS'}:
            w = Word('foo', 1, pos)
            self.assertFalse(w.isVerb())
            self.assertTrue(w.isNoun())

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
        self.assertFalse(n.isVerb())
        self.assertFalse(n.isNoun())
        n.appendWord('bar')
        self.assertEqual(str(DependenciesTree('foo bar', 1)), str(n))

    def testTreePos(self):
        n = DependenciesTree('foo', 1)
        n.wordList += [Word('eat', 2, 'VB'), Word('bar', 3)]
        self.assertTrue(n.isVerb())
        self.assertFalse(n.isNoun())
        n = DependenciesTree('foo', 1)
        n.wordList += [Word('broomstick', 2, 'NN'), Word('bar', 3)]
        self.assertFalse(n.isVerb())
        self.assertTrue(n.isNoun())


    ###############
    # computeTree #
    ###############

    def testStr1(self):
        tree=computeTree(data.give_john_smith())
        self.maxDiff=None
        tree.sort()
        self.assertEqual(str(tree), data.give_john_smith_string())

    ###############
    # Merge       #
    ###############
    def testMerge(self):
        root1 = DependenciesTree('root', 1)
        root2 = DependenciesTree('root', 2)
        node1 = DependenciesTree('n', 1, 'tag1', 'stype1', 'dep1', [DependenciesTree('childn', 1)])
        node1.parent = root1
        root1.child += [node1]
        node2 = DependenciesTree('n', 2, 'tag2', 'stype2', 'dep2', [DependenciesTree('childn', 2)])
        node2.parent = root2
        root2.child += [node2]
        node1.merge(node2, True)
        self.assertEqual(len(root2.child), 0)
        self.assertEqual(len(root1.child), 1)
        self.assertEqual(len(node1.child), 2)
        self.assertEqual(node1.wordList, [Word('n', 1), Word('n', 2)])
        self.assertEqual(node1.namedEntityTag, 'tag1')
        self.assertEqual(node1.dependency, 'dep1')
        self.assertEqual(node1.parent, root1)
        self.assertEqual(node1.subtreeType, 'stype1')
        self.assertEqual(node1.dfsTag, 0)

    ###############
    # correctTree #
    ###############

    def testAddNamedEntityTag1(self):
        foo1 = DependenciesTree('foo1', 1, namedEntityTag='42')
        foo2 = DependenciesTree('foo2', 3, namedEntityTag='42')
        bar = DependenciesTree('bar', 2, namedEntityTag='undef', dependency = 'nn', parent = foo1)
        generator = TreeGenerator(None)
        generator.nameToNodes = {('foo1',1) : foo1, ('bar',2) : bar, ('foo2', 3) : foo2}
        generator._correctTree(foo1)
        self.assertEqual(bar.namedEntityTag, '42')

    def testAddNamedEntityTag2(self):
        foo1 = DependenciesTree('foo1', 1, namedEntityTag='42')
        foo2 = DependenciesTree('foo2', 3, namedEntityTag='42')
        bar = DependenciesTree('bar', 2, namedEntityTag='27', dependency = 'nn', parent = foo1)
        generator = TreeGenerator(None)
        generator.nameToNodes = {('foo1',1) : foo1, ('bar',2) : bar, ('foo2', 3) : foo2}
        generator._correctTree(foo1)
        self.assertEqual(bar.namedEntityTag, '27')

    def testAddNamedEntityTag3(self):
        foo1 = DependenciesTree('foo1', 1, namedEntityTag='42')
        foo2 = DependenciesTree('foo2', 3, namedEntityTag='42')
        bar = DependenciesTree('bar', 2, namedEntityTag='undef', dependency = 'amod', parent = foo1)
        generator = TreeGenerator(None)
        generator.nameToNodes = {('foo1',1) : foo1, ('bar',2) : bar, ('foo2', 3) : foo2}
        generator._correctTree(foo1)
        self.assertEqual(bar.namedEntityTag, 'undef')

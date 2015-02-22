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
        tree=computeTree(data.give_john_smith()['sentences'][0])
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

    def testEntityTagMerge1(self):
        tree=computeTree(data.give_john_smith()['sentences'][0])
        tree.mergeNamedEntityTag()
        tree.sort()
        root=tree
        # Root
        self.assertEqual(root.wordList, [Word("ROOT", 0)])
        self.assertEqual(root.namedEntityTag, 'undef')
        self.assertEqual(root.dependency, 'undef')
        self.assertEqual(root.parent, None)
        self.assertEqual(len(root.child), 1)
        self.assertEqual(root.subtreeType, 'undef')
        self.assertEqual(root.dfsTag, 0)
        # Lives
        lives=root.child[0]
        self.assertEqual(lives.wordList, [Word("lives", 3, 'VBZ')])
        self.assertEqual(lives.namedEntityTag, 'undef')
        self.assertEqual(lives.dependency, 'root')
        self.assertEqual(lives.parent, tree)
        self.assertEqual(len(lives.child), 2)
        self.assertEqual(lives.subtreeType, 'undef')
        self.assertEqual(lives.dfsTag, 0)
        # John Smith
        smith=lives.child[0]
        self.assertEqual(smith.wordList, [Word("John", 1, 'NNP'), Word("Smith", 2, 'NNP')])
        self.assertEqual(smith.namedEntityTag, 'PERSON')
        self.assertEqual(smith.dependency, 'nsubj')
        self.assertEqual(smith.parent, lives)
        self.assertEqual(len(smith.child), 0)
        self.assertEqual(smith.subtreeType, 'undef')
        self.assertEqual(smith.dfsTag, 0)
        # United Kingdom
        kingdom=lives.child[1]
        self.assertEqual(kingdom.wordList, [Word("United", 6, 'NNP'), Word("Kingdom", 7, 'NNP')])
        self.assertEqual(kingdom.namedEntityTag, 'LOCATION')
        self.assertEqual(kingdom.dependency, 'prep_in')
        self.assertEqual(kingdom.parent, lives)
        self.assertEqual(len(kingdom.child), 1)
        self.assertEqual(kingdom.subtreeType, 'undef')
        self.assertEqual(kingdom.dfsTag, 0)
        # The
        the=kingdom.child[0]
        self.assertEqual(the.wordList, [Word("the", 5, 'DT')])
        self.assertEqual(the.namedEntityTag, 'undef')
        self.assertEqual(the.dependency, 'det')
        self.assertEqual(the.parent, kingdom)
        self.assertEqual(len(the.child), 0)
        self.assertEqual(the.subtreeType, 'undef')
        self.assertEqual(the.dfsTag, 0)

    def testEntityTagMerge2(self):
        tree=computeTree(data.give_obama_president_usa()['sentences'][0])
        tree.mergeNamedEntityTag()
        tree.sort()
        root=tree
        # Root
        self.assertEqual(root.wordList, [Word("ROOT", 0)])
        self.assertEqual(root.namedEntityTag, 'undef')
        self.assertEqual(root.dependency, 'undef')
        self.assertEqual(root.parent, None)
        self.assertEqual(len(root.child), 1)
        self.assertEqual(root.subtreeType, 'undef')
        self.assertEqual(root.dfsTag, 0)
        # Is
        is_=root.child[0]
        self.assertEqual(is_.wordList, [Word("is", 2, 'VBZ')])
        self.assertEqual(is_.namedEntityTag, 'undef')
        self.assertEqual(is_.dependency, 'root')
        self.assertEqual(is_.parent, tree)
        self.assertEqual(len(is_.child), 2)
        self.assertEqual(is_.subtreeType, 'undef')
        self.assertEqual(is_.dfsTag, 0)
        # Obama
        obama=is_.child[0]
        self.assertEqual(obama.wordList, [Word("Obama", 1, 'NNP')])
        self.assertEqual(obama.namedEntityTag, 'PERSON')
        self.assertEqual(obama.dependency, 'nsubj')
        self.assertEqual(obama.parent, is_)
        self.assertEqual(len(obama.child), 0)
        self.assertEqual(obama.subtreeType, 'undef')
        self.assertEqual(obama.dfsTag, 0)
        # president
        president =is_.child[1]
        self.assertEqual(president.wordList, [Word("president", 6, 'NN')])
        self.assertEqual(president.namedEntityTag, 'undef')
        self.assertEqual(president.dependency, 'xcomp')
        self.assertEqual(president.parent, is_)
        self.assertEqual(len(president.child), 2)
        self.assertEqual(president.subtreeType, 'undef')
        self.assertEqual(president.dfsTag, 0)
        # The
        the=president.child[0]
        self.assertEqual(the.wordList, [Word("the", 3, 'DT')])
        self.assertEqual(the.namedEntityTag, 'undef')
        self.assertEqual(the.dependency, 'det')
        self.assertEqual(the.parent, president)
        self.assertEqual(len(the.child), 0)
        self.assertEqual(the.subtreeType, 'undef')
        self.assertEqual(the.dfsTag, 0)
        # United States
        united=president.child[1]
        self.assertEqual(united.wordList, [Word("United", 4, 'NNP'), Word("States", 5, 'NNPS')])
        self.assertEqual(united.namedEntityTag, 'LOCATION')
        self.assertEqual(united.dependency, 'nn')
        self.assertEqual(united.parent, president)
        self.assertEqual(len(united.child), 0)
        self.assertEqual(united.subtreeType, 'undef')
        self.assertEqual(united.dfsTag, 0)

    def testStr2(self):
        tree=computeTree(data.give_john_smith()['sentences'][0])
        tree.mergeNamedEntityTag()
        tree.mergePreposition()
        self.maxDiff=None
        tree.sort()
        self.assertEqual(str(tree), data.give_john_smith_stringMerge())

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

import json
from nltk.stem.wordnet import WordNetLemmatizer
from ppp_questionparsing_grammatical import Word, DependenciesTree, computeTree, NamedEntityMerging, PrepositionMerging
import data

from unittest import TestCase

class PreprocessingMergeTests(TestCase):

    def testEntityTagMerge1(self):
        tree=computeTree(data.give_john_smith()['sentences'][0])
        NamedEntityMerging(tree).merge()
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
        NamedEntityMerging(tree).merge()
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
        NamedEntityMerging(tree).merge()
        PrepositionMerging(tree).merge()
        self.maxDiff=None
        tree.sort()
        self.assertEqual(str(tree), data.give_john_smith_stringMerge())

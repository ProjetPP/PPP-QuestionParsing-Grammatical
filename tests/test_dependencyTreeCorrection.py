import json
from nltk.stem.wordnet import WordNetLemmatizer
from ppp_questionparsing_grammatical import Word, correctTree, DependenciesTree
import data

from unittest import TestCase

class CorrectTreeTests(TestCase):

    def testAddNamedEntityTag1(self):
        foo1 = DependenciesTree('foo1', 1, namedEntityTag='42')
        foo2 = DependenciesTree('foo2', 3, namedEntityTag='42')
        bar = DependenciesTree('bar', 2, namedEntityTag='undef', dependency = 'nn', parent = foo1)
        correctTree(foo1, {'foo1-1' : foo1, 'bar-2' : bar, 'foo2-3' : foo2})
        self.assertEqual(bar.namedEntityTag, '42')

    def testAddNamedEntityTag2(self):
        foo1 = DependenciesTree('foo1', 1, namedEntityTag='42')
        foo2 = DependenciesTree('foo2', 3, namedEntityTag='42')
        bar = DependenciesTree('bar', 2, namedEntityTag='27', dependency = 'nn', parent = foo1)
        correctTree(foo1, {'foo1-1' : foo1, 'bar-2' : bar, 'foo2-3' : foo2})
        self.assertEqual(bar.namedEntityTag, '27')

    def testAddNamedEntityTag3(self):
        foo1 = DependenciesTree('foo1', 1, namedEntityTag='42')
        foo2 = DependenciesTree('foo2', 3, namedEntityTag='42')
        bar = DependenciesTree('bar', 2, namedEntityTag='undef', dependency = 'amod', parent = foo1)
        correctTree(foo1, {'foo1-1' : foo1, 'bar-2' : bar, 'foo2-3' : foo2})
        self.assertEqual(bar.namedEntityTag, 'undef')

import json

from ppp_nlp_classical import DependenciesTree

from unittest import TestCase


class DependenciesTreeTests(TestCase):

    def testBasicConstructor(self):
        n = DependenciesTree(['foo'])
        self.assertEqual(n.wordList, ['foo'])
        self.assertEqual(n.namedEntityTag, 'undef')
        self.assertEqual(n.dependency, 'undef')
        self.assertEqual(n.child, [])
        self.assertEqual(n.text,"")
        self.assertRaises(AttributeError, lambda: n.parent)

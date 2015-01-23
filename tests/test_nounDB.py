from ppp_questionparsing_grammatical import Nounificator

from unittest import TestCase

class DependenciesTreeTests(TestCase):

    def testBasicClass(self):
        n = Nounificator()
        self.assertRaises(KeyError,n.toNouns,'a')
        n.add('a','b')
        n.add('a','c')
        self.assertTrue('b' in n.toNouns('a'))
        self.assertTrue('c' in n.toNouns('a'))
        self.assertFalse('d' in n.toNouns('a'))
        self.assertRaises(KeyError,n.toNouns,'b')
        n.remove('a','b')
        self.assertFalse('b' in n.toNouns('a'))
        self.assertTrue('c' in n.toNouns('a'))
        n.remove('a','c')
        self.assertRaises(KeyError,n.toNouns,'a')

    def testPickle(self):
        n = Nounificator()
        n.add('a','b')
        n.add('a','c')
        n.add('s','t')
        n.add('x','z')
        n.save('/tmp/test.pickle')
        m = Nounificator()
        m.load('/tmp/test.pickle')
        self.assertEqual(n,m)

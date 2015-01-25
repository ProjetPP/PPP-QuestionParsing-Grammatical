from ppp_questionparsing_grammatical import Nounificator

from unittest import TestCase

class DependenciesTreeTests(TestCase):

    def testBasicClass(self):
        n = Nounificator()
        self.assertRaises(KeyError,n.toNouns,'a')
        n.add('a','b')
        n.add('a','c')
        n.addList('a','d e'.split(' '))
        self.assertEqual(str(n),'{\'a\': [\'b\', \'c\', \'d\', \'e\']}')
        self.assertTrue('b' in n.toNouns('a'))
        self.assertTrue('d' in n.toNouns('a'))
        self.assertFalse('f' in n.toNouns('a'))
        self.assertRaises(KeyError,n.toNouns,'b')
        n.remove('a','b')
        self.assertFalse('b' in n.toNouns('a'))
        self.assertTrue('c' in n.toNouns('a'))
        self.assertTrue(n.exists('a'))
        n.remove('a','c')
        n.remove('a','d')
        n.remove('a','e')        
        self.assertRaises(KeyError,n.toNouns,'a')
        n.addList('u',['r','t'])
        self.assertTrue('t' in n.toNouns('u'))
        n.removeVerb('u')
        self.assertFalse(n.exists('u'))
        m = Nounificator()
        m.add('k','l')
        n.merge(m)
        self.assertTrue('l' in n.toNouns('k'))

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

from ppp_questionparsing_grammatical import Nounificator

from unittest import TestCase

class DependenciesTreeTests(TestCase):

    def testBasicClass(self):
        n = Nounificator()
        self.assertEqual(n.toNouns('a', 0), [])
        n.add('a', 'b', 0)
        n.add('a', 'c', 1)
        n.addList('a', 'd e'.split(' '), 0)
        self.assertEqual(str(n), "a:\t->['b', 'd', 'e']\na:\t<-['c']")
        self.assertTrue('b' in n.toNouns('a', 0))
        self.assertTrue('c' in n.toNouns('a', 1))
        self.assertFalse('f' in n.toNouns('a', 1))
        self.assertEqual(n.toNouns('b', 0), [])
        n.remove('a', 'b', 0)
        self.assertFalse('b' in n.toNouns('a', 0))
        self.assertTrue('c' in n.toNouns('a', 1))
        self.assertTrue(n.exists('a'))
        n.remove('a', 'c', 1)
        n.remove('a', 'd', 0)
        n.remove('a', 'e', 0)
        self.assertEqual(n.toNouns('a', 0), [])
        n.addList('u', ['r', 't'], 1)
        self.assertTrue('t' in n.toNouns('u', 1))
        n.removeVerb('u', 1)
        self.assertFalse(n.exists('u'))
        m = Nounificator()
        m.add('k', 'l', 0)
        m.add('k', 'o', 1)
        n.merge(m)
        self.assertTrue('l' in n.toNouns('k', 0))
        self.assertTrue('o' in n.toNouns('k', 1))
        n.removeVerb('k', 0)
        self.assertFalse('l' in n.toNouns('k', 0))

    def testPickle(self):
        n = Nounificator()
        n.add('a', 'b', 0)
        n.add('a', 'c', 1)
        n.add('s', 't', 0)
        n.add('x', 'z', 1)
        n.save('/tmp/test.pickle')
        m = Nounificator()
        m.load('/tmp/test.pickle')
        self.assertEqual(n, m)

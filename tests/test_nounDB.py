from ppp_questionparsing_grammatical import Nounificator

from unittest import TestCase

class DependenciesTreeTests(TestCase):

    def testBasicClass(self):
        n = Nounificator()
        self.assertEqual(n.directNouns('a'), [])
        n.addDirect('a', 'b')
        n.addReverse('a', 'c')
        n.addListDirect('a', 'd e'.split(' '))
        self.assertEqual(str(n), "a:\t->['b', 'd', 'e']\na:\t<-['c']")
        self.assertTrue('b' in n.directNouns('a'))
        self.assertTrue('c' in n.reverseNouns('a'))
        self.assertFalse('f' in n.reverseNouns('a'))
        self.assertEqual(n.directNouns('b'), [])
        n.removeDirect('a', 'b')
        self.assertFalse('b' in n.directNouns('a'))
        self.assertTrue('c' in n.reverseNouns('a'))
        self.assertTrue(n.exists('a'))
        n.removeReverse('a', 'c')
        n.removeDirect('a', 'd')
        n.removeDirect('a', 'e')
        self.assertEqual(n.directNouns('a'), [])
        n.addListReverse('u', ['r', 't'])
        self.assertTrue('t' in n.reverseNouns('u'))
        n.removeVerbReverse('u')
        self.assertFalse(n.exists('u'))
        m = Nounificator()
        m.addDirect('k', 'l')
        m.addReverse('k', 'o')
        n.merge(m)
        self.assertTrue('l' in n.directNouns('k'))
        self.assertTrue('o' in n.reverseNouns('k'))
        n.removeVerbDirect('k')
        self.assertFalse('l' in n.directNouns('k'))

    def testPickle(self):
        n = Nounificator()
        n.addDirect('a', 'b')
        n.addReverse('a', 'c')
        n.addDirect('s', 't')
        n.addReverse('x', 'z')
        n.save('/tmp/test.pickle')
        m = Nounificator()
        m.load('/tmp/test.pickle')
        self.assertEqual(n, m)

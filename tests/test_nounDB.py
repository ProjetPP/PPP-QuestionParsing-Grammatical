from ppp_questionparsing_grammatical import Nounificator

from unittest import TestCase

class DependenciesTreeTests(TestCase):

    def testBasicClass(self):
        n = Nounificator()
        self.assertEqual(n.directNouns('a'), [])
        n.addDirect('a', 'b')
        n.addInverse('a', 'c')
        n.addListDirect('a', 'd e'.split(' '))
        self.assertEqual(str(n), "a:\t->['b', 'd', 'e']\na:\t<-['c']")
        self.assertTrue('b' in n.directNouns('a'))
        self.assertTrue('c' in n.inverseNouns('a'))
        self.assertFalse('f' in n.inverseNouns('a'))
        self.assertEqual(n.directNouns('b'), [])
        n.removeDirect('a', 'b')
        self.assertFalse('b' in n.directNouns('a'))
        self.assertTrue('c' in n.inverseNouns('a'))
        self.assertTrue(n.exists('a'))
        n.removeInverse('a', 'c')
        n.removeDirect('a', 'd')
        n.removeDirect('a', 'e')
        self.assertEqual(n.directNouns('a'), [])
        n.addListInverse('u', ['r', 't'])
        self.assertTrue('t' in n.inverseNouns('u'))
        n.removeVerbInverse('u')
        self.assertFalse(n.exists('u'))
        m = Nounificator()
        m.addDirect('k', 'l')
        m.addInverse('k', 'o')
        n.merge(m)
        self.assertTrue('l' in n.directNouns('k'))
        self.assertTrue('o' in n.inverseNouns('k'))
        n.removeVerbDirect('k')
        self.assertFalse('l' in n.directNouns('k'))

    def testLoadSave(self):
        n = Nounificator()
        n.addListDirect('a', ['b1', 'b2', 'b3'] )
        n.addInverse('a', 'c')
        n.addDirect('s', 't')
        n.addListInverse('x', ['z1', 'z2'])
        n.addInverse('s', 'e f')
        n.addInverse('r s', 'e f g')
        for ext in {'pickle', 'json', 'txt'}:
            n.save('/tmp/test.%s' % ext)
            m = Nounificator()
            m.load('/tmp/test.%s' % ext)
            self.assertEqual(n, m)

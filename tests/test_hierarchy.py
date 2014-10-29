import json

from ppp_nlp_classical import DependenciesTree, computeTree, simplify
import data

from unittest import TestCase

class HierarchyTests(TestCase):

    def testQuestion(self):
        tree=computeTree(data.give_president_of_USA()['sentences'][0])
        self.assertEqual(simplify(tree),'Who')

    def testQuestion2(self):
        tree=computeTree(data.give_how_hold()['sentences'][0])
        self.assertEqual(simplify(tree),'How old')

    def testHierarchySimplification(self):
        tree=computeTree(data.give_president_of_USA()['sentences'][0])
        simplify(tree)
        root=tree
        # Root
        self.assertEqual(root.wordList,[("ROOT",0)])
        self.assertEqual(root.namedEntityTag,'undef')
        self.assertEqual(root.dependency,'t0')
        self.assertEqual(root.parent,None)
        self.assertEqual(len(root.child),1)
        # Is
        is_=root.child[0]
        self.assertEqual(is_.wordList,[("is",2)])
        self.assertEqual(is_.namedEntityTag,'undef')
        self.assertEqual(is_.dependency,'t0')
        self.assertEqual(is_.parent,root)
        self.assertEqual(len(is_.child),1)
        # President
        president=is_.child[0]
        self.assertEqual(president.wordList,[("president",4)])
        self.assertEqual(president.namedEntityTag,'undef')
        self.assertEqual(president.dependency,'t1')
        self.assertEqual(president.parent,is_)
        self.assertEqual(len(president.child),1)
        # United States
        us=president.child[0]
        self.assertEqual(us.wordList,[("United",7),("States",8)])
        self.assertEqual(us.namedEntityTag,'LOCATION')
        self.assertEqual(us.dependency,'prep_of')
        self.assertEqual(us.parent,president)
        self.assertEqual(len(us.child),0)

    def testIgnore(self):
        tree=computeTree(data.give_how_hold()['sentences'][0])
        simplify(tree)
        root=tree
        # Root
        self.assertEqual(root.wordList,[("ROOT",0)])
        self.assertEqual(root.namedEntityTag,'undef')
        self.assertEqual(root.dependency,'t0')
        self.assertEqual(root.parent,None)
        self.assertEqual(len(root.child),1)
        # Are
        are=root.child[0]
        self.assertEqual(are.wordList,[("are",3)])
        self.assertEqual(are.namedEntityTag,'undef')
        self.assertEqual(are.dependency,'t0')
        self.assertEqual(are.parent,root)
        self.assertEqual(len(are.child),0)

    def testHierarchySimplification2(self):
        tree=computeTree(data.give_USA_president()['sentences'][0])
        simplify(tree)
        root=tree
        # Root
        self.assertEqual(root.wordList,[("ROOT",0)])
        self.assertEqual(root.namedEntityTag,'undef')
        self.assertEqual(root.dependency,'t0')
        self.assertEqual(root.parent,None)
        self.assertEqual(len(root.child),1)
        # Is
        is_=root.child[0]
        self.assertEqual(is_.wordList,[("is",2)])
        self.assertEqual(is_.namedEntityTag,'undef')
        self.assertEqual(is_.dependency,'t0')
        self.assertEqual(is_.parent,root)
        self.assertEqual(len(is_.child),1)
        # President
        president=is_.child[0]
        self.assertEqual(president.wordList,[("United",4),("States",5),("president",6)])
        self.assertEqual(president.namedEntityTag,'undef')
        self.assertEqual(president.dependency,'t1')
        self.assertEqual(president.parent,is_)
        self.assertEqual(len(president.child),0)

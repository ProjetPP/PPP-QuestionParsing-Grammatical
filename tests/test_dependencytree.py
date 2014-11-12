import json

from ppp_nlp_classical import Word, DependenciesTree, computeTree, mergeNamedEntityTagChildParent, mergeNamedEntityTagSisterBrother
import data

from unittest import TestCase

class DependenciesTreeTests(TestCase):

    def testBasicConstructor(self):
        n = DependenciesTree('foo-1')
        self.assertEqual(n.wordList, [Word('foo',1)])
        self.assertEqual(n.namedEntityTag, 'undef')
        self.assertEqual(n.dependency, 'undef')
        self.assertEqual(n.child, [])
        self.assertEqual(n.text,"")
        self.assertEqual(n.parent,None)

    def testMerge(self):
        root1 = DependenciesTree('root-1')
        root2 = DependenciesTree('root-2')
        node1 = DependenciesTree('n-1','tag1','dep1',[DependenciesTree('childn-1')])
        node1.parent = root1
        root1.child += [node1]
        node2 = DependenciesTree('n-2','tag2','dep2',[DependenciesTree('childn-2')])
        node2.parent = root2
        root2.child += [node2]
        node1.merge(node2,True)
        self.assertEqual(len(root2.child),0)
        self.assertEqual(len(root1.child),1)
        self.assertEqual(len(node1.child),2)
        self.assertEqual(node1.wordList,[Word('n',1),Word('n',2)])
        self.assertEqual(node1.namedEntityTag,'tag1')
        self.assertEqual(node1.dependency,'dep1')
        self.assertEqual(node1.parent,root1)

    def testStr(self):
        tree=computeTree(data.give_john_smith()['sentences'][0])
        self.maxDiff=None
        self.assertEqual(str(tree),data.give_john_smith_string())

    def testQuotationMerge(self):
        tree=computeTree(data.give_LSD_LIB()['sentences'][0])
        root=tree
        # Root
        self.assertEqual(root.wordList,[Word("ROOT",0)])
        self.assertEqual(root.namedEntityTag,'undef')
        self.assertEqual(root.dependency,'undef')
        self.assertEqual(root.parent,None)
        self.assertEqual(len(root.child),1)
        # Wrote
        wrote=root.child[0]
        self.assertEqual(wrote.wordList,[Word("write",2)])
        self.assertEqual(wrote.namedEntityTag,'undef')
        self.assertEqual(wrote.dependency,'root')
        self.assertEqual(wrote.parent,root)
        self.assertEqual(len(wrote.child),3)
        # Who
        who=wrote.child[0]
        self.assertEqual(who.wordList,[Word("Who",1)])
        self.assertEqual(who.namedEntityTag,'undef')
        self.assertEqual(who.dependency,'nsubj')
        self.assertEqual(who.parent,wrote)
        self.assertEqual(len(who.child),0)
        # Lucy in the Sky with Diamondss
        lucy=wrote.child[1]
        self.assertEqual(lucy.wordList,[Word("Lucy",4),Word("in",5),Word("the",6),Word("Sky",7),Word("with",8),Word("Diamonds",9)])
        self.assertEqual(lucy.namedEntityTag,'QUOTATION')
        self.assertEqual(lucy.dependency,'dobj')
        self.assertEqual(lucy.parent,wrote)
        self.assertEqual(len(lucy.child),0)
        # Let it be
        let=wrote.child[2]
        self.assertEqual(let.wordList,[Word("Let",13),Word("It",14),Word("Be",15)])
        self.assertEqual(let.namedEntityTag,'QUOTATION')
        self.assertEqual(let.dependency,'conj_and')
        self.assertEqual(let.parent,wrote)
        self.assertEqual(len(let.child),0)

    def testEntityTagMerge1(self):
        tree=computeTree(data.give_john_smith()['sentences'][0])
        root=tree
        # Root
        self.assertEqual(root.wordList,[Word("ROOT",0)])
        self.assertEqual(root.namedEntityTag,'undef')
        self.assertEqual(root.dependency,'undef')
        self.assertEqual(root.parent,None)
        self.assertEqual(len(root.child),1)
        # Lives
        lives=root.child[0]
        self.assertEqual(lives.wordList,[Word("life",3)])
        self.assertEqual(lives.namedEntityTag,'undef')
        self.assertEqual(lives.dependency,'root')
        self.assertEqual(lives.parent,tree)
        self.assertEqual(len(lives.child),2)
        # John Smith
        smith=lives.child[0]
        self.assertEqual(smith.wordList,[Word("John",1),Word("Smith",2)])
        self.assertEqual(smith.namedEntityTag,'PERSON')
        self.assertEqual(smith.dependency,'nsubj')
        self.assertEqual(smith.parent,lives)
        self.assertEqual(len(smith.child),0)
        # United Kingdom
        kingdom=lives.child[1]
        self.assertEqual(kingdom.wordList,[Word("United",6),Word("Kingdom",7)])
        self.assertEqual(kingdom.namedEntityTag,'LOCATION')
        self.assertEqual(kingdom.dependency,'prep_in')
        self.assertEqual(kingdom.parent,lives)
        self.assertEqual(len(kingdom.child),1)
        # The
        the=kingdom.child[0]
        self.assertEqual(the.wordList,[Word("the",5)])
        self.assertEqual(the.namedEntityTag,'undef')
        self.assertEqual(the.dependency,'det')
        self.assertEqual(the.parent,kingdom)
        self.assertEqual(len(the.child),0)

    def testEntityTagMerge2(self):
        tree=computeTree(data.give_obama_president_usa()['sentences'][0])
        root=tree
        # Root
        self.assertEqual(root.wordList,[Word("ROOT",0)])
        self.assertEqual(root.namedEntityTag,'undef')
        self.assertEqual(root.dependency,'undef')
        self.assertEqual(root.parent,None)
        self.assertEqual(len(root.child),1)
        # Is
        is_=root.child[0]
        self.assertEqual(is_.wordList,[Word("be",2)])
        self.assertEqual(is_.namedEntityTag,'undef')
        self.assertEqual(is_.dependency,'root')
        self.assertEqual(is_.parent,tree)
        self.assertEqual(len(is_.child),2)
        # Obama
        obama=is_.child[0]
        self.assertEqual(obama.wordList,[Word("Obama",1)])
        self.assertEqual(obama.namedEntityTag,'PERSON')
        self.assertEqual(obama.dependency,'nsubj')
        self.assertEqual(obama.parent,is_)
        self.assertEqual(len(obama.child),0)
        # president
        president =is_.child[1]
        self.assertEqual(president.wordList,[Word("president",6)])
        self.assertEqual(president.namedEntityTag,'undef')
        self.assertEqual(president.dependency,'xcomp')
        self.assertEqual(president.parent,is_)
        self.assertEqual(len(president.child),2)
        # The
        the=president.child[0]
        self.assertEqual(the.wordList,[Word("the",3)])
        self.assertEqual(the.namedEntityTag,'undef')
        self.assertEqual(the.dependency,'det')
        self.assertEqual(the.parent,president)
        self.assertEqual(len(the.child),0)
        # United States
        united=president.child[1]
        self.assertEqual(united.wordList,[Word("United",4),Word("States",5)])
        self.assertEqual(united.namedEntityTag,'LOCATION')
        self.assertEqual(united.dependency,'nn')
        self.assertEqual(united.parent,president)
        self.assertEqual(len(united.child),0)

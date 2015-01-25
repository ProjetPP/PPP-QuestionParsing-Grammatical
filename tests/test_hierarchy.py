import json

from ppp_questionparsing_grammatical import Word, DependenciesTree, computeTree, simplify
import data

from unittest import TestCase

class HierarchyTests(TestCase):

    def testQuestion(self):
        tree=computeTree(data.give_president_of_USA()['sentences'][0])
        self.assertEqual(simplify(tree),'who')

    def testQuestion2(self):
        tree=computeTree(data.give_how_old()['sentences'][0])
        self.assertEqual(simplify(tree),'how old')

    def testHierarchySimplification(self):
        tree=computeTree(data.give_president_of_USA()['sentences'][0])
        simplify(tree)
        tree.sort()
        root=tree
        # Root
        self.assertEqual(root.wordList,[[Word("ROOT",0)]])
        self.assertEqual(root.namedEntityTag,'undef')
        self.assertEqual(root.dependency,'R0')
        self.assertEqual(root.parent,None)
        self.assertEqual(len(root.child),1)
        self.assertEqual(root.subtreeType,'PERSON')
        self.assertEqual(root.dfsTag,0)
        # Is
        is_=root.child[0]
        self.assertEqual(is_.wordList,[[Word("identity",1001,None)]])
        self.assertEqual(is_.namedEntityTag,'undef')
        self.assertEqual(is_.dependency,'R0')
        self.assertEqual(is_.parent,root)
        self.assertEqual(len(is_.child),1)
        self.assertEqual(is_.subtreeType,'PERSON')
        self.assertEqual(is_.dfsTag,0)
        # President
        president=is_.child[0]
        self.assertEqual(president.wordList,[[Word("president",4,'NN')]])
        self.assertEqual(president.namedEntityTag,'undef')
        self.assertEqual(president.dependency,'R2')
        self.assertEqual(president.parent,is_)
        self.assertEqual(len(president.child),1)
        self.assertEqual(president.subtreeType,'PERSON')
        self.assertEqual(president.dfsTag,0)
        # United States
        us=president.child[0]
        self.assertEqual(us.wordList,[[Word("United",7,'NNP'),Word("States",8,'NNPS')]])
        self.assertEqual(us.namedEntityTag,'LOCATION')
        self.assertEqual(us.dependency,'R5')
        self.assertEqual(us.parent,president)
        self.assertEqual(len(us.child),0)
        self.assertEqual(us.subtreeType,'undef')
        self.assertEqual(us.dfsTag,0)
        
    def testIgnore(self):
        tree=computeTree(data.give_how_old()['sentences'][0])
        simplify(tree)
        tree.sort()
        root=tree
        # Root
        self.assertEqual(root.wordList,[[Word("ROOT",0)]])
        self.assertEqual(root.namedEntityTag,'undef')
        self.assertEqual(root.dependency,'R0')
        self.assertEqual(root.parent,None)
        self.assertEqual(len(root.child),1)
        self.assertEqual(root.subtreeType,'NUMBER')
        self.assertEqual(root.dfsTag,0)
        # Are
        are=root.child[0]
        self.assertEqual(are.wordList,[[Word("age",1001,None)]])
        self.assertEqual(are.namedEntityTag,'undef')
        self.assertEqual(are.dependency,'R0')
        self.assertEqual(are.parent,root)
        self.assertEqual(len(are.child),0)
        self.assertEqual(are.subtreeType,'NUMBER')
        self.assertEqual(are.dfsTag,0)
        
    def testHierarchySimplification2(self):
        tree=computeTree(data.give_USA_president()['sentences'][0])
        simplify(tree)
        tree.sort()
        root=tree
        # Root
        self.assertEqual(root.wordList,[[Word("ROOT",0)]])
        self.assertEqual(root.namedEntityTag,'undef')
        self.assertEqual(root.dependency,'R0')
        self.assertEqual(root.parent,None)
        self.assertEqual(len(root.child),1)
        self.assertEqual(root.subtreeType,'PERSON')
        self.assertEqual(root.dfsTag,0)
        # Is
        is_=root.child[0]
        self.assertEqual(is_.wordList,[[Word("identity",1001,None)]])
        self.assertEqual(is_.namedEntityTag,'undef')
        self.assertEqual(is_.dependency,'R0')
        self.assertEqual(is_.parent,root)
        self.assertEqual(len(is_.child),1)
        self.assertEqual(is_.subtreeType,'PERSON')
        self.assertEqual(is_.dfsTag,0)
        # President
        president=is_.child[0]
        self.assertEqual(president.wordList, [[Word("United",4,'NNP'),Word("States",5,'NNPS'),Word("president",6,'NN')]])
        self.assertEqual(president.namedEntityTag,'undef')
        self.assertEqual(president.dependency,'R5s')
        self.assertEqual(president.parent,is_)
        self.assertEqual(len(president.child),0)
        self.assertEqual(president.subtreeType,'PERSON')
        self.assertEqual(president.dfsTag,0)
        
    def testHierarchyConnectors1(self):
        tree=computeTree(data.give_opera()['sentences'][0])
        simplify(tree)
        tree.sort()
        root=tree
        # Root
        self.assertEqual(root.wordList,[[Word("ROOT",0)]])
        self.assertEqual(root.namedEntityTag,'undef')
        self.assertEqual(root.dependency,'R0')
        self.assertEqual(root.parent,None)
        self.assertEqual(len(root.child),1)
        self.assertEqual(root.subtreeType,'undef')
        self.assertEqual(root.dfsTag,0)
        # identity
        identity=root.child[0]
        self.assertEqual(identity.wordList,[[Word("definition",1001,None)]])
        self.assertEqual(identity.namedEntityTag,'undef')
        self.assertEqual(identity.dependency,'R0')
        self.assertEqual(identity.parent,root)
        self.assertEqual(len(identity.child),1)
        self.assertEqual(identity.subtreeType,'undef')
        self.assertEqual(identity.dfsTag,0)
        # and
        andw=identity.child[0]
        self.assertEqual(andw.wordList,[[Word("and",1000,None)]])
        self.assertEqual(andw.namedEntityTag,'undef')
        self.assertEqual(andw.dependency,'R2')
        self.assertEqual(andw.parent,identity)
        self.assertEqual(len(andw.child),2)
        self.assertEqual(andw.subtreeType,'undef')
        self.assertEqual(andw.dfsTag,0)
        # first1
        first1=andw.child[0]
        self.assertEqual(first1.wordList,[[Word("first",4,'JJ')]])
        self.assertEqual(first1.namedEntityTag,'ORDINAL')
        self.assertEqual(first1.dependency,'RconjT')
        self.assertEqual(first1.parent,andw)
        self.assertEqual(len(first1.child),1)
        self.assertEqual(first1.subtreeType,'undef')
        self.assertEqual(first1.dfsTag,0)
        # first2
        first2=andw.child[1]
        self.assertEqual(first2.wordList,[[Word("first",4,'JJ')]])
        self.assertEqual(first2.namedEntityTag,'ORDINAL')
        self.assertEqual(first2.dependency,'RconjB')
        self.assertEqual(first2.parent,andw)
        self.assertEqual(len(first2.child),1)
        self.assertEqual(first2.subtreeType,'undef')
        self.assertEqual(first2.dfsTag,0)
        # gilbert
        gilbert=first1.child[0]
        self.assertEqual(gilbert.wordList,[[Word("Gilbert",5,'NNP')]])
        self.assertEqual(gilbert.namedEntityTag,'PERSON')
        self.assertEqual(gilbert.dependency,'Rspl')
        self.assertEqual(gilbert.parent,first1)
        self.assertEqual(len(gilbert.child),0)
        self.assertEqual(gilbert.subtreeType,'undef')
        self.assertEqual(gilbert.dfsTag,0)
        # sullivan
        sullivan=first2.child[0]
        self.assertEqual(sullivan.wordList,[[Word("Sullivan",7,'NNP'),Word("opera",8,'NN')]])
        self.assertEqual(sullivan.namedEntityTag,'undef')
        self.assertEqual(sullivan.dependency,'Rspl')
        self.assertEqual(sullivan.parent,first2)
        self.assertEqual(len(sullivan.child),0)
        self.assertEqual(sullivan.subtreeType,'undef')
        self.assertEqual(sullivan.dfsTag,0)        

    def testHierarchyConnectors2(self):
        tree=computeTree(data.give_chief()['sentences'][0])
        simplify(tree)
        tree.sort()
        root=tree
        # Root
        self.assertEqual(root.wordList,[[Word("ROOT",0)]])
        self.assertEqual(root.namedEntityTag,'undef')
        self.assertEqual(root.dependency,'R0')
        self.assertEqual(root.parent,None)
        self.assertEqual(len(root.child),1)
        self.assertEqual(root.subtreeType,'PERSON')
        self.assertEqual(root.dfsTag,0)
        # and
        andw=root.child[0]
        self.assertEqual(andw.wordList,[[Word("and",1000,None)]])
        self.assertEqual(andw.namedEntityTag,'undef')
        self.assertEqual(andw.dependency,'R0')
        self.assertEqual(andw.parent,root)
        self.assertEqual(len(andw.child),2)
        self.assertEqual(andw.subtreeType,'PERSON')
        self.assertEqual(andw.dfsTag,0)
        # identity
        identity1=andw.child[0]
        self.assertEqual(identity1.wordList,[[Word("identity",1001,None)]])
        self.assertEqual(identity1.namedEntityTag,'undef')
        self.assertEqual(identity1.dependency,'RconjT')
        self.assertEqual(identity1.parent,andw)
        self.assertEqual(len(identity1.child),1)
        self.assertEqual(identity1.subtreeType,'PERSON')
        self.assertEqual(identity1.dfsTag,0)
        # identity
        identity2=andw.child[1]
        self.assertEqual(identity2.wordList,[[Word("identity",1001,None)]])
        self.assertEqual(identity2.namedEntityTag,'undef')
        self.assertEqual(identity2.dependency,'RconjB')
        self.assertEqual(identity2.parent,andw)
        self.assertEqual(len(identity2.child),1)
        self.assertEqual(identity2.subtreeType,'PERSON')
        self.assertEqual(identity2.dfsTag,0)
        # chief
        chief=identity1.child[0]
        self.assertEqual(chief.wordList,[[Word("chief",4,'NN')]])
        self.assertEqual(chief.namedEntityTag,'undef')
        self.assertEqual(chief.dependency,'R2')
        self.assertEqual(chief.parent,identity1)
        self.assertEqual(len(chief.child),0)
        self.assertEqual(chief.subtreeType,'PERSON')
        self.assertEqual(chief.dfsTag,0)
        # prime minister
        prime=identity2.child[0]
        self.assertEqual(prime.wordList,[[Word("prime",6,'JJ'),Word("minister",7,'NN')]])
        self.assertEqual(prime.namedEntityTag,'undef')
        self.assertEqual(prime.dependency,'R2')
        self.assertEqual(prime.parent,identity2)
        self.assertEqual(len(prime.child),0)
        self.assertEqual(prime.subtreeType,'PERSON')
        self.assertEqual(prime.dfsTag,0)        

    """
    def testYesNoQuestion(self):
        tree=computeTree(data.give_born()['sentences'][0])
        simplify(tree)
        tree.sort()
        root=tree
        # Root
        self.assertEqual(root.wordList,[[Word("ROOT",0)]])
        self.assertEqual(root.namedEntityTag,'undef')
        self.assertEqual(root.dependency,'R0')
        self.assertEqual(root.parent,None)
        self.assertEqual(len(root.child),1)
        self.assertEqual(root.subtreeType,'undef')
        self.assertEqual(root.dfsTag,0)
        # birth
        birth=root.child[0]
        self.assertEqual(birth.wordList,[[Word("birth",2,'VBN')]])
        self.assertEqual(birth.namedEntityTag,'undef')
        self.assertEqual(birth.dependency,'R0')
        self.assertEqual(birth.parent,root)
        self.assertEqual(len(birth.child),1)
        self.assertEqual(birth.subtreeType,'undef')
        self.assertEqual(birth.dfsTag,0)
        # date
        date=birth.child[0]
        self.assertEqual(date.wordList,[[Word("1900",4,'CD')]])
        self.assertEqual(date.namedEntityTag,'DATE')
        self.assertEqual(date.dependency,'R5')
        self.assertEqual(date.parent,birth)
        self.assertEqual(len(date.child),0)
        self.assertEqual(date.subtreeType,'undef')
        self.assertEqual(date.dfsTag,0)
    """

    def testNoQW(self):
        tree=computeTree(data.birth_date()['sentences'][0])
        simplify(tree)
        tree.sort()
        root=tree
        # Root
        self.assertEqual(root.wordList,[[Word("ROOT",0)]])
        self.assertEqual(root.namedEntityTag,'undef')
        self.assertEqual(root.dependency,'R0')
        self.assertEqual(root.parent,None)
        self.assertEqual(len(root.child),1)
        self.assertEqual(root.subtreeType,'undef')
        self.assertEqual(root.dfsTag,0)
        # president
        president=root.child[0]
        self.assertEqual(president.wordList,[[Word("President",1,'NNP')]])
        self.assertEqual(president.namedEntityTag,'undef')
        self.assertEqual(president.dependency,'R0')
        self.assertEqual(president.parent,root)
        self.assertEqual(len(president.child),1)
        self.assertEqual(president.subtreeType,'undef')
        self.assertEqual(president.dfsTag,0)
        # france
        france=president.child[0]
        self.assertEqual(france.wordList,[[Word("France",3,'NNP')]])
        self.assertEqual(france.namedEntityTag,'LOCATION')
        self.assertEqual(france.dependency,'R5')
        self.assertEqual(france.parent,president)
        self.assertEqual(len(france.child),0)
        self.assertEqual(france.subtreeType,'undef')
        self.assertEqual(france.dfsTag,0)
        
    def testQuestionInfo(self):
        tree=computeTree(data.birth_place()['sentences'][0])
        simplify(tree)
        tree.sort()
        root=tree
        # Root
        self.assertEqual(root.wordList,[[Word("ROOT",0)]])
        self.assertEqual(root.namedEntityTag,'undef')
        self.assertEqual(root.dependency,'R0')
        self.assertEqual(root.parent,None)
        self.assertEqual(len(root.child),1)
        self.assertEqual(root.subtreeType,'DATE')
        self.assertEqual(root.dfsTag,0)
        # birth date
        birth=root.child[0]
        self.assertEqual(birth.wordList,[[Word("birth",3,'VBN'),Word("date",1001,None)],[Word("birth",3,'VBN'),Word("time",1001,None)]])
        self.assertEqual(birth.namedEntityTag,'undef')
        self.assertEqual(birth.dependency,'R0')
        self.assertEqual(birth.parent,root)
        self.assertEqual(len(birth.child),1)
        self.assertEqual(birth.subtreeType,'DATE')
        self.assertEqual(birth.dfsTag,0)
        # obama
        obama=birth.child[0]
        self.assertEqual(obama.wordList,[[Word("Obama",4,'NNP')]])
        self.assertEqual(obama.namedEntityTag,'PERSON')
        self.assertEqual(obama.dependency,'R5')
        self.assertEqual(obama.parent,birth)
        self.assertEqual(len(obama.child),0)
        self.assertEqual(obama.subtreeType,'undef')
        self.assertEqual(obama.dfsTag,0)

    def testPassIdentity(self):
        tree=computeTree(data.mickey()['sentences'][0])
        simplify(tree)
        tree.sort()
        root=tree
        # Root
        self.assertEqual(root.wordList,[[Word("ROOT",0)]])
        self.assertEqual(root.namedEntityTag,'undef')
        self.assertEqual(root.dependency,'R0')
        self.assertEqual(root.parent,None)
        self.assertEqual(len(root.child),1)
        self.assertEqual(root.subtreeType,'DATE')
        self.assertEqual(root.dfsTag,0)
        # identity
        identity=root.child[0]
        self.assertEqual(identity.wordList,[[Word("identity",2,'VBZ')]])
        self.assertEqual(identity.namedEntityTag,'undef')
        self.assertEqual(identity.dependency,'R0')
        self.assertEqual(identity.parent,root)
        self.assertEqual(len(identity.child),1)
        self.assertEqual(identity.subtreeType,'DATE')
        self.assertEqual(identity.dfsTag,0)
        # birthday
        birthday=identity.child[0]
        self.assertEqual(birthday.wordList,[[Word("birthday",4,'NN')]])
        self.assertEqual(birthday.namedEntityTag,'undef')
        self.assertEqual(birthday.dependency,'R0')
        self.assertEqual(birthday.parent,identity)
        self.assertEqual(len(birthday.child),1)
        self.assertEqual(birthday.subtreeType,'DATE')
        self.assertEqual(birthday.dfsTag,0)
        # mickey
        mickey=birthday.child[0]
        self.assertEqual(mickey.wordList,[[Word("Mickey",6,'NNP'),Word("Mouse",7,'NNP')]])
        self.assertEqual(mickey.namedEntityTag,'PERSON')
        self.assertEqual(mickey.dependency,'R5')
        self.assertEqual(mickey.parent,birthday)
        self.assertEqual(len(mickey.child),0)
        self.assertEqual(mickey.subtreeType,'undef')
        self.assertEqual(root.dfsTag,0)

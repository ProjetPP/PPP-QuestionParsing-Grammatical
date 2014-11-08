import json

from ppp_nlp_classical import Triple, TriplesBucket, computeTree, simplify, buildBucket, DependenciesTree, tripleProduce1, tripleProduce2, tripleProduce3, tripleProduce4, tripleProduce5, tripleProduce6
import data

from unittest import TestCase

class TripleTests(TestCase):

    def testEasyTriple(self):
        triple = Triple(4,"President of","France")
        self.assertEqual(triple.subjectT,4)
        self.assertEqual(triple.predicateT,"President of")
        self.assertEqual(triple.objectT,"France")
        triple.renameUnknown(4,8)
        self.assertEqual(triple.subjectT,8)
        self.assertEqual(triple.predicateT,"President of")
        self.assertEqual(triple.objectT,"France")        
        self.assertEqual('%s' % triple,"(?8 | President of | France)") 

    def testRenaming(self):
        triple = Triple(1,2,3)
        triple.renameUnknown(1,4)
        triple.renameUnknown(2,4)
        triple.renameUnknown(3,4)
        triple.renameUnknown(4,8)
        self.assertEqual(triple.subjectT,8)
        self.assertEqual(triple.predicateT,8)
        self.assertEqual(triple.objectT,8)

    def testEasyTriplesBucket(self):
        tp = Triple(4,"President of","France")
        bt = TriplesBucket()
        bt.addTriple(tp)
        bt.renameUnknown(4,8)
        self.assertEqual('%s' % bt,"(?8 | President of | France)")
        bt.renameUnknown(8,0)
        self.assertEqual('%s' % bt,"(?? | President of | France)")

    def testTripleProduce1(self):
        (root,nodeToID,bt)=data.tripleProductionData()
        child=root.child[0]
        tripleProduce1(child,nodeToID,bt)
        self.assertEqual(len(bt.bucket),1)
        self.assertEqual(bt.bucket[0].subjectT,"child")
        self.assertEqual(bt.bucket[0].predicateT,"root")
        self.assertEqual(bt.bucket[0].objectT,0)

    def testTripleProduce1bis(self):
        (root,nodeToID,bt)=data.tripleProductionData()
        child=root.child[0]
        child.child = [DependenciesTree("leaf-2",dependency="dep",parent=child)]
        nodeToID[child.child[0]] = 2
        tripleProduce1(child,nodeToID,bt)
        self.assertEqual(len(bt.bucket),0)
        self.assertEqual(nodeToID[root],nodeToID[child])

    def testTripleProduce2(self):
        (root,nodeToID,bt)=data.tripleProductionData()
        child=root.child[0]
        tripleProduce2(child,nodeToID,bt,"foo")
        self.assertEqual(len(bt.bucket),1)
        self.assertEqual(bt.bucket[0].subjectT,0)
        self.assertEqual(bt.bucket[0].predicateT,"root foo")
        self.assertEqual(bt.bucket[0].objectT,"child")

    def testTripleProduce2bis(self):
        (root,nodeToID,bt)=data.tripleProductionData()
        child=root.child[0]
        child.child = [DependenciesTree("leaf-2",dependency="dep",parent=child)]
        nodeToID[child.child[0]] = 2
        tripleProduce2(child,nodeToID,bt)
        self.assertEqual(len(bt.bucket),1)
        self.assertEqual(bt.bucket[0].subjectT,0)
        self.assertEqual(bt.bucket[0].predicateT,"root")
        self.assertEqual(bt.bucket[0].objectT,1)

    def testTripleProduce3(self):
        (root,nodeToID,bt)=data.tripleProductionData()
        child=root.child[0]
        tripleProduce3(child,nodeToID,bt)
        self.assertEqual(len(bt.bucket),1)
        self.assertEqual(bt.bucket[0].subjectT,0)
        self.assertEqual(bt.bucket[0].predicateT,"child")
        self.assertEqual(bt.bucket[0].objectT,"root")

    def testTripleProduce3bis(self):
        (root,nodeToID,bt)=data.tripleProductionData()
        child=root.child[0]
        child.child = [DependenciesTree("leaf-2",dependency="dep",parent=child)]
        nodeToID[child.child[0]] = 2
        tripleProduce3(child,nodeToID,bt)
        self.assertEqual(len(bt.bucket),1)
        self.assertEqual(bt.bucket[0].subjectT,0)
        self.assertEqual(bt.bucket[0].predicateT,1)
        self.assertEqual(bt.bucket[0].objectT,"root")

    def testTripleProduce4(self):
        (root,nodeToID,bt)=data.tripleProductionData()
        child=root.child[0]
        tripleProduce4(child,nodeToID,bt)
        self.assertEqual(len(bt.bucket),1)
        self.assertEqual(bt.bucket[0].subjectT,"child")
        self.assertEqual(bt.bucket[0].predicateT,"root")
        self.assertEqual(bt.bucket[0].objectT,0)

    def testTripleProduce4bis(self):
        (root,nodeToID,bt)=data.tripleProductionData()
        child=root.child[0]
        child.child = [DependenciesTree("leaf-2",dependency="dep",parent=child)]
        nodeToID[child.child[0]] = 2
        tripleProduce4(child,nodeToID,bt)
        self.assertEqual(len(bt.bucket),1)
        self.assertEqual(bt.bucket[0].subjectT,1)
        self.assertEqual(bt.bucket[0].predicateT,"root")
        self.assertEqual(bt.bucket[0].objectT,0)

    def testTripleProduce5(self):
        (root,nodeToID,bt)=data.tripleProductionData()
        child=root.child[0]
        tripleProduce5(child,nodeToID,bt)
        self.assertEqual(len(bt.bucket),1)
        self.assertEqual(bt.bucket[0].subjectT,"root")
        self.assertEqual(bt.bucket[0].predicateT,"child")
        self.assertEqual(bt.bucket[0].objectT,0)

    def testTripleProduce5bis(self):
        (root,nodeToID,bt)=data.tripleProductionData()
        child=root.child[0]
        child.child = [DependenciesTree("leaf-2",dependency="dep",parent=child)]
        nodeToID[child.child[0]] = 2
        tripleProduce5(child,nodeToID,bt)
        self.assertEqual(len(bt.bucket),1)
        self.assertEqual(bt.bucket[0].subjectT,"root")
        self.assertEqual(bt.bucket[0].predicateT,1)
        self.assertEqual(bt.bucket[0].objectT,0)

    def testTripleProduce6(self):
        (root,nodeToID,bt)=data.tripleProductionData()
        child=root.child[0]
        child.child = [DependenciesTree("leaf-2",dependency="dep",parent=child)]
        tripleProduce6(child,nodeToID,bt)
        self.assertEqual(len(bt.bucket),0)

    def testBuildBucket(self):
        tree = computeTree(data.give_president_of_USA()['sentences'][0])
        qw = simplify(tree)
        tBucket = buildBucket(tree,qw)
        self.assertEqual(len(tBucket.bucket), 1)
        self.assertEqual(tBucket.bucket[0].subjectT, "United States")
        self.assertEqual(tBucket.bucket[0].predicateT, "president")
        self.assertEqual(tBucket.bucket[0].objectT, 0)
        t=tBucket.extractTriple(0)
        self.assertEqual(t.subjectT,"United States")
        self.assertEqual(t.predicateT,"president")
        self.assertEqual(t.objectT,0)
        self.assertEqual(len(tBucket.bucket), 0)
        t=tBucket.extractTriple(1)
        self.assertIsNone(t)

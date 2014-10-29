import json

from ppp_nlp_classical import Triple, TriplesBucket, computeTree, simplify, buildBucket, DependenciesTree, tripleProduce1, tripleProduce2, tripleProduce3
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

    def testTripleProduction(self):
        root = DependenciesTree("root-0")
        child = DependenciesTree("child-1",dependency="dep",parent=root)
        root.child = [child]
        nodeToID = {root:0, child:1}
        bt = TriplesBucket()
        tripleProduce1(child,nodeToID,bt)
        self.assertEqual(len(bt.bucket),1)
        self.assertEqual(bt.bucket[0].subjectT,0)
        self.assertEqual(bt.bucket[0].predicateT,"root")
        self.assertEqual(bt.bucket[0].objectT,"child")
        bt = TriplesBucket()
        tripleProduce3(child,nodeToID,bt)
        self.assertEqual(len(bt.bucket),1)
        self.assertEqual(bt.bucket[0].subjectT,0)
        self.assertEqual(bt.bucket[0].predicateT,"child")
        self.assertEqual(bt.bucket[0].objectT,"root")
        child.child = [DependenciesTree("leaf-2",dependency="dep",parent=child)]
        nodeToID[child.child[0]] = 2
        bt = TriplesBucket()
        tripleProduce2(child,nodeToID,bt)
        self.assertEqual(len(bt.bucket),1)
        self.assertEqual(bt.bucket[0].subjectT,0)
        self.assertEqual(bt.bucket[0].predicateT,"root")
        self.assertEqual(bt.bucket[0].objectT,1)

    def testBuildBucket(self):
        tree = computeTree(data.give_president_of_USA()['sentences'][0])
        qw = simplify(tree)
        tBucket = buildBucket(tree,qw)
        self.assertEqual(len(tBucket.bucket), 2)
        self.assertEqual(tBucket.bucket[0].subjectT, 1)
        self.assertEqual(tBucket.bucket[0].predicateT, "identity")
        self.assertEqual(tBucket.bucket[0].objectT, 0)
        self.assertEqual(tBucket.bucket[1].subjectT, 1)
        self.assertEqual(tBucket.bucket[1].predicateT, "president of")
        self.assertEqual(tBucket.bucket[1].objectT, "United States")

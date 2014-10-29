import json

from ppp_nlp_classical import Triple, TriplesBucket, computeTree, simplify, buildBucket
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

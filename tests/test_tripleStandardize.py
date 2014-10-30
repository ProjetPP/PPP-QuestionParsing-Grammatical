import json

from ppp_nlp_classical import Triple, TriplesBucket, computeTree, simplify, buildBucket, DependenciesTree, tripleProduce1, tripleProduce2, tripleProduce3, buildTree
from ppp_datamodel import Triple, Resource, Missing
import data

from unittest import TestCase

class StandardTripleTests(TestCase):

    def testBuildBucket(self):
        tree = computeTree(data.give_president_of_USA()['sentences'][0])
        qw = simplify(tree)
        triple = buildTree(buildBucket(tree,qw))
        self.assertIsInstance(triple,Triple)
        self.assertEqual(triple.get("predicate"),Resource("identity"))
        self.assertEqual(triple.get("object"),Missing())
        subj=triple.get("subject")
        self.assertEqual(subj.get("subject"),Missing())
        self.assertEqual(subj.get("predicate"),Resource("president of"))
        self.assertEqual(subj.get("object"),Resource("United States"))

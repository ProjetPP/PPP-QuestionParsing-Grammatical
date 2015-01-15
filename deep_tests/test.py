from unittest import TestCase
from ppp_datamodel.communication import Request
from ppp_datamodel import Triple, Resource, Missing, Intersection
from ppp_libmodule.tests import PPPTestCase

from ppp_questionparsing_grammatical import app

class RequestHandlerTest(PPPTestCase(app)):
    def getAnswer(self,sentence):
        j = {'id': '1', 'language': 'en', 'measures': {}, 'trace': [],
            'tree': {'type': 'sentence', 'value': sentence}}
        return self.request(j)

    def testBasic(self):
        answer = self.getAnswer("What is the birth date of George Washington?")
        self.assertEquals(len(answer), 1)
        self.assertIsInstance(answer[0].tree, Triple)
        t = answer[0].tree
        self.assertEqual(t.subject, Resource('George Washington'))
        self.assertIsInstance(t.predicate, Resource('birth date'))
        self.assertIsInstance(t.object, Missing)

    def testNested(self):
        answer = self.getAnswer("When was born the daughters of the wife of the president of the United States?")
        self.assertEquals(len(answer), 1)
        tree = answer[0].tree
        self.assertIsInstance(tree, Triple)
        predicate = tree.predicate
        self.assertEqual(predicate, Resource('birth date')
        self.assertIsInstance(tree.object, Missing)
        self.assertIsInstance(tree.subject, Triple)
        tree = tree.subject
        self.assertEqual(tree.predicate, Resource('daughter'))
        self.assertIsInstance(tree.object, Missing)
        self.assertIsInstance(tree.subject, Triple)
        tree = tree.subject
        self.assertEqual(tree.predicate, Resource('wife'))
        self.assertIsInstance(tree.object, Missing)
        self.assertIsInstance(tree.subject, Triple)
        tree = tree.subject
        self.assertEqual(tree.predicate, Resource('president'))
        self.assertIsInstance(tree.object, Missing)
        self.assertEqual(tree.subject, Resource('United States'))


    def testQuotationsIntersection(self):
        answer = self.getAnswer("Who wrote \"Le Petit Prince\" and \"Vol de Nuit\"?")
        self.assertEquals(len(answer), 1)
        tree = answer[0].tree
        self.assertIsInstance(tree, Intersection)
        l = tree.list
        self.assertEquals(len(l), 2, l)
        self.assertIsEqual(l[0].list[0], Triple(
                Resource('Le Petit Prince'),
                Resource('writer'),
                Missing()))
        self.assertIsInstance(l[1].list[0], Triple(
                Resource('Vol de Nuit'),
                Resource('writer'),
                Missing()))

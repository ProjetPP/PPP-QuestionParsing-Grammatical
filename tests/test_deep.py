from unittest import TestCase
from ppp_datamodel.communication import Request
from ppp_datamodel import Triple, Resource, Missing, Intersection, Exists
from ppp_libmodule.tests import PPPTestCase

from ppp_questionparsing_grammatical import app

class RequestHandlerTest(PPPTestCase(app)):
    def getAnswer(self,sentence):
        j = {'id': '1', 'language': 'en', 'measures': {}, 'trace': [],
            'tree': {'type': 'sentence', 'value': sentence}}
        return self.request(j)

    def testBasic(self):
        answer = self.getAnswer("What is the birth date of George Washington?")
        self.assertEqual(len(answer), 1)
        self.assertIsInstance(answer[0].tree, Triple)
        t = answer[0].tree
        self.assertEqual(t.subject, Resource('George Washington'))
        self.assertEqual(t.predicate, Resource('birth date'))
        self.assertIsInstance(t.object, Missing)

    def testNonSentence(self):
        answer = self.request({'id': '1', 'language': 'en', 'measures': {}, 'trace': [],
            'tree': {'type': 'resource', 'value': 'foo'}})
        self.assertEqual(len(answer), 0)

    def testQuotationError(self):
        answer = self.getAnswer("What is \"the birth\" date \"of George Washington?")
        self.assertEqual(len(answer), 0)

    def testResourceOutput(self):
        answer = self.getAnswer("Yoda")
        self.assertEqual(len(answer), 0)

    def testNested(self):
        answer = self.getAnswer("When was born the daughters of the wife of the president of the United States?")
        self.assertEqual(len(answer), 1)
        tree = answer[0].tree
        self.assertIsInstance(tree, Triple)
        predicate = tree.predicate
        self.assertIsInstance(predicate,Resource)
        self.assertTrue('birth date' in predicate.value)
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
        self.assertEqual(len(answer), 1)
        tree = answer[0].tree
        self.assertIsInstance(tree, Intersection)
        l = tree.list
        self.assertEqual(len(l), 2, l)
        self.assertIsInstance(l[0],Triple)
        self.assertIsInstance(l[1],Triple)
        self.assertTrue(l[0].subject == Resource('Le Petit Prince') or l[1].subject == Resource('Le Petit Prince'))
        self.assertTrue(l[0].subject == Resource('Vol de Nuit') or l[1].subject == Resource('Vol de Nuit'))
        self.assertIsInstance(l[0].predicate, Resource)
        self.assertIsInstance(l[1].predicate, Resource)
        self.assertTrue('writer' in l[0].predicate.value)
        self.assertTrue('writer' in l[1].predicate.value)
        self.assertIsInstance(l[0].object, Missing)
        self.assertIsInstance(l[1].object, Missing)

    def testExist(self):
        answer = self.getAnswer("Is there a capital of France?")
        self.assertEqual(len(answer), 1)
        tree = answer[0].tree
        self.assertIsInstance(tree, Exists)
        tree = tree.list
        self.assertEqual(tree,Triple(Resource('France'),Resource('capital'),Missing()))

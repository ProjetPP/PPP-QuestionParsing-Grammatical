from unittest import TestCase
from ppp_datamodel.communication import Request
from ppp_datamodel import Triple, Resource, Missing
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
        subject = answer[0].tree.subject
        self.assertIsInstance(subject, Resource)
        self.assertEquals(subject.value, 'George Washington')
        predicate = answer[0].tree.predicate
        self.assertIsInstance(predicate, Resource)
        self.assertEquals(predicate.value, 'birth date')
        object = answer[0].tree.object
        self.assertIsInstance(object, Missing)

    def testNested(self):
        answer = self.getAnswer("When was born the daughters of the wife of the president of the United States?")
        self.assertEquals(len(answer), 1)
        tree = answer[0].tree
        self.assertIsInstance(tree, Triple)
        predicate = tree.predicate
        self.assertIsInstance(predicate, Resource)
        self.assertEquals(predicate.value, 'birth date')
        object = tree.object
        self.assertIsInstance(object, Missing)
        subject = tree.subject
        self.assertIsInstance(subject, Triple)
        tree = tree.subject
        predicate = tree.predicate
        self.assertIsInstance(predicate, Resource)
        self.assertEquals(predicate.value, 'daughter')
        object = tree.object
        self.assertIsInstance(object, Missing)
        subject = tree.subject
        self.assertIsInstance(subject, Triple)
        tree = tree.subject
        predicate = tree.predicate
        self.assertIsInstance(predicate, Resource)
        self.assertEquals(predicate.value, 'wife')
        object = tree.object
        self.assertIsInstance(object, Missing)
        subject = tree.subject
        self.assertIsInstance(subject, Triple)
        tree = tree.subject
        predicate = tree.predicate
        self.assertIsInstance(predicate, Resource)
        self.assertEquals(predicate.value, 'president')
        object = tree.object
        self.assertIsInstance(object, Missing)
        subject = tree.subject
        self.assertIsInstance(subject, Resource)
        self.assertEquals(subject.value, 'United States')

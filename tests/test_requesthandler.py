from unittest import TestCase
from ppp_datamodel.communication import Request
from ppp_datamodel import Triple, Resource, Missing
from ppp_libmodule.tests import PPPTestCase

from ppp_questionparsing_grammatical import app

class RequestHandlerTest(PPPTestCase(app)):
    def testRH(self):
        j = {'id': '1', 'language': 'en', 'measures': {}, 'trace': [],
             'tree': {'type': 'sentence', 'value': 'What is the birth date of George Washington?'}}

        answer = self.request(j)

        self.assertEquals(len(answer), 1)

        self.assertTrue(isinstance(answer[0].tree, Triple))

        subject = answer[0].tree.subject
        self.assertTrue(isinstance(subject, Resource))
        self.assertEquals(subject.value, 'George Washington')

        predicate = answer[0].tree.predicate

        self.assertTrue(isinstance(predicate, Resource))
        self.assertEquals(predicate.value, 'birth date')

        object = answer[0].tree.object

        self.assertTrue(isinstance(object, Missing))

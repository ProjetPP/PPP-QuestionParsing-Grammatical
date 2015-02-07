from unittest import TestCase
from ppp_datamodel.communication import Request
from ppp_datamodel import Triple, Resource, Missing, Intersection, Exists
from ppp_libmodule.tests import PPPTestCase

from ppp_questionparsing_grammatical import app
from ppp_datamodel.utils import InclusionTestCase

import sys

import data_deep

class RequestHandlerTest(PPPTestCase(app),InclusionTestCase):
    def getAnswer(self, sentence, lenAnswer):
        assert(lenAnswer < 2)
        j = {'id': '1', 'language': 'en', 'measures': {}, 'trace': [],
            'tree': {'type': 'sentence', 'value': sentence}}
        r = self.request(j)
        self.assertEqual(len(r),lenAnswer)
        if len(r) == 0:
            return None
        else:
            return r[0].tree

    def checkQuestion(self, sentence, expectedTree):
        resultTree = self.getAnswer(sentence,1)
        self.assertIncluded(expectedTree,resultTree)

    def testNonSentence(self):
        answer = self.request({'id': '1', 'language': 'en', 'measures': {}, 'trace': [],
            'tree': {'type': 'resource', 'value': 'foo'}})
        self.assertEqual(len(answer), 0)

    def testQuotationError(self):
        self.getAnswer("What is \"the birth\" date \"of George Washington?",0)

    def testResourceOutput(self):
        self.getAnswer("Yoda",0)

    def testQuestions(self):
        for (sentence,expectedTree) in data_deep.expected.items():
            self.checkQuestion(sentence,expectedTree)
        print("Deep test: %s questions successfully checked." % len(data_deep.expected.items()), file=sys.stderr)

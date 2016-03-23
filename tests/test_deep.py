from unittest import TestCase
from ppp_datamodel.communication import Request
from ppp_datamodel import Triple, Resource, Missing, Intersection, Exists
from ppp_libmodule.tests import PPPTestCase

from ppp_questionparsing_grammatical import app
from ppp_datamodel.utils import InclusionTestCase

import sys

import data_deep

class RequestHandlerTest(PPPTestCase(app), InclusionTestCase):
    def getFrench(self, sentence, lenAnswer):
        assert(lenAnswer < 2)
        j = {'id': '1', 'language': 'fr', 'measures': {}, 'trace': [],
            'tree': {'type': 'sentence', 'value': 'Ceci est une phrase'}}
        r = self.request(j)
        self.assertEqual(len(r), [])

    def getAnswer(self, sentence, lenAnswer):
        assert(lenAnswer < 2)
        j = {'id': '1', 'language': 'en', 'measures': {}, 'trace': [],
            'tree': {'type': 'sentence', 'value': sentence}}
        r = self.request(j)
        self.assertEqual(len(r), lenAnswer, sentence)
        if len(r) == 0:
            return None
        else:
            return r[0].tree

    def checkQuestion(self, sentence, expectedTree):
        resultTree = self.getAnswer(sentence, 1)
        self.assertIncluded(expectedTree, resultTree)

    def testNonSentence(self):
        answer = self.request({'id': '1', 'language': 'en', 'measures': {}, 'trace': [],
            'tree': {'type': 'resource', 'value': 'foo'}})
        self.assertEqual(len(answer), 0)

    def testResourceOutput(self):
        self.getAnswer("Yoda", 0)

    def testQuestions(self):
        nbFailure = 0
        for (sentence, expectedTree) in data_deep.expected.items():
            try:
                self.checkQuestion(sentence, expectedTree)
            except AssertionError:
                print("[Deep test] The following question check failed: %s" % sentence, file=sys.stderr)
                nbFailure += 1
        print("[Deep test] %s question checks succeeded." % (len(data_deep.expected.items())-nbFailure), file=sys.stderr)
        if nbFailure > 0:
            print("[Deep test] %s question checks failed." % nbFailure, file=sys.stderr)
            raise AssertionError

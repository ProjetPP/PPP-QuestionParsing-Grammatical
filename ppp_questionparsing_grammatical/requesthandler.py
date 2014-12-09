"""Request handler of the module."""

import json
import jsonrpclib
import logging

from ppp_datamodel import Sentence, Resource
from ppp_datamodel.communication import TraceItem, Response
from ppp_libmodule.exceptions import ClientError

from .config import Config
from . import computeTree, simplify, normalize, QuotationHandler, QuotationError

class StanfordNLP:
    def __init__(self, url):
        self.server = jsonrpclib.Server(url)

    def parse(self, text):
        return json.loads(self.server.parse(text))
stanfordnlp = StanfordNLP(Config().corenlp_server)

class RequestHandler:
    def __init__(self, request):
        self.request = request

    def answer(self):
        if not isinstance(self.request.tree, Sentence):
            return []
        handler = QuotationHandler()
        sentence = self.request.tree.value
        try:
            nonAmbiguousSentence = handler.pull(sentence)
            result = stanfordnlp.parse(nonAmbiguousSentence)
            tree = computeTree(result['sentences'][0])
            handler.push(tree)
            qw = simplify(tree)
            tree = normalize(tree)
        except QuotationError: # no logging, the error is between the chair and the keyboard
            return []
        except Exception as e:
            logging.warning(e)
            return []
        if isinstance(tree,Resource):
            return []
        meas = {'accuracy': 0.5, 'relevance': 0.5}
        trace = self.request.trace + [TraceItem('QuestionParsing-Grammatical', tree, meas)]
        response = Response('en', tree, meas, trace)
        return [response]

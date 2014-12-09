"""Request handler of the module."""

import json
import logging
import functools
import jsonrpclib

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

def parse(sentence):
    nonAmbiguousSentence = handler.pull(sentence)
    result = stanfordnlp.parse(nonAmbiguousSentence)
    tree = computeTree(result['sentences'][0])
    handler.push(tree)
    qw = simplify(tree)
    return normalize(tree)
if Config().cache_size:
    parse = functools.lru_cache(Config().cache_size)(parse)

class RequestHandler:
    __slots__ = ('request',)
    def __init__(self, request):
        self.request = request

    def answer(self):
        if not isinstance(self.request.tree, Sentence):
            return []
        handler = QuotationHandler()
        sentence = self.request.tree.value
        try:
            tree = parse(sentence)
        except QuotationError: # no logging, the error is between the chair and the keyboard
            return []
        except KeyboardInterrupt:
            raise
        except Exception as e:
            logging.warning(e)
            return []
        if isinstance(tree,Resource):
            return []
        meas = {'accuracy': 0.5, 'relevance': 0.5}
        trace = self.request.trace + [TraceItem('QuestionParsing-Grammatical', tree, meas)]
        response = Response('en', tree, meas, trace)
        return [response]

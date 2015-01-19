"""Request handler of the module."""

import json
import random
import logging
import functools
import jsonrpclib

from ppp_datamodel import Sentence, Resource
from ppp_datamodel.communication import TraceItem, Response
from ppp_libmodule.exceptions import ClientError

from .config import Config
from . import computeTree, simplify, normalize, QuotationHandler, QuotationError

class StanfordNLP:
    def __init__(self, urls):
        self.servers = list(map(jsonrpclib.Server, urls))

    def parse(self, text):
        return json.loads(random.choice(self.servers).parse(text))
stanfordnlp = StanfordNLP(Config().corenlp_servers)

def parse(sentence):
    handler = QuotationHandler()
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

"""Request handler of the module."""

import json
import jsonrpclib

from ppp_datamodel import Sentence
from ppp_datamodel.communication import TraceItem, Response
from ppp_core.exceptions import ClientError

from .config import Config
from . import computeTree, simplify, buildTree, buildBucket

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
        result = stanfordnlp.parse(self.request.tree.value)
        tree = computeTree(result['sentences'][0])
        qw = simplify(tree)
        t = buildTree(buildBucket(tree,qw))
        m = {'accuracy': 0.5, 'relevance': 0.5}
        response = Response('en', t, m,
                            [TraceItem('NLP-Classical', t, m)])
        print(repr(response))
        return [response]

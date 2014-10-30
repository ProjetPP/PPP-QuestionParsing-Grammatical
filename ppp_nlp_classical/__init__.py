"""Natural language processing module for the PPP."""

from ppp_core import HttpRequestHandler
from .preprocessingMerge import mergeNamedEntityTagChildParent, mergeNamedEntityTagSisterBrother, mergeNamedEntityTag
from .preprocessing import DependenciesTree, computeTree
from .questionIdentify import identifyQuestionWord
from .dependencyAnalysis import simplify
from .tripleProduction import buildBucket, Triple, TriplesBucket, tripleProduce1, tripleProduce2, tripleProduce3
from .treeTranslation import buildTree

from .requesthandler import RequestHandler

def app(environ, start_response):
    """Function called by the WSGI server."""
    return HttpRequestHandler(environ, start_response, RequestHandler) \
            .dispatch()

__all__ = ['DependenciesTree','computeTree','mergeNamedEntityTagChildParent','mergeNamedEntityTagSisterBrother','mergeNamedEntityTag','simplify', 'identifyQuestionWord','buildBucket','Triple','TriplesBucket', 'tripleProduce1', 'tripleProduce2', 'tripleProduce3','buildTree']

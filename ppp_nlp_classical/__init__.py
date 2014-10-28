"""Natural language processing module for the PPP."""

from ppp_core import HttpRequestHandler
from .preprocessing import DependenciesTree, computeTree, mergeNamedEntityTagChildParent, mergeNamedEntityTagSisterBrother
from .dependencyAnalysis import simplify, identifyQuestionWord
from .tripleProduction import printTriples # HERE
#from .requesthandler import RequestHandler

def app(environ, start_response):
    """Function called by the WSGI server."""
    return HttpRequestHandler(environ, start_response, RequestHandler) \
            .dispatch()

__all__ = ['DependenciesTree','computeTree','mergeNamedEntityTagChildParent','mergeNamedEntityTagSisterBrother','simplify', 'identifyQuestionWord','printTriples'] # HERE

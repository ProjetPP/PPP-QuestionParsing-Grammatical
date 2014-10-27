"""Natural language processing module for the PPP."""

from ppp_core import HttpRequestHandler
from .preprocessing import DependenciesTree, computeTree
from .dependencyAnalysis import simplify2, identifyQuestionWord
#from .requesthandler import RequestHandler

def app(environ, start_response):
    """Function called by the WSGI server."""
    return HttpRequestHandler(environ, start_response, RequestHandler) \
            .dispatch()

__all__ = ['DependenciesTree','computeTree','simplify2', 'identifyQuestionWord']

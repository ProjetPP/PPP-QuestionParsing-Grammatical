"""Natural language processing module for the PPP."""

from ppp_core import HttpRequestHandler
from .parsetree_to_triple import DependenciesTree, computeTree, simplify
#from .requesthandler import RequestHandler

def app(environ, start_response):
    """Function called by the WSGI server."""
    return HttpRequestHandler(environ, start_response, RequestHandler) \
            .dispatch()

__all__ = ['DependenciesTree','computeTree','simplify']

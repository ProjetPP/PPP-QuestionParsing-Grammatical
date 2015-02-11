"""Natural language processing module for the PPP."""

from ppp_libmodule import HttpRequestHandler
from .preprocessingMerge import mergeNamedEntityTagChildParent, mergeNamedEntityTagSisterBrother, mergeNamedEntityTag
from .preprocessing import Word, DependenciesTree, computeTree, QuotationHandler, correctTree
from .questionWordProcessing import identifyQuestionWord
from .dependencyAnalysis import simplify
from .normalization import normalize
from .data.exceptions import QuotationError, NounificationError, GrammaticalError
from .nounDB import Nounificator

from .requesthandler import RequestHandler

def app(environ, start_response):
    """Function called by the WSGI server."""
    return HttpRequestHandler(environ, start_response, RequestHandler) \
            .dispatch()

__all__ = ['DependenciesTree','computeTree','QuotationHandler','correctTree','mergeNamedEntityTagChildParent','mergeNamedEntityTagSisterBrother','mergeNamedEntityTag','simplify', 'identifyQuestionWord','normalize','QuotationError','NounificationError','GrammaticalError','Nounificator']

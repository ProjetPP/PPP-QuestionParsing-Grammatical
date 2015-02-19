"""Natural language processing module for the PPP."""

from ppp_libmodule import HttpRequestHandler
from .dependencyTree import Word, DependenciesTree, computeTree
from .dependencyTreeCorrection import correctTree
from .preprocessingMerge import mergeNamedEntityTagChildParent, mergeNamedEntityTagSisterBrother, mergeNamedEntityTag, QuotationHandler, preprocessingMerge
from .questionWordProcessing import identifyQuestionWord, questionWordDependencyTree, questionWordNormalForm
from .dependencyAnalysis import simplify
from .normalization import normalFormProduction
from .data.exceptions import QuotationError, GrammaticalError
from .nounDB import Nounificator

from .requesthandler import RequestHandler

def app(environ, start_response):
    """Function called by the WSGI server."""
    return HttpRequestHandler(environ, start_response, RequestHandler) \
            .dispatch()

__all__ = ['DependenciesTree', 'computeTree', 'QuotationHandler', 'correctTree', 'mergeNamedEntityTagChildParent', 'mergeNamedEntityTagSisterBrother', 'mergeNamedEntityTag', 'simplify', 'identifyQuestionWord', 'QuotationError', 'GrammaticalError', 'Nounificator', 'preprocessingMerge', 'normalFormProduction']

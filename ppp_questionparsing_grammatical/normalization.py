import sys
import ppp_datamodel
from .preprocessing import DependenciesTree

def normalize(tree):
    if tree.child == []:
        return ppp_datamodel.Missing(tree.getWords())


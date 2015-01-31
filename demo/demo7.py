import os
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0,parentdir)
os.environ['PPP_QUESTIONPARSING_GRAMMATICAL_CONFIG'] = '../example_config.json'

from ppp_datamodel.communication import Request
from ppp_datamodel import Sentence, Triple, Resource, Missing, Intersection, Exists

from ppp_questionparsing_grammatical import RequestHandler

from ppp_cli.dot import print_responses

def getAnswer(sentence=None):
    if not sentence:
        sentence = input("")
    q = RequestHandler(Request(language="en",id=1,tree=Sentence(sentence)))
    return q.answer()

if __name__ == "__main__":
    print_responses(getAnswer())

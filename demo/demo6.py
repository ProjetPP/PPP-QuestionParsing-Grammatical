import json
#from jsonrpc import ServerProxy, JsonRpc20, TransportTcpIp
import jsonrpclib
import fileinput
import os
import time

parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0,parentdir)
os.environ['PPP_QUESTIONPARSING_GRAMMATICAL_CONFIG'] = '../example_config.json'
import ppp_questionparsing_grammatical

class StanfordNLP:
    def __init__(self, port_number=8080):
        self.server = jsonrpclib.Server("http://localhost:%d" % port_number)

    def parse(self, text):
        return json.loads(self.server.parse(text))

def get_answer(sentence=""):
    nlp = StanfordNLP()
    if sentence == "":
        sentence = input("")
    handler = ppp_questionparsing_grammatical.QuotationHandler()
    simplifiedSentence = handler.pull(sentence)
    result = nlp.parse(simplifiedSentence)
    tree = ppp_questionparsing_grammatical.computeTree(result['sentences'][0])
    handler.push(tree)
    ppp_questionparsing_grammatical.NamedEntityMerging(tree).merge()
    ppp_questionparsing_grammatical.PrepositionMerging(tree).merge()
    qw = ppp_questionparsing_grammatical.simplify(tree)
    t = ppp_questionparsing_grammatical.normalFormProduction(tree,qw)
    return t

if __name__ == "__main__":
    print(json.dumps(get_answer().as_dict(), indent=4))

import json
#from jsonrpc import ServerProxy, JsonRpc20, TransportTcpIp
import jsonrpclib
import fileinput
import os
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0,parentdir)
os.environ['PPP_QUESTIONPARSING_GRAMMATICAL_CONFIG'] = '../example_config.json'
import ppp_questionparsing_grammatical

class StanfordNLP:
    def __init__(self, port_number=8080):
        self.server = jsonrpclib.Server("http://localhost:%d" % port_number)

    def parse(self, text):
        return json.loads(self.server.parse(text))

def get_tree():
    nlp = StanfordNLP()
    sentence = input("")
    handler = ppp_questionparsing_grammatical.QuotationHandler()
    simplifiedSentence = handler.pull(sentence)
    result = nlp.parse(simplifiedSentence)
    tree = ppp_questionparsing_grammatical.computeTree(result['sentences'][0])
    handler.push(tree)
    tree.mergeNamedEntityTag()
    tree.mergePreposition()
    return tree

if __name__ == "__main__":
    print(get_tree())

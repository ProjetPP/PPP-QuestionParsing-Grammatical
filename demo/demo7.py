import json
#from jsonrpc import ServerProxy, JsonRpc20, TransportTcpIp
import jsonrpclib
import fileinput
import os
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0,parentdir) 
os.environ['PPP_NLP_CLASSICAL_CONFIG'] = '../example_config.json'
import ppp_questionparsing_grammatical

class StanfordNLP:
    def __init__(self, port_number=8080):
        self.server = jsonrpclib.Server("http://localhost:%d" % port_number)

    def parse(self, text):
        return json.loads(self.server.parse(text))

def get_answer():
    nlp = StanfordNLP()
    result = nlp.parse(input(""))
    tree = ppp_questionparsing_grammatical.computeTree(result['sentences'][0])
    qw = ppp_questionparsing_grammatical.simplify(tree)
    return ppp_questionparsing_grammatical.buildTree(ppp_questionparsing_grammatical.buildBucket(tree,qw))

print(json.dumps(get_answer().as_dict(), indent=4))

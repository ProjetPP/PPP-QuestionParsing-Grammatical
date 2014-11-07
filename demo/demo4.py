import json
#from jsonrpc import ServerProxy, JsonRpc20, TransportTcpIp
import jsonrpclib
import fileinput
import os
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0,parentdir)
os.environ['PPP_NLP_CLASSICAL_CONFIG'] = '../example_config.json'
import ppp_nlp_classical

class StanfordNLP:
    def __init__(self, port_number=8080):
        self.server = jsonrpclib.Server("http://localhost:%d" % port_number)

    def parse(self, text):
        return json.loads(self.server.parse(text))



def get_tree():
  nlp = StanfordNLP()
  result = nlp.parse(input(""))
  tree = ppp_nlp_classical.computeTree(result['sentences'][0])
  #ppp_nlp_classical.simplify(tree)
  return tree

print(get_tree())

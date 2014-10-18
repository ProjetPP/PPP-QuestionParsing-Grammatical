import json
#from jsonrpc import ServerProxy, JsonRpc20, TransportTcpIp
import jsonrpclib
import fileinput
import parsetree_to_triple

class StanfordNLP:
    def __init__(self, port_number=8080):
        self.server = jsonrpclib.Server("http://localhost:%d" % port_number)

    def parse(self, text):
        return json.loads(self.server.parse(text))



def get_tree():
  nlp = StanfordNLP()
  result = nlp.parse(input(""))
  return parsetree_to_triple.compute_tree(result['sentences'][0])
  
print(get_tree())

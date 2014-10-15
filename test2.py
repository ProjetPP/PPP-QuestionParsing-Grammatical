import json
#from jsonrpc import ServerProxy, JsonRpc20, TransportTcpIp
import jsonrpclib

class StanfordNLP:
    def __init__(self, port_number=8080):
        self.server = jsonrpclib.Server("http://localhost:%d" % port_number)

    def parse(self, text):
        return json.loads(self.server.parse(text))

nlp = StanfordNLP()

while(True):
  line=input("")
  result = nlp.parse(line)
  print(result['sentences'][0]['dependencies'])

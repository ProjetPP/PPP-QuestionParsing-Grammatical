import json
#from jsonrpc import ServerProxy, JsonRpc20, TransportTcpIp
import requests

class StanfordNLP:
    def __init__(self, port_number=9000):
        self.server = "http://localhost:%d" % port_number

    def parse(self, text):
        r = requests.post(self.server, params={'properties' : '{"annotators": "tokenize,ssplit,pos,lemma,ner,parse", "outputFormat": "json", "parse.flags": " -makeCopulaHead"}'}, data=text)
        result = r.json()['sentences'][0]
        result['text'] = text
        return result

nlp = StanfordNLP()

if __name__ == "__main__":
    while(True):
        line=input("")
        result = nlp.parse(line)
        print(result)

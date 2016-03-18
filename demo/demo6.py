import json
#from jsonrpc import ServerProxy, JsonRpc20, TransportTcpIp
import requests
import fileinput
import os
import time

parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0,parentdir)
os.environ['PPP_QUESTIONPARSING_GRAMMATICAL_CONFIG'] = '../example_config.json'
import ppp_questionparsing_grammatical

class StanfordNLP:
    def __init__(self, port_number=9000):
        self.server = "http://localhost:%d" % port_number

    def parse(self, text):
        r = requests.post(self.server, params={'properties' : '{"annotators": "tokenize,ssplit,pos,lemma,ner,parse", "outputFormat": "json", "parse.flags": " -makeCopulaHead"}'}, data=text)
        result = r.json()['sentences'][0]
        result['text'] = text
        return result

def get_answer(sentence=""):
    nlp = StanfordNLP()
    if sentence == "":
        sentence = input("")
    handler = ppp_questionparsing_grammatical.QuotationHandler()
    simplifiedSentence = handler.pull(sentence)
    result = nlp.parse(simplifiedSentence)
    tree = ppp_questionparsing_grammatical.computeTree(result)
    handler.push(tree)
    ppp_questionparsing_grammatical.NamedEntityMerging(tree).merge()
    qw = ppp_questionparsing_grammatical.simplify(tree)
    t = ppp_questionparsing_grammatical.normalFormProduction(tree,qw)
    return t

if __name__ == "__main__":
    print(json.dumps(get_answer().as_dict(), indent=4))

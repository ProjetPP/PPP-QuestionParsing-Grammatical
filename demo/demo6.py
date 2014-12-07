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

def get_answer(s=""):
    time_start = time.perf_counter()
    nlp = StanfordNLP()
    if s == "":
        s = input("")
    result = nlp.parse(s)
    time_stanford = time.perf_counter()
    tree = ppp_questionparsing_grammatical.computeTree(result['sentences'][0])
    time_computeTree = time.perf_counter()
    qw = ppp_questionparsing_grammatical.simplify(tree)
    time_simplify = time.perf_counter()
    t = ppp_questionparsing_grammatical.normalize(tree)
    time_normalize = time.perf_counter()
    print("Stanford:\t"+str(time_stanford - time_start))
    print("ComputeTree:\t"+str(time_computeTree - time_stanford))
    print("Simplify:\t"+str(time_simplify - time_computeTree))
    print("Normalize:\t"+str(time_normalize - time_simplify))
    return t

if __name__ == "__main__":
    print(json.dumps(get_answer().as_dict(), indent=4))

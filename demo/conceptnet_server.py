#!/usr/bin/env python3

import requests
import sys
import difflib # string similarity
import json
import jsonrpclib
import fileinput
import os
import time
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0,parentdir) 
os.environ['PPP_QUESTIONPARSING_GRAMMATICAL_CONFIG'] = '../example_config.json'
import ppp_questionparsing_grammatical

from conceptnet5.nodes import normalized_concept_name, uri_to_lemmas
from conceptnet5.query import lookup
# https://github.com/commonsense/conceptnet5/blob/master/conceptnet5/nodes.py
# https://github.com/commonsense/conceptnet5/wiki/API

# How to test in a terminal : 
#   python3
#   from conceptnet_local import *
#   normalize('en','elected')

# Run `./conceptnet_local.py elected` to obtain words nounified from elected

default_language = 'en'

class clock:
    def __init__(self):
        self.tic = time.time()
    def time_step(self,s):
        toc = time.time()
        print("%s: %ss" % (s,str(toc-self.tic)))
        self.tic=toc

CLOCK = None

class StanfordNLP:
    def __init__(self, port_number=8080):
        self.server = jsonrpclib.Server("http://localhost:%d" % port_number)

    def parse(self, text):
        return json.loads(self.server.parse(text))

class candidate:
    """
        A candidate is an entity that is candidate to nounified the input verb
    """
    def __init__(self, fullUri, relation, pattern, weight):
        self.fullUri = fullUri    # full uri of the word
        self.shortUri = ''        # short uri, we remove the optionnal info of the URI (pos tag + phrase distinguishing, see https://github.com/commonsense/conceptnet5/wiki/URI-hierarchy#concept-uris)
        self.word = ''            # candidate word to nounified pattern
        self.relation = relation  # relation of the involved edge
        self.tag = 0              # 0 : unknown, -1 : word is not a candidate, 1 : strong candidate
        self.pattern = pattern    # word to be nounified
        self.similarity = 0       # similarity between word and pattern
        self.weight = weight      # weight of the edge
        self.score = 0       longer     # global score of the candidate, 0<..<1, the greater the better

    def extractShortUri(self):
        """
            compute shortUri
        """
        if self.fullUri.count('/') == 3: # no optional info in the uri
            self.shortUri = self.fullUri
        else:
            pos = -1
            for i in range(0,4):
                pos = self.fullUri.index('/',pos+1)
            self.shortUri = self.fullUri[:pos]    
    
    def processURI(self):
        """
            compute shortUri, word, tag
        """
        self.extractShortUri()
        if '_' in self.shortUri: # we do not consider multi words expressions as candidates
            self.tag = -1
            return
        else:
            self.word = ' '.join(uri_to_lemmas(self.shortUri))
        if self.fullUri.endswith('/n') or '/n/' in self.fullUri: ## NN pos tag
            self.tag = 1       
        if self.fullUri.count('/') == 4 and self.fullUri[-2] != '/': # no pos tag
            self.tag = -1

    def posTag(self):
        """
            compute tag with stanford parser
        """
        tic = time.time()
        if self.tag == 0:
            nlp = StanfordNLP()
            result = nlp.parse(self.word)
            tag = result['sentences'][0]['words'][0][1]['PartOfSpeech']
            if tag == 'NN':
                self.tag = 1
            else:
                self.tag = -1
        toc = time.time()
        print("\tposTag: %ss" % str(toc-tic))

    def computeScore(self):
        """
            compute similarity, score
        """
        self.similarity = difflib.SequenceMatcher(a=self.word.lower(), b=self.pattern.lower()).ratio()
        self.score = self.similarity + self.weight # need to be improved

def computeWeight(r):
    maxw = 0
    for w in r:
        maxw = max(maxw,w.weight)
    for w in r:
        w.weight = w.weight / maxw
        w.computeScore()

def buildCandidate(pattern,edge):
    uri = "/c/{0}/{1}".format(default_language,pattern)
    if (edge['start'] == uri or edge['start'].startswith(uri+'/')) and edge['end'].startswith('/c/'+default_language):
        cand = candidate(edge['end'],edge['rel'],pattern,edge['weight'])
        cand.processURI()
        cand.posTag()
        return cand
    elif (edge['end'] == uri or edge['end'].startswith(uri+'/')) and edge['start'].startswith('/c/'+default_language):
        cand = candidate(edge['start'],edge['rel'],pattern,edge['weight'])
        cand.processURI()
        cand.posTag()
        return cand
    else:
        return None

def associatedWords(pattern,relations):
    uri = "/c/{0}/{1}".format(default_language,pattern)
    r = requests.get('http://127.0.0.1:8084/data/5.3' + uri,params={'limit':100}).json()
    CLOCK.time_step("lookup")
    res = []
    for e in r['edges']:
        if e['rel'] in relations:
            cand = buildCandidate(pattern,e)
            if cand != None and cand.tag != -1:
                res.append(cand)
    CLOCK.time_step("buildCandidate")
    for cand in res:
        cand.computeScore()
    computeWeight(res)
    res.sort(key = lambda x: x.score)
    CLOCK.time_step("weights")
    return {a.word for a in res}
    #return { res[i].word for i in range(-15,0)}#size(res)-15,size(res))}
    #return {cand.word for cand in res} # duplicate, set instead
    #return sorted(nodeNN,key = functools.partial(similarity,word))

if __name__ == "__main__":
    nlp = StanfordNLP()
    if len(sys.argv) != 2:
        sys.exit("Syntax: ./%s <word to search>" % sys.argv[0])
    CLOCK = clock()
    word=normalized_concept_name(default_language,sys.argv[1]) # Lemmatization+stemming
    CLOCK.time_step("lemmatization")
    print(associatedWords(word,{'/r/RelatedTo','/r/DerivedFrom','/r/CapableOf','/r/Synonym'}))

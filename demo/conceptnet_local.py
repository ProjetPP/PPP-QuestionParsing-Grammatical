#!/usr/bin/env python3

import requests
import sys
import difflib # string similarity
import functools # partial function application

import json
import jsonrpclib
import fileinput
import os
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
#   from conceptnet2 import *
#   associatedWords('elected','/r/RelatedTo')
#   normalize('elected')

# Run `./conceptnet_local.py banana` to search words related to banana.

default_language = 'en'

class StanfordNLP:
    def __init__(self, port_number=8080):
        self.server = jsonrpclib.Server("http://localhost:%d" % port_number)

    def parse(self, text):
        return json.loads(self.server.parse(text))

class candidate:
    def __init__(self, fullUri, relation, pattern, weight):
        self.fullUri = fullUri    # full uri of the word
        self.shortUri = ''        # short uri, we remove the optionnal info of the URI (pos tag + phrase distinguishing, see https://github.com/commonsense/conceptnet5/wiki/URI-hierarchy#concept-uris)
        self.word = ''            # candidate word to nounified pattern
        self.relation = relation  # relation of the involved edge
        self.tag = 0              # 0 : unknown, -1 : word is not a candidate, 1 : strong candidate
        self.pattern = pattern    # word to be nounified
        self.similarity = 0       # similarity between word and pattern
        self.weight = weight      # weight of the edge
        self.score = 0            # global score of the candidate, 0<..<1, the greater the better

    def extractShortUri(self):
        """
            compute shortUri
        """
        if self.fullUri.count('/') == 3:
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
        if '_' in self.shortUri:
            self.tag = -1
            return
        else:
            self.word = ' '.join(uri_to_lemmas(self.shortUri))
        if self.fullUri.endswith('/n') or '/n/' in self.fullUri:  
            self.tag = 1       
        if self.fullUri.count('/') == 4 and self.fullUri[-2] != '/': # no pos tag
            self.tag = -1

    def posTag(self):
        """
            compute tag with stanford parser
        """
        if self.tag == 0:
            nlp = StanfordNLP()
            result = nlp.parse(self.word)
            tag = result['sentences'][0]['words'][0][1]['PartOfSpeech']
            if tag == 'NN':
                self.tag = 1
            else:
                self.tag = -1
    
    def computeScore(self):
        """
            compute similarity, score
        """
        self.similarity = difflib.SequenceMatcher(a=self.word.lower(), b=self.pattern.lower()).ratio()
        self.score = self.similarity + self.weight

def buildCandidate(word,edge):
    uri = "/c/{0}/{1}".format(default_language,word)
    if edge['start'].startswith(uri) and edge['end'].startswith('/c/'+default_language):
        cand = candidate(edge['end'],edge['rel'],word,edge['weight'])
        cand.processURI()
        cand.posTag()
        return cand
    elif edge['end'].startswith(uri) and edge['start'].startswith('/c/'+default_language):
        cand = candidate(edge['start'],edge['rel'],word,edge['weight'])
        cand.processURI()
        cand.posTag()
        return cand
    else:
        return None

def normalize(language,word):
    """
        Lemmatization+stemming
    """
    return normalized_concept_name(language, word)                                            

def associatedWords(word,relations):
    uri = "/c/{0}/{1}".format(default_language,word)
    r = list(lookup(uri,limit=100))
    #for w in r:
    #    print(w['start'] + ' ' + w['rel'] + ' ' + w['end'] + ' ' + str(w['weight']))
    res = []
    for e in r:
        cand = buildCandidate(word,e)
        if cand != None and cand.tag != -1:
            res.append(cand)
    for cand in res:
        cand.computeScore()
    return {cand.word for cand in res} # duplicate, set instead
    #return sorted(nodeNN,key = functools.partial(similarity,word))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Syntax: ./%s <word to search>" % sys.argv[0])
    word=normalize(default_language,sys.argv[1])
    print(associatedWords(word,{'/r/RelatedTo','/r/DerivedFrom','/r/CapableOf','/r/Synonym'}))

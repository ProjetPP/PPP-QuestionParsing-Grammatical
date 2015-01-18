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

# Run `./conceptnet.py banana` to search words related to banana.

default_language = 'en'

class StanfordNLP:
    def __init__(self, port_number=8080):
        self.server = jsonrpclib.Server("http://localhost:%d" % port_number)

    def parse(self, text):
        return json.loads(self.server.parse(text))

def posTag(word):
    """
        Return the POS tag of word using the stanford parser
    """
    nlp = StanfordNLP()
    result = nlp.parse(word)
    tag = result['sentences'][0]['words'][0][1]['PartOfSpeech']
    return tag

def normalize(language,word):
    """
        Lemmatization+stemming
    """
    return normalized_concept_name(language, word)

def similarity(word1,word2):
    """
        Return a similarity score between the 2 words
        The lower is the result the most similars are the 2 words
    """
    return 1-difflib.SequenceMatcher(a=word1.lower(), b=word2.lower()).ratio()

def associatedWords(uri,word,relations):
    """
        Return words related to the given word by the given relations.
    """
    r = list(lookup(uri,limit=100))
    node = [w['start'] for w in r 
                       if w['end'] == uri
                          and w['rel'] in relations 
                          and w['start'].startswith('/c/'+default_language)]
    #for w in r:
    #    if w['end'] == uri and w['rel'] in relations and w['start'].startswith('/c/'+default_language):
    #        print(w['start'] + ' ' + w['rel'] + ' ' + w['end'] + ' ' + str(w['weight']))
    node = [' '.join(uri_to_lemmas(w)) for w in node if '_' not in w]
    #for s in node:
    #    print(s + ' ' + posTag(s))
    nodeNN = [w for w in node if posTag(w) == 'NN'] # keep only the nouns
    return sorted(nodeNN,key = functools.partial(similarity,word))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Syntax: ./%s <word to search>" % sys.argv[0])
    word=normalize(default_language,sys.argv[1])
    uri = "/c/{0}/{1}".format(default_language,word)
    print(associatedWords(uri,word,{'/r/RelatedTo'}))
    #print(associatedWords(uri,{'/r/CapableOf'},{'/r/RelatedTo', '/r/Synonym', '/r/Causes', '/r/DerivedFrom'}))

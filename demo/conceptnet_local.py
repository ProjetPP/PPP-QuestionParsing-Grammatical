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
    return 1 - difflib.SequenceMatcher(a=word1.lower(), b=word2.lower()).ratio()

def extractBaseURI(uri):
    """
        Remove the optionnal info to the URI (pos tag + phrase distinguishing, see https://github.com/commonsense/conceptnet5/wiki/URI-hierarchy#concept-uris)
    """
    if uri.count('/') == 3:
        return uri
    else:
        pos = -1
        for i in range(0,4):
            pos = uri.index('/',pos+1)
        return uri[:pos]

def extractURI(uri):
    """
        remove optional info + gives a code : 
            0 = pos tag unknown
            1 = NN pos tag (according to conceptnet)
            2 = pos tag different from NN (according to conceptnet)
    """
    if uri.count('/') == 3: # no additionnal info
        return [uri,0]
    elif uri.endswith('/n') or '/n/' in uri: # pos tag NN
        return [extractBaseURI(uri),1]
    elif uri.count('/') == 4 and uri[-2] != '/': # no pos tag
        return [uri,0]
    else: # pos tag != NN
        return [extractBaseURI(uri),2]
    
def associatedWords(uri,word,relations):
    """
        Return words related to the given word such that:
            - pos tag == NN (according to conceptnet or stanford parser)
            - language == english
            - single word (not an expression)
    """
    r = list(lookup(uri,limit=100))
    node1 = {extractURI(w['start'])[0] for w in r 
                                         if w['end'].startswith(uri)
                                            and w['rel'] in relations 
                                            and w['start'].startswith('/c/'+default_language)
                                            and extractURI(w['start'])[1] != 2}
    node2 = {extractURI(w['end'])[0] for w in r 
                                       if w['start'].startswith(uri)
                                         and w['rel'] in relations 
                                         and w['end'].startswith('/c/'+default_language)
                                         and extractURI(w['end'])[1] != 2}
    node = node1.union(node2)
    node = {' '.join(uri_to_lemmas(w)) for w in node if '_' not in w}
    nodeNN = [w for w in node if posTag(w) == 'NN'] # keep only the nouns
    return sorted(nodeNN,key = functools.partial(similarity,word))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Syntax: ./%s <word to search>" % sys.argv[0])
    word=normalize(default_language,sys.argv[1])
    uri = "/c/{0}/{1}".format(default_language,word)
    print(associatedWords(uri,word,{'/r/RelatedTo'}))#,'/r/DerivedFrom'}))
    #print(associatedWords(uri,{'/r/CapableOf'},{'/r/RelatedTo', '/r/Synonym', '/r/Causes', '/r/DerivedFrom'}))

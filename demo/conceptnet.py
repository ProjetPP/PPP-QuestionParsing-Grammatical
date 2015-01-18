#!/usr/bin/env python3

import requests
import sys

from conceptnet5.nodes import normalized_concept_name
# https://github.com/commonsense/conceptnet5/blob/master/conceptnet5/nodes.py
# https://github.com/commonsense/conceptnet5/wiki/API

# How to test in a terminal : 
#   python3
#   from conceptnet2 import *
#   associatedWords('elected','/r/RelatedTo')
#   normalize('elected')

# Run `./conceptnet.py banana` to search words related to banana.

api='http://conceptnet5.media.mit.edu/data/5.2/search'

def normalize(word):
    return normalized_concept_name('en', word)

def otherWord(word,edge):
    if edge['startLemmas'] == word:
        return edge['endLemmas']
    return edge['startLemmas']

def associatedWordsRelation(word,relation):
    """
        Return words related to the given word by the given relations.
    """
    r = requests.get(api,params={'surfaceText':word,'limit':20,'rel':relation}).json()
    res = r['edges']
    #r = requests.get(api,params={'uri':'/c/en/'+word,'limit':20,'rel':relation}).json()
    #res = r['edges']
    #r = requests.get(api,params={'end':'/c/en/'+word,'limit':20,'rel':relation}).json()
    #res += r['edges']
    for w in res:
        print(w['startLemmas'] + ' ' + w['endLemmas'] + ' ' + str(w['score']))
    return [otherWord(word,w) for w in res] # if w['score']/r['maxScore']>=0.5]

def associatedWords(word,relations):
    """
        Return words related to the given word by one of the given relations.
    """
    l=[]
    for r in relations:
        l.extend(associatedWordsRelation(word,r))
    return set(l)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Syntax: ./%s <word to search>" % sys.argv[0])
    print(associatedWords(normalize(sys.argv[1]),{'/r/RelatedTo'}))

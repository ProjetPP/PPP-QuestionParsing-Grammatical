#!/usr/bin/env python3

import requests
import sys

# Run `./conceptnet.py banana` to search words related to banana.

api='http://conceptnet5.media.mit.edu/data/5.2/search'

def otherWord(word,edge):
    if edge['startLemmas'] == word:
        return edge['endLemmas']
    return edge['startLemmas']

def associatedWordsRelation(word,relation):
    """
        Return words related to the given word by the given relations.
    """
    r = requests.get(api,params={'text':word,'limit':10,'rel':relation}).json()
    return [otherWord(word,w) for w in r['edges'] if w['score']/r['maxScore']>=0.5]

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
    print(associatedWords(sys.argv[1],{'/r/RelatedTo','/r/IsA','/r/causes'}))

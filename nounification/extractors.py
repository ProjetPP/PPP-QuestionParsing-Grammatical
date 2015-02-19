#!/usr/bin/env python3

import requests
import json
import pickle
import sys
from nltk.corpus import wordnet as wn

default_language = 'en'

def buildWikidataProperties():
    """
        Return the set of all Wikidata properties.
    """
    properties = set()
    maxRange=60
    for i in range(0, maxRange):
        print("%d/%d"%(i+1, maxRange))
        propertiesIDs = '|'.join(['P%d'%x for x in range(50*i+1, 50*(i+1)+1)])
        request = requests.get('http://www.wikidata.org/w/api.php', params={'action':'wbgetentities', 'sites':'itwiki', 'ids':propertiesIDs, 'format':'json'})
        j = request.json()
        if j['success'] == 0:
            continue
        for prop in j['entities'].values():
            if 'missing' in prop.keys():
                continue
            try:
                for alias in prop['aliases'][default_language]:
                    properties.add(alias['value'])
            except KeyError: # no alias
                pass
            properties.add(prop['labels'][default_language]['value'])
    return properties

def buildNouns():
    """
        Returns the set of all nouns of NLTK
    """
    return {x.name().split('.', 1)[0] for x in wn.all_synsets('n')}

def buildVerbs():
    """
        Returns the set of all verbs of NLTK
    """
    return {x.name().split(".", 1)[0] for x in wn.all_synsets("v")}

if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("Syntax: ./%s storage_file -<database description> (wiki : Wikidata properties, n : nouns, v : verbs)" % sys.argv[0]) # ex: ./extractors.py file.pkl -wiki
    data = {}
    if sys.argv[2] == '-wiki':
        data = buildWikidataProperties()
    if sys.argv[2] == '-n':
        data = buildNouns()
    if sys.argv[2] == '-v':
        data = buildVerbs()
    f = open(sys.argv[1], 'wb')
    pickle.dump(data, f)
    f.close()

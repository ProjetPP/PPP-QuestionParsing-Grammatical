#!/usr/bin/env python3

import requests
import sys
import difflib # string similarity
import time
from nltk.corpus import wordnet as wn
from conceptnet5.nodes import normalized_concept_name, uri_to_lemmas
from conceptnet5.query import lookup
# https://github.com/commonsense/conceptnet5/blob/master/conceptnet5/nodes.py
# https://github.com/commonsense/conceptnet5/wiki/API

default_language = 'en'
default_lookup_limit = 100
default_number_results = 50

nouns_set = {x.name().split(".", 1)[0] for x in wn.all_synsets("n")}

class clock:
    def __init__(self):
        self.tic = time.time()
    def time_step(self,s):
        toc = time.time()
        print("%s: %ss" % (s,str(toc-self.tic)))
        self.tic=toc

CLOCK = None

class candidate:
    """
        A candidate is an entity that is candidate to nounified the input verb
    """
    def __init__(self, fullUri, relation, pattern, weight):
        self.fullUri = fullUri    # full uri of the word
        self.shortUri = ''        # short uri, we remove the optionnal info of the URI (pos tag + phrase distinguishing, see https://github.com/commonsense/conceptnet5/wiki/URI-hierarchy#concept-uris)
        self.word = ''            # candidate word to nounified pattern
        self.relation = relation  # relation of the involved edge
        self.tag = 0              # 0 : unknown, -1 : word is no longer a candidate, 1 : strong candidate
        self.pattern = pattern    # word to be nounified
        self.similarity = 0       # similarity between word and pattern
        self.weight = weight      # weight of the edge
        self.score = 0            # global score of the candidate, 0<..<1, the greater the better

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
            compute tag with the set of nouns extracted from nltk
        """
        tic = time.time()
        if self.tag == 0:
            if self.word in nouns_set:
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
    r = requests.get('http://127.0.0.1:8084/data/5.3' + uri,params={'limit':default_lookup_limit}).json()
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
    nb_results = min(len(res),default_number_results)
    return {a.word for a in res[-nb_results:]}

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Syntax: ./%s <word to search>" % sys.argv[0])
    CLOCK = clock()
    word=normalized_concept_name(default_language,sys.argv[1]) # Lemmatization+stemming
    CLOCK.time_step("lemmatization")
    print(associatedWords(word,{'/r/RelatedTo','/r/DerivedFrom','/r/CapableOf','/r/Synonym'}))

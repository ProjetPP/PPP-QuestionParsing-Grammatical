#!/usr/bin/env python3

import requests
import sys
import difflib # string similarity
import time
from conceptnet5.nodes import normalized_concept_name, uri_to_lemmas
import pickle
import os
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0,parentdir)
os.environ['PPP_QUESTIONPARSING_GRAMMATICAL_CONFIG'] = '../example_config.json'
from ppp_questionparsing_grammatical import nounDB

default_language = 'en'
default_lookup_limit = 500  # number of uri to extract
default_number_results = 50 # number of results to return at the end

wikiFile = open('wikidataProperties.pickle','rb')
wikidataProperties = pickle.load(wikiFile)
wikiFile.close()

nounsFile = open('nouns.pickle','rb')
nounsSet = pickle.load(nounsFile)
nounsFile.close()

verbsFile = open('verbs.pickle','rb')
verbsSet = pickle.load(verbsFile)
verbsFile.close()

class Clock:
    def __init__(self):
        self.tic = time.time()
    def format_time(self,t):
        h = t//3600
        t -= h*3600
        m = t//60
        t -= m*60
        s=t
        return "%d:%d:%d" % (h,m,s)
    def time_step(self,s,done,total):
        toc = time.time()
        remaining_time = (toc-self.tic)*(total-done)/done
        print("%s\t-- %s" % (self.format_time(round(remaining_time)),s))

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
        if self.tag == 0:
            if self.word in nounsSet:
                self.tag = 1
            else:
                self.tag = -1

    def computeScore(self):
        """
            compute similarity, score
        """
        self.similarity = difflib.SequenceMatcher(a=self.word.lower(), b=self.pattern.lower()).ratio()
        self.score = self.similarity + self.weight # need to be improved
        if self.word in wikidataProperties:
            self.score += 10 # high bonus for the wikidata properties

def computeWeight(r):
    maxw = 0
    for w in r:
        maxw = max(maxw,w.weight)
    for w in r:
        w.weight = w.weight / maxw
        w.computeScore()

def buildCandidate(pattern,edge):
    """
        Return a candidate built from the input edge and the pattern (ie the word that is nounified)
    """
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

def associatedWords(verb,relations):
    """
        Returns the best nb_results candidates to nounify the pattern
    """
    pattern = normalized_concept_name(default_language,verb) # Lemmatization+stemming
    uri = "/c/{0}/{1}".format(default_language,pattern)
    r = requests.get('http://127.0.0.1:8084/data/5.3' + uri,params={'limit':default_lookup_limit}).json()
    res = []
    for e in r['edges']:
        if e['rel'] in relations:
            cand = buildCandidate(pattern,e)
            if cand != None and cand.tag != -1:
                res.append(cand)
    for cand in res:
        cand.computeScore()
    computeWeight(res)
    res.sort(key = lambda x: x.score)
    nb_results = min(len(res),default_number_results)
    return {a.word for a in res[-nb_results:]}

if __name__ == "__main__":
    database = nounDB.Nounificator()
    CLOCK = Clock()
    for verb in verbsSet:
        for noun in associatedWords(verb,{'/r/RelatedTo','/r/DerivedFrom','/r/CapableOf','/r/Synonym'}):
            database.add(verb,noun)
        CLOCK.time_step(verb,i+1,len(verb))
        if (i+1)%300 == 0: # save every 300 verbs (~ 20 min), in case of crash
            database.save('nounification.%d.pickle' % (i+1))
    database.save('nounification.pickle')

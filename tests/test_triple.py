import json

from ppp_nlp_classical import Triple, TriplesBucket, computeTree, simplify, buildBucket

from unittest import TestCase

# Parsing result of "Who is the president of the United States?"
def give_result():
    return  {'sentences': [{
  'words': [
    ['Who', 
      {'CharacterOffsetBegin': '0', 
       'PartOfSpeech': 'WP', 
       'Lemma': 'who', 
       'NamedEntityTag': 'O', 
       'CharacterOffsetEnd': '3'}], 
    ['is', 
      {'CharacterOffsetBegin': '4', 
       'PartOfSpeech': 'VBZ', 
       'Lemma': 'be', 
       'NamedEntityTag': 'O', 
       'CharacterOffsetEnd': '6'}], 
    ['the', 
      {'CharacterOffsetBegin': '7', 
       'PartOfSpeech': 'DT', 
       'Lemma': 'the', 
       'NamedEntityTag': 'O', 
       'CharacterOffsetEnd': '10'}], 
    ['president', 
      {'CharacterOffsetBegin': '11', 
       'PartOfSpeech': 'NN', 
       'Lemma': 'president', 
       'NamedEntityTag': 'O', 
       'CharacterOffsetEnd': '20'}], 
    ['of', 
      {'CharacterOffsetBegin': '21', 
       'PartOfSpeech': 'IN', 
       'Lemma': 'of', 
       'NamedEntityTag': 'O', 
       'CharacterOffsetEnd': '23'}], 
    ['the', 
      {'CharacterOffsetBegin': '24', 
       'PartOfSpeech': 'DT', 'Lemma': 
       'the', 'NamedEntityTag': 'O', 
       'CharacterOffsetEnd': '27'}], 
    ['United', 
      {'CharacterOffsetBegin': '28', 
       'PartOfSpeech': 'NNP', 
       'Lemma': 'United', 
       'NamedEntityTag': 'LOCATION', 
       'CharacterOffsetEnd': '34'}], 
    ['States', 
      {'CharacterOffsetBegin': '35', 
       'PartOfSpeech': 'NNPS', 
       'Lemma': 'States', 
       'NamedEntityTag': 'LOCATION', 
       'CharacterOffsetEnd': '41'}], 
    ['?', 
      {'CharacterOffsetBegin': '41', 
       'PartOfSpeech': '.', 
       'Lemma': '?', 
       'NamedEntityTag': 'O', 
       'CharacterOffsetEnd': '42'}]], 
  'text': 'Who is the president of the United States?', 
  'dependencies': [['root', 'ROOT', 'is'], ['dep', 'is', 'Who'], ['det', 'president', 'the'], ['nsubj', 'is', 'president'], ['det', 'States', 'the'], ['nn', 'States', 'United'], ['prep_of', 'president', 'States']], 
  'indexeddependencies': [['root', 'ROOT-0', 'is-2'], ['dep', 'is-2', 'Who-1'], ['det', 'president-4', 'the-3'], ['nsubj', 'is-2', 'president-4'], ['det', 'States-8', 'the-6'], ['nn', 'States-8', 'United-7'], ['prep_of', 'president-4', 'States-8']], 
  'parsetree': '(ROOT (SBARQ (WHNP (WP Who)) (SQ (VBZ is) (NP (NP (DT the) (NN president)) (PP (IN of) (NP (DT the) (NNP United) (NNPS States))))) (. ?)))'}]}

class TripleTests(TestCase):

    def testEasyTriple(self):
        triple = Triple(4,"President of","France")
        self.assertEqual(triple.subjectT,4)
        self.assertEqual(triple.predicateT,"President of")
        self.assertEqual(triple.objectT,"France")
        triple.renameUnknown(4,8)
        self.assertEqual(triple.subjectT,8)
        self.assertEqual(triple.predicateT,"President of")
        self.assertEqual(triple.objectT,"France")        
        self.assertEqual('%s' % triple,"(?8 | President of | France)") 

    def testEasyTriplesBucket(self):
        tp = Triple(4,"President of","France")
        bt = TriplesBucket()
        bt.addTriple(tp)
        bt.renameUnknown(4,8)
        #self.assertEqual('%s' % bt,"\n(?8 | President of | France)")     

    def testBuildBucket(self):
        tree = computeTree(give_result()['sentences'][0])
        qw = simplify(tree)
        tBucket = buildBucket(tree,qw)
        self.assertEqual(len(tBucket.bucket), 2)
        self.assertEqual(tBucket.bucket[0].subjectT, 1)
        self.assertEqual(tBucket.bucket[0].predicateT, "identity")
        self.assertEqual(tBucket.bucket[0].objectT, 0)
        self.assertEqual(tBucket.bucket[1].subjectT, 1)
        self.assertEqual(tBucket.bucket[1].predicateT, " president of")
        self.assertEqual(tBucket.bucket[1].objectT, " United States")

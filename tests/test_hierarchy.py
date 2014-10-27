import json

from ppp_nlp_classical import DependenciesTree, computeTree, simplify2, identifyQuestionWord

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


class HierarchyTests(TestCase):

    def testQuestion(self):
        tree=computeTree(give_result()['sentences'][0])
        self.assertEqual(identifyQuestionWord(tree),'Who')         
        
    def testHierarchySimplification(self):
        tree=computeTree(give_result()['sentences'][0])
        simplify2(tree)
        root=tree
        # Root
        self.assertEqual(root.wordList,[("ROOT",0)])
        self.assertEqual(root.namedEntityTag,'undef')
        self.assertEqual(root.dependency,'undef')
        self.assertRaises(root.parent,None)
        self.assertEqual(len(root.child),1)
        # Is
        is_=root.child[0]
        self.assertEqual(is_.wordList,[("is",2)])
        self.assertEqual(is_.namedEntityTag,'undef')
        self.assertEqual(is_.dependency,'root')
        self.assertEqual(is_.parent,root)
        self.assertEqual(len(is_.child),1)
        # President
        president=is_.child[0]
        self.assertEqual(president.wordList,[("president",4)])
        self.assertEqual(president.namedEntityTag,'undef')
        self.assertEqual(president.dependency,'subj')
        self.assertEqual(president.parent,is_)
        self.assertEqual(len(president.child),1)
        # United States
        us=president.child[0]
        self.assertEqual(us.wordList,[("United",7),("States",8)])
        self.assertEqual(us.namedEntityTag,'LOCATION')
        self.assertEqual(us.dependency,'prep_of')
        self.assertEqual(us.parent,president)
        self.assertEqual(len(us.child),0)
        

import json

from ppp_nlp_classical import DependenciesTree, computeTree, simplify

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

# Parsing result of "How old are there?"
def give_result2():
    return  {'sentences': [{'dependencies': [['root', 'ROOT', 'are'],
                ['advmod', 'old', 'How'],
                ['dep', 'are', 'old'],
                ['expl', 'are', 'there']],
               'indexeddependencies': [['root', 'ROOT-0', 'are-3'],
                ['advmod', 'old-2', 'How-1'],
                ['dep', 'are-3', 'old-2'],
                ['expl', 'are-3', 'there-4']],
               'parsetree': '(ROOT (SBARQ (WHADJP (WRB How) (JJ old)) (SQ (VBP are) (NP (EX there))) (. ?)))',
               'text': 'How old are there?',
               'words': [['How',
                 {'CharacterOffsetBegin': '0',
                  'CharacterOffsetEnd': '3',
                  'Lemma': 'how',
                  'NamedEntityTag': 'O',
                  'PartOfSpeech': 'WRB'}],
                ['old',
                 {'CharacterOffsetBegin': '4',
                  'CharacterOffsetEnd': '7',
                  'Lemma': 'old',
                  'NamedEntityTag': 'O',
                  'PartOfSpeech': 'JJ'}],
                ['are',
                 {'CharacterOffsetBegin': '8',
                  'CharacterOffsetEnd': '11',
                  'Lemma': 'be',
                  'NamedEntityTag': 'O',
                  'PartOfSpeech': 'VBP'}],
                ['there',
                 {'CharacterOffsetBegin': '12',
                  'CharacterOffsetEnd': '17',
                  'Lemma': 'there',
                  'NamedEntityTag': 'O',
                  'PartOfSpeech': 'EX'}],
                ['?',
                 {'CharacterOffsetBegin': '17',
                  'CharacterOffsetEnd': '18',
                  'Lemma': '?',
                  'NamedEntityTag': 'O',
                  'PartOfSpeech': '.'}]]}]}
                  
# Parsing result of "Who is the United States president?"
def give_result3():
    return  {'sentences': [{'dependencies': [['root', 'ROOT', 'is'],
                ['dep', 'is', 'Who'],
                ['det', 'president', 'the'],
                ['nn', 'president', 'United'],
                ['nn', 'president', 'States'],
                ['nsubj', 'is', 'president']],
               'indexeddependencies': [['root', 'ROOT-0', 'is-2'],
                ['dep', 'is-2', 'Who-1'],
                ['det', 'president-6', 'the-3'],
                ['nn', 'president-6', 'United-4'],
                ['nn', 'president-6', 'States-5'],
                ['nsubj', 'is-2', 'president-6']],
               'parsetree': '(ROOT (SBARQ (WHNP (WP Who)) (SQ (VBZ is) (NP (DT the) (NNP United) (NNPS States) (NN president))) (. ?)))',
               'text': 'Who is the United States president?',
               'words': [['Who',
                 {'CharacterOffsetBegin': '0',
                  'CharacterOffsetEnd': '3',
                  'Lemma': 'who',
                  'NamedEntityTag': 'O',
                  'PartOfSpeech': 'WP'}],
                ['is',
                 {'CharacterOffsetBegin': '4',
                  'CharacterOffsetEnd': '6',
                  'Lemma': 'be',
                  'NamedEntityTag': 'O',
                  'PartOfSpeech': 'VBZ'}],
                ['the',
                 {'CharacterOffsetBegin': '7',
                  'CharacterOffsetEnd': '10',
                  'Lemma': 'the',
                  'NamedEntityTag': 'O',
                  'PartOfSpeech': 'DT'}],
                ['United',
                 {'CharacterOffsetBegin': '11',
                  'CharacterOffsetEnd': '17',
                  'Lemma': 'United',
                  'NamedEntityTag': 'LOCATION',
                  'PartOfSpeech': 'NNP'}],
                ['States',
                 {'CharacterOffsetBegin': '18',
                  'CharacterOffsetEnd': '24',
                  'Lemma': 'States',
                  'NamedEntityTag': 'LOCATION',
                  'PartOfSpeech': 'NNPS'}],
                ['president',
                 {'CharacterOffsetBegin': '25',
                  'CharacterOffsetEnd': '34',
                  'Lemma': 'president',
                  'NamedEntityTag': 'O',
                  'PartOfSpeech': 'NN'}],
                ['?',
                 {'CharacterOffsetBegin': '34',
                  'CharacterOffsetEnd': '35',
                  'Lemma': '?',
                  'NamedEntityTag': 'O',
                  'PartOfSpeech': '.'}]]}]}

class HierarchyTests(TestCase):

    def testQuestion(self):
        tree=computeTree(give_result()['sentences'][0])
        self.assertEqual(simplify(tree),'Who')

    def testQuestion2(self):
        tree=computeTree(give_result2()['sentences'][0])
        self.assertEqual(simplify(tree),'How old')

    def testHierarchySimplification(self):
        tree=computeTree(give_result()['sentences'][0])
        simplify(tree)
        root=tree
        # Root
        self.assertEqual(root.wordList,[("ROOT",0)])
        self.assertEqual(root.namedEntityTag,'undef')
        self.assertEqual(root.dependency,'t0')
        self.assertEqual(root.parent,None)
        self.assertEqual(len(root.child),1)
        # Is
        is_=root.child[0]
        self.assertEqual(is_.wordList,[("is",2)])
        self.assertEqual(is_.namedEntityTag,'undef')
        self.assertEqual(is_.dependency,'t0')
        self.assertEqual(is_.parent,root)
        self.assertEqual(len(is_.child),1)
        # President
        president=is_.child[0]
        self.assertEqual(president.wordList,[("president",4)])
        self.assertEqual(president.namedEntityTag,'undef')
        self.assertEqual(president.dependency,'t1')
        self.assertEqual(president.parent,is_)
        self.assertEqual(len(president.child),1)
        # United States
        us=president.child[0]
        self.assertEqual(us.wordList,[("United",7),("States",8)])
        self.assertEqual(us.namedEntityTag,'LOCATION')
        self.assertEqual(us.dependency,'prep_of')
        self.assertEqual(us.parent,president)
        self.assertEqual(len(us.child),0)

    def testIgnore(self):
        tree=computeTree(give_result2()['sentences'][0])
        simplify(tree)
        root=tree
        # Root
        self.assertEqual(root.wordList,[("ROOT",0)])
        self.assertEqual(root.namedEntityTag,'undef')
        self.assertEqual(root.dependency,'t0')
        self.assertEqual(root.parent,None)
        self.assertEqual(len(root.child),1)
        # Are
        are=root.child[0]
        self.assertEqual(are.wordList,[("are",3)])
        self.assertEqual(are.namedEntityTag,'undef')
        self.assertEqual(are.dependency,'t0')
        self.assertEqual(are.parent,root)
        self.assertEqual(len(are.child),0)

    def testHierarchySimplification2(self):
        tree=computeTree(give_result3()['sentences'][0])
        simplify(tree)
        root=tree
        # Root
        self.assertEqual(root.wordList,[("ROOT",0)])
        self.assertEqual(root.namedEntityTag,'undef')
        self.assertEqual(root.dependency,'t0')
        self.assertEqual(root.parent,None)
        self.assertEqual(len(root.child),1)
        # Is
        is_=root.child[0]
        self.assertEqual(is_.wordList,[("is",2)])
        self.assertEqual(is_.namedEntityTag,'undef')
        self.assertEqual(is_.dependency,'t0')
        self.assertEqual(is_.parent,root)
        self.assertEqual(len(is_.child),1)
        # President
        president=is_.child[0]
        self.assertEqual(president.wordList,[("United",4),("States",5),("president",6)])
        self.assertEqual(president.namedEntityTag,'undef')
        self.assertEqual(president.dependency,'t1')
        self.assertEqual(president.parent,is_)
        self.assertEqual(len(president.child),0)

import json

from ppp_nlp_classical import DependenciesTree, compute_tree

from unittest import TestCase

# Parsing result of "John Smith lives in United Kingdom."
def give_result():
         return {'sentences': [{'dependencies': [['root', 'ROOT', 'lives'],
                    ['nn', 'Smith', 'John'],
                    ['nsubj', 'lives', 'Smith'],
                    ['nn', 'Kingdom', 'United'],
                    ['prep_in', 'lives', 'Kingdom']],
                   'indexeddependencies': [['root', 'ROOT-0', 'lives-3'],
                    ['nn', 'Smith-2', 'John-1'],
                    ['nsubj', 'lives-3', 'Smith-2'],
                    ['nn', 'Kingdom-6', 'United-5'],
                    ['prep_in', 'lives-3', 'Kingdom-6']],
                   'parsetree': '(ROOT (S (NP (NNP John) (NNP Smith)) (VP (VBZ lives) (PP (IN in) (NP (NNP United) (NNP Kingdom)))) (. .)))',
                   'text': 'John Smith lives in United Kingdom.',
                   'words': [['John',
                     {'CharacterOffsetBegin': '0',
                      'CharacterOffsetEnd': '4',
                      'Lemma': 'John',
                      'NamedEntityTag': 'PERSON',
                      'PartOfSpeech': 'NNP'}],
                    ['Smith',
                     {'CharacterOffsetBegin': '5',
                      'CharacterOffsetEnd': '10',
                      'Lemma': 'Smith',
                      'NamedEntityTag': 'PERSON',
                      'PartOfSpeech': 'NNP'}],
                    ['lives',
                     {'CharacterOffsetBegin': '11',
                      'CharacterOffsetEnd': '16',
                      'Lemma': 'live',
                      'NamedEntityTag': 'O',
                      'PartOfSpeech': 'VBZ'}],
                    ['in',
                     {'CharacterOffsetBegin': '17',
                      'CharacterOffsetEnd': '19',
                      'Lemma': 'in',
                      'NamedEntityTag': 'O',
                      'PartOfSpeech': 'IN'}],
                    ['United',
                     {'CharacterOffsetBegin': '20',
                      'CharacterOffsetEnd': '26',
                      'Lemma': 'United',
                      'NamedEntityTag': 'LOCATION',
                      'PartOfSpeech': 'NNP'}],
                    ['Kingdom',
                     {'CharacterOffsetBegin': '27',
                      'CharacterOffsetEnd': '34',
                      'Lemma': 'Kingdom',
                      'NamedEntityTag': 'LOCATION',
                      'PartOfSpeech': 'NNP'}],
                    ['.',
                     {'CharacterOffsetBegin': '34',
                      'CharacterOffsetEnd': '35',
                      'Lemma': '.',
                      'NamedEntityTag': 'O',
                      'PartOfSpeech': '.'}]]}]}


class DependenciesTreeTests(TestCase):

    def testBasicConstructor(self):
        n = DependenciesTree(['foo'])
        self.assertEqual(n.wordList, ['foo'])
        self.assertEqual(n.namedEntityTag, 'undef')
        self.assertEqual(n.dependency, 'undef')
        self.assertEqual(n.child, [])
        self.assertEqual(n.text,"")
        self.assertRaises(AttributeError, lambda: n.parent)
        
    def testTreeGeneration(self):
        tree=compute_tree(give_result()['sentences'][0])
        root=tree
        # Root
        self.assertEqual(root.wordList,["ROOT-0"])
        self.assertEqual(root.namedEntityTag,'undef')
        self.assertEqual(root.dependency,'undef')
        self.assertRaises(AttributeError, lambda: root.parent)        
        self.assertEqual(len(root.child),1)
        # Lives
        lives=root.child[0]
        self.assertEqual(lives.wordList,["lives-3"])
        self.assertEqual(lives.namedEntityTag,'undef')
        self.assertEqual(lives.dependency,'root')
        self.assertEqual(lives.parent,tree)        
        self.assertEqual(len(lives.child),2)
        # Smith
        smith=lives.child[0]
        self.assertEqual(smith.wordList,["Smith-2"])
        self.assertEqual(smith.namedEntityTag,'PERSON')
        self.assertEqual(smith.dependency,'nsubj')
        self.assertEqual(smith.parent,lives)        
        self.assertEqual(len(smith.child),1)
        # John
        john=smith.child[0]
        self.assertEqual(john.wordList,["John-1"])
        self.assertEqual(john.namedEntityTag,'PERSON')
        self.assertEqual(john.dependency,'nn')
        self.assertEqual(john.parent,smith)        
        self.assertEqual(len(john.child),0)
        # Kingdom
        kingdom=lives.child[1]
        self.assertEqual(kingdom.wordList,["Kingdom-6"])
        self.assertEqual(kingdom.namedEntityTag,'LOCATION')
        self.assertEqual(kingdom.dependency,'prep_in')
        self.assertEqual(kingdom.parent,lives)        
        self.assertEqual(len(kingdom.child),1)   
        # United
        united=kingdom.child[0]
        self.assertEqual(united.wordList,["United-5"])
        self.assertEqual(united.namedEntityTag,'LOCATION')
        self.assertEqual(united.dependency,'nn')
        self.assertEqual(united.parent,kingdom)        
        self.assertEqual(len(united.child),0)     

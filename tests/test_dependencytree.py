import json

from ppp_nlp_classical import DependenciesTree, compute_tree

from unittest import TestCase

# Parsing result of "George Washington is the first president of the United States."
def give_result():
         return {'coref': [[[['the first president of the United states', 0, 5, 3, 10],
                ['George Washington', 0, 1, 0, 2]]]],
                'sentences': [{'dependencies': [['root', 'ROOT', 'president'],
                ['nn', 'Washington', 'George'],
                ['nsubj', 'president', 'Washington'],
                ['cop', 'president', 'is'],
                ['det', 'president', 'the'],
                ['amod', 'president', 'first'],
                ['det', 'states', 'the'],
                ['nn', 'states', 'United'],
                ['prep_of', 'president', 'states']],
                'indexeddependencies': [['root', 'ROOT-0', 'president-6'],
                ['nn', 'Washington-2', 'George-1'],
                ['nsubj', 'president-6', 'Washington-2'],
                ['cop', 'president-6', 'is-3'],
                ['det', 'president-6', 'the-4'],
                ['amod', 'president-6', 'first-5'],
                ['det', 'states-10', 'the-8'],
                ['nn', 'states-10', 'United-9'],
                ['prep_of', 'president-6', 'states-10']],
                'parsetree': '(ROOT (S (NP (NNP George) (NNP Washington)) (VP (VBZ is) (NP (NP (DT the) (JJ first) (NN president)) (PP (IN of) (NP (DT the) (NNP United) (NNS states)))))))',
                'text': 'George Washington is the first president of the United states',
                'words': [['George',
                {'CharacterOffsetBegin': '0',
                'CharacterOffsetEnd': '6',
                'Lemma': 'George',
                'NamedEntityTag': 'PERSON',
                'PartOfSpeech': 'NNP'}],
                ['Washington',
                {'CharacterOffsetBegin': '7',
                'CharacterOffsetEnd': '17',
                'Lemma': 'Washington',
                'NamedEntityTag': 'PERSON',
                'PartOfSpeech': 'NNP'}],
                ['is',
                {'CharacterOffsetBegin': '18',
                'CharacterOffsetEnd': '20',
                'Lemma': 'be',
                'NamedEntityTag': 'O',
                'PartOfSpeech': 'VBZ'}],
                ['the',
                {'CharacterOffsetBegin': '21',
                'CharacterOffsetEnd': '24',
                'Lemma': 'the',
                'NamedEntityTag': 'O',
                'PartOfSpeech': 'DT'}],
                ['first',
                {'CharacterOffsetBegin': '25',
                'CharacterOffsetEnd': '30',
                'Lemma': 'first',
                'NamedEntityTag': 'ORDINAL',
                'NormalizedNamedEntityTag': '1.0',
                'PartOfSpeech': 'JJ'}],
                ['president',
                {'CharacterOffsetBegin': '31',
                'CharacterOffsetEnd': '40',
                'Lemma': 'president',
                'NamedEntityTag': 'O',
                'PartOfSpeech': 'NN'}],
                ['of',
                {'CharacterOffsetBegin': '41',
                'CharacterOffsetEnd': '43',
                'Lemma': 'of',
                'NamedEntityTag': 'O',
                'PartOfSpeech': 'IN'}],
                ['the',
                {'CharacterOffsetBegin': '44',
                'CharacterOffsetEnd': '47',
                'Lemma': 'the',
                'NamedEntityTag': 'O',
                'PartOfSpeech': 'DT'}],
                ['United',
                {'CharacterOffsetBegin': '48',
                'CharacterOffsetEnd': '54',
                'Lemma': 'United',
                'NamedEntityTag': 'ORGANIZATION',
                'PartOfSpeech': 'NNP'}],
                ['states',
                {'CharacterOffsetBegin': '55',
                'CharacterOffsetEnd': '61',
                'Lemma': 'state',
                'NamedEntityTag': 'O',
                'PartOfSpeech': 'NNS'}]]}]}

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

import json

from ppp_nlp_classical import DependenciesTree, compute_tree, simplify

from unittest import TestCase

# Parsing result of "John Smith lives in United Kingdom."
def give_result():
    return  {'sentences': [{'dependencies': [['root', 'ROOT', 'lives'],
                ['nn', 'Smith', 'John'],
                ['nsubj', 'lives', 'Smith'],
                ['det', 'Kingdom', 'the'],
                ['nn', 'Kingdom', 'United'],
                ['prep_in', 'lives', 'Kingdom']],
               'indexeddependencies': [['root', 'ROOT-0', 'lives-3'],
                ['nn', 'Smith-2', 'John-1'],
                ['nsubj', 'lives-3', 'Smith-2'],
                ['det', 'Kingdom-7', 'the-5'],
                ['nn', 'Kingdom-7', 'United-6'],
                ['prep_in', 'lives-3', 'Kingdom-7']],
               'parsetree': '(ROOT (S (NP (NNP John) (NNP Smith)) (VP (VBZ lives) (PP (IN in) (NP (DT the) (NNP United) (NNP Kingdom)))) (. .)))',
               'text': 'John Smith lives in the United Kingdom.',
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
                ['the',
                 {'CharacterOffsetBegin': '20',
                  'CharacterOffsetEnd': '23',
                  'Lemma': 'the',
                  'NamedEntityTag': 'O',
                  'PartOfSpeech': 'DT'}],
                ['United',
                 {'CharacterOffsetBegin': '24',
                  'CharacterOffsetEnd': '30',
                  'Lemma': 'United',
                  'NamedEntityTag': 'LOCATION',
                  'PartOfSpeech': 'NNP'}],
                ['Kingdom',
                 {'CharacterOffsetBegin': '31',
                  'CharacterOffsetEnd': '38',
                  'Lemma': 'Kingdom',
                  'NamedEntityTag': 'LOCATION',
                  'PartOfSpeech': 'NNP'}],
                ['.',
                 {'CharacterOffsetBegin': '38',
                  'CharacterOffsetEnd': '39',
                  'Lemma': '.',
                  'NamedEntityTag': 'O',
                  'PartOfSpeech': '.'}]]}]}


class DependenciesTreeTests(TestCase):

    def testBasicConstructor(self):
        n = DependenciesTree('foo-1')
        self.assertEqual(n.wordList, [('foo',1)])
        self.assertEqual(n.namedEntityTag, 'undef')
        self.assertEqual(n.dependency, 'undef')
        self.assertEqual(n.child, [])
        self.assertEqual(n.text,"")
        self.assertRaises(AttributeError, lambda: n.parent)

    def testMerge(self):
        root1 = DependenciesTree('root-1')
        root2 = DependenciesTree('root-2')
        node1 = DependenciesTree('n-1','tag1','dep1',[DependenciesTree('childn-1')])
        node1.parent = root1
        root1.child += [node1]
        node2 = DependenciesTree('n-2','tag2','dep2',[DependenciesTree('childn-2')])
        node2.parent = root2
        root2.child += [node2]
        node1.merge(node2)
        self.assertEqual(len(root2.child),0)
        self.assertEqual(len(root1.child),1)
        self.assertEqual(len(node1.child),2)
        self.assertEqual(node1.wordList,[('n',1),('n',2)])
        self.assertEqual(node1.namedEntityTag,'tag1')
        self.assertEqual(node1.dependency,'dep1')
        self.assertEqual(node1.parent,root1)
        
    def testTreeGeneration(self):
        tree=compute_tree(give_result()['sentences'][0])
        root=tree
        # Root
        self.assertEqual(root.wordList,[("ROOT",0)])
        self.assertEqual(root.namedEntityTag,'undef')
        self.assertEqual(root.dependency,'undef')
        self.assertRaises(AttributeError, lambda: root.parent)
        self.assertEqual(len(root.child),1)
        # Lives
        lives=root.child[0]
        self.assertEqual(lives.wordList,[("lives",3)])
        self.assertEqual(lives.namedEntityTag,'undef')
        self.assertEqual(lives.dependency,'root')
        self.assertEqual(lives.parent,tree)
        self.assertEqual(len(lives.child),2)
        # Smith
        smith=lives.child[0]
        self.assertEqual(smith.wordList,[("Smith",2)])
        self.assertEqual(smith.namedEntityTag,'PERSON')
        self.assertEqual(smith.dependency,'nsubj')
        self.assertEqual(smith.parent,lives)
        self.assertEqual(len(smith.child),1)
        # John
        john=smith.child[0]
        self.assertEqual(john.wordList,[("John",1)])
        self.assertEqual(john.namedEntityTag,'PERSON')
        self.assertEqual(john.dependency,'nn')
        self.assertEqual(john.parent,smith)
        self.assertEqual(len(john.child),0)
        # Kingdom
        kingdom=lives.child[1]
        self.assertEqual(kingdom.wordList,[("Kingdom",7)])
        self.assertEqual(kingdom.namedEntityTag,'LOCATION')
        self.assertEqual(kingdom.dependency,'prep_in')
        self.assertEqual(kingdom.parent,lives)
        self.assertEqual(len(kingdom.child),2)
        # The
        the=kingdom.child[0]
        self.assertEqual(the.wordList,[("the",5)])
        self.assertEqual(the.namedEntityTag,'undef')
        self.assertEqual(the.dependency,'det')
        self.assertEqual(the.parent,kingdom)
        self.assertEqual(len(the.child),0)
        # United
        united=kingdom.child[1]
        self.assertEqual(united.wordList,[("United",6)])
        self.assertEqual(united.namedEntityTag,'LOCATION')
        self.assertEqual(united.dependency,'nn')
        self.assertEqual(united.parent,kingdom)
        self.assertEqual(len(united.child),0)

    def testTreeSimplification(self):
        tree=compute_tree(give_result()['sentences'][0])
        simplify(tree)
        root=tree
        # Root
        self.assertEqual(root.wordList,[("ROOT",0)])
        self.assertEqual(root.namedEntityTag,'undef')
        self.assertEqual(root.dependency,'undef')
        self.assertRaises(AttributeError, lambda: root.parent)
        self.assertEqual(len(root.child),1)
        # Lives
        lives=root.child[0]
        self.assertEqual(lives.wordList,[("lives",3)])
        self.assertEqual(lives.namedEntityTag,'undef')
        self.assertEqual(lives.dependency,'root')
        self.assertEqual(lives.parent,tree)
        self.assertEqual(len(lives.child),2)
        # Smith
        smith=lives.child[0]
        self.assertEqual(smith.wordList,[("John",1),("Smith",2)])
        self.assertEqual(smith.namedEntityTag,'PERSON')
        self.assertEqual(smith.dependency,'nsubj')
        self.assertEqual(smith.parent,lives)
        self.assertEqual(len(smith.child),0)
        # Kingdom
        kingdom=lives.child[1]
        self.assertEqual(kingdom.wordList,[("United",6),("Kingdom",7)])
        self.assertEqual(kingdom.namedEntityTag,'LOCATION')
        self.assertEqual(kingdom.dependency,'prep_in')
        self.assertEqual(kingdom.parent,lives)
        self.assertEqual(len(kingdom.child),0)

import json

from ppp_nlp_classical import DependenciesTree, computeTree, mergeNamedEntityTagChildParent, mergeNamedEntityTagSisterBrother

from unittest import TestCase

# Parsing result of "John Smith lives in the United Kingdom."
def give_result1():
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

def give_string1():
    s="digraph relations {\n"
    s+="\t\"ROOT0\"[label=\"ROOT\",shape=box];\n"
    s+="\t\"ROOT0\" -> \"lives3\"[label=\"root\"];\n"
    s+="\t\"lives3\"[label=\"lives\",shape=box];\n"
    s+="\t\"lives3\" -> \"Smith2\"[label=\"nsubj\"];\n"
    s+="\t\"lives3\" -> \"Kingdom7\"[label=\"prep_in\"];\n"
    s+="\t\"Smith2\"[label=\"Smith [PERSON]\",shape=box];\n"
    s+="\t\"Smith2\" -> \"John1\"[label=\"nn\"];\n"
    s+="\t\"John1\"[label=\"John [PERSON]\",shape=box];\n"
    s+="\t\"Kingdom7\"[label=\"Kingdom [LOCATION]\",shape=box];\n"
    s+="\t\"Kingdom7\" -> \"the5\"[label=\"det\"];\n"
    s+="\t\"Kingdom7\" -> \"United6\"[label=\"nn\"];\n"
    s+="\t\"the5\"[label=\"the\",shape=box];\n"
    s+="\t\"United6\"[label=\"United [LOCATION]\",shape=box];\n"
    s+="\tlabelloc=\"t\"\tlabel=\"John Smith lives in the United Kingdom.\";\n"
    s+="}"
    return s

# Parse result of "Who wrote \"Lucy in the Sky with Diamonds\" and \"Let It Be\"?"
def give_result2():
    return  {'coref': [[[['It', 0, 13, 13, 14], ['the Sky with Diamonds', 0, 6, 5, 9]]]],
             'sentences': [{'dependencies': [['root', 'ROOT', 'wrote'],
                ['nsubj', 'wrote', 'Who'],
                ['dobj', 'wrote', 'Lucy'],
                ['det', 'Sky', 'the'],
                ['prep_in', 'Lucy', 'Sky'],
                ['prep_with', 'Sky', 'Diamonds'],
                ['conj_and', 'wrote', 'Let'],
                ['nsubj', 'Be', 'It'],
                ['ccomp', 'Let', 'Be']],
               'indexeddependencies': [['root', 'ROOT-0', 'wrote-2'],
                ['nsubj', 'wrote-2', 'Who-1'],
                ['dobj', 'wrote-2', 'Lucy-4'],
                ['det', 'Sky-7', 'the-6'],
                ['prep_in', 'Lucy-4', 'Sky-7'],
                ['prep_with', 'Sky-7', 'Diamonds-9'],
                ['conj_and', 'wrote-2', 'Let-13'],
                ['nsubj', 'Be-15', 'It-14'],
                ['ccomp', 'Let-13', 'Be-15']],
               'parsetree': "(ROOT (SBARQ (SBARQ (WHNP (WP Who)) (SQ (VP (VBD wrote) (`` ``) (NP (NP (NNP Lucy)) (PP (IN in) (NP (NP (DT the) (NN Sky)) (PP (IN with) (NP (NNP Diamonds)))))) ('' '')))) (CC and) (S (VP (`` ``) (VB Let) (S (NP (PRP It)) (VP (VB Be) ('' ''))))) (. ?)))",
               'text': 'Who wrote "Lucy in the Sky with Diamonds" and "Let It Be"?',
               'words': [['Who',
                 {'CharacterOffsetBegin': '0',
                  'CharacterOffsetEnd': '3',
                  'Lemma': 'who',
                  'NamedEntityTag': 'O',
                  'PartOfSpeech': 'WP'}],
                ['wrote',
                 {'CharacterOffsetBegin': '4',
                  'CharacterOffsetEnd': '9',
                  'Lemma': 'write',
                  'NamedEntityTag': 'O',
                  'PartOfSpeech': 'VBD'}],
                ['``',
                 {'CharacterOffsetBegin': '10',
                  'CharacterOffsetEnd': '11',
                  'Lemma': '``',
                  'NamedEntityTag': 'O',
                  'PartOfSpeech': '``'}],
                ['Lucy',
                 {'CharacterOffsetBegin': '11',
                  'CharacterOffsetEnd': '15',
                  'Lemma': 'Lucy',
                  'NamedEntityTag': 'PERSON',
                  'PartOfSpeech': 'NNP'}],
                ['in',
                 {'CharacterOffsetBegin': '16',
                  'CharacterOffsetEnd': '18',
                  'Lemma': 'in',
                  'NamedEntityTag': 'O',
                  'PartOfSpeech': 'IN'}],
                ['the',
                 {'CharacterOffsetBegin': '19',
                  'CharacterOffsetEnd': '22',
                  'Lemma': 'the',
                  'NamedEntityTag': 'O',
                  'PartOfSpeech': 'DT'}],
                ['Sky',
                 {'CharacterOffsetBegin': '23',
                  'CharacterOffsetEnd': '26',
                  'Lemma': 'sky',
                  'NamedEntityTag': 'O',
                  'PartOfSpeech': 'NN'}],
                ['with',
                 {'CharacterOffsetBegin': '27',
                  'CharacterOffsetEnd': '31',
                  'Lemma': 'with',
                  'NamedEntityTag': 'O',
                  'PartOfSpeech': 'IN'}],
                ['Diamonds',
                 {'CharacterOffsetBegin': '32',
                  'CharacterOffsetEnd': '39',
                  'Lemma': 'Diamonds',
                  'NamedEntityTag': 'O',
                  'PartOfSpeech': 'NNP'}],
                ["''",
                 {'CharacterOffsetBegin': '39',
                  'CharacterOffsetEnd': '40',
                  'Lemma': "''",
                  'NamedEntityTag': 'O',
                  'PartOfSpeech': "''"}],
                ['and',
                 {'CharacterOffsetBegin': '41',
                  'CharacterOffsetEnd': '44',
                  'Lemma': 'and',
                  'NamedEntityTag': 'O',
                  'PartOfSpeech': 'CC'}],
                ['``',
                 {'CharacterOffsetBegin': '45',
                  'CharacterOffsetEnd': '46',
                  'Lemma': '``',
                  'NamedEntityTag': 'O',
                  'PartOfSpeech': '``'}],
                ['Let',
                 {'CharacterOffsetBegin': '46',
                  'CharacterOffsetEnd': '49',
                  'Lemma': 'let',
                  'NamedEntityTag': 'O',
                  'PartOfSpeech': 'VB'}],
                ['It',
                 {'CharacterOffsetBegin': '50',
                  'CharacterOffsetEnd': '52',
                  'Lemma': 'it',
                  'NamedEntityTag': 'O',
                  'PartOfSpeech': 'PRP'}],
                ['Be',
                 {'CharacterOffsetBegin': '53',
                  'CharacterOffsetEnd': '55',
                  'Lemma': 'be',
                  'NamedEntityTag': 'O',
                  'PartOfSpeech': 'VB'}],
                ["''",
                 {'CharacterOffsetBegin': '55',
                  'CharacterOffsetEnd': '56',
                  'Lemma': "''",
                  'NamedEntityTag': 'O',
                  'PartOfSpeech': "''"}],
                ['?',
                 {'CharacterOffsetBegin': '56',
                  'CharacterOffsetEnd': '57',
                  'Lemma': '?',
                  'NamedEntityTag': 'O',
                  'PartOfSpeech': '.'}]]}]}

# Parse result of "Obama is the United States president."
def give_result3():
    return  {'coref': [[[['the United States president', 0, 5, 2, 6],
                ['Obama', 0, 0, 0, 1]]]],
             'sentences': [{'dependencies': [['root', 'ROOT', 'is'],
                ['nsubj', 'is', 'Obama'],
                ['det', 'president', 'the'],
                ['nn', 'president', 'United'],
                ['nn', 'president', 'States'],
                ['xcomp', 'is', 'president']],
               'indexeddependencies': [['root', 'ROOT-0', 'is-2'],
                ['nsubj', 'is-2', 'Obama-1'],
                ['det', 'president-6', 'the-3'],
                ['nn', 'president-6', 'United-4'],
                ['nn', 'president-6', 'States-5'],
                ['xcomp', 'is-2', 'president-6']],
               'parsetree': '(ROOT (S (NP (NNP Obama)) (VP (VBZ is) (NP (DT the) (NNP United) (NNPS States) (NN president))) (. .)))',
               'text': 'Obama is the United States president.',
               'words': [['Obama',
                 {'CharacterOffsetBegin': '0',
                  'CharacterOffsetEnd': '5',
                  'Lemma': 'Obama',
                  'NamedEntityTag': 'PERSON',
                  'PartOfSpeech': 'NNP'}],
                ['is',
                 {'CharacterOffsetBegin': '6',
                  'CharacterOffsetEnd': '8',
                  'Lemma': 'be',
                  'NamedEntityTag': 'O',
                  'PartOfSpeech': 'VBZ'}],
                ['the',
                 {'CharacterOffsetBegin': '9',
                  'CharacterOffsetEnd': '12',
                  'Lemma': 'the',
                  'NamedEntityTag': 'O',
                  'PartOfSpeech': 'DT'}],
                ['United',
                 {'CharacterOffsetBegin': '13',
                  'CharacterOffsetEnd': '19',
                  'Lemma': 'United',
                  'NamedEntityTag': 'LOCATION',
                  'PartOfSpeech': 'NNP'}],
                ['States',
                 {'CharacterOffsetBegin': '20',
                  'CharacterOffsetEnd': '26',
                  'Lemma': 'States',
                  'NamedEntityTag': 'LOCATION',
                  'PartOfSpeech': 'NNPS'}],
                ['president',
                 {'CharacterOffsetBegin': '27',
                  'CharacterOffsetEnd': '36',
                  'Lemma': 'president',
                  'NamedEntityTag': 'O',
                  'PartOfSpeech': 'NN'}],
                ['.',
                 {'CharacterOffsetBegin': '36',
                  'CharacterOffsetEnd': '37',
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
        self.assertEqual(n.parent,None)

    def testMerge(self):
        root1 = DependenciesTree('root-1')
        root2 = DependenciesTree('root-2')
        node1 = DependenciesTree('n-1','tag1','dep1',[DependenciesTree('childn-1')])
        node1.parent = root1
        root1.child += [node1]
        node2 = DependenciesTree('n-2','tag2','dep2',[DependenciesTree('childn-2')])
        node2.parent = root2
        root2.child += [node2]
        node1.merge(node2,True)
        self.assertEqual(len(root2.child),0)
        self.assertEqual(len(root1.child),1)
        self.assertEqual(len(node1.child),2)
        self.assertEqual(node1.wordList,[('n',1),('n',2)])
        self.assertEqual(node1.namedEntityTag,'tag1')
        self.assertEqual(node1.dependency,'dep1')
        self.assertEqual(node1.parent,root1)
        
    def testTreeGeneration(self):
        tree=computeTree(give_result1()['sentences'][0])
        root=tree
        # Root
        self.assertEqual(root.wordList,[("ROOT",0)])
        self.assertEqual(root.namedEntityTag,'undef')
        self.assertEqual(root.dependency,'undef')
        self.assertEqual(root.parent,None)
        self.assertEqual(len(root.child),1)
        # Lives
        lives=root.child[0]
        self.assertEqual(lives.wordList,[("lives",3)])
        self.assertEqual(lives.namedEntityTag,'undef')
        self.assertEqual(lives.dependency,'root')
        self.assertEqual(lives.parent,tree)
        self.assertEqual(len(lives.child),2)
        # John Smith
        jsmith=lives.child[0]
        self.assertEqual(jsmith.wordList,[("John",1),("Smith",2)])
        self.assertEqual(jsmith.namedEntityTag,'PERSON')
        self.assertEqual(jsmith.dependency,'nsubj')
        self.assertEqual(jsmith.parent,lives)
        self.assertEqual(len(jsmith.child),0)
        # United Kingdom
        ukingdom=lives.child[1]
        self.assertEqual(ukingdom.wordList,[("United",6),("Kingdom",7)])
        self.assertEqual(ukingdom.namedEntityTag,'LOCATION')
        self.assertEqual(ukingdom.dependency,'prep_in')
        self.assertEqual(ukingdom.parent,lives)
        self.assertEqual(len(ukingdom.child),1)
        # The
        the=ukingdom.child[0]
        self.assertEqual(the.wordList,[("the",5)])
        self.assertEqual(the.namedEntityTag,'undef')
        self.assertEqual(the.dependency,'det')
        self.assertEqual(the.parent,ukingdom)
        self.assertEqual(len(the.child),0)

    def testQuotationMerge(self):
        tree=computeTree(give_result2()['sentences'][0])
        root=tree
        # Root
        self.assertEqual(root.wordList,[("ROOT",0)])
        self.assertEqual(root.namedEntityTag,'undef')
        self.assertEqual(root.dependency,'undef')
        self.assertEqual(root.parent,None)
        self.assertEqual(len(root.child),1)
        # Wrote
        wrote=root.child[0]
        self.assertEqual(wrote.wordList,[("wrote",2)])
        self.assertEqual(wrote.namedEntityTag,'undef')
        self.assertEqual(wrote.dependency,'root')
        self.assertEqual(wrote.parent,root)
        self.assertEqual(len(wrote.child),3)
        # Who
        who=wrote.child[0]
        self.assertEqual(who.wordList,[("Who",1)])
        self.assertEqual(who.namedEntityTag,'undef')
        self.assertEqual(who.dependency,'nsubj')
        self.assertEqual(who.parent,wrote)
        self.assertEqual(len(who.child),0)
        # Lucy in the Sky with Diamondss
        lucy=wrote.child[1]
        self.assertEqual(lucy.wordList,[("Lucy",4),("in",5),("the",6),("Sky",7),("with",8),("Diamonds",9)])
        self.assertEqual(lucy.namedEntityTag,'undef')
        self.assertEqual(lucy.dependency,'dobj')
        self.assertEqual(lucy.parent,wrote)
        self.assertEqual(len(lucy.child),0)
        # Let it be
        let=wrote.child[2]
        self.assertEqual(let.wordList,[("Let",13),("It",14),("Be",15)])
        self.assertEqual(let.namedEntityTag,'undef')
        self.assertEqual(let.dependency,'conj_and')
        self.assertEqual(let.parent,wrote)
        self.assertEqual(len(let.child),0)

    def testEntityTagMerge1(self):
        tree=computeTree(give_result1()['sentences'][0])
        mergeNamedEntityTagChildParent(tree)
        root=tree
        # Root
        self.assertEqual(root.wordList,[("ROOT",0)])
        self.assertEqual(root.namedEntityTag,'undef')
        self.assertEqual(root.dependency,'undef')
        self.assertEqual(root.parent,None)
        self.assertEqual(len(root.child),1)
        # Lives
        lives=root.child[0]
        self.assertEqual(lives.wordList,[("lives",3)])
        self.assertEqual(lives.namedEntityTag,'undef')
        self.assertEqual(lives.dependency,'root')
        self.assertEqual(lives.parent,tree)
        self.assertEqual(len(lives.child),2)
        # John Smith
        smith=lives.child[0]
        self.assertEqual(smith.wordList,[("John",1),("Smith",2)])
        self.assertEqual(smith.namedEntityTag,'PERSON')
        self.assertEqual(smith.dependency,'nsubj')
        self.assertEqual(smith.parent,lives)
        self.assertEqual(len(smith.child),0)
        # United Kingdom
        kingdom=lives.child[1]
        self.assertEqual(kingdom.wordList,[("United",6),("Kingdom",7)])
        self.assertEqual(kingdom.namedEntityTag,'LOCATION')
        self.assertEqual(kingdom.dependency,'prep_in')
        self.assertEqual(kingdom.parent,lives)
        self.assertEqual(len(kingdom.child),1)
        # The
        the=kingdom.child[0]
        self.assertEqual(the.wordList,[("the",5)])
        self.assertEqual(the.namedEntityTag,'undef')
        self.assertEqual(the.dependency,'det')
        self.assertEqual(the.parent,kingdom)
        self.assertEqual(len(the.child),0)

    def testEntityTagMerge2(self):
        tree=computeTree(give_result3()['sentences'][0])
        mergeNamedEntityTagSisterBrother(tree)
        root=tree
        # Root
        self.assertEqual(root.wordList,[("ROOT",0)])
        self.assertEqual(root.namedEntityTag,'undef')
        self.assertEqual(root.dependency,'undef')
        self.assertEqual(root.parent,None)
        self.assertEqual(len(root.child),1)
        # Is
        is_=root.child[0]
        self.assertEqual(is_.wordList,[("is",2)])
        self.assertEqual(is_.namedEntityTag,'undef')
        self.assertEqual(is_.dependency,'root')
        self.assertEqual(is_.parent,tree)
        self.assertEqual(len(is_.child),2)
        # Obama
        obama=is_.child[0]
        self.assertEqual(obama.wordList,[("Obama",1)])
        self.assertEqual(obama.namedEntityTag,'PERSON')
        self.assertEqual(obama.dependency,'nsubj')
        self.assertEqual(obama.parent,is_)
        self.assertEqual(len(obama.child),0)
        # president
        president =is_.child[1]
        self.assertEqual(president.wordList,[("president",6)])
        self.assertEqual(president.namedEntityTag,'undef')
        self.assertEqual(president.dependency,'xcomp')
        self.assertEqual(president.parent,is_)
        self.assertEqual(len(president.child),2)
        # The
        the=president.child[0]
        self.assertEqual(the.wordList,[("the",3)])
        self.assertEqual(the.namedEntityTag,'undef')
        self.assertEqual(the.dependency,'det')
        self.assertEqual(the.parent,president)
        self.assertEqual(len(the.child),0)
        # United States
        united=president.child[1]
        self.assertEqual(united.wordList,[("United",4),("States",5)])
        self.assertEqual(united.namedEntityTag,'LOCATION')
        self.assertEqual(united.dependency,'nn')
        self.assertEqual(united.parent,president)
        self.assertEqual(len(united.child),0)

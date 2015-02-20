import json
from nltk.stem.wordnet import WordNetLemmatizer
from ppp_questionparsing_grammatical import Word, QuotationHandler, DependenciesTree, computeTree, mergeNamedEntityTagChildParent, mergeNamedEntityTagSisterBrother, QuotationError, preprocessingMerge
import data

from unittest import TestCase

class PreprocessingMergeTests(TestCase):

    #####################
    # Quotation handler #
    #####################

    def testBasicQuotationHandler(self):
        handler = QuotationHandler("foo")
        sentence = "The person who sing \"Let It Be\" and \"Lucy in the Sky with Diamonds\" also sing \"Yellow Submarine\"."
        expected = "The person who sing foo0 and foo1 also sing foo2."
        real = handler.pull(sentence)
        self.assertEqual(real, expected)
        self.assertEqual(handler.quotations["foo0"], "Let It Be")
        self.assertEqual(handler.quotations["foo1"], "Lucy in the Sky with Diamonds")
        self.assertEqual(handler.quotations["foo2"], "Yellow Submarine")

    def testOtherQuotationMarks(self):
        handler = QuotationHandler("foo")
        sentence = "The person who sing “Let It Be” and “Lucy in the Sky with Diamonds” also sing \"Yellow Submarine\"."
        expected = "The person who sing foo0 and foo1 also sing foo2."
        real = handler.pull(sentence)
        self.assertEqual(real, expected)
        self.assertEqual(handler.quotations["foo0"], "Let It Be")
        self.assertEqual(handler.quotations["foo1"], "Lucy in the Sky with Diamonds")
        self.assertEqual(handler.quotations["foo2"], "Yellow Submarine")

    def testRandomQuotationHandler(self):
        handler = QuotationHandler()
        sentence = "The person who sing \"Let It Be\" and \"Lucy in the Sky with Diamonds\" also sing \"Yellow Submarine\"."
        real = handler.pull(sentence)
        for key in handler.quotations.keys():
            real = real.replace(key, '"'+handler.quotations[key]+'"')
        self.assertEqual(real, sentence)

    def testWrongQuotation(self):
        handler = QuotationHandler()
        sentence1 = "What is \"bla?"
        sentence2 = "What is \"bla of \"blu\"?"
        self.assertRaises(QuotationError, handler.pull, sentence1)
        self.assertRaises(QuotationError, handler.pull, sentence2)

    ###############
    # NER merging #
    ###############

    def testMerge(self):
        root1 = DependenciesTree('root', 1)
        root2 = DependenciesTree('root', 2)
        node1 = DependenciesTree('n', 1, 'tag1', 'stype1', 'dep1', [DependenciesTree('childn', 1)])
        node1.parent = root1
        root1.child += [node1]
        node2 = DependenciesTree('n', 2, 'tag2', 'stype2', 'dep2', [DependenciesTree('childn', 2)])
        node2.parent = root2
        root2.child += [node2]
        node1.merge(node2, True)
        self.assertEqual(len(root2.child), 0)
        self.assertEqual(len(root1.child), 1)
        self.assertEqual(len(node1.child), 2)
        self.assertEqual(node1.wordList, [Word('n', 1), Word('n', 2)])
        self.assertEqual(node1.namedEntityTag, 'tag1')
        self.assertEqual(node1.dependency, 'dep1')
        self.assertEqual(node1.parent, root1)
        self.assertEqual(node1.subtreeType, 'stype1')
        self.assertEqual(node1.dfsTag, 0)

    ######################
    # preprocessingMerge #
    ######################

    def testStr(self):
        tree=computeTree(data.give_john_smith()['sentences'][0])
        preprocessingMerge(tree)
        self.maxDiff=None
        tree.sort()
        self.assertEqual(str(tree), data.give_john_smith_stringMerge())

    def testQuotationMerge(self):
        handler = QuotationHandler('foo')
        sentence = 'Who wrote "Lucy in the Sky with Diamonds" and "Let It Be"?'
        nonAmbiguousSentence = handler.pull(sentence)
        result=data.give_LSD_LIB()
        tree=computeTree(result['sentences'][0])
        preprocessingMerge(tree)
        handler.push(tree)
        tree.sort()
        root=tree
        # Root
        self.assertEqual(root.wordList, [Word("ROOT", 0)])
        self.assertEqual(root.namedEntityTag, 'undef')
        self.assertEqual(root.dependency, 'undef')
        self.assertEqual(root.parent, None)
        self.assertEqual(len(root.child), 1)
        self.assertEqual(root.subtreeType, 'undef')
        self.assertEqual(root.dfsTag, 0)
        # Wrote
        wrote=root.child[0]
        self.assertEqual(wrote.wordList, [Word("wrote", 2, 'VBD')])
        self.assertEqual(wrote.namedEntityTag, 'undef')
        self.assertEqual(wrote.dependency, 'root')
        self.assertEqual(wrote.parent, root)
        self.assertEqual(len(wrote.child), 2)
        self.assertEqual(wrote.subtreeType, 'undef')
        self.assertEqual(wrote.dfsTag, 0)
        # Who
        who=wrote.child[0]
        self.assertEqual(who.wordList, [Word("Who", 1, 'WP')])
        self.assertEqual(who.namedEntityTag, 'undef')
        self.assertEqual(who.dependency, 'nsubj')
        self.assertEqual(who.parent, wrote)
        self.assertEqual(len(who.child), 0)
        self.assertEqual(who.subtreeType, 'undef')
        self.assertEqual(who.dfsTag, 0)
        # Lucy in the Sky with Diamondss
        lucy=wrote.child[1]
        self.assertEqual(lucy.wordList, [Word("Lucy in the Sky with Diamonds", 3, 'QUOTE')])
        self.assertEqual(lucy.namedEntityTag, 'QUOTATION')
        self.assertEqual(lucy.dependency, 'dobj')
        self.assertEqual(lucy.parent, wrote)
        self.assertEqual(len(lucy.child), 1)
        self.assertEqual(lucy.subtreeType, 'undef')
        self.assertEqual(lucy.dfsTag, 0)
        # Let it be
        let=lucy.child[0]
        self.assertEqual(let.wordList, [Word("Let It Be", 5, 'QUOTE')])
        self.assertEqual(let.namedEntityTag, 'QUOTATION')
        self.assertEqual(let.dependency, 'conj_and')
        self.assertEqual(let.parent, lucy)
        self.assertEqual(len(let.child), 0)
        self.assertEqual(let.subtreeType, 'undef')
        self.assertEqual(let.dfsTag, 0)

    def testEntityTagMerge1(self):
        tree=computeTree(data.give_john_smith()['sentences'][0])
        preprocessingMerge(tree)
        tree.sort()
        root=tree
        # Root
        self.assertEqual(root.wordList, [Word("ROOT", 0)])
        self.assertEqual(root.namedEntityTag, 'undef')
        self.assertEqual(root.dependency, 'undef')
        self.assertEqual(root.parent, None)
        self.assertEqual(len(root.child), 1)
        self.assertEqual(root.subtreeType, 'undef')
        self.assertEqual(root.dfsTag, 0)
        # Lives
        lives=root.child[0]
        self.assertEqual(lives.wordList, [Word("lives in", 3, 'VBZ')])
        self.assertEqual(lives.namedEntityTag, 'undef')
        self.assertEqual(lives.dependency, 'root')
        self.assertEqual(lives.parent, tree)
        self.assertEqual(len(lives.child), 2)
        self.assertEqual(lives.subtreeType, 'undef')
        self.assertEqual(lives.dfsTag, 0)
        # John Smith
        smith=lives.child[0]
        self.assertEqual(smith.wordList, [Word("John", 1, 'NNP'), Word("Smith", 2, 'NNP')])
        self.assertEqual(smith.namedEntityTag, 'PERSON')
        self.assertEqual(smith.dependency, 'nsubj')
        self.assertEqual(smith.parent, lives)
        self.assertEqual(len(smith.child), 0)
        self.assertEqual(smith.subtreeType, 'undef')
        self.assertEqual(smith.dfsTag, 0)
        # United Kingdom
        kingdom=lives.child[1]
        self.assertEqual(kingdom.wordList, [Word("United", 6, 'NNP'), Word("Kingdom", 7, 'NNP')])
        self.assertEqual(kingdom.namedEntityTag, 'LOCATION')
        self.assertEqual(kingdom.dependency, 'prep')
        self.assertEqual(kingdom.parent, lives)
        self.assertEqual(len(kingdom.child), 1)
        self.assertEqual(kingdom.subtreeType, 'undef')
        self.assertEqual(kingdom.dfsTag, 0)
        # The
        the=kingdom.child[0]
        self.assertEqual(the.wordList, [Word("the", 5, 'DT')])
        self.assertEqual(the.namedEntityTag, 'undef')
        self.assertEqual(the.dependency, 'det')
        self.assertEqual(the.parent, kingdom)
        self.assertEqual(len(the.child), 0)
        self.assertEqual(the.subtreeType, 'undef')
        self.assertEqual(the.dfsTag, 0)

    def testEntityTagMerge2(self):
        tree=computeTree(data.give_obama_president_usa()['sentences'][0])
        preprocessingMerge(tree)
        tree.sort()
        root=tree
        # Root
        self.assertEqual(root.wordList, [Word("ROOT", 0)])
        self.assertEqual(root.namedEntityTag, 'undef')
        self.assertEqual(root.dependency, 'undef')
        self.assertEqual(root.parent, None)
        self.assertEqual(len(root.child), 1)
        self.assertEqual(root.subtreeType, 'undef')
        self.assertEqual(root.dfsTag, 0)
        # Is
        is_=root.child[0]
        self.assertEqual(is_.wordList, [Word("is", 2, 'VBZ')])
        self.assertEqual(is_.namedEntityTag, 'undef')
        self.assertEqual(is_.dependency, 'root')
        self.assertEqual(is_.parent, tree)
        self.assertEqual(len(is_.child), 2)
        self.assertEqual(is_.subtreeType, 'undef')
        self.assertEqual(is_.dfsTag, 0)
        # Obama
        obama=is_.child[0]
        self.assertEqual(obama.wordList, [Word("Obama", 1, 'NNP')])
        self.assertEqual(obama.namedEntityTag, 'PERSON')
        self.assertEqual(obama.dependency, 'nsubj')
        self.assertEqual(obama.parent, is_)
        self.assertEqual(len(obama.child), 0)
        self.assertEqual(obama.subtreeType, 'undef')
        self.assertEqual(obama.dfsTag, 0)
        # president
        president =is_.child[1]
        self.assertEqual(president.wordList, [Word("president", 6, 'NN')])
        self.assertEqual(president.namedEntityTag, 'undef')
        self.assertEqual(president.dependency, 'xcomp')
        self.assertEqual(president.parent, is_)
        self.assertEqual(len(president.child), 2)
        self.assertEqual(president.subtreeType, 'undef')
        self.assertEqual(president.dfsTag, 0)
        # The
        the=president.child[0]
        self.assertEqual(the.wordList, [Word("the", 3, 'DT')])
        self.assertEqual(the.namedEntityTag, 'undef')
        self.assertEqual(the.dependency, 'det')
        self.assertEqual(the.parent, president)
        self.assertEqual(len(the.child), 0)
        self.assertEqual(the.subtreeType, 'undef')
        self.assertEqual(the.dfsTag, 0)
        # United States
        united=president.child[1]
        self.assertEqual(united.wordList, [Word("United", 4, 'NNP'), Word("States", 5, 'NNPS')])
        self.assertEqual(united.namedEntityTag, 'LOCATION')
        self.assertEqual(united.dependency, 'nn')
        self.assertEqual(united.parent, president)
        self.assertEqual(len(united.child), 0)
        self.assertEqual(united.subtreeType, 'undef')
        self.assertEqual(united.dfsTag, 0)

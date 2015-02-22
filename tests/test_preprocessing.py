import json
from nltk.stem.wordnet import WordNetLemmatizer
from ppp_questionparsing_grammatical import Word, QuotationHandler, DependenciesTree, computeTree, QuotationError
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

    def testQuotationMerge(self):
        handler = QuotationHandler('foo')
        sentence = 'Who wrote "Lucy in the Sky with Diamonds" and "Let It Be"?'
        nonAmbiguousSentence = handler.pull(sentence)
        result=data.give_LSD_LIB()
        tree=computeTree(result['sentences'][0])
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

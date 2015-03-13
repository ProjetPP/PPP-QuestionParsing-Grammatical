import json
import itertools
from nltk.stem.wordnet import WordNetLemmatizer
from ppp_questionparsing_grammatical import Word, QuotationHandler, DependenciesTree, computeTree, QuotationError
import data

from unittest import TestCase

class PreprocessingMergeTests(TestCase):

    #####################
    # Quotation handler #
    #####################

    def testBasicQuotationHandler(self):
        for quotes in ['""', '“”', '‘’', '«»']:
            handler = QuotationHandler("foo")
            sentence = 'The person who sings {0}Let It Be{1} and {0}Lucy in the Sky with Diamonds{1} also sings {0}Yellow Submarine{1}.'.format(quotes[0], quotes[1])
            expected = 'The person who sings foo21 and foo37 also sings foo80.'
            real = handler.pull(sentence)
            self.assertEqual(real, expected)
            self.assertEqual(handler.quotations['foo21'], 'Let It Be')
            self.assertEqual(handler.quotations['foo37'], 'Lucy in the Sky with Diamonds')
            self.assertEqual(handler.quotations['foo80'], 'Yellow Submarine')

    def testRandomQuotationHandler(self):
        for quotes in ['""', '“”', '‘’', '«»']:
            handler = QuotationHandler()
            sentence = 'The person who sings {0}Let It Be{1} and {0}Lucy in the Sky with Diamonds{1} also sings {0}Yellow Submarine{1}.'.format(quotes[0], quotes[1])
            real = handler.pull(sentence)
            for replacement, original in handler.quotations.items():
                real = real.replace(replacement, '%s%s%s' % (quotes[0], original, quotes[1]))
            self.assertEqual(real, sentence)

    def testNestedQuotation(self):
        for quotes in itertools.permutations(['""', '“”', '‘’', '«»'], 2):
            handler = QuotationHandler('foo')
            sentence = 'This {0}is {2}a nested{3} quotation{1} for tests purposes.'.format(quotes[0][0], quotes[0][1], quotes[1][0], quotes[1][1])
            expected = 'This foo5 for tests purposes.'
            real = handler.pull(sentence)
            self.assertEqual(real, expected)
            self.assertEqual(handler.quotations['foo5'], 'is {0}a nested{1} quotation'.format(quotes[1][0], quotes[1][1]))

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

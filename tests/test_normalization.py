import json

from ppp_questionparsing_grammatical import computeTree, simplify, DependenciesTree,\
    QuotationHandler, normalFormProduction, GrammaticalError, NamedEntityMerging, PrepositionMerging
import data

from unittest import TestCase

class StandardTripleTests(TestCase):

    def testAndnormalFormProduction(self):
        tree = computeTree(data.give_chief()['sentences'][0])
        NamedEntityMerging(tree).merge()
        PrepositionMerging(tree).merge()
        qw = simplify(tree)
        result = normalFormProduction(tree, qw)
        self.assertEqual(result, {
    "list": [
        {
            "type": "triple",
            "subject": {
                "type": "resource",
                "value": "chief"
            },
            "object": {
                "type": "missing"
            },
            "predicate": {
                "list": [
                    {
                        "type": "resource",
                        "value": "identity"
                    }
                ],
                "type": "list"
            }
        },
        {
            "type": "triple",
            "subject": {
                "type": "resource",
                "value": "prime minister"
            },
            "object": {
                "type": "missing"
            },
            "predicate": {
                "list": [
                    {
                        "type": "resource",
                        "value": "identity"
                    }
                ],
                "type": "list"
            }
        }
    ],
    "type": "intersection"
})

    def testSuperlativenormalFormProduction(self):
        tree = computeTree(data.give_opera()['sentences'][0])
        NamedEntityMerging(tree).merge()
        PrepositionMerging(tree).merge()
        qw = simplify(tree)
        result = normalFormProduction(tree, qw)
        self.assertEqual(result, {
    "list": [
        {
            "list": {
                "predicate": {
                    "value": "default",
                    "type": "resource"
                },
                "list": {
                    "value": "Gilbert",
                    "type": "resource"
                },
                "type": "sort"
            },
            "type": "first"
        },
        {
            "list": {
                "predicate": {
                    "value": "default",
                    "type": "resource"
                },
                "list": {
                    "value": "Sullivan opera",
                    "type": "resource"
                },
                "type": "sort"
            },
            "type": "first"
        }
    ],
    "type": "intersection"
})

    def testnormalFormProduction1(self):
        tree = computeTree(data.give_president_of_USA()['sentences'][0])
        NamedEntityMerging(tree).merge()
        PrepositionMerging(tree).merge()
        qw = simplify(tree)
        result = normalFormProduction(tree, qw)
        self.assertEqual(result, {
    "object": {
        "type": "missing"
    },
    "subject": {
        "type": "resource",
        "value": "United States"
    },
    "predicate": {
        "type": "resource",
        "value": "president"
    },
    "type": "triple"
})

    def testnormalFormProduction2(self):
        handler = QuotationHandler('foo')
        sentence = 'Who wrote "Lucy in the Sky with Diamonds" and "Let It Be"?'
        nonAmbiguousSentence = handler.pull(sentence)
        result=data.give_LSD_LIB()
        tree=computeTree(result['sentences'][0])
        handler.push(tree)
        NamedEntityMerging(tree).merge()
        PrepositionMerging(tree).merge()
        qw = simplify(tree)
        result = normalFormProduction(tree, qw)
        self.assertEqual(result, {
    "list": [
        {
            "inverse-predicate": {
                "list": [
                    {
                        "value": "author",
                        "type": "resource"
                    },
                    {
                        "value": "writer",
                        "type": "resource"
                    }
                ],
                "type": "list"
            },
            "subject": {
                "type": "missing"
            },
            "object": {
                "value": "Lucy in the Sky with Diamonds",
                "type": "resource"
            },
            "type": "triple",
            "predicate": {
                "list": [
                    {
                        "value": "written",
                        "type": "resource"
                    },
                    {
                        "value": "literary works",
                        "type": "resource"
                    },
                    {
                        "value": "bibliography",
                        "type": "resource"
                    },
                    {
                        "value": "work",
                        "type": "resource"
                    },
                    {
                        "value": "works",
                        "type": "resource"
                    }
                ],
                "type": "list"
            }
        },
        {
            "inverse-predicate": {
                "list": [
                    {
                        "value": "author",
                        "type": "resource"
                    },
                    {
                        "value": "writer",
                        "type": "resource"
                    }
                ],
                "type": "list"
            },
            "subject": {
                "type": "missing"
            },
            "object": {
                "value": "Let It Be",
                "type": "resource"
            },
            "type": "triple",
            "predicate": {
                "list": [
                    {
                        "value": "written",
                        "type": "resource"
                    },
                    {
                        "value": "literary works",
                        "type": "resource"
                    },
                    {
                        "value": "bibliography",
                        "type": "resource"
                    },
                    {
                        "value": "work",
                        "type": "resource"
                    },
                    {
                        "value": "works",
                        "type": "resource"
                    }
                ],
                "type": "list"
            }
        }
    ],
    "type": "intersection"
})

    def testnormalFormProduction3(self):
        tree = computeTree(data.give_obama_president_usa()['sentences'][0])
        NamedEntityMerging(tree).merge()
        PrepositionMerging(tree).merge()
        qw = simplify(tree)
        result = normalFormProduction(tree, qw)
        self.assertEqual(result, {
    "type": "intersection",
    "list": [
        {
            "predicate": {
                "type": "list",
                "list": [
                    {
                        "type": "resource",
                        "value": "been"
                    },
                    {
                        "type": "resource",
                        "value": "identity"
                    }
                ]
            },
            "type": "triple",
            "subject": {
                "type": "resource",
                "value": "Obama"
            },
            "inverse-predicate": {
                "type": "resource",
                "value": "identity"
            },
            "object": {
                "type": "missing"
            }
        },
        {
            "predicate": {
                "type": "list",
                "list": [
                    {
                        "type": "resource",
                        "value": "been"
                    },
                    {
                        "type": "resource",
                        "value": "identity"
                    }
                ]
            },
            "type": "triple",
            "subject": {
                "type": "resource",
                "value": "United States president"
            },
            "inverse-predicate": {
                "type": "resource",
                "value": "identity"
            },
            "object": {
                "type": "missing"
            }
        }
    ]
})

    def testnormalFormProductionR8(self):
        tree = computeTree(data.mistake()['sentences'][0])
        NamedEntityMerging(tree).merge()
        PrepositionMerging(tree).merge()
        qw = simplify(tree)
        result = normalFormProduction(tree, qw)
        self.assertEqual(result, {
    "subject": {
        "type": "resource",
        "value": "mistake"
    },
    "object": {
        "type": "missing"
    },
    "predicate": {
        "type": "list",
        "list": [
            {
                "type": "resource",
                "value": "place"
            },
            {
                "type": "resource",
                "value": "location"
            },
            {
                "type": "resource",
                "value": "residence"
            },
            {
                "type": "resource",
                "value": "country"
            }
        ]
    },
    "type": "triple"
})


    def testnormalFormProductionSuperl(self):
        tree = computeTree(data.tanzania()['sentences'][0])
        NamedEntityMerging(tree).merge()
        PrepositionMerging(tree).merge()
        qw = simplify(tree)
        result = normalFormProduction(tree, qw)
        self.assertEqual(result, {
    "list": {
        "list": {
            "object": {
                "type": "missing"
            },
            "predicate": {
                "value": "mountain",
                "type": "resource"
            },
            "subject": {
                "value": "Tanzania",
                "type": "resource"
            },
            "type": "triple"
        },
        "predicate": {
                    "value" : "height",
                    "type"  : "resource"
                },
        "type": "sort"
    },
    "type": "last"
})

    def testnormalFormProductionSuperl2(self):
        tree = computeTree(data.car()['sentences'][0])
        NamedEntityMerging(tree).merge()
        PrepositionMerging(tree).merge()
        qw = simplify(tree)
        result = normalFormProduction(tree, qw)
        self.assertEqual(result, {
    "list": {
        "list": {
            "subject": {
                "value": "world",
                "type": "resource"
            },
            "predicate": {
                "value": "car",
                "type": "resource"
            },
            "object": {
                "type": "missing"
            },
            "type": "triple"
        },
        "predicate": {
                    "value" : "cost",
                    "type"  : "resource"
                },
        "type": "sort"
    },
    "type": "last"
})

    def testCop(self):
        tree = computeTree(data.black()['sentences'][0])
        NamedEntityMerging(tree).merge()
        PrepositionMerging(tree).merge()
        self.assertRaises(GrammaticalError, lambda: simplify(tree))

    def testExists(self):
        tree = computeTree(data.king_england()['sentences'][0])
        NamedEntityMerging(tree).merge()
        PrepositionMerging(tree).merge()
        qw = simplify(tree)
        result = normalFormProduction(tree, qw)
        self.assertEqual(result, {
    "list": {
        "predicate": {
            "type": "resource",
            "value": "king"
        },
        "subject": {
            "type": "resource",
            "value": "England"
        },
        "type": "triple",
        "object": {
            "type": "missing"
        }
    },
    "type": "exists"
})

    def testSemiQuestionWord1(self):
        tree = computeTree(data.roald()['sentences'][0])
        NamedEntityMerging(tree).merge()
        PrepositionMerging(tree).merge()
        qw = simplify(tree)
        result = normalFormProduction(tree, qw)
        self.assertEqual(result, {
    "subject": {
        "value": "Roald Dahl",
        "type": "resource"
    },
    "type": "triple",
    "predicate": {
        "value": "book",
        "type": "resource"
    },
    "object": {
        "type": "missing"
    }
})

    def testSemiQuestionWord3(self):
        tree = computeTree(data.list_president2()['sentences'][0])
        NamedEntityMerging(tree).merge()
        PrepositionMerging(tree).merge()
        qw = simplify(tree)
        result = normalFormProduction(tree, qw)
        self.assertEqual(result, {
    "type": "triple",
    "object": {
        "type": "missing"
    },
    "predicate": {
        "type": "resource",
        "value": "president"
    },
    "subject": {
        "type": "resource",
        "value": "France"
    }
})

    def testSemiQuestionWord4(self):
        tree = computeTree(data.capital1()['sentences'][0])
        NamedEntityMerging(tree).merge()
        PrepositionMerging(tree).merge()
        qw = simplify(tree)
        result = normalFormProduction(tree, qw)
        self.assertEqual(result, {
    "predicate": {
        "type": "resource",
        "value": "capital"
    },
    "type": "triple",
    "subject": {
        "type": "resource",
        "value": "France"
    },
    "object": {
        "type": "missing"
    }
})

    def testSemiQuestionWord5(self):
        tree = computeTree(data.capital2()['sentences'][0])
        NamedEntityMerging(tree).merge()
        PrepositionMerging(tree).merge()
        qw = simplify(tree)
        result = normalFormProduction(tree, qw)
        self.assertEqual(result, {
    "predicate": {
        "type": "resource",
        "value": "capital"
    },
    "type": "triple",
    "subject": {
        "type": "resource",
        "value": "France"
    },
    "object": {
        "type": "missing"
    }
})

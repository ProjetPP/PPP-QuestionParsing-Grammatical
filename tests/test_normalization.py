import json

from ppp_questionparsing_grammatical import computeTree, simplify, DependenciesTree, QuotationHandler, normalize
#from ppp_datamodel import Resource, Missing
import data

from unittest import TestCase

class StandardTripleTests(TestCase):

    def testAndNormalize(self):
        tree = computeTree(data.give_chief()['sentences'][0])
        qw = simplify(tree)
        result = normalize(tree)
        self.assertEqual(result,{
    "type": "intersection",
    "list": [
        {
            "subject": {
                "value": "chief",
                "type": "resource"
            },
            "type": "triple",
            "predicate": {
                "value": "identity",
                "type": "resource"
            },
            "object": {
                "type": "missing"
            }
        },
        {
            "subject": {
                "value": "prime minister",
                "type": "resource"
            },
            "type": "triple",
            "predicate": {
                "value": "identity",
                "type": "resource"
            },
            "object": {
                "type": "missing"
            }
        }
    ]
}
)

    def testSuperlativeNormalize(self):
        tree = computeTree(data.give_opera()['sentences'][0])
        qw = simplify(tree)
        result = normalize(tree)
        self.assertEqual(result,{
    "list": [
        {
            "list": {
                "list": {
                    "value": "Gilbert",
                    "type": "resource"
                },
                "predicate": "default",
                "type": "sort"
            },
            "type": "first"
        },
        {
            "list": {
                "list": {
                    "value": "Sullivan opera",
                    "type": "resource"
                },
                "predicate": "default",
                "type": "sort"
            },
            "type": "first"
        }
    ],
    "type": "intersection"
}
)

    def testNormalize1(self):
        tree = computeTree(data.give_president_of_USA()['sentences'][0])
        qw = simplify(tree)
        result = normalize(tree)
        self.assertEqual(result,{
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

    def testNormalize2(self):
        handler = QuotationHandler('foo')
        sentence = 'Who wrote "Lucy in the Sky with Diamonds" and "Let It Be"?'
        nonAmbiguousSentence = handler.pull(sentence)
        result=data.give_LSD_LIB()
        tree=computeTree(result['sentences'][0])
        handler.push(tree)
        qw = simplify(tree)
        result = normalize(tree)
        self.assertEqual(result,{
    "list": [
        {
            "object": {
                "type": "missing"
            },
            "subject": {
                "value": "Lucy in the Sky with Diamonds",
                "type": "resource"
            },
            "type": "triple",
            "predicate": {
                "value": "writer",
                "type": "resource"
            }
        },
        {
            "object": {
                "type": "missing"
            },
            "subject": {
                "value": "Let It Be",
                "type": "resource"
            },
            "type": "triple",
            "predicate": {
                "value": "writer",
                "type": "resource"
            }
        }
    ],
    "type": "intersection"
})

    def testNormalize3(self):
        tree = computeTree(data.give_obama_president_usa()['sentences'][0])
        qw = simplify(tree)
        result = normalize(tree)
        self.assertEqual(result,{
    "type": "intersection",
    "list": [
        {
            "object": {
                "type": "missing"
            },
            "type": "triple",
            "predicate": {
                "value": "identity",
                "type": "resource"
            },
            "subject": {
                "value": "Obama",
                "type": "resource"
            }
        },
        {
            "object": {
                "value": "United States president",
                "type": "resource"
            },
            "type": "triple",
            "predicate": {
                "value": "identity",
                "type": "resource"
            },
            "subject": {
                "type": "missing"
            }
        }
    ]
})

    def testNormalizeR8(self):
        tree = computeTree(data.mistake()['sentences'][0])
        qw = simplify(tree)
        result = normalize(tree)
        self.assertEqual(result,{
    "predicate": {
        "value": "location",
        "type": "resource"
    },
    "object": {
        "type": "missing"
    },
    "subject": {
        "value": "mistake",
        "type": "resource"
    },
    "type": "triple"
})

    def testNormalizeR3(self):
        tree = computeTree(data.king()['sentences'][0])
        qw = simplify(tree)
        result = normalize(tree)
        self.assertEqual(result,{
    "type": "intersection",
    "list": [
        {
            "predicate": {
                "value": "king",
                "type": "resource"
            },
            "subject": {
                "type": "missing"
            },
            "type": "triple",
            "object": {
                "value": "Louis XIV",
                "type": "resource"
            }
        },
        {
            "predicate": {
                "value": "Louis XIV",
                "type": "resource"
            },
            "subject": {
                "value": "France",
                "type": "resource"
            },
            "type": "triple",
            "object": {
                "type": "missing"
            }
        }
    ]
})

    def testNormalizeSuperl(self):
        tree = computeTree(data.tanzania()['sentences'][0])
        qw = simplify(tree)
        result = normalize(tree)
        self.assertEqual(result,{
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
        "predicate": "height",
        "type": "sort"
    },
    "type": "last"
})

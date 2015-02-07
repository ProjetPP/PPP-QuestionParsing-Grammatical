from demo6 import get_answer
import json
import sys
import os
from ppp_questionparsing_grammatical.data.exceptions import GrammaticalError, QuotationError, QuestionWordError

INDENT_NUMBER=4
BASE_INDENT=1

class TripleError(Exception):
    """
        Raised when a triple contains connectors (e.g. AND, FIRST).
    """
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message

symbol = {
    'missing': 'M',
    'resource': 'R',
    'triple': 'T',
    'list': 'List',
    'intersection': 'I',
    'union': 'U',
    'exists': 'E',
    'first': 'F',
    'last': 'L',
    'sort': 'S',
}

def smallDepth(t):
    allowedTypes = {'resource', 'missing'}
    return t.subject.type in allowedTypes and t.predicate.type in allowedTypes and t.object.type in allowedTypes

def string_of_triple(t, indent=BASE_INDENT):
    if t.type == 'missing':
        return '%s%s()' % (' '*indent*INDENT_NUMBER, symbol[t.type])
    elif t.type == 'resource':
        return '%s%s("%s")' % (' '*indent*INDENT_NUMBER, symbol[t.type], t.value)
    elif t.type == 'triple':
        if smallDepth(t):
            i = 0
        else:
            i = indent+1
        _subject = string_of_triple(t.subject, i)
        _predicate = string_of_triple(t.predicate, i)
        _object = string_of_triple(t.object, i)
        if smallDepth(t):
            return '%s%s(%s, %s, %s)' % (' '*indent*INDENT_NUMBER, symbol[t.type], _subject, _predicate, _object)
        else:
            return '{0}{1}(\n{2},\n{3},\n{4}\n{0})'.format(' '*indent*INDENT_NUMBER, symbol[t.type], _subject, _predicate, _object)
    elif t.type in {'list', 'intersection', 'union'}:
        l = ',\n'.join(string_of_triple(x, indent+1) for x in t.list)
        return '{0}{1}([\n{2}\n{0}])'.format(' '*indent*INDENT_NUMBER, symbol[t.type], l)
    elif t.type in {'exists', 'first', 'last', 'sort'}:
        l = string_of_triple(t.list, indent+1)
        return '{0}{1}(\n{2}\n{0})'.format(' '*indent*INDENT_NUMBER, symbol[t.type], l)
    raise TripleError(t,"Wrong triple (new datamodel connectors?).")

def process_string(s):
    return string_of_triple(get_answer(s))

if __name__ == "__main__":
    flag = False
    print('data = {')
    while True:
        try:
            s = input("")
        except EOFError:
            break
        try:
            result = process_string(s)
        except GrammaticalError:
            sys.stderr.write("#GrammaticalError:\t{0}\n".format(s))
            continue
        except QuotationError:
            sys.stderr.write("#QuotationError:\t{0}\n".format(s))
            continue
        except QuestionWordError:
            sys.stderr.write("#QuestionWordError:\t{0}\n".format(s))
            continue
        except RuntimeError:
            sys.stderr.write("#RuntimeError:\t{0}\n".format(s))
            continue
        except IndexError:
            sys.stderr.write("#IndexError:\t{0}\n".format(s))
            continue
        if flag:
            print('')
        else:
            flag=True
        print('%s\'%s\':' % (' '*BASE_INDENT*INDENT_NUMBER, s))
        print('%s,' % result)
    print('}')

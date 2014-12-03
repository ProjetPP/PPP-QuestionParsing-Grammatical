from demo7 import get_answer
import json

class TripleError(Exception):
    """
        Raised when a triple contains connectors (e.g. AND, FIRST).
    """
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message

def string_of_triple(t,missing,separator):
    if t.type == 'missing':
        return missing
    if t.type == 'resource':
        return str(t.value)
    if t.type == 'triple':
        _subject = string_of_triple(t.subject,missing,separator)
        _predicate = string_of_triple(t.predicate,missing,separator)
        _object = string_of_triple(t.object,missing,separator)
        return "({1}{0}{2}{0}{3})".format(separator,_subject,_predicate,_object)
    raise TripleError(t,"Wrong triple (new datamodel connectors?).")


def process_string(s,missing='?',separator=','):
    return string_of_triple(get_answer(s),missing,separator)

if __name__ == "__main__":
    while True:
        try:
            s = input("")
        except EOFError:
            break
        print(s)
        print(process_string(s))

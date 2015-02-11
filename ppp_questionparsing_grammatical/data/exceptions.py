class GrammaticalError(Exception):
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message

class QuotationError(Exception):
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message

class NounificationError(Exception):
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message

class GrammaticalError(Exception):
    """
        Raised when a triple contains connectors (e.g. AND, FIRST).
    """
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message

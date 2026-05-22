class OrhunError(Exception):
    pass


class LexerError(OrhunError):
    pass


class ParserError(OrhunError):
    pass


class SemanticError(OrhunError):
    pass
from tokens import Token, KEYWORDS
from errors import LexerError


class Lexer:
    def __init__(self, source):
        self.source = source
        self.pos = 0
        self.line = 1
        self.column = 1

    def current(self):
        if self.pos >= len(self.source):
            return None
        return self.source[self.pos]

    def peek(self):
        if self.pos + 1 >= len(self.source):
            return None
        return self.source[self.pos + 1]

    def advance(self):
        ch = self.current()
        self.pos += 1

        if ch == "\n":
            self.line += 1
            self.column = 1
        else:
            self.column += 1

        return ch

    def skip_whitespace(self):
        while self.current() is not None and self.current().isspace():
            self.advance()

    def skip_comment(self):
        while self.current() is not None and self.current() != "\n":
            self.advance()

    def number(self):
        line, col = self.line, self.column
        value = ""

        while self.current() is not None and self.current().isdigit():
            value += self.advance()

        return Token("NUMBER", int(value), line, col)

    def string(self):
        line, col = self.line, self.column
        self.advance()
        value = ""

        while self.current() is not None and self.current() != '"':
            value += self.advance()

        if self.current() != '"':
            raise LexerError(f"Lexer Error [{line}:{col}] String kapanmadı.")

        self.advance()
        return Token("STRING", value, line, col)

    def identifier(self):
        line, col = self.line, self.column
        value = ""

        while self.current() is not None and (
            self.current().isalnum() or self.current() == "_"
        ):
            value += self.advance()

        if value in {"var", "yok"}:
            return Token("BOOLEAN", value == "var", line, col)

        if value in KEYWORDS:
            return Token("KEYWORD", value, line, col)

        return Token("IDENTIFIER", value, line, col)

    def tokenize(self):
        tokens = []

        while self.current() is not None:
            ch = self.current()

            if ch.isspace():
                self.skip_whitespace()
                continue

            if ch == "/" and self.peek() == "/":
                self.skip_comment()
                continue

            if ch.isdigit():
                tokens.append(self.number())
                continue

            if ch.isalpha() or ch == "_":
                tokens.append(self.identifier())
                continue

            if ch == '"':
                tokens.append(self.string())
                continue

            line, col = self.line, self.column

            two = ch + (self.peek() or "")

            if two in {"==", "!=", ">=", "<=", "=>"}:
                self.advance()
                self.advance()
                tokens.append(Token("OPERATOR", two, line, col))
                continue

            if ch in "+-*/=><":
                self.advance()
                tokens.append(Token("OPERATOR", ch, line, col))
                continue

            if ch in "(){};":
                self.advance()
                tokens.append(Token("PUNCTUATION", ch, line, col))
                continue

            raise LexerError(f"Lexer Error [{line}:{col}] Geçersiz karakter: {ch}")

        tokens.append(Token("EOF", None, self.line, self.column))
        return tokens
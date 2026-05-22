from ast_nodes import *
from errors import ParserError


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current(self):
        return self.tokens[self.pos]

    def advance(self):
        self.pos += 1

    def match(self, token_type, value=None):
        token = self.current()

        if token.type != token_type:
            raise ParserError(
                f"Parser Error [{token.line}:{token.column}] "
                f"{token_type} bekleniyor."
            )

        if value is not None and token.value != value:
            raise ParserError(
                f"Parser Error [{token.line}:{token.column}] "
                f"'{value}' bekleniyor."
            )

        self.advance()
        return token

    def parse(self):
        self.match("KEYWORD", "bitig")
        block = self.block()
        self.match("EOF")
        return ProgramNode(block)

    def block(self):
        self.match("PUNCTUATION", "{")

        statements = []

        while not (
            self.current().type == "PUNCTUATION"
            and self.current().value == "}"
        ):
            statements.append(self.statement())

        self.match("PUNCTUATION", "}")

        return BlockNode(statements)

    def statement(self):
        token = self.current()

        if token.type == "KEYWORD":

            if token.value == "tamga":
                return self.var_decl()

            if token.value == "sesver":
                return self.print_stmt()

            if token.value == "yokla":
                return self.if_stmt()

            if token.value == "yuru":
                return self.while_stmt()

            if token.value == "kurultay":
                return self.kurultay_stmt()

        if token.type == "IDENTIFIER":
            return self.assignment()

        raise ParserError(
            f"Parser Error [{token.line}:{token.column}] Geçersiz ifade."
        )

    def var_decl(self):
        self.match("KEYWORD", "tamga")

        var_type = self.match("KEYWORD").value
        name = self.match("IDENTIFIER").value

        self.match("OPERATOR", "=")

        value = self.expression()

        self.match("PUNCTUATION", ";")

        return VarDeclNode(var_type, name, value)

    def assignment(self):
        name = self.match("IDENTIFIER").value

        self.match("OPERATOR", "=")

        value = self.expression()

        self.match("PUNCTUATION", ";")

        return AssignNode(name, value)

    def print_stmt(self):
        self.match("KEYWORD", "sesver")

        self.match("PUNCTUATION", "(")

        value = self.expression()

        self.match("PUNCTUATION", ")")
        self.match("PUNCTUATION", ";")

        return PrintNode(value)

    def if_stmt(self):
        self.match("KEYWORD", "yokla")

        self.match("PUNCTUATION", "(")

        condition = self.expression()

        self.match("PUNCTUATION", ")")

        then_block = self.block()

        else_block = None

        if (
            self.current().type == "KEYWORD"
            and self.current().value == "yada"
        ):
            self.advance()
            else_block = self.block()

        return IfNode(condition, then_block, else_block)

    def while_stmt(self):
        self.match("KEYWORD", "yuru")

        self.match("PUNCTUATION", "(")

        condition = self.expression()

        self.match("PUNCTUATION", ")")

        block = self.block()

        return WhileNode(condition, block)

    def kurultay_stmt(self):
        self.match("KEYWORD", "kurultay")

        self.match("PUNCTUATION", "(")

        expr = self.expression()

        self.match("PUNCTUATION", ")")

        self.match("PUNCTUATION", "{")

        cases = []
        default = None

        while not (
            self.current().type == "PUNCTUATION"
            and self.current().value == "}"
        ):

            if self.current().value == "boy":
                self.advance()

                case_value = self.expression()

                self.match("OPERATOR", "=>")

                stmt = self.statement()

                cases.append(CaseNode(case_value, stmt))

            elif self.current().value == "son":
                self.advance()

                self.match("OPERATOR", "=>")

                default = self.statement()

            else:
                token = self.current()

                raise ParserError(
                    f"Parser Error [{token.line}:{token.column}] "
                    f"Geçersiz kurultay bloğu."
                )

        self.match("PUNCTUATION", "}")

        return KurultayNode(expr, cases, default)

    def expression(self):
        return self.logic_or()

    def logic_or(self):
        node = self.logic_and()

        while (
            self.current().type == "KEYWORD"
            and self.current().value == "veya"
        ):
            op = self.current().value
            self.advance()

            right = self.logic_and()

            node = BinaryOpNode(node, op, right)

        return node

    def logic_and(self):
        node = self.equality()

        while (
            self.current().type == "KEYWORD"
            and self.current().value == "ve"
        ):
            op = self.current().value
            self.advance()

            right = self.equality()

            node = BinaryOpNode(node, op, right)

        return node

    def equality(self):
        node = self.comparison()

        while (
            self.current().type == "OPERATOR"
            and self.current().value in {"==", "!="}
        ):
            op = self.current().value
            self.advance()

            right = self.comparison()

            node = BinaryOpNode(node, op, right)

        return node

    def comparison(self):
        node = self.term()

        while (
            self.current().type == "OPERATOR"
            and self.current().value in {">", "<", ">=", "<="}
        ):
            op = self.current().value
            self.advance()

            right = self.term()

            node = BinaryOpNode(node, op, right)

        return node

    def term(self):
        node = self.factor()

        while (
            self.current().type == "OPERATOR"
            and self.current().value in {"+", "-"}
        ):
            op = self.current().value
            self.advance()

            right = self.factor()

            node = BinaryOpNode(node, op, right)

        return node

    def factor(self):
        node = self.unary()

        while (
            self.current().type == "OPERATOR"
            and self.current().value in {"*", "/"}
        ):
            op = self.current().value
            self.advance()

            right = self.unary()

            node = BinaryOpNode(node, op, right)

        return node

    def unary(self):
        token = self.current()

        if (
            token.type == "KEYWORD"
            and token.value == "degil"
        ):
            self.advance()

            return UnaryOpNode("degil", self.unary())

        if (
            token.type == "OPERATOR"
            and token.value == "-"
        ):
            self.advance()

            return UnaryOpNode("-", self.unary())

        return self.primary()

    def primary(self):
        token = self.current()

        if token.type == "NUMBER":
            self.advance()
            return NumberNode(token.value)

        if token.type == "STRING":
            self.advance()
            return StringNode(token.value)

        if token.type == "BOOLEAN":
            self.advance()
            return BooleanNode(token.value)

        if token.type == "IDENTIFIER":
            self.advance()
            return VariableNode(token.value)

        if token.type == "PUNCTUATION" and token.value == "(":
            self.advance()

            expr = self.expression()

            self.match("PUNCTUATION", ")")

            return expr

        raise ParserError(
            f"Parser Error [{token.line}:{token.column}] Geçersiz ifade."
        )
from ast_nodes import *
from errors import SemanticError


class Interpreter:
    def __init__(self):
        self.environment = {}

    def visit(self, node):

        method_name = f"visit_{type(node).__name__}"

        method = getattr(self, method_name)

        return method(node)

    def visit_ProgramNode(self, node):
        return self.visit(node.block)

    def visit_BlockNode(self, node):
        for stmt in node.statements:
            self.visit(stmt)

    def visit_VarDeclNode(self, node):

        value = self.visit(node.value)

        self.check_type(node.var_type, value)

        self.environment[node.name] = {
            "type": node.var_type,
            "value": value
        }

    def visit_AssignNode(self, node):

        if node.name not in self.environment:
            raise SemanticError(
                f"Semantic Error: '{node.name}' tanımlanmamış."
            )

        value = self.visit(node.value)

        expected_type = self.environment[node.name]["type"]

        self.check_type(expected_type, value)

        self.environment[node.name]["value"] = value

    def visit_PrintNode(self, node):
        value = self.visit(node.value)
        print(value)

    def visit_IfNode(self, node):

        condition = self.visit(node.condition)

        if condition:
            self.visit(node.then_block)

        elif node.else_block:
            self.visit(node.else_block)

    def visit_WhileNode(self, node):

        while self.visit(node.condition):
            self.visit(node.block)

    def visit_KurultayNode(self, node):

        value = self.visit(node.expr)

        matched = False

        for case in node.cases:

            case_value = self.visit(case.value)

            if value == case_value:
                matched = True
                self.visit(case.statement)
                break

        if not matched and node.default:
            self.visit(node.default)

    def visit_NumberNode(self, node):
        return node.value

    def visit_StringNode(self, node):
        return node.value

    def visit_BooleanNode(self, node):
        return node.value

    def visit_VariableNode(self, node):

        if node.name not in self.environment:
            raise SemanticError(
                f"Semantic Error: '{node.name}' tanımlanmamış."
            )

        return self.environment[node.name]["value"]

    def visit_UnaryOpNode(self, node):

        value = self.visit(node.expr)

        if node.op == "-":
            return -value

        if node.op == "degil":
            return not value

    def visit_BinaryOpNode(self, node):

        left = self.visit(node.left)
        right = self.visit(node.right)

        if node.op == "+":
            return left + right

        if node.op == "-":
            return left - right

        if node.op == "*":
            return left * right

        if node.op == "/":
            return left / right

        if node.op == "==":
            return left == right

        if node.op == "!=":
            return left != right

        if node.op == ">":
            return left > right

        if node.op == "<":
            return left < right

        if node.op == ">=":
            return left >= right

        if node.op == "<=":
            return left <= right

        if node.op == "ve":
            return left and right

        if node.op == "veya":
            return left or right

    def check_type(self, expected, value):

        if expected == "sayi" and not isinstance(value, int):
            raise SemanticError(
                "Semantic Error: sayi tipine uygun olmayan değer."
            )

        if expected == "yazi" and not isinstance(value, str):
            raise SemanticError(
                "Semantic Error: yazi tipine uygun olmayan değer."
            )

        if expected == "kut" and not isinstance(value, bool):
            raise SemanticError(
                "Semantic Error: kut tipine uygun olmayan değer."
            )
from dataclasses import dataclass


@dataclass
class ProgramNode:
    block: object


@dataclass
class BlockNode:
    statements: list


@dataclass
class VarDeclNode:
    var_type: str
    name: str
    value: object


@dataclass
class AssignNode:
    name: str
    value: object


@dataclass
class PrintNode:
    value: object


@dataclass
class IfNode:
    condition: object
    then_block: object
    else_block: object = None


@dataclass
class WhileNode:
    condition: object
    block: object


@dataclass
class KurultayNode:
    expr: object
    cases: list
    default: object = None


@dataclass
class CaseNode:
    value: object
    statement: object


@dataclass
class BinaryOpNode:
    left: object
    op: str
    right: object


@dataclass
class UnaryOpNode:
    op: str
    expr: object


@dataclass
class NumberNode:
    value: int


@dataclass
class StringNode:
    value: str


@dataclass
class BooleanNode:
    value: bool


@dataclass
class VariableNode:
    name: str
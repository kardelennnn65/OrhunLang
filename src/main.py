import sys

from lexer import Lexer
from parser import Parser
from interpreter import Interpreter
from errors import OrhunError


DEBUG = True


def main():
    if len(sys.argv) < 2:
        print("Kullanım:")
        print("python src/main.py examples/ordu.orh")
        return

    filename = sys.argv[1]

    try:
        with open(filename, "r", encoding="utf-8") as file:
            source = file.read()

        lexer = Lexer(source)
        tokens = lexer.tokenize()

        if DEBUG:
            print("\n--- TOKENLAR ---\n")
            for token in tokens:
                print(token)

        parser = Parser(tokens)
        tree = parser.parse()

        if DEBUG:
            print("\n--- AST ---\n")
            print(tree)

            print("\n--- PROGRAM CIKTISI ---\n")

        interpreter = Interpreter()
        interpreter.visit(tree)

    except OrhunError as error:
        print(error)


if __name__ == "__main__":
    main()
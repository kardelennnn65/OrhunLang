from dataclasses import dataclass


@dataclass
class Token:
    type: str
    value: object
    line: int
    column: int

    def __repr__(self):
        return f"Token({self.type}, {self.value}, line={self.line}, col={self.column})"


KEYWORDS = {
    "bitig", "tamga", "sayi", "yazi", "kut",
    "var", "yok",
    "sesver", "yokla", "yada", "yuru",
    "kurultay", "boy", "son",
    "ve", "veya", "degil"
}
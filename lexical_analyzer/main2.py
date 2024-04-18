KEY_WORDS = ['bool', 'break', 'char', 'continue', 'else', 'false', 'for', 'if', 'int', 'print', 'return', 'true']
KEY_WORDS.sort()

print(KEY_WORDS)
firsts = [st[0] for st in KEY_WORDS]
print(firsts)

# Identifier allowed characters
ID_CHARS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_'

OPERATORS = {
    '+': 'PLUS',
    '-': 'MINUS',
    '*': 'MULT',
    '/': 'DIV',
    '%': 'MOD',
    '==': 'EQUALS',
    '!=': 'NOT-EQUALS',
    '>': 'GT',
    '<': 'LT',
    '>=': 'GE',
    '<=': 'LE',
    '&&': 'AND',
    '||': 'OR',
    '!': 'NOT',
    '=': 'ASSIGN'
}
OPERATOR_KEYS = sorted(list(OPERATORS.keys()))

SEPARATORS = {
    '(': 'LP',
    ')': 'RP',
    '{': 'LCB',
    '}': 'RCB',
    '[': 'LSB',
    ']': 'RSB',
    ';': 'SEMICOLON',
    ',': 'COMMA'
}
SEPARATOR_KEYS = sorted(list(SEPARATORS.keys()))

QUOTATIONS = {
    '"': 'D-QUOTE',
    '\'': 'S-QUOTE'
}
QUOTATION_KEYS = sorted(list(QUOTATIONS.keys()))

WHITESPACE = {
    ' ': 'WS',
    '\n': 'NEWLINE',
    '\t': 'TAB'
}


class Token:
    def __init__(self, lexeme, row, column):
        self.lexeme = lexeme
        self.token_type = None
        self.token = None
        self.row = row + 1
        self.column = column + 1
        self.analyze_lexeme()

    def __str__(self):
        return f'{self.lexeme} -> {self.token_type} -> {self.token} -> row:{self.row}'


def keyword(line, col, row):
    match line[col]:
        case 'b':
            match line[col: col + 4]:
                case 'bool':
                    if line[col + 4] not in ID_CHARS:
                        return Token('bool', row, col), col + 4
            match line[col: col + 5]:
                case 'break':
                    if line[col + 5] not in ID_CHARS:
                        return Token('break', row, col), col + 5

        case 'c':
            match line[col: col + 4]:
                case 'char':
                    if line[col + 4] not in ID_CHARS:
                        return Token('char', row, col), col + 4
            match line[col: col + 8]:
                case 'continue':
                    if line[col + 8] not in ID_CHARS:
                        return Token('continue', row, col), col + 8

        case 'e':
            match line[col: col + 4]:
                case 'else':
                    if line[col + 4] not in ID_CHARS:
                        return Token('else', row, col), col + 4
                    else:
                        return None, col

        case 'f':
            match line[col: col + 5]:
                case 'false':
                    if line[col + 5] not in ID_CHARS:
                        return Token('false', row, col), col + 5
            match line[col: col + 3]:
                case 'for':
                    if line[col + 3] not in ID_CHARS:
                        return Token('for', row, col), col + 3

        case 'i':
            match line[col: col + 2]:
                case 'if':
                    if line[col + 2] not in ID_CHARS:
                        return Token('if', row, col), col + 2
            match line[col: col + 3]:
                case 'int':
                    if line[col + 3] not in ID_CHARS:
                        return Token('int', row, col), col + 3
        case 'p':
            match line[col: col + 5]:
                case 'print':
                    if line[col + 5] not in ID_CHARS:
                        return Token('print', row, col), col + 5
        case 'r':
            match line[col: col + 6]:
                case 'return':
                    if line[col + 6] not in ID_CHARS:
                        return Token('return', row, col), col + 6
        case 't':
            match line[col: col + 4]:
                case 'true':
                    if line[col + 4] not in ID_CHARS:
                        return Token('true', row, col), col + 4

    return None, col


def identifier(line, col, row):
    if line[col] in ID_CHARS:
        while line[col] in ID_CHARS:
            col += 1
        return Token(line[col: col], row, col), col
    return None, col


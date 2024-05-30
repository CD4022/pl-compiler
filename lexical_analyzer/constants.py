KEY_WORDS = ['bool', 'break', 'char', 'continue', 'else', 'false', 'for', 'if', 'int', 'print', 'return', 'true', 'void']
KEY_WORDS.sort()

# print(KEY_WORDS)
# firsts = [st[0] for st in KEY_WORDS]
# print(firsts)

# Identifier allowed characters
ID_CHARS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_'
HEX_DIGITS = '0123456789abcdefABCDEF'

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
# a list of all chars used in operators
OP_CHARS = list(set(''.join(OPERATOR_KEYS)))
# print(OP_CHARS)

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


KEY_WORDS = ['bool', 'break', 'char', 'continue', 'else', 'false', 'for', 'if', 'int', 'print', 'return', 'true']
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

SEPARATORS = {
    '(': 'LP',
    ')': 'RP',
    '{': 'LCB',
    '}': 'RCB',
    '[': 'LSB',
    ']': 'RSB',
    ';': 'SEMICOLON',
    ',': 'COMMA',
    '"': 'D-QUOTE',
    '\'': 'S-QUOTE'}

WHITESPACE = {
    ' ': 'WS',
    '\n': 'NEWLINE',
    '\t': 'TAB'
}


class Token:
    def __init__(self, lexeme, row):
        self.lexeme = lexeme
        self.token_type = None
        self.token = None
        self.row = row + 1
        self.analyze_lexeme()

    def __str__(self):
        return f'{self.lexeme} -> {self.token_type} -> {self.token} -> row:{self.row}'

    def is_key_word(self):
        return self.lexeme in KEY_WORDS

    def is_operator(self):
        return self.lexeme in OPERATORS.keys()

    def is_separator(self):
        return self.lexeme in SEPARATORS.keys()

    def is_whitespace(self):
        return self.lexeme in WHITESPACE.keys()

    def is_identifier(self):
        # if token starts with _ or a letter is an identifier
        if self.lexeme[0].isalpha() or self.lexeme[0] == '_':
            return True
        return False

    def is_constant(self):
        # if token is a number is a constant
        if self.lexeme.isdigit():
            return True
        elif self.lexeme[0] == "'" and self.lexeme[-1] == "'":
            return True
        return False

    def analyze_lexeme(self):
        if self.is_key_word():
            self.token_type = 'KEY_WORD'
            self.token = self.lexeme.upper()
        elif self.is_operator():
            self.token_type = 'OPERATOR'
            self.token = OPERATORS[self.lexeme]
        elif self.is_separator():
            self.token_type = 'SEPARATOR'
            self.token = SEPARATORS[self.lexeme]
        elif self.is_whitespace():
            self.token_type = 'WHITESPACE'
            self.token = WHITESPACE[self.lexeme]
        elif self.is_identifier():
            self.token_type = 'IDENTIFIER'
            self.token = 'ID'
        elif self.is_constant():
            self.token_type = 'CONSTANT'
            # TODO: check if constant is a number or a char
        else:
            raise ValueError(f'Invalid token: {self.lexeme}')


def is_comment(line):
    return line.startswith('//')


def analyze_line(line, row):
    tokens_str = line.split()
    tokens = []
    for token_str in tokens_str:
        # TODO: find the starting index of the token in the line
        tokens.append(Token(token_str, row))
    return tokens


def analyze_file(file_path):
    with open(file_path, 'r') as file:
        for row, line in enumerate(file):
            if is_comment(line):
                continue
            tokens = analyze_line(line, row)
            for token in tokens:
                print(token.__dict__)
                # TODO: find a way to pass the tokens to the parser


def main():
    analyze_file('test.pl')


if __name__ == '__main__':
    main()



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
    ',': 'COMMA'
}

QUOTATIONS = {
    '"': 'D-QUOTE',
    '\'': 'S-QUOTE'
}

WHITESPACE = {
    ' ': 'WS',
    '\n': 'NEWLINE',
    '\t': 'TAB'
}

RESERVED_CHARACTERS = '(){}[];,+-*/%<>=!&|"\' \n\t'


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

    def is_key_word(self):
        return self.lexeme in KEY_WORDS

    def is_operator(self):
        return self.lexeme in OPERATORS.keys()

    def is_separator(self):
        return self.lexeme in SEPARATORS.keys()

    def is_quotation(self):
        return self.lexeme in QUOTATIONS.keys()

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

    def is_comment(self):
        return self.lexeme.startswith('//')

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
        elif self.is_quotation():
            self.token_type = 'QUOTATION'
            self.token = QUOTATIONS[self.lexeme]
        elif self.is_whitespace():
            self.token_type = 'WHITESPACE'
            self.token = WHITESPACE[self.lexeme]
        elif self.is_identifier():
            self.token_type = 'IDENTIFIER'
            self.token = 'ID'
        elif self.is_constant():
            self.token_type = 'CONSTANT'
            # TODO: check if constant is a number or a char
        elif self.is_comment():
            self.token_type = 'COMMENT'
            self.token = 'COMMENT'
        else:
            raise ValueError(f'Invalid token: {self.lexeme}')


def is_comment(line):
    return line.startswith('//')


def space_separator(line):
    for separator in SEPARATORS.keys():
        line = line.replace(separator, f' {separator} ')
    return line


# def space_operator(line : str):
#     # find all double char operators
#     for operator in OPERATORS.keys():
#         if len(operator) == 2:
#             line = line.replace(operator, f' {operator} ')

#     # find all single char operators
#     for operator in OPERATORS.keys():
#         if len(operator) == 1:
#             if operator == '=':
#                 occurrences = [pos for pos, char in enumerate(line) if line[pos:pos+len(operator)] == operator]
#                 for occurrence in occurrences:
#                     if line[occurrence-1] != '!'\
#                             and line[occurrence-1] != '='\
#                             and line[occurrence-1] != '<'\
#                             and line[occurrence-1] != '>'\
#                             and line[occurrence+1] != '=':
#                         # replace the single occurrence of '=' with ' = '
#                         line = line[:occurrence] + ' = ' + line[occurrence+1:]

#             elif operator == '<' or operator == '>' or operator == '!':
#                 occurrences = [pos for pos, char in enumerate(line) if line[pos:pos+len(operator)] == operator]
#                 for occurrence in occurrences:
#                     if line[occurrence+1] != '=':
#                         # replace the single occurrence of '<' or '>' with ' < ' or ' > '
#                         line = line[:occurrence] + f' {operator} ' + line[occurrence+1:]

#             else:
#                 line = line.replace(operator, f' {operator} ')
#     return line

def space_operator(line):
    for i, char in enumerate(line):
        if char in OPERATORS.keys():
            if ((char == '=' and line[i+1] == '=' or line[i-1] == '=') or
            (char == '>' and line[i+1] == '=' or char == '=' and line[i-1] == '>') or
            (char == '<' and line[i+1] == '=' or char == '=' and line[i-1] == '<') or
            (char == '!' and line[i+1] == '=' or char == '=' and line[i-1] == '!')):
                line = line.replace(line[i:i+2], f' {line[i]}{line[i+1]} ')
                continue
            
            line = line.replace(char, f' {char} ')
    return line


def find_word_occurrences(word: str, line):
    occurrences = []
    # check if word contains reserved chars
    contains_reserved_char = False
    for char in RESERVED_CHARACTERS:
        if char in word:
            contains_reserved_char = True
            break
    for pos, char in enumerate(line):
        if (line[pos:pos+len(word)] == word and ((line[pos-1] in RESERVED_CHARACTERS
                                                 and line[pos+len(word)] in RESERVED_CHARACTERS)
                                                 or contains_reserved_char)):
            occurrences.append(pos)
    return occurrences


def analyze_line(line, row):
    tokens = []
    seen_words = set()

    # split by // and take the first part as the line and the rest as the comment
    if '//' in line:
        line, comment = line.split('//')
        tokens.append(Token('//' + comment, row, len(line) + 1))

    line = line + ' '

    spaced_line = space_separator(line)
    spaced_line = space_operator(spaced_line)

    for column, word in enumerate(spaced_line.split(), start=1):
        if word in seen_words:
            continue 
        seen_words.add(word)

        # Find all occurrences of the word in the line
        # word_occurrences = [pos for pos, char in enumerate(line) if line[pos:pos+len(word)] == word and
        #                     (line[pos-1] in RESERVED_CHARACTERS and line[pos+len(word)] in RESERVED_CHARACTERS)]

        word_occurrences = find_word_occurrences(word, line)

        for occurrence in word_occurrences:
            tokens.append(Token(word, row, occurrence))
        
    tokens.sort(key=lambda x: x.column)
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
    analyze_file('../test.pl')


if __name__ == '__main__':
    main()

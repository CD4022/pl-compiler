from sys import argv
from lexical_analyzer.constants import *


class Token:
    def __init__(self, lexeme, row, column, token_type, file_index):
        self.lexeme = lexeme
        self.token_type = token_type
        self.row = row + 1
        self.column = column + 1
        self.file_index = file_index + column

    # def __repr__(self):
    #     return f'{self.lexeme}\t:\t{self.token_type}\trow:{self.row}\tcolumn:{self.column}\tfile index:{self.file_index}'

    def __str__(self):
        return self.lexeme


class Error:
    def __init__(self, lexeme, row, column, error_msg, file_index):
        self.lexeme = lexeme
        self.row = row + 1
        self.column = column + 1
        self.error_msg = error_msg
        self.file_index = file_index + column

    def __str__(self):
        return f'Error at {self.lexeme}\t:\t{self.error_msg}\trow:{self.row}\tcolumn:{self.column}\tfile index:{self.file_index}'


def keyword(line, col, row, file_index):
    match line[col]:
        case 'b':
            match line[col: col + 4]:
                case 'bool':
                    if line[col + 4] not in ID_CHARS:
                        return Token('bool', row, col, 'BOOL', file_index), col + 4
            match line[col: col + 5]:
                case 'break':
                    if line[col + 5] not in ID_CHARS:
                        return Token('break', row, col, 'BREAK', file_index), col + 5

        case 'c':
            match line[col: col + 4]:
                case 'char':
                    if line[col + 4] not in ID_CHARS:
                        return Token('char', row, col, 'CHAR', file_index), col + 4
            match line[col: col + 8]:
                case 'continue':
                    if line[col + 8] not in ID_CHARS:
                        return Token('continue', row, col, 'CONTINUE', file_index), col + 8

        case 'e':
            match line[col: col + 4]:
                case 'else':
                    if line[col + 4] not in ID_CHARS:
                        return Token('else', row, col, 'ELSE', file_index), col + 4
                    else:
                        return None, col

        case 'f':
            match line[col: col + 5]:
                case 'false':
                    if line[col + 5] not in ID_CHARS:
                        return Token('false', row, col, 'FALSE', file_index), col + 5
            match line[col: col + 3]:
                case 'for':
                    if line[col + 3] not in ID_CHARS:
                        return Token('for', row, col, 'FOR', file_index), col + 3

        case 'i':
            match line[col: col + 2]:
                case 'if':
                    if line[col + 2] not in ID_CHARS:
                        return Token('if', row, col, 'IF', file_index), col + 2
            match line[col: col + 3]:
                case 'int':
                    if line[col + 3] not in ID_CHARS:
                        return Token('int', row, col, 'INT', file_index), col + 3
        case 'p':
            match line[col: col + 5]:
                case 'print':
                    if line[col + 5] not in ID_CHARS:
                        return Token('print', row, col, 'PRINT', file_index), col + 5
        case 'r':
            match line[col: col + 6]:
                case 'return':
                    if line[col + 6] not in ID_CHARS:
                        return Token('return', row, col, 'RETURN', file_index), col + 6
        case 't':
            match line[col: col + 4]:
                case 'true':
                    if line[col + 4] not in ID_CHARS:
                        return Token('true', row, col, 'TRUE', file_index), col + 4

        case 'v':
            match line[col: col + 4]:
                case 'void':
                    if line[col + 4] not in ID_CHARS:
                        return Token('void', row, col, 'VOID', file_index), col + 4

    return None, col


def identifier(line, col, row, file_index):
    if line[col] in ID_CHARS:
        length = 1
        while line[col + length] in ID_CHARS:
            length += 1
        return Token(line[col: col + length], row, col, 'ID', file_index), col + length
    return None, col


def operator(line, col, row, file_index):  # int a
    match line[col]:
        case '+':
            if line[col + 1] not in OP_CHARS:
                return Token('+', row, col, OPERATORS['+'], file_index), col + 1
            return op_error(line, col, row, file_index)

        case '-':
            if line[col + 1] not in OP_CHARS:
                return Token('-', row, col, OPERATORS['-'], file_index), col + 1
            return op_error(line, col, row, file_index)

        case '*':
            if line[col + 1] not in OP_CHARS:
                return Token('*', row, col, OPERATORS['*'], file_index), col + 1
            return op_error(line, col, row, file_index)

        case '/':
            if line[col + 1] not in OP_CHARS:
                return Token('/', row, col, OPERATORS['/'], file_index), col + 1
            return op_error(line, col, row, file_index)

        case '%':
            if line[col + 1] not in OP_CHARS:
                return Token('%', row, col, OPERATORS['%'], file_index), col + 1
            return op_error(line, col, row, file_index)

        case '&':
            match line[col + 1]:
                case '&':
                    if line[col + 2] not in OP_CHARS:
                        return Token('&&', row, col, OPERATORS['&&'], file_index), col + 2
            return op_error(line, col, row, file_index)

        case '|':
            match line[col + 1]:
                case '|':
                    if line[col + 2] not in OP_CHARS:
                        return Token('||', row, col, OPERATORS['||'], file_index), col + 2
            return op_error(line, col, row, file_index)

        case '!':
            if line[col + 1] not in OP_CHARS:
                return Token('!', row, col, OPERATORS['!'], file_index), col + 1
            match line[col + 1]:
                case '=':
                    if line[col + 2] not in OP_CHARS:
                        return Token('!=', row, col, OPERATORS['!='], file_index), col + 2
            return op_error(line, col, row, file_index)

        case '=':
            if line[col + 1] not in OP_CHARS:
                return Token('=', row, col, OPERATORS['='], file_index), col + 1
            match line[col + 1]:
                case '=':
                    if line[col + 2] not in OP_CHARS:
                        return Token('==', row, col, OPERATORS['=='], file_index), col + 2
            return op_error(line, col, row, file_index)

        case '>':
            if line[col + 1] not in OP_CHARS:
                return Token('>', row, col, OPERATORS['>'], file_index), col + 1
            match line[col + 1]:
                case '=':
                    if line[col + 2] not in OP_CHARS:
                        return Token('>=', row, col, OPERATORS['>='], file_index), col + 2
            return op_error(line, col, row, file_index)

        case '<':
            if line[col + 1] not in OP_CHARS:
                return Token('<', row, col, OPERATORS['<'], file_index), col + 1
            match line[col + 1]:
                case '=':
                    if line[col + 2] not in OP_CHARS:
                        return Token('<=', row, col, OPERATORS['<='], file_index), col + 2
            return op_error(line, col, row, file_index)

    return None, col


def comment(line, col, row, file_index):
    match line[col]:
        case '/':
            match line[col + 1]:
                case '/':
                    return Token(line[col:len(line) - 1], row, col, 'COMMENT', file_index), len(line)
    return None, col


def separator(line, col, row, file_index):
    match line[col]:
        case '(':
            return Token('(', row, col, SEPARATORS['('], file_index), col + 1
        case ')':
            return Token(')', row, col, SEPARATORS[')'], file_index), col + 1
        case '{':
            return Token('{', row, col, SEPARATORS['{'], file_index), col + 1
        case '}':
            return Token('}', row, col, SEPARATORS['}'], file_index), col + 1
        case '[':
            return Token('[', row, col, SEPARATORS['['], file_index), col + 1
        case ']':
            return Token(']', row, col, SEPARATORS[']'], file_index), col + 1
        case ';':
            return Token(';', row, col, SEPARATORS[';'], file_index), col + 1
        case ',':
            return Token(',', row, col, SEPARATORS[','], file_index), col + 1
    return None, col


def value(line, col, row, file_index):
    match line[col]:
        case '"':
            length = 0
            while line[col + 1 + length] != '"' or line[col + length] == '\\':
                length += 1
            return Token(line[col: col + length + 2], row, col, 'STR_VAL', file_index), col + length + 2
        case '\'':
            match line[col + 1]:
                case '\\':
                    if line[col + 3] == '\'':
                        return Token(line[col: col + 4], row, col, 'CHAR_VAL', file_index), col + 4

                case _:
                    if line[col + 2] == '\'':
                        return Token(line[col: col + 3], row, col, 'CHAR_VAL', file_index), col + 3

            length = 1
            while line[col + length] != '\'' or line[col + length - 1] == '\\':
                length += 1
            return Error(line[col: col + length + 1], row, col, 'Invalid Char Value', file_index), len(line)

        case _:
            if line[col].isdigit():
                match line[col + 1]:
                    case 'X' | 'x':
                        length = 2
                        while line[col + length] in HEX_DIGITS:
                            length += 1
                        
                        if line[col + length].isalpha():
                            return Error(line[col: col + length], row, col, 'Invalid Value', file_index), len(line)
                        
                        return Token(line[col: col + length], row, col, 'HEX_VAL', file_index), col + length
                    
                    case _:
                        length = 1
                        while line[col + length].isdigit():
                            length += 1

                        if line[col + length].isalpha():
                            return Error(line[col: col + length], row, col, 'Invalid Value', file_index), len(line)
                        
                        return Token(line[col: col + length], row, col, 'DEC_VAL', file_index), col + length


    return None, col


def op_error(line, col, row, file_index):
    length = 1
    while line[col + length] in OP_CHARS:
        length += 1
    return Error(line[col: col + length], row, col, 'Invalid operator', file_index), len(line)


def analyze_file(file_path):
    tokens = []
    file_index = 0
    with open(file_path, 'r') as file:
        for row, line in enumerate(file):
            col = 0
            while col < len(line):
                if line[col] in WHITESPACE:
                    tokens.append(Token(line[col], row, col, WHITESPACE[line[col]], file_index))
                    col += 1
                    continue

                token, col = separator(line, col, row, file_index)
                if token:
                    tokens.append(token)
                    continue

                token, col = value(line, col, row, file_index)
                if token:
                    tokens.append(token)
                    continue

                token, col = keyword(line, col, row, file_index)
                if token:
                    tokens.append(token)
                    continue

                token, col = identifier(line, col, row, file_index)
                if token:
                    tokens.append(token)
                    continue

                token, col = comment(line, col, row, file_index)
                if token:
                    tokens.append(token)
                    continue

                token, col = operator(line, col, row, file_index)
                if token:
                    tokens.append(token)
                    continue

                tokens.append(Error(line[col], row, col, 'Invalid character', file_index))
                col += 1

            file_index += col

    # add $ token (end of file)
    tokens.append(Token('$', row, col, 'EOF', file_index))

    return tokens


def lex(file_path):
    if not file_path:
        print('Please provide a file path')
        return
    tokens = analyze_file(file_path)
    err_count = 0
    errors = []
    for token in tokens:
        if isinstance(token, Error):
            err_count += 1
            errors.append(token)

    return errors, tokens


def main():
    file_path = argv[1]
    errors, tokens = lex(file_path)
    if len(errors) > 0:
        for error in errors:
            print(error)
    else:
        for token in tokens:
            print(token)


if __name__ == '__main__':
    main()

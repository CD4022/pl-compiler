from constants import *


class Token:
    def __init__(self, lexeme, row, column, token_type):
        self.lexeme = lexeme
        self.token_type = token_type
        self.row = row + 1
        self.column = column + 1

    def __str__(self):
        return f'{self.lexeme}\t:\t{self.token_type}\trow:{self.row}\tcolumn:{self.column}'


class Error:
    def __init__(self, lexeme, row, column, error_msg):
        self.lexeme = lexeme
        self.row = row + 1
        self.column = column + 1
        self.error_msg = error_msg

    def __str__(self):
        return f'Error at {self.lexeme} -> {self.error_msg} -> row:{self.row} -> column:{self.column}'


def keyword(line, col, row):
    match line[col]:
        case 'b':
            match line[col: col + 4]:
                case 'bool':
                    if line[col + 4] not in ID_CHARS:
                        return Token('bool', row, col, 'BOOL'), col + 4
            match line[col: col + 5]:
                case 'break':
                    if line[col + 5] not in ID_CHARS:
                        return Token('break', row, col, 'BREAK'), col + 5

        case 'c':
            match line[col: col + 4]:
                case 'char':
                    if line[col + 4] not in ID_CHARS:
                        return Token('char', row, col, 'CHAR'), col + 4
            match line[col: col + 8]:
                case 'continue':
                    if line[col + 8] not in ID_CHARS:
                        return Token('continue', row, col, 'CONTINUE'), col + 8

        case 'e':
            match line[col: col + 4]:
                case 'else':
                    if line[col + 4] not in ID_CHARS:
                        return Token('else', row, col, 'ELSE'), col + 4
                    else:
                        return None, col

        case 'f':
            match line[col: col + 5]:
                case 'false':
                    if line[col + 5] not in ID_CHARS:
                        return Token('false', row, col, 'FALSE'), col + 5
            match line[col: col + 3]:
                case 'for':
                    if line[col + 3] not in ID_CHARS:
                        return Token('for', row, col, 'FOR'), col + 3

        case 'i':
            match line[col: col + 2]:
                case 'if':
                    if line[col + 2] not in ID_CHARS:
                        return Token('if', row, col, 'IF'), col + 2
            match line[col: col + 3]:
                case 'int':
                    if line[col + 3] not in ID_CHARS:
                        return Token('int', row, col, 'INT'), col + 3
        case 'p':
            match line[col: col + 5]:
                case 'print':
                    if line[col + 5] not in ID_CHARS:
                        return Token('print', row, col, 'PRINT'), col + 5
        case 'r':
            match line[col: col + 6]:
                case 'return':
                    if line[col + 6] not in ID_CHARS:
                        return Token('return', row, col, 'RETURN'), col + 6
        case 't':
            match line[col: col + 4]:
                case 'true':
                    if line[col + 4] not in ID_CHARS:
                        return Token('true', row, col, 'TRUE'), col + 4

    return None, col


def identifier(line, col, row):
    if line[col] in ID_CHARS:
        length = 1
        while line[col + length] in ID_CHARS:
            length += 1
        return Token(line[col: col + length], row, col, 'ID'), col + length
    return None, col


def operator(line, col, row):  # int a
    match line[col]:
        case '+':
            if line[col + 1] not in OP_CHARS:
                return Token('+', row, col, OPERATORS['+']), col + 1
            return op_error(line, col, row)

        case '-':
            if line[col + 1] not in OP_CHARS:
                return Token('-', row, col, OPERATORS['-']), col + 1
            return op_error(line, col, row)

        case '*':
            if line[col + 1] not in OP_CHARS:
                return Token('*', row, col, OPERATORS['*']), col + 1
            return op_error(line, col, row)

        case '/':
            if line[col + 1] not in OP_CHARS:
                return Token('/', row, col, OPERATORS['/']), col + 1
            return op_error(line, col, row)

        case '%':
            if line[col + 1] not in OP_CHARS:
                return Token('%', row, col, OPERATORS['%']), col + 1
            return op_error(line, col, row)

        case '&':
            match line[col + 1]:
                case '&':
                    if line[col + 2] not in OP_CHARS:
                        return Token('&&', row, col, OPERATORS['&&']), col + 2
            return op_error(line, col, row)

        case '|':
            match line[col + 1]:
                case '|':
                    if line[col + 2] not in OP_CHARS:
                        return Token('||', row, col, OPERATORS['||']), col + 2
            return op_error(line, col, row)

        case '!':
            if line[col + 1] not in OP_CHARS:
                return Token('!', row, col, OPERATORS['!']), col + 1
            match line[col + 1]:
                case '=':
                    if line[col + 2] not in OP_CHARS:
                        return Token('!=', row, col, OPERATORS['!=']), col + 2
            return op_error(line, col, row)

        case '=':
            if line[col + 1] not in OP_CHARS:
                return Token('=', row, col, OPERATORS['=']), col + 1
            match line[col + 1]:
                case '=':
                    if line[col + 2] not in OP_CHARS:
                        return Token('==', row, col, OPERATORS['==']), col + 2
            return op_error(line, col, row)

        case '>':
            if line[col + 1] not in OP_CHARS:
                return Token('>', row, col, OPERATORS['>']), col + 1
            match line[col + 1]:
                case '=':
                    if line[col + 2] not in OP_CHARS:
                        return Token('>=', row, col, OPERATORS['>=']), col + 2
            return op_error(line, col, row)

        case '<':
            if line[col + 1] not in OP_CHARS:
                return Token('<', row, col, OPERATORS['<']), col + 1
            match line[col + 1]:
                case '=':
                    if line[col + 2] not in OP_CHARS:
                        return Token('<=', row, col, OPERATORS['<=']), col + 2
            return op_error(line, col, row)

    return None, col


def comment(line, col, row):
    match line[col]:
        case '/':
            match line[col + 1]:
                case '/':
                    return Token(line[col:len(line) - 1], row, col, 'COMMENT'), len(line)
    return None, col


def separator(line, col, row):
    match line[col]:
        case '(':
            return Token('(', row, col, SEPARATORS['(']), col + 1
        case ')':
            return Token(')', row, col, SEPARATORS[')']), col + 1
        case '{':
            return Token('{', row, col, SEPARATORS['{']), col + 1
        case '}':
            return Token('}', row, col, SEPARATORS['}']), col + 1
        case '[':
            return Token('[', row, col, SEPARATORS['[']), col + 1
        case ']':
            return Token(']', row, col, SEPARATORS[']']), col + 1
        case ';':
            return Token(';', row, col, SEPARATORS[';']), col + 1
        case ',':
            return Token(',', row, col, SEPARATORS[',']), col + 1
    return None, col


def value(line, col, row):
    match line[col]:
        case '"':
            length = 0
            while line[col + 1 + length] != '"' or line[col + length] == '\\':
                length += 1
            return Token(line[col: col + length + 2], row, col, 'STR_VAL'), col + length + 2
        case '\'':
            match line[col + 1]:
                case '\\':
                    if line[col + 3] == '\'':
                        return Token(line[col: col + 4], row, col, 'CHAR_VAL'), col + 4

                case _:
                    if line[col + 2] == '\'':
                        return Token(line[col: col + 3], row, col, 'CHAR_VAL'), col + 3

            length = 1
            while line[col + length] != '\'' or line[col + length - 1] == '\\':
                length += 1
            return Error(line[col: col + length + 1], row, col, 'Invalid Char Value'), len(line)

        case _:
            if line[col].isdigit():
                length = 0
                while line[col + length] in '0123456789':
                    length += 1

                if line[col + length].isalpha():
                    return Error(line[col: col + length], row, col, 'Invalid Value'), len(line)

                return Token(line[col: col + length], row, col, 'INT_VAL'), col + length
    return None, col


def op_error(line, col, row):
    length = 1
    while line[col + length] in OP_CHARS:
        length += 1
    return Error(line[col: col + length], row, col, 'Invalid operator'), len(line)


def analyze_file(file_path):
    tokens = []
    with open(file_path, 'r') as file:
        for row, line in enumerate(file):
            col = 0
            while col < len(line):
                if line[col] in WHITESPACE:
                    col += 1
                    continue

                token, col = separator(line, col, row)
                if token:
                    tokens.append(token)
                    continue

                token, col = value(line, col, row)
                if token:
                    tokens.append(token)
                    continue

                token, col = keyword(line, col, row)
                if token:
                    tokens.append(token)
                    continue

                token, col = identifier(line, col, row)
                if token:
                    tokens.append(token)
                    continue

                token, col = comment(line, col, row)
                if token:
                    tokens.append(token)
                    continue

                token, col = operator(line, col, row)
                if token:
                    tokens.append(token)
                    continue

                tokens.append(Error(line[col], row, col, 'Invalid character'))
                col += 1
    return tokens


def main():
    tokens = analyze_file('../test.pl')
    err_count = 0
    for token in tokens:
        if isinstance(token, Error):
            err_count += 1
            print(token)

    if err_count == 0:
        for token in tokens:
            print(token)


if __name__ == '__main__':
    main()

from sys import argv
from collections import deque

import json

from lexical_analyzer import lexer


class Node:
    def __init__(self, value, parent=None):
        self.value = value
        self.children = []
        self.parent = parent
        self.parent.add_child(self) if parent else None

    def add_child(self, child):
        self.children.append(child)

    def set_parent(self, parent):
        self.parent = parent

    def extend_children(self, children):
        self.children.extend(children)

    def last_child(self):
        return self.children[-1]

    def print_tree(self, level=0):
        print('\t' * level, self.value)
        for child in self.children:
            child.print_tree(level + 1)

    def __repr__(self):
        return self.value


class Error:
    def __init__(self, line, column):
        self.line = line
        self.column = column

    def __str__(self):
        return f'Error: at line {self.line} column {self.column}'


def parse(tokens, parse_table):
    stack = deque()

    track_back_lst = [2]
    stack.append('$')
    stack.append('program')

    root = None
    errors = []
    curr_node = None
    i, non_ws_i = 0, 0
    key_error_occurred = False
    while i < len(tokens):
        if tokens[i].lexeme in lexer.WHITESPACE.keys() or tokens[i].token_type == 'COMMENT':
            i += 1
            continue

        if track_back_lst[-1] and track_back_lst[-1] == 0:
            curr_node = curr_node.parent
            track_back_lst.pop()
            continue
        track_back_lst[-1] -= 1

        if not key_error_occurred:
            current = stack.pop()
            curr_node = Node(current, curr_node)

        key_error_occurred = False

        if root is None:
            root = curr_node

        if current == 'E':
            curr_node = curr_node.parent
            continue

        if current == '$':
            if tokens[i].token_type == 'EOF':
                break
            else:
                print(f'Error: expected EOF got {tokens[i].token_type}')
                return

        if current.startswith('T_'):
            if current == f'T_{tokens[i].token_type}':
                curr_node.add_child(Node(f"{tokens[i].lexeme}"))
                curr_node = curr_node.parent
                non_ws_i = i
                i += 1
                continue
            else:
                error = Error(tokens[non_ws_i + 1].row, tokens[non_ws_i + 1].column)
                errors.append(error)
                continue

        if current == "else_if_blocks" and i + 1 < len(tokens):
            j = i + 1
            token = tokens[j]
            while token.lexeme in lexer.WHITESPACE.keys():
                j += 1
                token = tokens[j]
            if token.token_type == 'LCB':
                stack.append('E')
                track_back_lst.append(1)
                continue

        try:
            applied_rule = parse_table[current][f"T_{tokens[i].token_type}".replace('T_EOF', '$')]
            track_back_lst.append(len(applied_rule))
        except KeyError:
            try:
                applied_rule = parse_table[current]['*']
                track_back_lst.append(len(applied_rule))
            except KeyError:
                # i, error = panic_mode_recovery(tokens, i, parse_table, stack, curr_node.parent, track_back_lst)
                error = Error(tokens[non_ws_i + 1].row, tokens[non_ws_i + 1].column)
                key_error_occurred = True
                i += 1
                errors.append(error)
                continue

        for t in applied_rule[::-1]:
            stack.append(t)

    print("hi")
    return root, errors


def panic_mode_recovery(tokens, token_index: int, parse_table, stack, current, track_back_lst):
    start_index = token_index
    parent_count = 1
    while True:
        track_back_lst[-parent_count] = 0

        # get all the synch for the nt from the parse table
        synchs = []
        for key, value in parse_table[current.value].items():
            if value == "synch":
                synchs.append(key)

        j = token_index
        while j < len(tokens):
            if f'T_{tokens[token_index].token_type}' in synchs:
                token_index = j
                break
            j += 1
        else:
            parent_count += 1
            current = current.parent
            continue

        error = Error(tokens[start_index].row,
                      tokens[start_index].column)

        return token_index, error


def main():
    with open(argv[1]) as f:
        code = f.readlines()
        code[-1] = code[-1] + '\n'

    lex_errors, tokens = lexer.lex(argv[1])
    with open('parse_table.json') as f:
        parse_table = json.load(f)

    if len(lex_errors) > 0:
        for error in lex_errors:
            print(error)

    else:
        root, syn_errors = parse(tokens, parse_table)
        if len(syn_errors):
            for error in syn_errors:

                print(f"\033[31mSyntax error at {error.line}:{error.column}")
                print(f"\t{code[error.line - 1]}", end='')
                print(f"\t{'-' * (error.column - 1)}^\033[0m")
        else:
            root.print_tree()


if __name__ == '__main__':
    main()

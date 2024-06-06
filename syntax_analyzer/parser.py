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
    def __init__(self, line, column, length):
        self.line = line
        self.column = column
        self.length = length

    def __str__(self):
        return f'Error: at line {self.line} column {self.column}'


def parse(tokens, parse_table):
    stack = deque()

    track_back_lst = [2]
    stack.append('$')
    stack.append('program')

    root = None
    curr_node = None
    i = 0
    while i < len(tokens):
        if tokens[i].lexeme in lexer.WHITESPACE.keys() or tokens[i].token_type == 'COMMENT':
            i += 1
            continue

        if track_back_lst[-1] == 0:
            curr_node = curr_node.parent
            track_back_lst.pop()
            continue
        track_back_lst[-1] -= 1

        current = stack.pop()
        curr_node = Node(current, curr_node)

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
                i += 1
                continue
            else:
                print(f'Error: expected {current} got {tokens[i].token_type}')
                i, error = panic_mode_recovery(tokens, i, parse_table, stack, curr_node.parent.value)
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
            i, error = panic_mode_recovery(tokens, i, parse_table, stack, curr_node.parent.value)
            continue

        for t in applied_rule[::-1]:
            stack.append(t)

    return root


def panic_mode_recovery(tokens, token_index: int, parse_table, stack, current):
    start_index = token_index

    top_nt = current
    while top_nt.startswith('T_'):
        top_nt = stack.pop()

    # get all the synch for the nt from the parse table
    synchs = []
    for key, value in parse_table[top_nt].items():
        if value == "synch":
            synchs.append(key)

    while f'T_{tokens[token_index].token_type}' not in synchs:
        token_index += 1

    error = Error(tokens[start_index].row,
                  tokens[start_index].column,
                  len(tokens[token_index].lexeme) + (tokens[token_index].column - tokens[start_index].column + 1))

    return token_index, error


def main():
    with open(argv[1]) as f:
        code = f.read()

    errors, tokens = lexer.lex(argv[1])
    with open('parse_table.json') as f:
        parse_table = json.load(f)

    if len(errors) > 0:
        for error in errors:
            print(error)

    else:
        root = parse(tokens, parse_table)
        root.print_tree()


if __name__ == '__main__':
    main()

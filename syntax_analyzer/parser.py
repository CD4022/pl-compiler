from sys import argv
from collections import deque

import json

from lexical_analyzer import lexer


class Tree:
    def __init__(self, value):
        self.value = value
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def extend_children(self, children):
        self.children.extend(children)

    def last_child(self):
        return self.children[-1]

    def __str__(self):
        tree = f'{self.value}'
        for child in self.children:
            tree += f'\n{" " * 4}{child}'


def parse(tokens, parse_table):
    tree = Tree('program')
    stack = deque()
    stack.append('$')
    stack.append('program')

    cur_tree = tree
    i = 0
    while i < len(tokens):
        if tokens[i].lexeme in lexer.WHITESPACE.keys() or tokens[i].token_type == 'COMMENT':
            i += 1
            continue

        current = stack.pop()
        while current == 'E':
            current = stack.pop()

        if current.startswith('T_'):
            if current == f'T_{tokens[i].token_type}':
                cur_tree.add_child(f'{current} {tokens[i].lexeme}')
                i += 1
                continue
            else:
                print(f'Error: expected {current} got {tokens[i].token_type}')  # TODO: sync
                return

        cur_tree.add_child(Tree(current))
        applied_rule = parse_table[current][f"T_{tokens[i].token_type}"]

        for t in applied_rule[::-1]:
            cur_tree = Tree(current)
            stack.append(t)

        print("llll")


def main():
    errors, tokens = lexer.lex(argv[1])
    with open('parse_table.json') as f:
        parse_table = json.load(f)

    if len(errors) > 0:
        for error in errors:
            print(error)

    else:
        parse(tokens, parse_table)



if __name__ == '__main__':
    main()

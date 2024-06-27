from sys import argv
import constants

from syntax_analyzer import parser


class Symbol:
    def __init__(self, var_name, var_type, scope: list = None, value=0, args=None, is_func=False):
        self.var_name = var_name
        self.var_type = var_type
        self.scope = scope if scope else list()
        self.value = value
        self.args = args
        self.is_func = is_func


SYMBOL_TABLE = []


def traverse_arg_list(node, func_type, func_name):
    global SYMBOL_TABLE
    if node.children[0].value == "E":
        symbol = Symbol(func_name, func_type, [], args=[], is_func=True)
        SYMBOL_TABLE.append(symbol)
        return


def traverse_declaration(node: parser.Node):
    ids = []
    symbol_type = node.children[0].children[0].value
    ids.append(node.children[1].children[0].value)
    is_func = True if node.children[2].children[0].value == "func" else False
    if is_func:
        pass # TODO


def traverse_bin_expr(node: parser.Node):

    if node.children[1].children[0].children[0].value in constants.bin_operators:
        # Check the first child
        is_valid = check_child(node)
        # Check the second child
        if is_valid:
            check_child(node.children[1].children[1])


def check_child(node):
    while len(node.children) != 0:
        node = node.children[0]

        if node.value == 'expr':
            traverse_bin_expr(node)

        if str(node.value).startswith('T_'):
            if node.value in constants.non_int_terminals:
                print("operands do not have the same type")
                return False
            elif node.value in constants.int_terminals:
                return True
            node = node.parent.children[1]


def traverse_parse_tree(node: parser.Node, depth=0):
    current = node
    for child in node.children:
        # if child.value == "declaration":
        #     pass # TODO: Alireza
        if child.value == "expr":
            traverse_bin_expr(child)
        # elif child.value == "if":
        #     pass # TODO: Ali
        # elif child.value == "func_call":
        #     pass # TODO: Alireza
        # elif child.value == "main":
        #     pass # TODO: Alireza
        # elif child.value == "args":
        #     pass # TODO: Alireza
        # elif child.value == "pars":
        #     pass # TODO: Ali
        # elif child.value == "return":
        #     pass # TODO: Alireza

        elif len(child.children) != 0:
            traverse_parse_tree(child)


def semantic_analyze(parse_tree: parser.Node):
    curr_node = parse_tree
    traverse_parse_tree(curr_node)


def main():
    parse_tree = parser.parse(argv[1])
    if parse_tree:
        semantic_analyze(parse_tree)


if __name__ == "__main__":
    main()

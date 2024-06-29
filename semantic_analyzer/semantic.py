from sys import argv
import constants

from syntax_analyzer import parser


class Symbol:
    def __init__(self, var_name, var_type, scope: list, length, value=0, args=None, sym_type="variable"):
        self.var_name = var_name
        self.var_type = var_type
        self.scope = scope
        self.length = length
        self.value = value
        self.args = args
        self.is_func = True if sym_type == "function" else False
        self.is_arr = True if sym_type.startswith("array") else False
        self.is_arg = True if sym_type.endswith("argument") else False

    def __repr__(self):
        return (f"{self.var_name} {self.var_type} {self.value if not self.is_func and not self.is_arr else '\b'}"
                f" {'func' if self.is_func else ''} {'arr' if self.is_arr else ''}"
                f" {f'arg for {self.scope[-1]}' if self.is_arg else ''}")


class Error:
    def __init__(self, message: str, row: int):
        self.message: str = message
        self.row: int = row

    def __str__(self):
        return f'Error: at line {self.row}: {self.message}'


SYMBOL_TABLE = []
ERRORS = []
SCOPES = []


def traverse_declaration(node: parser.Node, scope):
    ids = []
    # type is the first child of the declaration node
    symbol_type = node.children[0].children[0].value[2:]
    # add the name which is being declared to the ids list
    ids.append(node.children[1].children[0].value)
    # check if the declaration is a function
    is_func = True if node.children[2].children[0].value == "func" else False
    if is_func:
        # traverse the argument_list child
        traverse_arg_list(node.children[2].children[0].children[1], scope, symbol_type, ids[0], [])


def traverse_arg_list(node, scope: list, func_type, func_name, args):
    global SYMBOL_TABLE
    length = 4 if func_type in ('BOOL', 'INT') else 1
    if node.children[0].value == "E":
        symbol = Symbol(func_name, func_type, scope, length, args=args, sym_type="function")
        # check if symbol with the same name already exists
        for sym in SYMBOL_TABLE:
            if sym.var_name == func_name and sym.scope == scope:
                error = Error(f"redefinition of {func_name}", node.row)
                ERRORS.append(error)

        SYMBOL_TABLE.append(symbol)
        return
    arg_node_index = 0 if node.value == "argument_list" else 1
    if node.children[arg_node_index].value == "argument":
        arg_type = node.children[arg_node_index].children[0].children[0].value[2:]
        arg_name = node.children[arg_node_index].children[1].children[0].children[0].value

        arg_length = 4 if arg_type in ('BOOL', 'INT') else 1
        is_arr = False

        # check if the argument is an array
        if node.children[arg_node_index].children[1].children[1].children[0].value != 'E':
            arg_length = arg_length * expr_value(node.children[arg_node_index].children[1].children[1].children[1])
            is_arr = True

        symbol = Symbol(arg_name, arg_type, scope + [func_name], arg_length,
                        sym_type=f"{'array_' if is_arr else ''}{'argument'}")
        # check if the argument with the same name already exists
        for sym in SYMBOL_TABLE:
            if sym.var_name == symbol.var_name and sym.scope == symbol.scope:
                error = Error(f"redefinition of {arg_name}", node.row)
                ERRORS.append(error)
        SYMBOL_TABLE.append(symbol)
        args.append(symbol)
        traverse_arg_list(node.children[arg_node_index + 1], scope, func_type, func_name, args)


def expr_value(node):
    pass  # TODO: Ali


def traverse_expr(node: parser.Node):
    if len(node.children) == 1 and len(node.children[0].children) == 0:
        if node.value == "T_ID":
            node.node_type = "UNDEFINED"
            for symbol in SYMBOL_TABLE:
                if symbol.var_name == node.children[0].value:
                    node.node_type = symbol.var_type

        elif node.value in constants.int_terminals:
            node.node_type = "INT"
        
        elif node.value in constants.bool_terminals:
            node.node_type = "BOOL"

        elif node.value in constants.non_int_bool_terminals:
            node.node_type = "NON_INT_BOOL"

        elif node.value in constants.separators:
            node.node_type = "SEPARATOR"

        else:
            node.node_type = "E"
        
        return

    for child in node.children:
        traverse_expr(child)
        
        # if all children have traversed and have a type
        # find the type of the parent node
        if all([child.node_type is not None for child in node.children]):
            if len(node.children) == 1:
                node.node_type = node.children[0].node_type

            elif all([child.node_type in ["INT", "SEPARATOR", "E"] for child in node.children]):
                node.node_type = "INT"

            elif all([child.node_type in ["BOOL", "SEPARATOR", "E"] for child in node.children]):
                node.node_type = "BOOL"
            
            elif any([child.node_type == "UNDEFINED" for child in node.children]):
                print("undefined variable")
                return

            else:
                print("operands do not have the same type")
                return
    
    return node.node_type


def check_array(node: parser.Node):
    if node.children[0].value != "E":
        expr_type = traverse_expr(node.children[1])
        # TODO: result must be int and > 0
        if expr_type != "INT":
            print("array index must be an integer")


def traverse_parse_tree(node: parser.Node, scope, depth=0):
    for child in node.children:

        if child.value == "declaration":
            traverse_declaration(child, scope)
        if child.value == "argument_list":
            continue
        if child.value == "expr":
            traverse_expr(child)
        if child.value == "id_name'":
            check_array(child)
        if child.value == "term":
            continue
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

        if len(child.children) != 0:
            traverse_parse_tree(child, scope)


def semantic_analyze(parse_tree: parser.Node):
    curr_node = parse_tree
    traverse_parse_tree(curr_node, [])
    if not len(ERRORS):
        for symbol in SYMBOL_TABLE:
            print(symbol)
    else:
        for error in ERRORS:
            print(error)


def main():
    parse_tree = parser.parse(argv[1])
    if parse_tree:
        semantic_analyze(parse_tree)


if __name__ == "__main__":
    main()

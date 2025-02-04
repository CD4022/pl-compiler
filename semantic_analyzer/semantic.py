from sys import argv
from typing import List, Optional

from syntax_analyzer import parser
import constants


class Symbol:
    def __init__(self, var_name, var_type, scope: list, length, value=0,
                 args: Optional['List["Symbol"]'] = None, sym_type="variable"):
        self.var_name = var_name
        self.var_type = var_type
        self.scope = scope
        self.length = length
        self.value = value
        self.args: Optional['List["Symbol"]'] = args
        self.is_func = True if sym_type == "function" else False
        self.is_arr = True if sym_type.startswith("array") else False
        self.is_arg = True if sym_type.endswith("argument") else False

    def __repr__(self):
        value_str = self.value if not self.is_func and not self.is_arr else ""
        func_str = "function" if self.is_func else ""
        arr_str = f"array<{self.var_type}>" if self.is_arr else ""
        arg_str = f"argument for {self.scope[-1]}" if self.is_arg else ""

        return f"{self.var_name} {self.var_type} {value_str} {func_str} {arr_str} {arg_str}".strip()


class Error:
    def __init__(self, message: str, row: int):
        self.message: str = message
        self.row: int = row

    def __str__(self):
        return f'Error: at line {self.row}: {self.message}'

    def __eq__(self, other):
        return self.message == other.message and self.row == other.row


SYMBOL_TABLE = []
ERRORS = []
SCOPES = [[]]


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
    else:
        traverse_var_declaration(node.children[2], ids, symbol_type, scope)


def traverse_arg_list(node, scope: list, func_type, func_name, args):
    global SYMBOL_TABLE, SCOPES, ERRORS
    length = 4 if func_type in ('BOOL', 'INT') else 1
    if node.children[0].value == "E":
        symbol = Symbol(func_name, func_type, scope, length, args=args, sym_type="function")
        # check if symbol with the same name already exists
        for sym in SYMBOL_TABLE:
            if sym.var_name == func_name and sym.scope == scope:
                error = Error(f"redefinition of {func_name}", node.row)
                ERRORS.append(error)
                break

        SYMBOL_TABLE.append(symbol)
        SCOPES.append(scope + [func_name])
        return
    arg_node_index = 0 if node.value == "argument_list" else 1
    if node.children[arg_node_index].value == "argument":
        arg_type = node.children[arg_node_index].children[0].children[0].value[2:]
        arg_name = node.children[arg_node_index].children[1].children[0].children[0].value

        arg_length = 4 if arg_type in ('BOOL', 'INT') else 1
        is_arr = False

        # check if the argument is an array
        if node.children[arg_node_index].children[1].children[1].children[0].value != 'E':
            arg_length = arg_length * expr_value(node.children[arg_node_index].children[1].children[1].children[1],
                                                 scope)
            is_arr = True

        symbol = Symbol(arg_name, arg_type, scope + [func_name], arg_length,
                        sym_type=f"{'array_' if is_arr else ''}{'argument'}")
        # check if the argument with the same name already exists
        for sym in SYMBOL_TABLE:
            if sym.var_name == symbol.var_name and sym.scope == symbol.scope:
                error = Error(f"redefinition of {arg_name}", node.row)
                ERRORS.append(error)
                break
        SYMBOL_TABLE.append(symbol)
        args.append(symbol)
        traverse_arg_list(node.children[arg_node_index + 1], scope, func_type, func_name, args)


def traverse_var_declaration(node, ids, var_type, scope):
    var_length = 4 if var_type in ('BOOL', 'INT') else 1
    if node.children[0].value == "id_name'":
        var_name = ids[-1]

        # check if the variable is an array
        is_arr = True if node.children[0].children[0].value != 'E' else False
        if is_arr:
            var_length = var_length * expr_value(node.children[0].children[1], scope)

        list_index = 0
        var_value = 0
        if node.children[1].children[0].value == "assign_expr":
            list_index = 1
            if var_type == expr_type(node.children[1].children[0].children[1], scope):
                var_value = expr_value(node.children[1].children[0].children[1], scope)
            else:
                error = Error("type mismatch in variable declaration", node.row)
                ERRORS.append(error)

        add_variable(var_name, var_type, scope, var_length, var_value,
                     f"{'array' if is_arr else 'variable'}", node.row)

        traverse_var_declaration(node.children[1].children[list_index], ids, var_type, scope)

    if node.children[0].value == "T_COMMA":
        main_clause = node.children[1]
        var_name = main_clause.children[0].children[0].children[0].value

        # check if the variable is an array
        is_arr = True if main_clause.children[0].children[1].children[0].value != 'E' else False
        if is_arr:
            var_length = var_length * expr_value(main_clause.children[0].children[1].children[1], scope)

        var_value = 0
        if main_clause.children[1].children[0].value == "assign_expr":
            var_value = expr_value(main_clause.children[1].children[0].children[1], scope)

        add_variable(var_name, var_type, scope, var_length, var_value,
                     f"{'array' if is_arr else 'variable'}", node.row)

        traverse_var_declaration(node.children[2], ids, var_type, scope)


def expr_value(node: parser.Node, scope):
    _, value = traverse_expr(node, scope)
    return value


def add_variable(var_name, var_type, scope, length, value, sym_type, row):
    global SYMBOL_TABLE
    symbol = Symbol(var_name, var_type, scope, length, value, sym_type=sym_type)
    # check if the variable with the same name already exists
    for sym in SYMBOL_TABLE:
        if sym.var_name == var_name and sym.scope == scope:
            error = Error(f"redefinition of {var_name}", row)
            ERRORS.append(error)
            break
    SYMBOL_TABLE.append(symbol)


def traverse_expr(node: parser.Node, scope):
    if len(node.children) == 1 and len(node.children[0].children) == 0:
        if node.value == "T_ID":
            node.node_type = "UNDEFINED"
            for symbol in SYMBOL_TABLE:
                if symbol.var_name == node.children[0].value:
                    symbol_scope = symbol.scope
                    if symbol_scope != scope[:len(symbol_scope)]:
                        continue
                    node.node_type = symbol.var_type
                    if symbol.value != None and symbol.var_type == "INT":
                        node.imm_val = int(symbol.value)
                    elif symbol.value != None and symbol.var_type == "BOOL":
                        node.imm_val = symbol.value
                    else:
                        node.imm_val = None

                    return "VALID", None
                    
            return "UNDEFINED", None

        elif node.value in constants.INT_TERMINALS:
            node.node_type = "INT"
            if isinstance(node.children[0].value, str):
                node.imm_val = int(node.children[0].value, 16)
            else:
                node.imm_val = int(node.children[0].value)

        elif node.value in constants.BOOL_TERMINALS:
            node.node_type = "BOOL"
            node.imm_val = True if node.children[0].value == "true" else False

        elif node.value in constants.NON_INT_BOOL_TERMINALS:
            node.node_type = f"{node.value}"
            node.imm_val = node.value

        elif node.value in constants.SEPARATORS:
            node.node_type = "SEPARATOR"

        elif node.value in constants.ALL_OPS:
            node.node_type = f'{node.value}'

        else:
            node.imm_val = node.inh_val
            node.parent.imm_val = node.inh_val
            if node.parent.node_type and node.node_type != node.parent.node_type:
                return "INVALID", None
            node.parent.node_type = node.node_type

        return "VALID", None

    for child in node.children:
        is_valid, _ = traverse_expr(child, scope)

        if is_valid == "INVALID":
            error_msg = "There is a type mismatch in the expression!"
            error = Error(error_msg, node.row)
            if error not in ERRORS:
                ERRORS.append(error)
            return "INVALID", None
        
        if is_valid == "UNDEFINED":
            error_msg = "There is an undefined variable in the expression!"
            error = Error(error_msg, node.row)
            if error not in ERRORS:
                ERRORS.append(error)
            return "UNDEFINED", None

        # if child.node_type == "SEPARATOR":
        #     continue

        if len(node.children) == 1:
            node.node_type = node.children[0].node_type
            node.imm_val = node.children[0].imm_val

        elif child.value in ["term", "fact", "expr", "T_ID"]:
            node.children[-1].node_type = child.node_type
            node.children[-1].inh_val = child.imm_val
            if any([child_.node_type in constants.BIN_T_OPS for child_ in node.children]):
                if node.children[0].node_type == "T_PLUS":
                    node.children[-1].inh_val = node.inh_val + node.children[-2].imm_val
                elif node.children[0].node_type == "T_MINUS":
                    node.children[-1].inh_val = node.inh_val - node.children[-2].imm_val
                elif node.children[0].node_type == "T_MULT":
                    node.children[-1].inh_val = node.inh_val * node.children[-2].imm_val
                elif node.children[0].node_type == "T_DIV":
                    node.children[-1].inh_val = node.inh_val / node.children[-2].imm_val
                elif node.children[0].node_type == "T_MOD":
                    node.children[-1].inh_val = node.inh_val % node.children[-2].imm_val

            elif any([child_.node_type in constants.UN_T_OPS for child_ in node.children]):
                if node.children[0].node_type == "T_AND":
                    node.children[-1].inh_val = node.inh_val and node.children[-2].imm_val
                elif node.children[0].node_type == "T_OR":
                    node.children[-1].inh_val = node.inh_val or node.children[-2].imm_val
                elif node.children[0].node_type == "T_NOT":
                    node.children[-1].inh_val = not node.children[-2].imm_val

        elif node.value in ["comp_expr'"] and node.children[-1].imm_val and child.children[0].value not in constants.COM_T_OPS:
            if any([child_.node_type in constants.COM_T_OPS for child_ in node.children]):
                if node.node_type == node.children[-1].node_type:
                    node.node_type = "BOOL"
                    if node.children[0].node_type == "T_EQUALS":
                        node.imm_val = node.inh_val == node.children[-1].imm_val
                    elif node.children[0].node_type == "T_NOT_EQUALS":
                        node.imm_val = node.inh_val != node.children[-1].imm_val
                    elif node.children[0].node_type == "T_GT":
                        node.imm_val = node.inh_val > node.children[-1].imm_val
                    elif node.children[0].node_type == "T_LT":
                        node.imm_val = node.inh_val < node.children[-1].imm_val
                    elif node.children[0].node_type == "T_GE":
                        node.imm_val = node.inh_val >= node.children[-1].imm_val
                    elif node.children[0].node_type == "T_LE":
                        node.imm_val = node.inh_val <= node.children[-1].imm_val
                else:
                    error_msg = "There is a type mismatch in the expression!"
                    error = Error(error_msg, node.row)
                    if error not in ERRORS:
                        ERRORS.append(error)
                    return "INVALID", None

        elif node.value in ["term'", "expr'"]:
            node.parent.imm_val = node.imm_val
            node.parent.node_type = node.node_type

        elif node.value == "comp_expr":
            if child.value == "expr":
                node.children[-1].node_type = child.node_type
                node.children[-1].inh_val = child.imm_val
            else:
                node.imm_val = child.imm_val
                node.node_type = child.node_type

        elif node.value == "fact" and node.children[0].node_type == "SEPARATOR":
            node.node_type = node.children[1].node_type
            node.imm_val = node.children[1].imm_val

        elif node.value == "un_expr" and len(node.children) > 1 and node.children[1].node_type:
            node.node_type = node.children[-1].node_type
            node.imm_val = -node.children[-1].imm_val if node.children[0].node_type == "T_MINUS" \
                else not node.children[-1].imm_val
    
    return node.node_type, node.imm_val


def check_array(node: parser.Node, scope):
    if node.children[0].value != "E":
        _expr_type, expr_val = traverse_expr(node.children[1], scope)
        if _expr_type != "INT" and expr_val > 0:
            error = Error("array index must be an integer", node.row)
            ERRORS.append(error)


def check_if(node: parser.Node, scope):
    _expr_type = expr_type(node, scope)
    if _expr_type not in ["BOOL", "INVALID", "UNDEFINED"]:
        error = Error("condition in if statement must be of type BOOL", node.row)
        ERRORS.append(error)
        return


def new_scope(scope):
    global SCOPES
    i = 0
    while True:
        temp_scope = scope + [i]
        if temp_scope not in SCOPES:
            SCOPES.append(temp_scope)
            return temp_scope.copy()
        i += 1


def traverse_return_stmt(node: parser.Node, scope):
    return_type = "VOID" if node.children[1].children[0].value == "E" else expr_type(node.children[1].children[0],
                                                                                     scope)
    function_name = ''
    for member in scope[::-1]:
        if isinstance(member, str):
            function_name = member
            break
    if function_name == '':
        error = Error("return statement outside of a function", node.row)
        ERRORS.append(error)
        return
    else:
        for symbol in SYMBOL_TABLE:
            if symbol.var_name == function_name and symbol.is_func:
                if symbol.var_type != return_type:
                    error = Error(f"return type does not match function type", node.row)
                    ERRORS.append(error)
                break


def traverse_func_call(node: parser.Node, func_name, scope):
    # find function in symbol table
    func_id = None
    for symbol in SYMBOL_TABLE:
        if symbol.var_name == func_name and symbol.is_func:
            func_id = symbol
            break
    if func_id is None:
        error = Error(f"function {func_name} is not defined", node.row)
        ERRORS.append(error)
        return
    func_args = func_id.args
    traverse_func_pars(node.children[1], func_args, scope)


def traverse_func_pars(node: parser.Node, func_args, scope, depth=0):
    expr_index = 0 if node.value == "par_list" else 1

    if node.children[0].value == "E":
        if len(func_args) != depth:
            error = Error(f"missing arguments for function call", node.row)
            ERRORS.append(error)
        return

    if depth > len(func_args) - 1:
        error = Error(f"too many arguments for function call", node.row)
        ERRORS.append(error)
        return

    if func_args[depth].var_type != expr_type(node.children[expr_index], scope):
        error = Error(f"argument type does not match function parameter type", node.row)
        ERRORS.append(error)
        return
    traverse_func_pars(node.children[expr_index + 1], func_args, scope, depth + 1)


def check_variable_scope(node: parser.Node, var_name, scope):
    lhs_symbol_candidates = []
    for symbol in SYMBOL_TABLE:
        if symbol.var_name == var_name:
            lhs_symbol_candidates.append(symbol)

    if len(lhs_symbol_candidates) == 0:
        error = Error(f"variable {var_name} is not defined", node.row)
        ERRORS.append(error)
        return None

    lhs_symbol = None
    for symbol in lhs_symbol_candidates:
        if symbol.scope == scope[:len(symbol.scope)]:
            lhs_symbol = symbol
            break
    if not lhs_symbol:
        error = Error(f"variable {var_name} is not defined in this scope", node.row)
        ERRORS.append(error)
        return None

    return lhs_symbol


def check_assign_expr(node: parser.Node, scope):
    lhs_id = node.children[0].children[0].value

    lhs_symbol = check_variable_scope(node, lhs_id, scope)
    if lhs_symbol:
        rhs_type = expr_type(node.children[1].children[1].children[1], scope)
        if lhs_symbol.var_type != rhs_type:
            error = Error(f"assignment type does not match variable type", node.row)
            ERRORS.append(error)


def expr_type(node: parser.Node, scope):
    e_type, _ = traverse_expr(node, scope)
    return e_type


def traverse_parse_tree(node: parser.Node, scope):
    for child in node.children:
        if child.value == "declaration":
            traverse_declaration(child, scope.copy())
        if child.value == "argument_list":
            continue
        if child.value == "dec''":
            continue
        if child.value == "T_LCB":
            if child.parent.value == "func":
                scope = SCOPES[-1].copy()
            else:
                scope = new_scope(scope)
        if child.value == "T_RCB":
            scope.pop()
        if child.value == "expr":
            traverse_expr(child, scope)
        if child.value == "id_name'":
            check_array(child, scope)
        if child.value == "term":
            continue
        if child.value == "return_stmt":
            traverse_return_stmt(child, scope)
        if child.value == "return_val":
            continue
        if len(child.children) > 1:
            if child.value == "stmt":
                if len(child.children[1].children) >= 1 and child.children[1].children[0].value == "func_call":
                    func_name = child.children[0].children[0].value
                    traverse_func_call(child.children[1].children[0], func_name, scope)
                    continue
                if len(child.children[1].children) >= 2 and child.children[1].children[1].value == "assign_expr":
                    check_assign_expr(child, scope)
                    continue
        elif child.value == "if":
            if node.parent.value == "if_block":
                check_if(node.parent.children[2], scope)
            else:
                check_if(node.parent.children[3], scope)

        if len(child.children) != 0:
            traverse_parse_tree(child, scope)


def check_main_func():
    for symbol in SYMBOL_TABLE:
        if symbol.var_name == "main" and symbol.is_func and symbol.var_type == "INT":
            return
    error = Error("no main function with return type <INT>", 0)
    ERRORS.append(error)


def semantic_analyze(parse_tree: parser.Node):
    curr_node = parse_tree
    traverse_parse_tree(curr_node, [])
    check_main_func()
    if not len(ERRORS):
        for symbol in SYMBOL_TABLE:
            print(symbol)
    else:
        for error in ERRORS:
            print(error)

    print("Done!")


def main():
    parse_tree = parser.parse(argv[1])
    if parse_tree:
        semantic_analyze(parse_tree)


if __name__ == "__main__":
    main()

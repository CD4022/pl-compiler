import json

GRAMMAR = {
    'program': [['stmt', 'program'], ['func', 'program'], ['T_EPSILON']],
    'stmt': [['declare', 'T_SEMICOLON'], ['func_call', 'T_SEMICOLON'], ['assign_expr', 'T_SEMICOLON'], ['return_stmt']],
    'declare': [['type', 'id_list', 'T_SEMICOLON']],
    'type': [['T_INT'], ['T_CHAR'], ['T_BOOL'], ['T_VOID']],
    'id_list': [['assign_expr', 'T_COMMA', 'id_list'], ['id_name', 'T_COMMA', 'id_list'], ['id_name'], ['assign_expr']],
    'id_name': [['T_ID', 'T_LSB', 'calc_expr', 'T_RSB'], ['T_ID']],
    'func_call': [['T_ID', 'T_LP', 'par_list', 'T_RP']],
    'par_list': [['par', 'T_COMMA', 'par_list'], ['T_EPSILON']],
    'par': [['calc_expr'], ['comp_expr']],
    'assign_expr': [['id_name', 'T_ASSIGN', 'calc_expr'], ['id_name', 'T_ASSIGN', 'comp_expr']],
    'calc_expr': [['term', 'calc_expr2']],
    'clac_expr2': [['low_bin_op', 'term', 'calc_expr2'], ['T_EPSILON']],
    'term': [['fact', 'term2']],
    'term2': [['high_bin_op', 'fact', 'term2'], ['T_EPSILON']],
    'fact': [['T_LP', 'calc_expr', 'T_RP'], ['un_expr']],
    'un_expr': [['un_op', 'value'], ['value']],
    'value': [['id_name'], ['imm'], ['func_call'], ['logic_imm']],
    'logic_imm': [['T_TRUE'], ['T_FALSE']],
    'low_bin_op': [['T_PLUS'], ['T_MINUS']],
    'high_bin_op': [['T_MULT'], ['T_DIV'], ['T_MOD']],
    'un_op': [['T_PLUS'], ['T_MINUS'], ['T_NOT']],
    'block_expr': [['if_block'], ['else_block'], ['for_block']],
    'if_block': [['T_IF', 'T_LP', 'comp_expr', 'T_RP', 'T_LCB', 'block', 'T_RCB']],
    'else_block': [['T_ELSE', 'if_block'], ['T_ELSE', 'T_LCB', 'block', 'T_RCB']],
    'for_block': [['T_FOR', 'T_LP', 'for_stmt', 'T_RP', 'T_LCB', 'block', 'T_RCB']],
    'for_stmt': [['for_init', 'T_SEMICOLON', 'for_cond', 'T_SEMICOLON', 'for_step']],
    'for_init': [['declare'], ['assign_expr'], ['T_EPSILON']],
    'for_cond': [['comp_expr'], ['T_EPSILON']],
    'for_step': [['assign_expr'], ['T_EPSILON']],
    'comp_expr': [['logic_term', 'comp_expr2']],
    'comp_expr2': [['comp_bin_op', 'logic_term', 'comp_expr2'], ['T_EPSILON']],
    'logic_term': [['logic_fact', 'logic_term2']],
    'logic_term2': [['logic_bin_op', 'logic_fact', 'logic_term2'], ['T_EPSILON']],
    'logic_fact': [['T_LP', 'comp_expr', 'T_RP'], ['un_expr']],
    'comp_bin_op': [['T_EQUALS'], ['T_NOT_EQUALS'], ['T_GT'], ['T_LT'], ['T_GE'], ['T_LE']],
    'logic_bin_op': [['T_AND'], ['T_OR']],
    'func': [['type', 'T_ID', 'T_LP', 'argument_list', 'T_RP', 'T_LCB', 'block', 'T_RCB']],
    'argument_list': [['argument', 'T_COMMA', 'argument_list'], ['T_EPSILON']],
    'argument': [['type', 'id_name']],
    'block': [['stmt', 'block'], ['T_EPSILON']],
    'return_stmt': [['T_RETURN', 'return_val', 'T_SEMICOLON']],
    'return_val': [['calc_expr'], ['comp_expr'], ['T_EPSILON']]
}

FIRSTS = dict()
FOLLOWS = dict()


def make_grammar():
    return GRAMMAR


def LeftFactoring(rulesDiction):
    # for rule: A->aDF|aCV|k
    # result: A->aA'|k, A'->DF|CV

    # newDict stores newly generated
    # - rules after left factoring
    newDict = {}
    # iterate over all rules of dictionary
    for lhs in rulesDiction:
        # get rhs for given lhs
        allrhs = rulesDiction[lhs]
        # temp dictionary helps detect left factoring
        temp = dict()
        for subrhs in allrhs:
            if subrhs[0] not in list(temp.keys()):
                temp[subrhs[0]] = [subrhs]
            else:
                temp[subrhs[0]].append(subrhs)
        # if value list count for any key in temp is > 1,
        # - it has left factoring
        # new_rule stores new subrules for current LHS symbol
        new_rule = []
        # temp_dict stores new subrules for left factoring
        tempo_dict = {}
        for term_key in temp:
            # get value from temp for term_key
            allStartingWithTermKey = temp[term_key]
            if len(allStartingWithTermKey) > 1:
                # left factoring required
                # to generate new unique symbol
                # - add ' till unique not generated
                lhs_ = lhs + "'"
                while (lhs_ in rulesDiction.keys()) \
                        or (lhs_ in tempo_dict.keys()):
                    lhs_ += "'"
                # append the left factored result
                new_rule.append([term_key, lhs_])
                # add expanded rules to tempo_dict
                ex_rules = []
                for g in temp[term_key]:
                    ex_rules.append(g[1:])
                tempo_dict[lhs_] = ex_rules
            else:
                # no left factoring required
                new_rule.append(allStartingWithTermKey[0])
        # add original rule
        newDict[lhs] = new_rule
        # add newly generated rules after left factoring
        for key in tempo_dict:
            newDict[key] = tempo_dict[key]
    return newDict

def follow_terminals(statement: str):
    global FOLLOWS
    if statement in FOLLOWS.keys():
        return FOLLOWS[statement]

    follow_terminal_list = []
    for key, value in GRAMMAR.items():
        for rule in value:
            if statement in rule:
                if rule[-1] == statement:
                    follow_terminal_list.extend(follow_terminals(key))
                else:
                    i = rule.index(statement) + 1
                    if rule[i].startswith('T_'):
                        follow_terminal_list.append(rule[i])
                        break
                    else:
                        follow_terminal_list.extend(first_terminals(rule[i]))
                        break
    FOLLOWS[statement] = follow_terminal_list
    return follow_terminal_list


def first_terminals(statement: str):
    global FIRSTS
    if statement in FIRSTS.keys():
        return False, FIRSTS[statement]

    last_is_epsilon = False
    first_terminal_list = []
    for rule in GRAMMAR[statement]:
        if rule[0].startswith('T_'):
            if rule[0] == 'T_EPSILON':
                last_is_epsilon = True
                break
            first_terminal_list.append(rule[0])
        else:
            lie, rule_first = first_terminals(rule[0])
            first_terminal_list.extend(rule_first)
            if lie:
                first_terminal_list.extend(follow_terminals(rule[0]))

                # S -> ACb
                # A -> a | epsilon
                # C -> c | epsilon

    FIRSTS[statement] = list(set(first_terminal_list))
    return last_is_epsilon, first_terminal_list


if __name__ == '__main__':
    print(json.dumps(LeftFactoring(GRAMMAR), indent=4))
    # for key in GRAMMAR:
    #     follow_terminals(key)
    #     first_terminals(key)
    #
    # print(FOLLOWS)
    # print(FIRSTS)

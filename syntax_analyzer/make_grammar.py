import json

GRAMMAR = {
    'program': [['stmt', 'program'], ['declaration', 'program'], ['E']],
    'declaration': [['type', 'T_ID', "dec'"]],
    "dec'": [['func'], ["id_name'", "assign_expr", "id_list'", 'T_SEMICOLON'], ["id_name'", "id_list'", 'T_SEMICOLON']],
    'stmt': [['T_ID', "stmt'"], ['T_PRINT', "func_call", 'T_SEMICOLON'], ['return_stmt', 'T_SEMICOLON'],
             ['T_CONTINUE', 'T_SEMICOLON'], ['T_BREAK', 'T_SEMICOLON'], ['block_expr']],
    "stmt'": [['func_call', 'T_SEMICOLON'], ["id_name'", 'assign_expr', 'T_SEMICOLON']],
    'type': [['T_INT'], ['T_CHAR'], ['T_BOOL'], ['T_VOID']],
    'id_name': [['T_ID', "id_name'"]],
    "id_name'": [["T_LSB", "expr", "T_RSB"], ["E"]],
    "id_list": [["id_list''", "id_list'"]],
    "id_list'": [["T_COMMA", "id_list''", "id_list'"], ["E"]],
    "id_list''": [["id_name", "id_list'''"]],
    "id_list'''": [["E"], ["assign_expr"]],
    'func_call': [['T_LP', 'par_list', 'T_RP']],
    'par_list': [["expr", "par_list'"], ['E']],
    "par_list'": [["T_COMMA", "expr", "par_list'"], ["E"]],
    'assign_expr': [['T_ASSIGN', 'expr']],
    'expr': [['term', "expr'"]],
    "expr'": [['low_bin_op', 'term', "expr'"], ['E']],
    'term': [['fact', "term'"]],
    "term'": [['high_bin_op', 'fact', "term'"], ['E']],
    'fact': [['T_LP', 'expr', 'T_RP'], ['un_expr']],
    'un_expr': [['un_op', 'value'], ['value']],
    'value': [['T_ID', "id_name'"], ['imm'], ['T_ID', 'func_call'], ['logic_imm']],
    'imm': [['T_STR_VAL'], ['T_CHAR_VAL'], ['T_DEC_VAL'], ['T_HEX_VAL']],
    'logic_imm': [['T_TRUE'], ['T_FALSE']],
    'low_bin_op': [['T_PLUS'], ['T_MINUS'], ['T_OR'], ['T_AND']],
    'high_bin_op': [['T_MULT'], ['T_DIV'], ['T_MOD']],
    'un_op': [['T_PLUS'], ['T_MINUS'], ['T_NOT']],
    'block_expr': [['if_block'], ['for_block']],
    'if_block': [['T_IF', 'T_LP', 'comp_expr', 'T_RP', 'T_LCB', 'block', 'T_RCB', "else_if_blocks", 'else_block']],
    'else_if_blocks': [['T_ELSE', 'T_IF', 'T_LP', 'comp_expr', 'T_RP', 'T_LCB', 'block', 'T_RCB', 'else_if_blocks'],
                       ['E']],
    'else_block': [['T_ELSE', 'T_LCB', 'block', 'T_RCB'], ['E']],
    'for_block': [['T_FOR', 'T_LP', 'for_stmt', 'T_RP', 'T_LCB', 'block', 'T_RCB']],
    'for_stmt': [['for_init', 'T_SEMICOLON', 'for_cond', 'T_SEMICOLON', 'for_step']],
    'for_init': [['type', 'id_name', 'assign_expr'], ['id_name', 'assign_expr'], ['E']],
    'for_cond': [['comp_expr'], ['E']],
    'for_step': [['id_name', 'assign_expr'], ['E']],
    'comp_expr': [['expr', 'comp_bin_op', 'comp_expr'], ['expr']],
    'comp_bin_op': [['T_EQUALS'], ['T_NOT_EQUALS'], ['T_GT'], ['T_LT'], ['T_GE'], ['T_LE']],
    'func': [['T_LP', 'argument_list', 'T_RP', 'T_LCB', 'block', 'T_RCB']],
    'argument_list': [["argument", "argument_list'"], ['E']],
    "argument_list'": [["T_COMMA", "argument", "argument_list'"], ["E"]],
    'argument': [['type', 'id_name']],
    'block': [['stmt', 'block'], ['declaration', 'block'], ['E']],
    'return_stmt': [['T_RETURN', 'return_val']],
    'return_val': [['expr'], ['E']]
}

try:
    with open('lf.json') as f:
        LF_GRAMMAR = json.load(f)
except FileNotFoundError:
    LF_GRAMMAR = dict()

try:
    with open('firsts.json') as f:
        FIRSTS = json.load(f)
except FileNotFoundError:
    FIRSTS = dict()

try:
    with open('follows.json') as f:
        FOLLOWS = json.load(f)
except FileNotFoundError:
    FOLLOWS = dict()

try:
    with open('terminals.json') as f:
        TERMINALS = json.load(f)
except FileNotFoundError:
    TERMINALS = []

try:
    with open('non_terminals.json') as f:
        NON_TERMINALS = json.load(f)
except FileNotFoundError:
    NON_TERMINALS = []


# this is only executed once
def left_factoring(rules_diction):
    # for rule: A->aDF|aCV|k
    # result: A->aA'|k, A'->DF|CV

    # new_dict stores newly generated rules after left factoring
    new_dict = {}
    # iterate over all rules of dictionary
    for lhs in rules_diction:
        # get rhs(right-hand-side) for given lhs(left-hand-side)
        all_rhs = rules_diction[lhs]
        # temp dictionary helps detect left factoring by checking the first sym
        temp = dict()
        for sub_rhs in all_rhs:
            if sub_rhs[0] not in list(temp.keys()):
                temp[sub_rhs[0]] = [sub_rhs]
            else:
                temp[sub_rhs[0]].append(sub_rhs)

        # if value list count for any key in temp is > 1, it has left factoring
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
                while (lhs_ in rules_diction.keys()) \
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
        new_dict[lhs] = new_rule
        # add newly generated rules after left factoring
        for key in tempo_dict:
            new_dict[key] = tempo_dict[key]
    return new_dict


def first(rule):
    global LF_GRAMMAR, FIRSTS
    # recursion base condition
    # (for terminal or epsilon)
    if len(rule) != 0 and (rule is not None):
        if rule[0].startswith('T_'):
            return rule[0]
        elif rule[0] == 'E':
            return 'E'

    # condition for Non-Terminals
    if len(rule) != 0:
        if rule[0] in list(LF_GRAMMAR.keys()):
            # f_res temporary list of result
            f_res = []
            rhs_rules = LF_GRAMMAR[rule[0]]
            # call first on each rule of RHS
            # fetched (& take union)
            for itr in rhs_rules:
                individual_res = first(itr)
                if type(individual_res) is list:
                    for i in individual_res:
                        f_res.append(i)
                else:
                    f_res.append(individual_res)

            # if no epsilon in result received return fres
            if 'E' not in f_res:
                return f_res
            else:
                # apply epsilon
                # rule => f(ABC)=f(A)-{e} U f(BC)
                new_list = []
                f_res.remove('E')
                if len(rule) > 1:
                    ansNew = first(rule[1:])
                    if ansNew != None:
                        if type(ansNew) is list:
                            new_list = f_res + ansNew
                        else:
                            new_list = f_res + [ansNew]
                    else:
                        new_list = f_res
                    return new_list
                # if result is not already returned control reaches here
                # lastly if eplison still persists keep it in result of first
                f_res.append('E')
                return f_res


def follow(NT):
    global LF_GRAMMAR, FIRSTS, FOLLOWS

    # if NT in FOLLOW_STACK:
    #     return set()

    # FOLLOW_STACK.append(NT)

    if NT == 'program':
        # FOLLOW_STACK.pop()
        return ['$']
    
    # if already computed return
    if NT in FOLLOWS:
        return FOLLOWS[NT]
    
    # initialize result set
    res = set()
    for key in LF_GRAMMAR:
        for rule in LF_GRAMMAR[key]:
            if NT in rule:
                idx = rule.index(NT)
                if idx == len(rule) - 1:
                    print(key)
                    if key != NT:
                        res = res.union(follow(key))
                else:
                    if rule[idx + 1].startswith('T_'):
                        res.add(rule[idx + 1])
                    else:
                        f = FIRSTS[rule[idx + 1]]
                        if 'E' in f:
                            f.remove('E')
                            res = res.union(f)
                            res = res.union(follow(key))

                        else:
                            res = res.union(f)

    FOLLOWS[NT] = res
    # FOLLOW_STACK.pop()
    return res


def compute_all_follows():
    global LF_GRAMMAR, FIRSTS, FOLLOWS
    for NT in LF_GRAMMAR:
        solset = set()
        sol = follow(NT)
        if sol is not None:
            for g in sol:
                solset.add(g)
        FOLLOWS[NT] = solset


def compute_all_firsts():
    global LF_GRAMMAR, FIRSTS

    # calculate first for each rule
    # - (call first() on all RHS)
    for y in list(LF_GRAMMAR.keys()):
        t = set()
        for sub in LF_GRAMMAR.get(y):
            res = first(sub)
            if res is not None:
                if type(res) is list:
                    for u in res:
                        t.add(u)
                else:
                    t.add(res)

        # save result in 'firsts' list
        FIRSTS[y] = t


def create_lf_file():
    lf = left_factoring(GRAMMAR)

    # save the lf dict to firsts.json
    with open('lf.json', 'w') as f:
        json.dump(lf, f, indent=4)


def create_firsts_file():

    compute_all_firsts()
    for key in FIRSTS.keys():
        FIRSTS[key] = list(FIRSTS[key])

    # save the FIRSTS dict to firsts.json
    with open('firsts.json', 'w') as file:
        json.dump(FIRSTS, file, indent=4)


def create_follows_file():
    compute_all_follows()
    print(FOLLOWS)
    for key in FOLLOWS.keys():
        FOLLOWS[key] = list(FOLLOWS[key])

    # save the FOLLOWS dict to follows.json
    with open('follows.json', 'w') as file:
        json.dump(FOLLOWS, file, indent=4)


def compute_terminals():
    global GRAMMAR, TERMINALS
    for key in GRAMMAR.keys():
        for rule in GRAMMAR[key]:
            for sym in rule:
                if sym.startswith('T_'):
                    TERMINALS.append(sym)

    TERMINALS.append('E')

    # write them to a file
    with open('terminals.json', 'w') as file:
        json.dump(TERMINALS, file, indent=4)


def compute_non_terminals():
    global LF_GRAMMAR, NON_TERMINALS
    for key in LF_GRAMMAR.keys():
        NON_TERMINALS.append(key)

    # write them to a file
    with open('non_terminals.json', 'w') as file:
        json.dump(NON_TERMINALS, file, indent=4)


def rule_firsts(rule):
    firsts = set()
    for sym in rule:
        if sym in TERMINALS:
            firsts.add(sym)
            if 'E' in firsts:
                firsts.remove('E')
            break
        else:
            firsts = firsts.union(FIRSTS[sym])
            if 'E' not in FIRSTS[sym]:
                if 'E' in firsts:
                    firsts.remove('E')
                break
    else:
        firsts.add('E')

    return firsts


def create_parse_table():
    global FIRSTS, FOLLOWS, LF_GRAMMAR, TERMINALS
    parse_table = dict()
    for NT in NON_TERMINALS:
        for rule in LF_GRAMMAR[NT]:
            if rule[0] in TERMINALS:
                if NT not in parse_table:
                    parse_table[NT] = dict()
                parse_table[NT][rule[0]] = rule
            else:
                rf = rule_firsts(rule)
                for term in rf:
                    if term != 'E':
                        if NT not in parse_table:
                            parse_table[NT] = dict()
                        parse_table[NT][term] = rule
                if 'E' in rf:
                    for term in FOLLOWS[NT]:
                        if NT not in parse_table:
                            parse_table[NT] = dict()
                        parse_table[NT][term] = rule
                else:
                    nt_follow = set(FOLLOWS[NT]) - set(FIRSTS[NT])
                    if 'E' not in FIRSTS[NT]:
                        for term in nt_follow:
                            if NT not in parse_table:
                                parse_table[NT] = dict()
                            parse_table[NT][term] = 'synch'

        if 'E' in FIRSTS[NT]:
            for term in FOLLOWS[NT]:
                if NT not in parse_table:
                    parse_table[NT] = dict()
                parse_table[NT][term] = ['E']

    with open('parse_table.json', 'w') as file:
        json.dump(parse_table, file, indent=4)


def represent_grammar():
    global GRAMMAR
    for key in GRAMMAR.keys():
        print(key, '->', end=' ')
        flag = False
        for rule in GRAMMAR[key]:
            if flag:
                print('|', end=' ')
            flag = True
            for sym in rule:
                print(sym, end=' ')

        print()


def check_parse_table():
    with open('parse_table.json') as file:
        parse_table = json.load(file)

    for NT in NON_TERMINALS:
        for f in FIRSTS[NT]:
            if parse_table[NT].get(f) is None:
                print(NT, f)
                return False

    return True


if __name__ == '__main__':
    compute_terminals()
    compute_non_terminals()

    create_lf_file()

    create_firsts_file()

    create_follows_file()

    create_parse_table()
    print(check_parse_table())

    # represent_grammar()





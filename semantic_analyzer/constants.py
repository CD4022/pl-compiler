SEPARATORS = [
    'T_LP',
    'T_RP'
]

INT_TERMINALS = [
    "T_DEC_VAL",
    "T_HEX_VAL"
]

BOOL_TERMINALS = [
    'T_TRUE',
    'T_FALSE',
    'T_NOT'
]

NON_INT_BOOL_TERMINALS = [
    'T_STR_VAL',
    'T_CHAR_VAL',
]

BIN_T_OPS = {
    '+': 'T_PLUS',
    '-': 'T_MINUS',
    '*': 'T_MULT',
    '/': 'T_DIV',
    '%': 'T_MOD'
}

from sys import argv
from lexical_analyzer import lexer


class Grammar:
    def __init__(self, rules=None):
        self.rules = []
        if rules:
            self.rules = self.rules.extend(rules)


class Rule:
    def __init__(self, name, body=None):
        self.name = name
        
        


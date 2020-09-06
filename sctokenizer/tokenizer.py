from __future__ import absolute_import
import enum
from sctokenizer.token import TokenType, Token

class TokenizerState(enum.Enum):
    REGULAR = 0
    IN_STRING = 1
    IN_CHAR = 2
    IN_COMMENT = 3
    IN_LINECOMMENT = 4
    IN_MACRO = 5

    IN_NUMBER = 6
    IN_INCLUDE = 7
    IN_INCLUDE_HEADER = 8

class Tokenizer():
    def __init__(self):
        self.keyword_set = None
        self.operator_set = None
        self.linenumber = 1
        self.colnumber = 1

    def tokenize(self):
        pass

    def add_pending(self, tokens, pending, token_type, len_lines, t):
        if pending <= ' ':
            return
        for k in range(t):
            self.colnumber -= (len_lines[k] + 1)

        if pending in self.operator_set:
            tokens.append(Token(pending, TokenType.OPERATOR, self.linenumber, self.colnumber + 1))
        elif pending in self.keyword_set:
            tokens.append(Token(pending, TokenType.KEYWORD, self.linenumber, self.colnumber + 1))
        else:
            tokens.append(Token(pending, token_type, self.linenumber, self.colnumber + 1))
    
    def compact_operators(self, tokens):
        correct = []
        cur = None
        for next in tokens:
            if cur:
                if cur.token_type == TokenType.OPERATOR and \
                    next.token_type == TokenType.OPERATOR and \
                    cur.token_value not in '()[]{};' and \
                    next.token_value not in '()[]{};':
                    if (cur.token_value + next.token_value) in self.operator_set:
                        cur.token_value += next.token_value
                        next = None
                correct.append(cur)
            cur = next
        if cur:
            correct.append(cur)
        tokens = correct
        return tokens

    def is_alpha(self, cur):
        return (cur >= 'a' and cur <= 'z') or \
                (cur >= 'A' and cur <= 'Z') or \
                cur == '_' or ord(cur) > 127


    
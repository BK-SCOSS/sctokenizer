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
    # IN_OPERATOR = 6
    IN_NUMBER = 7
    IN_INCLUDE = 8
    IN_INCLUDE_HEADER = 9

class Tokenizer():
    def __init__(self):
        self.keyword_set = None
        self.operator_set = None
        self.linenumber = 1
        self.colnumber = 1

    def tokenize(self):
        pass

    def compute_line_starts(self, source_str):
        lines = source_str.split('\n')
        len_lines = [0]
        for x in lines:
            len_lines.append(len_lines[-1] + len(x) + 1)
        return len_lines

    def add_pending(self, tokens, pending, token_type, line_starts, t):
        if pending <= ' ':
            return
        self.colnumber -= line_starts[t]
        if pending in self.operator_set:
            tokens.append(Token(pending, TokenType.OPERATOR, self.linenumber, self.colnumber + 1))
        elif pending in self.keyword_set:
            tokens.append(Token(pending, TokenType.KEYWORD, self.linenumber, self.colnumber + 1))
        else:
            tokens.append(Token(pending, token_type, self.linenumber, self.colnumber + 1))

    def is_alpha(self, cur):
        return (cur >= 'a' and cur <= 'z') or \
                (cur >= 'A' and cur <= 'Z') or \
                cur == '_' or ord(cur) > 127

    def is_identifier(self, str, allow_symbols=['_']):
        temp = str
        for symbol in allow_symbols:
            temp = temp.replace(symbol, '')
        return (len(str) > 0 and len(temp) == 0) or temp.isalnum()


    

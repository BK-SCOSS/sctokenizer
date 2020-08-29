from __future__ import absolute_import

from sctokenizer.cpp_tokenizer import CppTokenizer
from sctokenizer.aset.java_keywords import keyword_set
# from sctokenizer.aset.java_operator_set import java_operator_set
from sctokenizer.token import TokenType, Token

class JavaTokenizer(CppTokenizer):
    def __init__(self):
        super().__init__()
        self.keyword_set = keyword_set

    def tokenize(self, source_str):
        len_lines = [len(x) for x in source_str.split('\n')]
        state = self.REGULAR
        pending = ''
        first_no_space = ''
        last_no_space = ''
        first_no_space_in_word = ''
        cur = ''
        prev = ''
        i = 0
        t = 0
        while i < len(source_str):
            prev = cur
            cur = source_str[i]
            if i < len(source_str) - 1:
                next = source_str[i+1]
            if prev == self.LF:
                last_no_space = ''
                first_no_space = ''
                self.linenumber += 1
                t += 1
            if cur == self.CR:
                if next == self.LF:
                    continue
                else: 
                    self.linenumber += 1
                    t += 1
                    cur = self.LF
            if cur != ' ' and cur != self.TAB:
                if cur != self.LF:
                    last_no_space = cur
                if first_no_space == '':
                    first_no_space = cur
                if first_no_space_in_word == '':
                    first_no_space_in_word = cur
                    self.colnumber = i
            if state == self.IN_COMMENT:
                # Check end of block comment
                if cur == '*':
                    if next == '/':
                        self.colnumber = i
                        self.add_pending('*/', TokenType.IDENTIFIER, len_lines, t)
                        i += 1
                        state = self.REGULAR
                        continue
            elif state == self.IN_LINECOMMENT:
                # Check end of block comment
                if cur == self.LF:
                    state = self.REGULAR
            elif state == self.IN_STRING:
                # Check end of string
                if cur == '"' and prev != '\\':
                    state = self.REGULAR
                    self.add_pending(pending, TokenType.STRING, len_lines, t)
                    pending = ''
                    first_no_space_in_word = ''
                    self.colnumber = i
                    self.add_pending(cur, TokenType.SPECIAL_SYMBOL, len_lines, t)
                else:
                    pending += cur
            elif state == self.IN_CHAR:
                # Check end of char
                if cur == "'" and prev != '\\':
                    state = self.REGULAR
                    self.add_pending(pending, TokenType.CONSTANT, len_lines, t)
                    pending = ''
                    first_no_space_in_word = ''
                    self.colnumber = i
                    self.add_pending(cur, TokenType.SPECIAL_SYMBOL, len_lines, t)
                else:
                    pending += cur
            elif state == self.IN_NUMBER:
                if (cur >= '0' and cur <= '9') or \
                    cur == '.' or cur == 'E' or cur == 'e':
                    pending += cur
                    i += 1
                    # self.colnumber += 1
                    continue
                if (cur == '-' or cur == '+') and \
                    (prev == 'E' or prev == 'e'):
                    pending += cur
                    i += 1
                    # self.colnumber += 1
                    continue
                self.add_pending(pending, TokenType.CONSTANT, len_lines, t)
                pending = ''
                first_no_space_in_word = ''
                self.colnumber = i
                if cur in self.operator_set:
                    self.add_pending(cur, TokenType.OPERATOR, len_lines, t)
                else:
                    self.add_pending(cur, TokenType.SPECIAL_SYMBOL, len_lines, t)
                state = self.REGULAR 
            elif state == self.REGULAR:
                if cur == '/':
                    if next == '*': # Begin block comments
                        state = self.IN_COMMENT
                        self.add_pending(pending, TokenType.IDENTIFIER, len_lines, t)
                        pending = ''
                        first_no_space_in_word = ''
                        self.colnumber = i
                        self.add_pending('/*', TokenType.SPECIAL_SYMBOL, len_lines, t)
                        i += 1
                        continue
                    if next == '/': # Begin line comment
                        state = self.IN_LINECOMMENT
                        self.add_pending(pending, TokenType.IDENTIFIER, len_lines, t)
                        pending = ''
                        first_no_space_in_word = ''
                        self.colnumber = i
                        self.add_pending('//', TokenType.SPECIAL_SYMBOL, len_lines, t)
                        i += 1
                        continue
                elif cur == '"':
                    state = self.IN_STRING
                    self.add_pending(pending, TokenType.IDENTIFIER, len_lines, t)
                    pending = ''
                    first_no_space_in_word = ''
                    self.colnumber = i
                    self.add_pending('"', TokenType.SPECIAL_SYMBOL, len_lines, t)
                elif cur == "'":
                    state = self.IN_CHAR
                    self.add_pending(pending, TokenType.IDENTIFIER, len_lines, t)
                    pending = ''
                    first_no_space_in_word = ''
                    self.colnumber = i
                    self.add_pending("'", TokenType.SPECIAL_SYMBOL, len_lines, t)
                elif cur >= '0' and cur <= '9':
                    if first_no_space_in_word == cur:
                        state = self.IN_NUMBER
                        self.add_pending(pending, TokenType.IDENTIFIER, len_lines, t)
                        # first_no_space_in_word = ''
                        pending = cur
                    else:
                        pending += cur
                elif self.is_alpha(cur):
                    pending += cur
                else: # cur = + - * / , ; ...
                    self.add_pending(pending, TokenType.IDENTIFIER, len_lines, t)
                    pending = ''
                    first_no_space_in_word = ''
                    if cur > ' ': 
                        self.colnumber = i
                        if cur in self.operator_set:
                            self.add_pending(cur, TokenType.OPERATOR, len_lines, t)
                        else:
                            self.add_pending(cur, TokenType.SPECIAL_SYMBOL, len_lines, t)
                        pending = ''
            i += 1
        # is Java always ends with } ?
        if len(cur) > 1:
            self.add_pending(pending, TokenType.SPECIAL_SYMBOL, len_lines, t) 
        elif pending in self.operator_set:
            self.add_pending(pending, TokenType.OPERATOR, len_lines, t)
        else:
            self.add_pending(pending, TokenType.SPECIAL_SYMBOL, len_lines, t)
        self.compact_operators()
        self.compact_operators()
        return self.tokens

    def is_alpha(self, cur):
        return (cur >= 'a' and cur <= 'z') or \
                (cur >= 'A' and cur <= 'Z') or \
                cur == '_' or cur == '$' or ord(cur) > 127


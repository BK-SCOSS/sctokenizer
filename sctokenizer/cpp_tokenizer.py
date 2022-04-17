from __future__ import absolute_import

from sctokenizer.tokenizer import Tokenizer, TokenizerState
from sctokenizer.assets.cpp_keywords import cpp_keyword_set
from sctokenizer.assets.cpp_operators import cpp_operator_set
from sctokenizer.token import TokenType, Token

class CppTokenizer(Tokenizer):
    def __init__(self):
        super().__init__()
        self.keyword_set = cpp_keyword_set
        self.operator_set = cpp_operator_set

    def tokenize(self, source_str):
        if len(source_str) < 1:
            return []
        len_lines = [len(x) for x in source_str.split('\n')]
        tokens = []
        state = TokenizerState.REGULAR
        pending = ''
        first_no_space = ''
        last_no_space = ''
        first_no_space_in_macro = ''
        second_no_space_in_macro = ''
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
            if prev == '\n':
                last_no_space = ''
                first_no_space = ''
                first_no_space_in_word = ''
                self.linenumber += 1
                t += 1
            if cur == '\r':
                if next == '\n':
                    i += 1
                    continue
                else: # Not sure about this part
                    self.linenumber += 1
                    t += 1
                    cur = '\n'
            if cur != ' ' and cur != '\t':
                if cur != '\n':
                    last_no_space = cur
                if first_no_space == '':
                    first_no_space = cur
                if first_no_space_in_word == '':
                    first_no_space_in_word = cur
                    self.colnumber = i

            if state == TokenizerState.IN_COMMENT:
                # Check end of block comment
                if cur == '*':
                    if next == '/':
                        self.colnumber = i
                        self.add_pending(tokens, '*/', TokenType.COMMENT_SYMBOL, len_lines, t)
                        i += 1
                        state = TokenizerState.REGULAR
                        continue

            elif state == TokenizerState.IN_LINECOMMENT:
                # Check end of line comment
                if cur == '\n':
                    state = TokenizerState.REGULAR

            elif state == TokenizerState.IN_MACRO:
                # Get first char after # in marco
                if cur == ' ' or cur == '\t':
                    i += 1
                    continue
                if cur != ' ' and cur != '\t' and first_no_space_in_macro == '':
                    first_no_space_in_macro = cur
                    second_no_space_in_macro = next
                # Check end of marco
                if cur == '\n' and last_no_space != '\\':
                    state = TokenizerState.REGULAR
                    first_no_space_in_macro = ''
                    second_no_space_in_macro = ''

                # Can handle:
                # include <bits/stdc++.h>
                # define circleArea(r) (3.1415*(r)*(r))
                # define PI 3.1415
                # handle #include vs #define, undef, pragma
                if first_no_space_in_macro == 'i' and second_no_space_in_macro == 'n':
                    state = TokenizerState.IN_INCLUDE
                    first_no_space_in_macro = ''
                    second_no_space_in_macro = ''
                else:
                    state = TokenizerState.REGULAR
                    first_no_space_in_macro = ''
                    second_no_space_in_macro = ''
                if self.is_alpha(cur):
                    pending += cur

            elif state == TokenizerState.IN_INCLUDE:
                if cur == '<' or cur == '"':
                    state = TokenizerState.IN_INCLUDE_HEADER
                    self.add_pending(tokens, pending, TokenType.KEYWORD, len_lines, t) # pending is "include"
                    pending = ''
                    first_no_space_in_word = ''
                    self.colnumber = i
                    self.add_pending(tokens, cur, TokenType.SPECIAL_SYMBOL, len_lines, t)
                elif cur != ' ' and cur != '\t':
                    pending += cur

            elif state == TokenizerState.IN_INCLUDE_HEADER:
                if cur == '>' or cur == '"':
                    state = TokenizerState.REGULAR
                    self.add_pending(tokens, pending, TokenType.IDENTIFIER, len_lines, t) # header is an identifier
                    pending = ''
                    first_no_space_in_word = ''
                    self.colnumber = i
                    self.add_pending(tokens, cur, TokenType.SPECIAL_SYMBOL, len_lines, t)
                elif cur != ' ' and cur != '\t':
                    pending += cur

            elif state == TokenizerState.IN_STRING:
                # Check end of string
                if cur == '"' and prev != '\\':
                    state = TokenizerState.REGULAR
                    self.add_pending(tokens, pending, TokenType.STRING, len_lines, t)
                    pending = ''
                    first_no_space_in_word = ''
                    self.colnumber = i
                    self.add_pending(tokens, cur, TokenType.SPECIAL_SYMBOL, len_lines, t)
                else:
                    pending += cur

            elif state == TokenizerState.IN_CHAR:
                # Check end of char
                if cur == "'" and prev != '\\':
                    state = TokenizerState.REGULAR
                    self.add_pending(tokens, pending, TokenType.CONSTANT, len_lines, t)
                    pending = ''
                    first_no_space_in_word = ''
                    self.colnumber = i
                    self.add_pending(tokens, cur, TokenType.SPECIAL_SYMBOL, len_lines, t)
                else:
                    pending += cur

            elif state == TokenizerState.IN_NUMBER:
                if (cur >= '0' and cur <= '9') or cur == '.' \
                    or (cur >= 'A' and cur <= 'F') \
                    or (cur >= 'a' and cur <= 'f') \
                    or cur == 'X' or cur == 'x':
                    pending += cur
                    i += 1
                    continue
                if (cur == '-' or cur == '+') and \
                    (prev == 'E' or prev == 'e'):
                    pending += cur
                    i += 1
                    continue
                self.add_pending(tokens, pending, TokenType.CONSTANT, len_lines, t)
                first_no_space_in_word = cur
                pending = cur
                self.colnumber = i
                state = TokenizerState.REGULAR 

            elif state == TokenizerState.REGULAR:
                if pending in self.operator_set:
                    if (pending + cur) in self.operator_set:
                        pending += cur
                        i += 1
                        continue
                    else:
                        self.add_pending(tokens, pending, TokenType.OPERATOR, len_lines, t)
                        pending = ''
                        first_no_space_in_word = cur
                        self.colnumber = i

                if len(pending) == 1 and not self.is_identifier(pending):
                    self.add_pending(tokens, pending, TokenType.SPECIAL_SYMBOL, len_lines, t)
                    pending = ''
                    first_no_space_in_word = cur
                    self.colnumber = i
                
                if cur == '/':
                    if next == '*': # Begin block comments
                        state = TokenizerState.IN_COMMENT
                        if self.is_identifier(pending):
                            self.add_pending(tokens, pending, TokenType.IDENTIFIER, len_lines, t)
                        else:
                            self.add_pending(tokens, pending, TokenType.SPECIAL_SYMBOL, len_lines, t)
                        pending = ''
                        first_no_space_in_word = ''
                        self.colnumber = i
                        self.add_pending(tokens, '/*', TokenType.COMMENT_SYMBOL, len_lines, t)
                        i += 1
                        continue
                    if next == '/': # Begin line comment
                        state = TokenizerState.IN_LINECOMMENT
                        if self.is_identifier(pending):
                            self.add_pending(tokens, pending, TokenType.IDENTIFIER, len_lines, t)
                        else:
                            self.add_pending(tokens, pending, TokenType.SPECIAL_SYMBOL, len_lines, t)
                        pending = ''
                        first_no_space_in_word = ''
                        self.colnumber = i
                        self.add_pending(tokens, '//', TokenType.COMMENT_SYMBOL, len_lines, t)
                        i += 1
                        continue
                elif cur == '"':
                    state = TokenizerState.IN_STRING
                    if self.is_identifier(pending):
                        self.add_pending(tokens, pending, TokenType.IDENTIFIER, len_lines, t)
                    else:
                        self.add_pending(tokens, pending, TokenType.SPECIAL_SYMBOL, len_lines, t)
                    pending = ''
                    first_no_space_in_word = ''
                    self.colnumber = i
                    self.add_pending(tokens, '"', TokenType.SPECIAL_SYMBOL, len_lines, t)
                elif cur == "'":
                    state = TokenizerState.IN_CHAR
                    if self.is_identifier(pending):
                        self.add_pending(tokens, pending, TokenType.IDENTIFIER, len_lines, t)
                    else:
                        self.add_pending(tokens, pending, TokenType.SPECIAL_SYMBOL, len_lines, t)
                    pending = ''
                    first_no_space_in_word = ''
                    self.colnumber = i
                    self.add_pending(tokens, "'", TokenType.SPECIAL_SYMBOL, len_lines, t)
                elif cur == '#' and first_no_space == cur:
                    state = TokenizerState.IN_MACRO
                    if self.is_identifier(pending):
                        self.add_pending(tokens, pending, TokenType.IDENTIFIER, len_lines, t)
                    else:
                        self.add_pending(tokens, pending, TokenType.SPECIAL_SYMBOL, len_lines, t)
                    pending = ''
                    first_no_space_in_word = ''
                    self.colnumber = i
                    self.add_pending(tokens, '#', TokenType.SPECIAL_SYMBOL, len_lines, t)
                elif cur >= '0' and cur <= '9':
                    if first_no_space_in_word == cur:
                        state = TokenizerState.IN_NUMBER
                        if self.is_identifier(pending):
                            self.add_pending(tokens, pending, TokenType.IDENTIFIER, len_lines, t)
                        else:
                            self.add_pending(tokens, pending, TokenType.SPECIAL_SYMBOL, len_lines, t)
                        self.colnumber = i
                        # first_no_space_in_word = ''
                        pending = cur
                    else:
                        pending += cur
                elif self.is_alpha(cur): 
                    pending += cur
                elif cur in self.operator_set: # cur = + - * / , ...
                    if self.is_identifier(pending):
                        self.add_pending(tokens, pending, TokenType.IDENTIFIER, len_lines, t)
                    else:
                        self.add_pending(tokens, pending, TokenType.SPECIAL_SYMBOL, len_lines, t)
                    pending = cur
                    first_no_space_in_word = cur
                    self.colnumber = i
                else: # cur = ;, ', space
                    if self.is_identifier(pending):
                        self.add_pending(tokens, pending, TokenType.IDENTIFIER, len_lines, t)
                    else:
                        self.add_pending(tokens, pending, TokenType.SPECIAL_SYMBOL, len_lines, t)
                    pending = ''
                    first_no_space_in_word = ''
                    if cur > ' ': 
                        self.colnumber = i
                        self.add_pending(tokens, cur, TokenType.SPECIAL_SYMBOL, len_lines, t)
            i += 1
        # is Cpp always ends with } ?
        if self.is_identifier(pending):
            self.add_pending(tokens, pending, TokenType.IDENTIFIER, len_lines, t)
        else:
            self.add_pending(tokens, pending, TokenType.SPECIAL_SYMBOL, len_lines, t)
        return tokens
from __future__ import absolute_import

from sctokenizer.tokenizer import Tokenizer, TokenizerState
from sctokenizer.assets.python_keywords import python_keyword_set
from sctokenizer.assets.python_operators import python_operator_set
from sctokenizer.token import TokenType, Token

class PythonTokenizer(Tokenizer):
    def __init__(self):
        super().__init__()
        self.keyword_set = python_keyword_set
        self.operator_set = python_operator_set

    def tokenize(self, source_str):
        if len(source_str) < 1:
            return []
        line_starts = self.compute_line_starts(source_str)
        tokens = []
        state = TokenizerState.REGULAR
        pending = ''
        first_no_space = ''
        first_no_space_in_word = ''
        first_char_in_string = ''
        first_char_in_comment = ''
        cur = ''
        prev = ''
        i = 0
        t = 0
        while i < len(source_str):
            prev = cur
            cur = source_str[i]
            if i < len(source_str) - 1:
                next = source_str[i+1]
            else:
                next = ''

            if i < len(source_str) - 2:
                nextnext = source_str[i+2]
            else:
                nextnext = ''

            if prev == '\n':
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
                if first_no_space == '':
                    first_no_space = cur
                if first_no_space_in_word == '':
                    first_no_space_in_word = cur
                    self.colnumber = i
            if state == TokenizerState.IN_COMMENT:
                # Check end of block comment
                if cur == first_char_in_comment and \
                    next == first_char_in_comment and \
                    nextnext == first_char_in_comment:
                    first_char_in_comment = ''
                    self.colnumber = i
                    self.add_pending(tokens, cur*3, TokenType.COMMENT_SYMBOL, line_starts, t)
                    i += 3
                    state = TokenizerState.REGULAR
                    continue
            elif state == TokenizerState.IN_LINECOMMENT:
                # Check end of line comment
                if cur == '\n':
                    state = TokenizerState.REGULAR
            elif state == TokenizerState.IN_STRING:
                # Check end of string
                if cur == first_char_in_string and prev != '\\':
                    first_char_in_string = ''
                    state = TokenizerState.REGULAR
                    self.add_pending(tokens, pending, TokenType.STRING, line_starts, t)
                    pending = ''
                    first_no_space_in_word = ''
                    self.colnumber = i
                    self.add_pending(tokens, cur, TokenType.SPECIAL_SYMBOL, line_starts, t)
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
                self.add_pending(tokens, pending, TokenType.CONSTANT, line_starts, t)
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
                        self.add_pending(tokens, pending, TokenType.OPERATOR, line_starts, t)
                        pending = ''
                        first_no_space_in_word = cur
                        self.colnumber = i

                if len(pending) == 1 and not self.is_identifier(pending):
                    self.add_pending(tokens, pending, TokenType.SPECIAL_SYMBOL, line_starts, t)
                    pending = ''
                    first_no_space_in_word = cur
                    self.colnumber = i

                if (first_no_space == '"' or first_no_space == "'") and \
                    cur == first_no_space and \
                    next == first_no_space and \
                    nextnext == first_no_space:
                    # Begin block comment
                    if first_char_in_comment == '':
                        first_char_in_comment = cur
                    state = TokenizerState.IN_COMMENT
                    if self.is_identifier(pending):
                        self.add_pending(tokens, pending, TokenType.IDENTIFIER, line_starts, t)
                    else:
                        self.add_pending(tokens, pending, TokenType.SPECIAL_SYMBOL, line_starts, t)
                    pending = ''
                    first_no_space_in_word = ''
                    self.colnumber = i
                    self.add_pending(tokens, cur*3, TokenType.COMMENT_SYMBOL, line_starts, t)
                    i += 3
                    continue
                elif cur == '"' or cur == "'":
                    if first_char_in_string == '':
                        first_char_in_string = cur
                    state = TokenizerState.IN_STRING
                    if self.is_identifier(pending):
                        self.add_pending(tokens, pending, TokenType.IDENTIFIER, line_starts, t)
                    else:
                        self.add_pending(tokens, pending, TokenType.SPECIAL_SYMBOL, line_starts, t)
                    pending = ''
                    first_no_space_in_word = ''
                    self.colnumber = i
                    self.add_pending(tokens, cur, TokenType.SPECIAL_SYMBOL, line_starts, t)
                elif cur == '#':
                    # Begin line comment
                    state = TokenizerState.IN_LINECOMMENT
                    if self.is_identifier(pending):
                        self.add_pending(tokens, pending, TokenType.IDENTIFIER, line_starts, t)
                    else:
                        self.add_pending(tokens, pending, TokenType.SPECIAL_SYMBOL, line_starts, t)
                    pending = ''
                    first_no_space_in_word = ''
                    self.colnumber = i
                    self.add_pending(tokens, '#', TokenType.COMMENT_SYMBOL, line_starts, t)
                    i += 1
                    continue
                elif cur >= '0' and cur <= '9':
                    if first_no_space_in_word == cur:
                        state = TokenizerState.IN_NUMBER
                        if self.is_identifier(pending):
                            self.add_pending(tokens, pending, TokenType.IDENTIFIER, line_starts, t)
                        else:
                            self.add_pending(tokens, pending, TokenType.SPECIAL_SYMBOL, line_starts, t)
                        # first_no_space_in_word = ''
                        pending = cur
                    else:
                        pending += cur
                elif self.is_alpha(cur):
                    pending += cur
                elif cur in self.operator_set: # cur = + - * / , ...
                    if self.is_identifier(pending):
                        self.add_pending(tokens, pending, TokenType.IDENTIFIER, line_starts, t)
                    else:
                        self.add_pending(tokens, pending, TokenType.SPECIAL_SYMBOL, line_starts, t)
                    pending = cur
                    first_no_space_in_word = cur
                    self.colnumber = i
                else: # cur = ;, ', space
                    if self.is_identifier(pending):
                        self.add_pending(tokens, pending, TokenType.IDENTIFIER, line_starts, t)
                    else:
                        self.add_pending(tokens, pending, TokenType.SPECIAL_SYMBOL, line_starts, t)
                    pending = ''
                    first_no_space_in_word = ''
                    if cur > ' ': 
                        self.colnumber = i
                        self.add_pending(tokens, cur, TokenType.SPECIAL_SYMBOL, line_starts, t)
            i += 1
        # End of the program
        # This need to be fixed in the future
        if self.is_identifier(pending):
            self.add_pending(tokens, pending, TokenType.IDENTIFIER, line_starts, t)
        else:
            self.add_pending(tokens, pending, TokenType.SPECIAL_SYMBOL, line_starts, t)
        return tokens


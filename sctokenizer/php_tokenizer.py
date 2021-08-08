from __future__ import absolute_import

from sctokenizer.tokenizer import Tokenizer, TokenizerState
from sctokenizer.assets.php_keywords import php_keyword_set
from sctokenizer.assets.php_operators import php_operator_set
from sctokenizer.token import TokenType, Token

class PhpTokenizer(Tokenizer):
    
    def __init__(self):
        super().__init__()
        self.keyword_set = php_keyword_set
        self.operator_set = php_operator_set

    def tokenize(self, source_str):
        if len(source_str) < 1:
            return []
        len_lines = [len(x) for x in source_str.split('\n')]
        tokens = []
        state = TokenizerState.REGULAR
        pending = ''
        first_no_space = ''
        first_no_space_in_word = ''
        first_char_in_string = ''
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
            elif state == TokenizerState.IN_STRING:
                # Check end of string
                if cur == first_char_in_string and prev != '\\':
                    first_char_in_string = ''
                    state = TokenizerState.REGULAR
                    self.add_pending(tokens, pending, TokenType.STRING, len_lines, t)
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

                if len(pending) == 1 and not self.is_identifier(pending, ['_', '$']):
                    self.add_pending(tokens, pending, TokenType.SPECIAL_SYMBOL, len_lines, t)
                    pending = ''
                    first_no_space_in_word = cur
                    self.colnumber = i

                if cur == '/':
                    if next == '*': # Begin block comments
                        state = TokenizerState.IN_COMMENT
                        if self.is_identifier(pending, ['_', '$']):
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
                        if self.is_identifier(pending, ['_', '$']):
                            self.add_pending(tokens, pending, TokenType.IDENTIFIER, len_lines, t)
                        else:
                            self.add_pending(tokens, pending, TokenType.SPECIAL_SYMBOL, len_lines, t)
                        pending = ''
                        first_no_space_in_word = ''
                        self.colnumber = i
                        self.add_pending(tokens, '//', TokenType.COMMENT_SYMBOL, len_lines, t)
                        i += 1
                        continue
                elif cur == '"' or cur == "'":
                    if first_char_in_string == '':
                        first_char_in_string = cur
                    state = TokenizerState.IN_STRING
                    if self.is_identifier(pending, ['_', '$']):
                        self.add_pending(tokens, pending, TokenType.IDENTIFIER, len_lines, t)
                    else:
                        self.add_pending(tokens, pending, TokenType.SPECIAL_SYMBOL, len_lines, t)
                    pending = ''
                    first_no_space_in_word = ''
                    self.colnumber = i
                    self.add_pending(tokens, cur, TokenType.SPECIAL_SYMBOL, len_lines, t)
                elif cur == '#':
                    # Begin line comment
                    state = TokenizerState.IN_LINECOMMENT
                    if self.is_identifier(pending, ['_', '$']):
                        self.add_pending(tokens, pending, TokenType.IDENTIFIER, len_lines, t)
                    else:
                        self.add_pending(tokens, pending, TokenType.SPECIAL_SYMBOL, len_lines, t)
                    pending = ''
                    first_no_space_in_word = ''
                    self.colnumber = i
                    self.add_pending(tokens, '#', TokenType.COMMENT_SYMBOL, len_lines, t)
                    i += 1
                    continue
                elif cur >= '0' and cur <= '9':
                    if first_no_space_in_word == cur:
                        state = TokenizerState.IN_NUMBER
                        if self.is_identifier(pending, ['_', '$']):
                            self.add_pending(tokens, pending, TokenType.IDENTIFIER, len_lines, t)
                        else:
                            self.add_pending(tokens, pending, TokenType.SPECIAL_SYMBOL, len_lines, t)
                        # first_no_space_in_word = ''
                        pending = cur
                    else:
                        pending += cur
                elif self.is_alpha(cur):
                    pending += cur
                elif cur in self.operator_set: # cur = + - * / , ...
                    if self.is_identifier(pending, ['_', '$']):
                        self.add_pending(tokens, pending, TokenType.IDENTIFIER, len_lines, t)
                    else:
                        self.add_pending(tokens, pending, TokenType.SPECIAL_SYMBOL, len_lines, t)
                    pending = cur
                    first_no_space_in_word = cur
                    self.colnumber = i
                elif cur == '$':
                    pending += cur
                else: # cur = ;, ', space
                    if self.is_identifier(pending, ['_', '$']):
                        self.add_pending(tokens, pending, TokenType.IDENTIFIER, len_lines, t)
                    else:
                        self.add_pending(tokens, pending, TokenType.SPECIAL_SYMBOL, len_lines, t)
                    pending = ''
                    first_no_space_in_word = ''
                    if cur > ' ': 
                        self.colnumber = i
                        self.add_pending(tokens, cur, TokenType.SPECIAL_SYMBOL, len_lines, t)
            i += 1
        # End of the program
        # This need to be fixed in the future
        if self.is_identifier(pending, ['_', '$']):
            self.add_pending(tokens, pending, TokenType.IDENTIFIER, len_lines, t)
        else:
            self.add_pending(tokens, pending, TokenType.SPECIAL_SYMBOL, len_lines, t)
        return tokens


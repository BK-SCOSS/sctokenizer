from __future__ import absolute_import

from sctokenizer.tokenizer import Tokenizer
from sctokenizer.keyword.cpp_keyword import keyword_set
from sctokenizer.token import TokenType, Token

class CppTokenizer(Tokenizer):
    def __init__(self):
        super().__init__()
        self.REGULAR = 0
        self.IN_STRING = 1
        self.IN_CHAR = 2
        self.IN_MACRO = 3
        self.IN_COMMENT = 4
        self.IN_LINECOMMENT = 5
        self.IN_NUMBER = 6
        self.keyword_set = keyword_set
        self.operator_set = {
            '++', '--', '+', '-', '*', '/', '%', '<', '>', '<=', '^=', 
            '>=', '==', '!=', '&&', '||', '!', '&', '|', '<<', '>>', '&='
            '~', '^', '=', '+=', '-=', '*=', '/=', '%=', '|=', '?', ':',
            '<<=', '>>='
        } # Becareful with ?: operator
        self.linenumber = 1
        self.tokens = []

    def tokenize(self, source_str):
        state = self.REGULAR
        pending = ''
        first_no_space = ''
        last_no_space = ''
        first_no_space_in_macro = ''
        cur = ''
        prev = ''
        i = 0
        while i < len(source_str):
            prev = cur
            cur = source_str[i]
            # print ('this cur = ' + cur)
            # next = ''
            if i < len(source_str) - 1:
                next = source_str[i+1]
            if prev == self.LF:
                last_no_space = ''
                first_no_space = ''
                self.linenumber += 1
            if cur == self.CR:
                if next == self.LF:
                    continue
                else: 
                    self.linenumber += 1
                    cur = self.LF
            if cur != ' ' and cur != self.TAB:
                if cur != self.LF:
                    last_no_space = cur
                if first_no_space == '':
                    first_no_space = cur
            if state == self.IN_COMMENT:
                # Check end of block comment
                if cur == '*':
                    if next == '/':
                        i += 1
                        state = self.REGULAR
                        continue
            elif state == self.IN_LINECOMMENT:
                # Check end of block comment
                if cur == self.LF:
                    state = self.REGULAR
            elif state == self.IN_MACRO:
                # Get first char after # in marco
                if cur != ' ' and cur != self.TAB and first_no_space_in_macro == '':
                    first_no_space_in_macro = cur
                # Check end of marco
                if cur == self.LF and last_no_space != '\\':
                    state = self.REGULAR
                    first_no_space_in_macro = ''

                # Can handle:
                # include <bits/stdc++.h>
                # define circleArea(r) (3.1415*(r)*(r))
                # define PI 3.1415
                # handle #define, undef and #include
                if first_no_space_in_macro == 'd' or first_no_space_in_macro == 'u':
                    state = self.REGULAR
                    if self.is_alpha(cur):
                        pending += cur
                elif self.is_alpha(cur) or cur == '/' or cur == '.' or cur == '+' or cur == '"':
                    pending += cur

                else: # cur is <, >, ), number...
                    self.add_pending(pending, TokenType.IDENTIFIER)
                    pending = ''
                    self.add_pending(cur, TokenType.SPECIAL_SYMBOL)

                # print('pending = ' + pending)
                
            elif state == self.IN_STRING:
                # Check end of string
                if cur == '"' and prev != '\\':
                    state = self.REGULAR
                    self.add_pending(pending, TokenType.STRING)
                    pending = ''
                    self.add_pending(cur, TokenType.SPECIAL_SYMBOL)
                else:
                    pending += cur
                # Discard two backslash?
                # if cur == '\\' and prev == '\\':
                #     cur = ' '
            elif state == self.IN_CHAR:
                # Check end of char
                if cur == "'" and prev != '\\':
                    # pending += "'"
                    state = self.REGULAR
                    self.add_pending(pending, TokenType.CONSTANT)
                    pending = ''
                    self.add_pending(cur, TokenType.SPECIAL_SYMBOL)
                else:
                    pending += cur
                # Discard two backslash?
                # if cur == '\\' and prev == '\\':
                #     cur = ' '
            elif state == self.IN_NUMBER:
                if (cur >= '0' and cur <= '9') or \
                    cur == '.' or cur == 'E' or cur == 'e':
                    pending += cur
                    i += 1
                    continue
                if (cur == '-' or cur == '+') and \
                    (prev == 'E' or prev == 'e'):
                    pending += cur
                    i += 1
                    continue
                self.add_pending(pending, TokenType.CONSTANT)
                pending = ''
                if cur in self.operator_set:
                    self.add_pending(cur, TokenType.OPERATOR)
                else:
                    self.add_pending(cur, TokenType.SPECIAL_SYMBOL)
                state = self.REGULAR 
            elif state == self.REGULAR:
                if cur == '/':
                    if next == '*': # Begin block comments
                        state = self.IN_COMMENT
                        self.add_pending(pending, TokenType.IDENTIFIER)
                        pending = ''
                        i += 1
                        self.add_pending('/*', TokenType.SPECIAL_SYMBOL)
                        continue
                    if next == '/': # Begin line comment
                        state = self.IN_LINECOMMENT
                        self.add_pending(pending, TokenType.IDENTIFIER)
                        pending = ''
                        i += 1
                        self.add_pending('//', TokenType.SPECIAL_SYMBOL)
                        continue
                elif cur == '"':
                    state = self.IN_STRING
                    self.add_pending(pending, TokenType.IDENTIFIER)
                    pending = ''
                    self.add_pending('"', TokenType.SPECIAL_SYMBOL)
                elif cur == "'":
                    state = self.IN_CHAR
                    self.add_pending(pending, TokenType.IDENTIFIER)
                    pending = ''
                    self.add_pending("'", TokenType.SPECIAL_SYMBOL)
                elif cur == '#' and first_no_space == cur:
                    state = self.IN_MACRO
                    self.add_pending(pending, TokenType.IDENTIFIER)
                    pending = ''
                    self.add_pending('#', TokenType.SPECIAL_SYMBOL)
                elif cur >= '0' and cur <= '9':
                    state = self.IN_NUMBER
                    self.add_pending(pending, TokenType.IDENTIFIER)
                    pending = cur
                elif self.is_alpha(cur):
                    pending += cur
                else: # cur = + - * / , ; ...
                    self.add_pending(pending, TokenType.IDENTIFIER)
                    pending = ''
                    if cur > ' ': # cur may be operator or special character
                        # Need to handle "cin >>", "cout <<"
                        if cur in self.operator_set:
                            self.add_pending(cur, TokenType.OPERATOR)
                        else:
                            self.add_pending(cur, TokenType.SPECIAL_SYMBOL)
                        pending = ''
            i += 1
        self.add_pending(pending, TokenType.SPECIAL_SYMBOL) # is Cpp always ends with } ?
        self.compact_operators()
        self.compact_operators()
        return self.tokens

    def add_pending(self, pending, token_type):
        if pending <= ' ':
            return
        if token_type == TokenType.IDENTIFIER and \
            pending in self.keyword_set:
            self.tokens.append(Token(pending, TokenType.KEYWORD, self.linenumber))
        else:
            self.tokens.append(Token(pending, token_type, self.linenumber))

    def is_alpha(self, cur):
        return (cur >= 'a' and cur <= 'z') or \
                (cur >= 'A' and cur <= 'Z') or \
                cur == '_' or ord(cur) > 127

    def compact_operators(self):
        correct = []
        cur = None
        for next in self.tokens:
            if cur:
                if cur.token_type == TokenType.OPERATOR and \
                    next.token_type == TokenType.OPERATOR and \
                    cur.token_value not in '()[]{};' and \
                    next.token_value not in '()[]{};':
                    cur.token_value += next.token_value
                    next = None
                correct.append(cur)
            cur = next
        if cur:
            correct.append(cur)
        self.tokens = correct
                    
    # def correct_operators():
    #     # A Function to correct those operators which is similar to special symbols
    #     # such as: * (in a*b or int *a) or << (in a << 2 or cout << a) or & (in a = 3 & 2 or scanf("%d", &a))
    #     # But are * and << operators?
    #     # References:
    #     # https://www3.ntu.edu.sg/home/ehchua/programming/cpp/cp4_PointerReference.html
    #     # http://www.cplusplus.com/reference/istream/istream/operator%3E%3E/
    #     pass


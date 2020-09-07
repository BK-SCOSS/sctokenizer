from __future__ import absolute_import

from sctokenizer.cpp_tokenizer import CppTokenizer
from sctokenizer.assets.c_keywords import c_keyword_set
from sctokenizer.assets.c_operators import c_operator_set
from sctokenizer.token import TokenType, Token

class CTokenizer(CppTokenizer):
    def __init__(self):
        super().__init__()
        self.keyword_set = c_keyword_set
        self.operator_set = c_operator_set


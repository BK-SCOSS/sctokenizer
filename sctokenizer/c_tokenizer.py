from __future__ import absolute_import

from sctokenizer.cpp_tokenizer import CppTokenizer
from sctokenizer.assets.c_keywords import keyword_set
# from sctokenizer.aset.c_operator_set import c_operator_set
from sctokenizer.token import TokenType, Token

class CTokenizer(CppTokenizer):
    def __init__(self):
        super().__init__()
        self.keyword_set = keyword_set

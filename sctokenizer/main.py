from __future__ import absolute_import

from .source import Source
from .c_tokenizer import CTokenizer
from .cpp_tokenizer import CppTokenizer
from .java_tokenizer import JavaTokenizer
from .python_tokenizer import PythonTokenizer

def tokenize_str(source_str, lang=None):
    src = Source.from_str(source_str, lang)
    return src.tokenize() 

def tokenize_file(filepath, lang=None):
    src = Source.from_file(filepath, lang)
    return src.tokenize()

    
from __future__ import absolute_import

from .source import Source
from .c_tokenizer import CTokenizer
from .cpp_tokenizer import CppTokenizer
from .java_tokenizer import JavaTokenizer
from .python_tokenizer import PythonTokenizer

def tokenize_str(source_str, lang=None):
    src = Source.from_str(source_str, lang)
    if src.lang == 'c':
        c_tokenizer = CTokenizer()
        return c_tokenizer.tokenize(src.source_str)
    elif src.lang == 'cpp':
        cpp_tokenizer = CppTokenizer()
        return cpp_tokenizer.tokenize(src.source_str)
    elif src.lang == 'java':
        java_tokenizer = JavaTokenizer()
        return java_tokenizer.tokenize(src.source_str)
    elif src.lang == 'py':
        python_tokenizer = PythonTokenizer()
        return python_tokenizer.tokenize(src.source_str)
    else:
        return None
    

def tokenize_file(filepath, lang=None):
    src = Source.from_file(filepath, lang)
    return tokenize_str(src.source_str, src.lang)

    

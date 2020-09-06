from __future__ import absolute_import

from sctokenizer.c_tokenizer import CTokenizer
from sctokenizer.cpp_tokenizer import CppTokenizer
from sctokenizer.java_tokenizer import JavaTokenizer
from sctokenizer.python_tokenizer import PythonTokenizer

class Source():
    def __init__(self, source_str, lang=None):
        self.source_str = source_str
        if lang is None:
            self.lang = self.detect_language(self.source_str)
        else:
            self.lang = lang
    
    @classmethod
    def from_file(cls, filepath, lang=None):
        """
            return the Source object
            :rtype: Source
        """
        with open(filepath) as f:
            source_str = f.read()
        if lang is None:
            lang = cls.detect_language(source_str)
        return Source(source_str, lang)


    @classmethod
    def from_str(cls, source_str, lang=None):
        """
            return the Source object
            :rtype: Source
        """
        if lang is None:
            lang = cls.detect_language(source_str)
        return Source(source_str, lang)

    def tokenize(self):
        if self.lang == 'c':
            c_tokenizer = CTokenizer()
            return c_tokenizer.tokenize(self.source_str)
        elif self.lang == 'cpp':
            cpp_tokenizer = CppTokenizer()
            return cpp_tokenizer.tokenize(self.source_str)
        elif self.lang == 'java':
            java_tokenizer = JavaTokenizer()
            return java_tokenizer.tokenize(self.source_str)
        elif self.lang == 'py':
            python_tokenizer = PythonTokenizer()
            return python_tokenizer.tokenize(self.source_str)
        else:
            raise ValueError("Upsupported language")

    @classmethod
    def detect_language(cls, source_str):
        """
            detect languge of source code
            :rtype: str
        """
        return 'cpp'


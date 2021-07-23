from __future__ import absolute_import

from sctokenizer.c_tokenizer import CTokenizer
from sctokenizer.cpp_tokenizer import CppTokenizer
from sctokenizer.java_tokenizer import JavaTokenizer
from sctokenizer.python_tokenizer import PythonTokenizer
from sctokenizer.php_tokenizer import PhpTokenizer

import os
import enum

LANG_MAP = {
    'cc': 'cpp',
    'py': 'python',
}

def check_language(lang):
    if lang in LANG_MAP:
        return LANG_MAP[lang]
    return lang

class SourceState(enum.Enum):
    INIT = 0
    UNTOKENIZED = 1
    TOKENIZED = 2

class Source():
    def __init__(self, source_str, lang=None, name=None):
        self.__state = SourceState.INIT

        self.source_str = source_str
        if lang is None:
            self.lang = self.detect_language(self.source_str)
        else:
            self.lang = check_language(lang)
        self.name = name
        self.tokens = None
    
    @classmethod
    def from_file(cls, filepath, lang=None, name=None):
        """
            return the Source object
            :rtype: Source
        """
        with open(filepath, encoding='utf-8') as f:
            source_str = f.read()
        if lang is None:
            ext = os.path.splitext(filepath)[1][1:]
            lang = LANG_MAP[ext]
        if name is None:
            name = filepath
        return Source(source_str, lang, name)

    @classmethod
    def from_str(cls, source_str, lang=None, name=None):
        """
            return the Source object
            :rtype: Source
        """
        if lang is None:
            lang = cls.detect_language(source_str)
        return Source(source_str, lang, name)

    def get_language(self):
        return self.lang

    def get_name(self):
        return self.name

    def get_source_str(self):
        return self.source_str

    def tokenize(self):
        if self.__state == SourceState.TOKENIZED:
            return self.tokens

        if self.lang == 'c':
            c_tokenizer = CTokenizer()
            self.tokens = c_tokenizer.tokenize(self.source_str)
        elif self.lang == 'cpp':
            cpp_tokenizer = CppTokenizer()
            self.tokens = cpp_tokenizer.tokenize(self.source_str)
        elif self.lang == 'java':
            java_tokenizer = JavaTokenizer()
            self.tokens = java_tokenizer.tokenize(self.source_str)
        elif self.lang == 'python':
            python_tokenizer = PythonTokenizer()
            self.tokens = python_tokenizer.tokenize(self.source_str)
        elif self.lang == 'php':
            php_tokenizer = PhpTokenizer()
            self.tokens = php_tokenizer.tokenize(self.source_str)
        else:
            raise ValueError("Upsupported language")

        self.__state = SourceState.TOKENIZED
        return self.tokens

    @classmethod
    def detect_language(cls, source_str):
        """
            detect languge of source code
            :rtype: str
        """
        return 'cpp'
from __future__ import absolute_import

from .source import Source

def tokenize_str(source_str):
    source = Source.from_str(source_str)
    pass

def tokenize_file(filepath):
    source = Source.from_file(filepath)
    pass

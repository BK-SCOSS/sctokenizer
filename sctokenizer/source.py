from __future__ import absolute_import

class Source():
    def __init__(self, source_str, lang=None):
        self.source_str = source_str
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
    
    @classmethod
    def detect_language(cls, source_str):
        """
            detect languge of source code
            :rtype: str
        """
        return None

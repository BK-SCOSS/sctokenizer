from __future__ import absolute_import

class Source():
    def __init__(self):
        self.source_str = ""
        self.lang = ""
    
    @classmethod
    def from_file(cls, filepath, lang=None):
        """
            return the Source object
            :rtype: Source
        """
        src = Source()
        src.lang = lang
        with open(filepath) as f:
            src.source_str = f.read()
        return src


    @classmethod
    def from_str(cls, source_str, lang=None):
        """
            return the Source object
            :rtype: Source
        """
        src = Source()
        src.lang = lang
        src.source_str = source_str
        return src
    
    def detect_language(self):
        """
            detect languge of source code
            :rtype: str
        """
        pass

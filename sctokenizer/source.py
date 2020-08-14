from __future__ import absolute_import

class Source():
    def __init__(self):
        self.source_str = ""
        self.lang = ""
    
    @classmethod
    def from_file(cls, filepath):
        """
            return the Source object
            :rtype: Source
        """
        pass

    @classmethod
    def from_str(cls, source_str):
        """
            return the Source object
            :rtype: Source
        """
        pass
    
    def detect_language(self):
        """
            detect languge of source code
            :rtype: str
        """
        pass

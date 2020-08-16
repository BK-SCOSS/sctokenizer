import enum

class TokenType(enum.Enum):
    KEYWORD = 0 
    IDENTIFIER = 1 
    CONSTANT = 2 # numbers and characters
    STRING = 3
    SPECIAL_SYMBOL = 4
    OPERATOR = 5
    OTHER = 6 

class Token():
    def __init__(self, token_value, token_type, line): # is line necessary?
        self.token_value = token_value
        self.token_type = token_type
        self.line = line

    def __str__(self):
        return 'Token {} is {} at line {}'.\
            format(self.token_value, self.token_type, self.line)

    
    


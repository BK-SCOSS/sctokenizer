# sctokenizer
A Source Code Tokenizer

Support those languages: ```C, C++, Java, Python```

## How to install
```
pip install git+https://github.com/ngocjr7/sctokenizer
```

## How to use
Use ```sctokenizer```:
```python
import sctokenizer

tokens = sctokenizer.tokenize_file(filepath='tests/data/a.cpp', lang='cpp')
for token in tokens:
    print(token)
```

Or create new ```CppTokenizer```:
```python
from sctokenizer import CppTokenizer

tokenizer = CppTokenizer()
with open('tests/data/a.cpp') as f:
	source = f.read()
	tokens = tokenizer.tokenize(source)
	print(tokens)
```

Results is a ```list``` of ```Token```. Each ```Token``` has four attributes including ```token_value, token_type, line, column```:
```
(#, TokenType.SPECIAL_SYMBOL, (1, 1))
(include, TokenType.KEYWORD, (1, 5))
(<, TokenType.OPERATOR, (1, 13))
(bits/stdc++.h, TokenType.IDENTIFIER, (1, 14))
(>, TokenType.OPERATOR, (1, 27))
(#, TokenType.SPECIAL_SYMBOL, (2, 1))
(define, TokenType.KEYWORD, (2, 3))
(circleArea, TokenType.IDENTIFIER, (2, 10))
((, TokenType.SPECIAL_SYMBOL, (2, 20))
(r, TokenType.IDENTIFIER, (2, 21))
(), TokenType.SPECIAL_SYMBOL, (2, 22))
((, TokenType.SPECIAL_SYMBOL, (2, 24))
(3.1415, TokenType.CONSTANT, (2, 25))
(*, TokenType.OPERATOR, (2, 31))
...
```

## TODO
* Support other languages: ```PHP, Matlab, Javascript, Typescript,...```
* Auto detect language
* Parse source to a tree of tokens???

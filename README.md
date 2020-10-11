# sctokenizer
A Source Code Tokenizer

Supports those languages: ```C, C++, Java, Python, PHP```

## How to install

```
pip install sctokenizer
```

## How to use
Use ```sctokenizer```:
```python
import sctokenizer

tokens = sctokenizer.tokenize_file(filepath='tests/data/hello_world.cpp', lang='cpp')
for token in tokens:
    print(token)
```

Or create new ```CppTokenizer```:
```python
from sctokenizer import CppTokenizer

tokenizer = CppTokenizer() # this object can be used for multiple source files
with open('tests/data/hello_world.cpp') as f:
    source = f.read()
    tokens = tokenizer.tokenize(source)
    for token in tokens:
        print(token)
```

Or better solution:
```python
from sctokenizer import Source

src = Source.from_file('tests/data/hello_world.cpp', lang='cpp')
tokens = src.tokenize()
for token in tokens:
    print(token)
```

Result is a ```list``` of ```Token```. Each ```Token``` has four attributes including ```token_value, token_type, line, column```:
```
(#, TokenType.SPECIAL_SYMBOL, (1, 1))
(include, TokenType.KEYWORD, (1, 2))
(<, TokenType.OPERATOR, (1, 10))
(bits/stdc++.h, TokenType.IDENTIFIER, (1, 11))
(>, TokenType.OPERATOR, (1, 24))
(using, TokenType.KEYWORD, (3, 1))
(namespace, TokenType.KEYWORD, (3, 7))
(std, TokenType.IDENTIFIER, (3, 17))
(;, TokenType.SPECIAL_SYMBOL, (3, 20))
(int, TokenType.KEYWORD, (5, 1))
(main, TokenType.IDENTIFIER, (5, 5))
((, TokenType.SPECIAL_SYMBOL, (5, 9))
(), TokenType.SPECIAL_SYMBOL, (5, 10))
({, TokenType.SPECIAL_SYMBOL, (6, 1))
(cout, TokenType.IDENTIFIER, (7, 5))
(<<, TokenType.OPERATOR, (7, 11))
(", TokenType.SPECIAL_SYMBOL, (7, 13))
(Hello World, TokenType.STRING, (7, 14))
(", TokenType.SPECIAL_SYMBOL, (7, 25))
(;, TokenType.SPECIAL_SYMBOL, (7, 26))
(return, TokenType.KEYWORD, (8, 5))
(0, TokenType.CONSTANT, (8, 12))
(;, TokenType.SPECIAL_SYMBOL, (8, 13))
(}, TokenType.SPECIAL_SYMBOL, (9, 1))
```

## TODO
* Support other languages: ```Matlab, Javascript, Typescript,...```
* Auto detect language
* Parse source to a tree of tokens???

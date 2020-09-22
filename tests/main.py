import os
import sys
WORKING_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(WORKING_DIR, '../../sctokenizer'))

# import sctokenizer

# tokens = sctokenizer.tokenize_file(filepath='tests/data/hello_world.cpp', lang='cpp')
# # tokens = sctokenizer.tokenize_file(filepath='tests/data/java_a.java', lang='java')
# # tokens = sctokenizer.tokenize_file(filepath='tests/data/python_a.py', lang='py')
# for token in tokens:
#     print(token)

# from sctokenizer import CppTokenizer

# tokenizer = CppTokenizer() # this object can be used for multiple source files
# with open('tests/data/hello_world.cpp') as f:
# 	source = f.read()
# 	tokens = tokenizer.tokenize(source)
# 	print(tokens)

from sctokenizer import Source

src = Source.from_file('tests/data/hello_world.cpp')
tokens = src.tokenize()
for token in tokens:
    print(token)

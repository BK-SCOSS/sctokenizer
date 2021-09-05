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

# from sctokenizer import PhpTokenizer
# from sctokenizer import CppTokenizer
# tokenizer = PhpTokenizer() # this object can be used for multiple source files
# with open('tests/data/test_php.php') as f:
# 	source = f.read()
# 	tokens = tokenizer.tokenize(source)
# 	for token in tokens:
# 		print(token)

from sctokenizer import Source
with open('tests/data/java_a.java', 'r') as f:
	source_str = f.read()
src = Source.from_str(source_str)
print('Detected programming language:', src.lang)
print('Tokenizer result:')
tokens = src.tokenize()
for token in tokens:
    print(token)


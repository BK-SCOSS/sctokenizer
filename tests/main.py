import os
import sys
WORKING_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(WORKING_DIR, '../../sctokenizer'))

import sctokenizer

# tokens = sctokenizer.tokenize_file(filepath='tests/data/a.cpp', lang='cpp')
tokens = sctokenizer.tokenize_file(filepath='tests/data/java_a.java', lang='java')
for token in tokens:
    print(token)



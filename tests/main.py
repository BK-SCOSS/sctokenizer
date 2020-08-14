import os
import sys
WORKING_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(WORKING_DIR, '../sctokenizer'))

import sctokenizer

sctokenizer.tokenize_file(filepath='./data/a.cpp')



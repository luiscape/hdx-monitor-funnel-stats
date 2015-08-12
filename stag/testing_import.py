

import os
import sys

dir = os.path.split(os.path.dirname(__file__))[0]
print dir
sys.path.append(dir)
from scripts.utilities.format_prompt import item as I



print I.item('prompt_success') + " Import successful."
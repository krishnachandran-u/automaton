import sys

sys.path.append('./../')

from typing import List, Dict
import json
from dfa import is_lang_subset
from type import DFA

if __name__ == '__main__':
    DFAs: Dict[str, DFA]
    with open ('./inputs/dfas.json', 'r') as file:
        DFAs = json.load(file)

    for name_1, dfa_1 in DFAs.items():
        for name_2, dfa_2 in DFAs.items():
            if name_1 != name_2:
                if is_lang_subset(dfa_1, dfa_2) and is_lang_subset(dfa_2, dfa_1):
                    print(f'{name_1} and {name_2} are equivalent')
                else:
                    print(f'{name_1} and {name_2} are not equivalent')
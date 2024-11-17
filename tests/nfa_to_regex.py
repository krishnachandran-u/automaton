import sys

sys.path.append('./../')

import json
from typing import Dict
from nfa import nfa_to_regex
from draw import draw_nfa
from type import NFA

if __name__ == '__main__':
    NFAs: Dict[str, NFA]
    with open ('./inputs/nfas.json', 'r') as file:
        NFAs = json.load(file)

    for key, nfa in NFAs.items():
        draw_nfa(nfa)
        regex = nfa_to_regex(nfa)
        print(f'NFA: {key} -> {regex}')
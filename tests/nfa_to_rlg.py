import sys

sys.path.append('./../')

import json
from typing import Dict
from nfa import nfa_to_rlg 
from grammar import print_rlg
from draw import draw_nfa
from type import NFA, RG

if __name__ == '__main__':
    NFAs: Dict[str, NFA]
    with open ('./inputs/nfas.json', 'r') as file:
        NFAs = json.load(file)

    for key, nfa in NFAs.items():
        draw_nfa(nfa)
        rlg: RG = nfa_to_rlg(nfa)
        print_rlg(rlg)
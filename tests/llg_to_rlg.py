import sys

sys.path.append('./../')

import json
from typing import Dict
from typing import List
from grammar import reverse_rg, print_rg, rlg_to_nfa
from nfa import reverse_nfa, nfa_to_rlg
from draw import draw_nfa
from type import RG

if __name__ == '__main__':
    LLGs: RG 
    with open ('./inputs/llgs.json', 'r') as file:
        LLGs = json.load(file)
    for name, llg in LLGs.items():
        print_rg(llg)
        rlgR = reverse_rg(llg) 
        print_rg(rlgR)
        nfa = rlg_to_nfa(rlgR)
        draw_nfa(nfa)
        reversed_nfa = reverse_nfa(nfa)
        draw_nfa(reversed_nfa)
        rlg = nfa_to_rlg(reversed_nfa)
        print_rg(rlg)

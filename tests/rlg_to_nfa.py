import sys

sys.path.append('./../')

import json
from typing import Dict
from typing import List
from grammar import rlg_to_nfa
from draw import draw_nfa
from type import RG

if __name__ == '__main__':
    RLGs: RG 
    with open ('./inputs/rlgs.json', 'r') as file:
        RLGs = json.load(file)
    for name, rlg in RLGs.items():
        print(f'RLG: {name}')
        nfa = rlg_to_nfa(rlg)
        draw_nfa(nfa)
        
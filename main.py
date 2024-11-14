from typing import List, Dict
import json
import copy
from draw import draw_dfa
from dfa import get_minimal_dfa, is_isomorphic

if __name__ == '__main__':
    DFAs: Dict[str, Dict[str, int | List[str] | List[List[str]]]]
    with open ('input.json', 'r') as file:
        DFAs = json.load(file)

    for name_1, dfa_1 in DFAs.items():
        for name_2, dfa_2 in DFAs.items():
            if name_1 != name_2:
                draw_dfa(dfa_1)
                draw_dfa(dfa_2)
                draw_dfa(get_minimal_dfa(dfa_1))
                draw_dfa(get_minimal_dfa(dfa_2))
                if is_isomorphic(dfa_1, dfa_2):
                    print(f'{name_1} and {name_2} are equivalent')
                else:
                    print(f'{name_1} and {name_2} are not equivalent')
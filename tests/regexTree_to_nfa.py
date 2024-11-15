import sys

sys.path.append('./../')

import json
from typing import Dict
from regex import get_regexTree
from nfa import regexTree_to_nfa
from draw import draw_nfa, draw_regexTree

if __name__ == '__main__':
    Regexes: Dict[str, str]
    with open ('./inputs/regexes.json', 'r') as file:
        Regexes = json.load(file)

    for name, regex in Regexes.items():
        regexTree = get_regexTree(regex)
        draw_regexTree(regexTree)
        nfa, _ = regexTree_to_nfa(regexTree)
        draw_nfa(nfa)

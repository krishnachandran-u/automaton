import sys

sys.path.append('./../')

import json
from typing import Dict
from regex import get_regexTree, format_regex
from draw import draw_regexTree

if __name__ == '__main__':
    Regexes: Dict[str, str]
    with open ('./inputs/regexes.json', 'r') as file:
        Regexes = json.load(file)

    for name, regex in Regexes.items():
        print(format_regex(regex))
        draw_regexTree(get_regexTree(regex)) 
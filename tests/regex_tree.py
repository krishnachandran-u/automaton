import sys

sys.path.append('./../')

import json
from typing import Dict
from regex import infix_to_postfix, postfix_to_tree, TreeNode
from draw import draw_regexTree

if __name__ == '__main__':
    Regexes: Dict[str, str]
    with open ('./inputs/regexes.json', 'r') as file:
        Regexes = json.load(file)

    for name, regex in Regexes.items():
        postfix: str = infix_to_postfix(regex)
        print(f'{regex} (postfix): {postfix}')
        regex_tree_root: TreeNode = postfix_to_tree(postfix)
        draw_regexTree(regex_tree_root)
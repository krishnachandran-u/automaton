import sys

sys.path.append('./../')

import json
from typing import Dict
from regex import infix_to_postfix 
from nfa import postfix_to_nfa
from regex import format_regex
from draw import draw_nfa

if __name__ == '__main__':
    Regexes: Dict[str, str]
    with open ('./inputs/regexes.json', 'r') as file:
        Regexes = json.load(file)

    for name, regex in Regexes.items():
        formatted_regex = format_regex(regex)
        print(f'Regex: {name} -> {formatted_regex}')
        postfix = infix_to_postfix(formatted_regex) 
        nfa = postfix_to_nfa(postfix)
        draw_nfa(nfa)




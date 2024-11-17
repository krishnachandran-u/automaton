from typing import Dict, List
from nfa import add_transition

def rlg_to_nfa(rlg: Dict[str, Dict[str, List[str]] | List[str]]) -> Dict[str, str | List[str] | List[List[str]]]:
    nfa = {
        'name': f"<{id(rlg)}>nfa",
        'states': [rlg['start_symbol']],
        'alphabet': rlg['terminals'],
        'transitions': [],
        'start_states': [rlg['start_symbol']],
        'final_states': [],
    }
    cnt = 0
    for symbol, productions in rlg['productions'].items():
        for production in productions:
            if production == 'ε':
                nfa['final_states'].append(symbol) if symbol not in nfa['final_states'] else None
            elif production in rlg['terminals']:
                new_state = f'p{cnt}'
                cnt += 1
                nfa['states'].append(new_state)
                nfa = add_transition(nfa, symbol, production, new_state)
                nfa['final_states'].append(new_state)
            elif production in rlg['non_terminals']:
                new_state = production
                nfa = add_transition(nfa, symbol, 'ε', production)
            else:
                curr_state = symbol
                for i, char in enumerate(production):
                    if i == len(production) - 2 and production[i + 1] in rlg['non_terminals']:
                        new_state = production[i + 1]
                        nfa['states'].append(new_state) if new_state not in nfa['states'] else None
                        nfa = add_transition(nfa, curr_state, char, new_state)
                        break
                    if i == len(production) - 1: # implied that production[i] is a terminal
                        new_state = f'p{cnt}'
                        cnt += 1
                        nfa['states'].append(new_state)
                        nfa = add_transition(nfa, curr_state, char, new_state)
                        nfa['final_states'].append(new_state)
                    else:
                        new_state = f'p{cnt}'
                        cnt += 1
                        nfa['states'].append(new_state)
                        nfa = add_transition(nfa, curr_state, char, new_state)
                        curr_state = new_state
    return nfa

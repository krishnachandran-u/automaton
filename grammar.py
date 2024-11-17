from typing import Dict, List
from nfa import add_transition
from type import RG, NFA

def rlg_to_nfa(rlg: RG) -> NFA:
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
                next_state = f'p{cnt}'
                cnt += 1
                nfa['states'].append(next_state)
                nfa = add_transition(nfa, symbol, production, next_state)
                nfa['final_states'].append(next_state)
            elif production in rlg['non_terminals']:
                next_state = production
                nfa = add_transition(nfa, symbol, 'ε', next_state)
            else:
                curr_state = symbol
                for i, char in enumerate(production):
                    if i == len(production) - 2 and production[i + 1] in rlg['non_terminals']:
                        next_state = production[i + 1]
                        nfa['states'].append(next_state) if next_state not in nfa['states'] else None
                        nfa = add_transition(nfa, curr_state, char, next_state)
                        break
                    if i == len(production) - 1: # implied that production[i] is a terminal
                        next_state = f'p{cnt}'
                        cnt += 1
                        nfa['states'].append(next_state)
                        nfa = add_transition(nfa, curr_state, char, next_state)
                        nfa['final_states'].append(next_state)
                    else:
                        next_state = f'p{cnt}'
                        cnt += 1
                        nfa['states'].append(next_state)
                        nfa = add_transition(nfa, curr_state, char, next_state)
                        curr_state = next_state
    return nfa

def print_rlg(rlg: RG):
    print(f"Start Symbol: {rlg['start_symbol']}")
    print(f"Terminals: {rlg['terminals']}")
    print(f"Non Terminals: {rlg['non_terminals']}")
    print("Productions:")
    for symbol, productions in rlg['productions'].items():
        print(f"\t{symbol} -> {' | '.join(productions)}")
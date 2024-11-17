from typing import Dict, List
from regex import TreeNode
from copy import deepcopy
import json
from type import NFA, RG
from util import get_next_letter

operators_and_brackets = ['+', '.', '*', '(', ')']

def add_transition(nfa: NFA, start_state: str, symbol: str, end_state: str) -> NFA:
    for transition in nfa['transitions']:
        if transition[0] == start_state and transition[1] == symbol:
            if end_state not in transition[2]:
                transition[2].append(end_state)
            return nfa
    nfa['transitions'].append([start_state, symbol, [end_state]])
    return nfa

"""
def combine_transitions(t1: List[str | List[str]], t2: List[str | List[str]]) -> Dict[str, str | List[str] | List[List[str | List[str]]]]:
    combined = {}
    for t in t1 + t2:
        if (t[0], t[1]) not in combined:
            combined[(t[0], t[1])] = []
        if t[2] not in combined[(t[0], t[1])]:
            combined[(t[0], t[1])].append(t[2])
    combined_transitions = []    
    for key, value in combined.items():
        combined_transitions.append([key[0], key[1], value])    
    return combined_transitions
"""

def regexTree_to_nfa(tree: TreeNode, cnt: int = 0) -> tuple[NFA, int]: # postorder traversal of the regex tree
    def is_symbol(char: str) -> bool:
        return char not in operators_and_brackets

    left_nfa: NFA 
    right_nfa: NFA 

    if tree.left != None:        
        left_nfa, cnt = regexTree_to_nfa(tree.left, cnt)
    if tree.right != None:
        right_nfa, cnt = regexTree_to_nfa(tree.right, cnt)

    if is_symbol(tree.value):
        new_nfa = {
            'name': f"<{id(tree)}>nfa",
            'states': [f'p{cnt}', f'p{cnt + 1}'],
            'alphabet': [tree.value] if tree.value not in ['ε', 'φ'] else [],
            'transitions': [],
            'start_states': [f'p{cnt}'],
            'final_states': [f'p{cnt + 1}'],
        }
        if tree.value != 'φ':
            new_nfa = add_transition(new_nfa, f'p{cnt}', tree.value, f'p{cnt + 1}')
        else:
            new_nfa['transitions'] = []
        cnt += 2
        return new_nfa, cnt
    elif tree.value == '*':
        new_nfa = deepcopy(left_nfa)
        new_nfa = add_transition(new_nfa, left_nfa['start_states'][0], 'ε', left_nfa['final_states'][0])
        new_nfa = add_transition(new_nfa, left_nfa['final_states'][0], 'ε', left_nfa['start_states'][0])
        return new_nfa, cnt

    elif tree.value == '+':
        new_nfa = {
            'name': f"<{id(tree)}>nfa",
            'states': left_nfa['states'] + right_nfa['states'],
            'alphabet': list(set(left_nfa['alphabet'] + right_nfa['alphabet'])),
            'transitions': left_nfa['transitions'] + right_nfa['transitions'],
            'start_states':  left_nfa['start_states'], 
            'final_states': right_nfa['final_states']
        }

        new_nfa = add_transition(new_nfa, left_nfa['start_states'][0], 'ε', right_nfa['start_states'][0])
        new_nfa = add_transition(new_nfa, left_nfa['final_states'][0], 'ε', right_nfa['final_states'][0])
        return new_nfa, cnt

    elif tree.value == '.':
        new_nfa = {
            'name': f"<{id(tree)}>nfa",
            'states': left_nfa['states'] + right_nfa['states'],
            'alphabet': list(set(left_nfa['alphabet'] + right_nfa['alphabet'])),
            'transitions': left_nfa['transitions'] + right_nfa['transitions'],
            'start_states':  left_nfa['start_states'], 
            'final_states': right_nfa['final_states']
        }

        new_nfa = add_transition(new_nfa, left_nfa['final_states'][0], 'ε', right_nfa['start_states'][0])
        return new_nfa, cnt

    else:
        raise ValueError(f"Invalid operator {tree.value}")

def postfix_to_nfa(postfix: str) -> NFA: 
    stack: List[NFA] = []
    operators = ['+', '.', '*']
    cnt: int = 0
    for char in postfix: 
        if char not in operators:
            new_nfa = {
                'name': f"<{id(postfix)}>nfa",
                'states': [f'p{cnt}', f'p{cnt + 1}'],
                'alphabet': [char] if char not in ['ε', 'φ'] else [],
                'transitions': [],
                'start_states': [f'p{cnt}'],
                'final_states': [f'p{cnt + 1}'],
            }
            if char != 'φ':
                new_nfa = add_transition(new_nfa, f'p{cnt}', char, f'p{cnt + 1}')
            else:
                new_nfa['transitions'] = []
            cnt += 2
            stack.append(new_nfa)
        else:
            if char == '*':
                left_nfa = stack.pop()
                new_nfa = deepcopy(left_nfa)
                new_nfa = add_transition(new_nfa, left_nfa['start_states'][0], 'ε', left_nfa['final_states'][0])
                new_nfa = add_transition(new_nfa, left_nfa['final_states'][0], 'ε', left_nfa['start_states'][0])

            elif char == '+':
                right_nfa = stack.pop()
                left_nfa = stack.pop()
                new_nfa = {
                    'name': f"<{id(postfix)}>nfa",
                    'states': left_nfa['states'] + right_nfa['states'],
                    'alphabet': list(set(left_nfa['alphabet'] + right_nfa['alphabet'])),
                    'transitions': left_nfa['transitions'] + right_nfa['transitions'],
                    'start_states':  left_nfa['start_states'], 
                    'final_states': right_nfa['final_states']
                }
        
                new_nfa = add_transition(new_nfa, left_nfa['start_states'][0], 'ε', right_nfa['start_states'][0])
                new_nfa = add_transition(new_nfa, left_nfa['final_states'][0], 'ε', right_nfa['final_states'][0])

            elif char == '.':
                right_nfa = stack.pop()
                left_nfa = stack.pop()
                new_nfa = {
                    'name': f"<{id(postfix)}>nfa",
                    'states': left_nfa['states'] + right_nfa['states'],
                    'alphabet': list(set(left_nfa['alphabet'] + right_nfa['alphabet'])),
                    'transitions': left_nfa['transitions'] + right_nfa['transitions'],
                    'start_states':  left_nfa['start_states'], 
                    'final_states': right_nfa['final_states']
                }
        
                new_nfa = add_transition(new_nfa, left_nfa['final_states'][0], 'ε', right_nfa['start_states'][0])

            else:
                raise ValueError(f"Invalid operator {char}")
            stack.append(new_nfa) 
    # print(json.dumps(stack[0],indent=2))
    print(stack[0])
    return stack.pop()

def convert_to_single_start_state(nfa: NFA) -> NFA:
    if len(nfa['start_states']) == 1:
        return nfa
    else:
        new_nfa = deepcopy(nfa)
        new_start_state = f'α'
        new_nfa['states'].append(new_start_state)
        new_nfa['transitions'].append([new_start_state, 'ε', nfa['start_states']])
        new_nfa['start_states'] = [new_start_state]
        return new_nfa

def convert_to_single_final_state(nfa: NFA) -> NFA:
    if len(nfa['final_states']) == 1:
        return nfa
    else:
        new_nfa = deepcopy(nfa)
        new_final_state = f'β'
        new_nfa['states'].append(new_final_state)
        for final_state in nfa['final_states']:
            new_nfa = add_transition(new_nfa, final_state, 'ε', new_final_state)
        new_nfa['final_states'] = [new_final_state]
        return new_nfa

def nfa_to_regex(nfa: NFA) -> str:
    nfa = convert_to_single_start_state(nfa)
    nfa = convert_to_single_final_state(nfa)

    def R(s: str, states: List[str], f: str) -> str:
        if len(states) == 0:
            symbols = []
            for transition in nfa['transitions']:
                if transition[0] == s and f in transition[2]:
                    symbols.append(transition[1])
            if s != f:
                if len(symbols) == 0:
                    return 'φ'
                else:
                    return '+'.join(symbols)
            if s == f:
                if 'ε' not in symbols:
                    symbols.append('ε')
                return '+'.join(symbols)
        else:
            r = states.pop()
            X = states
            return(f'{R(s, X, f)}+{R(s, X, r)}({R(r, X, r)})*{R(r, X, f)}')
    
    return R(nfa['start_states'][0], nfa['states'], nfa['final_states'][0])


def nfa_to_rlg(nfa: NFA) -> RG:
    nfa = convert_to_single_start_state(nfa)
    rlg: RG = {
        'start_symbol': '',
        'terminals': nfa['alphabet'],
        'non_terminals': [],
        'productions': {}
    }
    state_to_symbol = {}
    curr_symbol = 'A'
    for transition in nfa['transitions']:
        if transition[0] not in state_to_symbol:
            state_to_symbol[transition[0]] = curr_symbol
            curr_symbol = get_next_letter(curr_symbol)
        for end_state in transition[2]:
            if end_state not in state_to_symbol:
                state_to_symbol[end_state] = curr_symbol
                curr_symbol = get_next_letter(curr_symbol)
        for end_state in transition[2]:
            LHS = state_to_symbol[transition[0]]
            RHS = (transition[1] if transition[1] != 'ε' else '') + state_to_symbol[end_state]
            if LHS not in rlg['productions']:
                rlg['productions'][LHS] = []
            rlg['productions'][LHS].append(RHS)
    for _, value in state_to_symbol.items():
        rlg['non_terminals'].append(value)
    rlg['start_symbol'] = state_to_symbol[nfa['start_states'][0]]
    for state in nfa['final_states']:
        if state_to_symbol[state] not in rlg['productions']:
            rlg['productions'][state_to_symbol[state]] = []
        rlg['productions'][state_to_symbol[state]].append('ε')
    return rlg

def reverse_nfa(nfa: NFA) -> NFA:
    reversed_nfa = {
        'name': f"<{id(nfa)}>nfa",
        'states': nfa['states'],
        'alphabet': nfa['alphabet'],
        'transitions': [],
        'start_states': nfa['final_states'],
        'final_states': nfa['start_states']
    }
    transition_map: Dict[tuple[str, str], List[str]] = {}
    for transition in nfa['transitions']:
        for end_state in transition[2]:
            if (end_state, transition[1]) not in transition_map:
                transition_map[(end_state, transition[1])] = []
            if transition[0] not in transition_map[(end_state, transition[1])]:
                transition_map[(end_state, transition[1])].append(transition[0])
    new_transitions = []
    for key, value in transition_map.items():
        new_transitions.append([key[0], key[1], value])
    reversed_nfa['transitions'] = new_transitions
    return reversed_nfa
    
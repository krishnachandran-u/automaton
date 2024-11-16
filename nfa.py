from typing import Dict, List
from regex import TreeNode
from copy import deepcopy

operators_and_brackets = ['+', '.', '*', '(', ')']

def add_transition(nfa: Dict[str, str | List[str] | List[List[str | List[str]]]], start_state: str, symbol: str, end_state: str) -> Dict[str, str | List[str] | List[List[str | List[str]]]]:
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

def regexTree_to_nfa(tree: TreeNode, cnt: int = 0) -> tuple[Dict[str, str | List[str] | List[List[str]]], int]: # postorder traversal of the regex tree
    def is_symbol(char: str) -> bool:
        return char not in operators_and_brackets

    left_nfa = Dict[str, str | List[str] | List[List[str]]]
    right_nfa = Dict[str, str | List[str] | List[List[str]]]

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
        new_nfa = add_transition(new_nfa, right_nfa['final_states'][0], 'ε', right_nfa['final_states'][0])
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

def postfix_to_nfa(postfix: str) -> Dict[str, str | List[str] | List[List[str]]]: 
    stack: List[Dict[str, str | List[str] | List[List[str]]]] = []
    operators = ['+', '.', '*']
    cnt: int = 0
    for char in postfix: 
        if char not in operators:
            new_nfa = {
                'name': f"<{postfix}>postfix_to_nfa",
                'states': [f'p{cnt}', f'p{cnt + 1}'],
                'alphabet': [char] if char not in ['ε', 'φ'] else [],
                'transitions': [[f'p{cnt}', char, f'p{cnt + 1}']] if char != 'φ' else [],
                'start_state': f'p{cnt}',
                'final_states': [f'p{cnt + 1}'],
            }
            cnt += 2
            stack.append(new_nfa)
        else:
            if char == '*':
                left_nfa = stack.pop()
                new_nfa = deepcopy(left_nfa)
                new_nfa['transitions'].append([left_nfa['start_state'], 'ε', left_nfa['final_states'][0]])
                new_nfa['transitions'].append([left_nfa['final_states'][0], 'ε', left_nfa['start_state']])
            elif char == '+':
                right_nfa = stack.pop()
                left_nfa = stack.pop()
                new_nfa = {
                   'name': f"<{postfix}>postfix_to_nfa",
                   'states': left_nfa['states'] + right_nfa['states'],
                   'alphabet': list(set(left_nfa['alphabet'] + right_nfa['alphabet'])),
                   'transitions': left_nfa['transitions'] + right_nfa['transitions'],
                   'start_state':  left_nfa['start_state'], 
                   'final_states': right_nfa['final_states']
                }
        
                new_nfa['transitions'].append([left_nfa['start_state'], 'ε', right_nfa['start_state']])
                new_nfa['transitions'].append([right_nfa['final_states'][0], 'ε', right_nfa['final_states'][0]])

            elif char == '.':
                right_nfa = stack.pop()
                left_nfa = stack.pop()
                new_nfa = {
                    'name': f"<{postfix}>postfix_to_nfa",
                    'states': left_nfa['states'] + right_nfa['states'],
                    'alphabet': list(set(left_nfa['alphabet'] + right_nfa['alphabet'])),
                    'transitions': left_nfa['transitions'] + right_nfa['transitions'],
                    'start_state':  left_nfa['start_state'], 
                    'final_states': right_nfa['final_states']
                }
                new_nfa['transitions'].append([left_nfa['final_states'][0], 'ε', right_nfa['start_state']])

            else:
                raise ValueError(f"Invalid operator {char}")
            stack.append(new_nfa) 
    return stack.pop()
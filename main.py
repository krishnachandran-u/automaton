from typing import List, Dict
import json
import copy
from draw import draw_dfa

# you are not allowed to give a name starting with 'q' to any state. It is reserved for the minimization algorithm. 

def run_transition(dfa: Dict[str, int | List[str] | List[List[str]]] , state: str, symbol: str) -> str:
    for transition in dfa['transitions']:
        if transition[0] == state and transition[1] == symbol:
            return transition[2]
    raise ValueError(f'No transition found for state {state} and symbol {symbol} <> {json.dumps(dfa, indent=4)}')

def run_dfa(dfa: Dict[str, int | List[str] | List[List[str]]], input_string: str) -> bool:
    current_state = dfa['start_state']
    for symbol in input_string:
        current_state = run_transition(dfa, current_state, symbol)
    return current_state in dfa['final_states']

def get_minimal_dfa(dfa: Dict[str, int | List[str] | List[List[str]]]):
    dfa = copy.deepcopy(dfa)
    states = dfa['states']
    alphabet = dfa['alphabet']
    transitions = dfa['transitions']
    final_states = dfa['final_states']

    grid = [[True for _ in range(len(states))] for _ in range(len(states))]
    equivalence_classes: List[List[str]] = []

    strings = get_all_strings(alphabet, len(states) - 1)
    for i in range(len(states)):
        for j in range(i):
            dfa_1 = dfa.copy()
            dfa_2 = dfa.copy()
            dfa_1['start_state'] = states[i]
            dfa_2['start_state'] = states[j]
            for string in strings:
                if run_dfa(dfa_1, string) != run_dfa(dfa_2, string):
                    grid[i][j] = False
                    break
    
    for i in range(len(states)):
        for j in range(i + 1):
            if grid[i][j]:
                equivalence_class_found = False
                if i != j:
                    for equivalence_class in equivalence_classes:
                        if states[i] in equivalence_class:
                            equivalence_class.append(states[j])
                            equivalence_class_found = True
                            break
                        elif states[j] in equivalence_class:
                            equivalence_class.append(states[i])
                            equivalence_class_found = True
                            break
                    if not equivalence_class_found:
                        equivalence_classes.append([states[i], states[j]])
                else:
                    for equivalence_class in equivalence_classes:
                        if states[i] in equivalence_class:
                            equivalence_class_found = True
                            break
                    if not equivalence_class_found:
                        equivalence_classes.append([states[i]])

    new_transitions = transitions.copy()
    for transition in new_transitions: 
        for equivalence_class in equivalence_classes:
            if transition[0] in equivalence_class:
                transition[0] = str(equivalence_class)
            if transition[2] in equivalence_class:
                transition[2] = str(equivalence_class)

    new_start_state: str = None                
    for equivalence_class in equivalence_classes:
        if dfa['start_state'] in equivalence_class:
            new_start_state = str(equivalence_class)
            break

    new_final_states: List[str] = []
    for states in final_states:
        for equivalence_class in equivalence_classes:
            if states in equivalence_class and str(equivalence_class) not in new_final_states:
                new_final_states.append(str(equivalence_class))
                break

    new_states: List[str] = [str(equivalence_class) for equivalence_class in equivalence_classes]

    new_dfa = {
        'name': f'Minimized {dfa["name"]}',
        'states': new_states,
        'alphabet': alphabet,
        'transitions': new_transitions,
        'start_state': new_start_state,
        'final_states': new_final_states
    }
    # print(json.dumps(new_dfa, indent=4))
    return new_dfa

def is_isomorphic(dfa_1: Dict[str, int | List[str] | List[List[str]]], dfa_2: Dict[str, int | List[str] | List[List[str]]]) -> bool:
    min_dfa_1 = get_minimal_dfa(dfa_1)
    min_dfa_2 = get_minimal_dfa(dfa_2)

    if set(min_dfa_1['alphabet']) != set(min_dfa_2['alphabet']):
        return False
    alphabet = min_dfa_1['alphabet']

    if len(min_dfa_1['states']) != len(min_dfa_2['states']):
        return False

    if not is_equivalent(min_dfa_1, min_dfa_1['start_state'], min_dfa_2, min_dfa_2['start_state']):
        return False

    count = 0

    min_dfa_1 = rename_state(min_dfa_1, min_dfa_1['start_state'], f'q{count}')
    min_dfa_2 = rename_state(min_dfa_2, min_dfa_2['start_state'], f'q{count}')
    bfs_queue = [f'q{count}']

    count += 1        

    while bfs_queue:
        state_1 = bfs_queue[0]
        state_2 = bfs_queue[0]
        bfs_queue.pop(0)
        for symbol in alphabet:
            next_state_1 = run_transition(min_dfa_1, state_1, symbol)
            next_state_2 = run_transition(min_dfa_2, state_2, symbol)
            if not is_equivalent(min_dfa_1, next_state_1, min_dfa_2, next_state_2):
                return False
            if (not next_state_1.startswith('q')) and (not next_state_2.startswith('q')):
                min_dfa_1 = rename_state(min_dfa_1, next_state_1, f'q{count}')
                min_dfa_2 = rename_state(min_dfa_2, next_state_2, f'q{count}')
                bfs_queue.append(f'q{count}')
                count += 1

    return True

def rename_state(dfa: Dict[str, int | List[str] | List[List[str]]], old_name: str, new_name: str) -> Dict[str, int | List[str] | List[List[str]]]:
    new_dfa = copy.deepcopy(dfa) 

    for i in range(len(new_dfa['states'])):
        if new_dfa['states'][i] == old_name:
            new_dfa['states'][i] = new_name
            # print(f"Renamed state {old_name} to {new_name}")
            break

    if new_dfa['start_state'] == old_name:
        new_dfa['start_state'] = new_name

    for i in range(len(new_dfa['final_states'])):
        if new_dfa['final_states'][i] == old_name:
            new_dfa['final_states'][i] = new_name

    for transition in new_dfa['transitions']:
        if transition[0] == old_name:
            transition[0] = new_name
        if transition[2] == old_name:
            transition[2] = new_name

    # print(json.dumps(new_dfa, indent=4))
    return new_dfa

def is_equivalent(dfa_1: Dict[str, int | List[str] | List[List[str]]], state_1: str, dfa_2: Dict[str, int | List[str] | List[List[str]]], state_2: str) -> bool:
    if state_1 in dfa_1['final_states'] and state_2 not in dfa_2['final_states']:
        return False
    if state_1 not in dfa_1['final_states'] and state_2 in dfa_2['final_states']:
        return False
    if state_1.startswith('q') ^ state_2.startswith('q'): 
        return False
    if (state_1.startswith('q') and state_2.startswith('q')) and state_1 != state_2:
        return False

    return True

def get_all_strings(alphabets: list, length: int) -> list[str]:
    if length < 0:
        raise Exception(f"Inside get_all_strings: variable length cannot be negative")
    if length == 0:
        return [""]
    strings = []
    for string in get_all_strings(alphabets, length - 1):
        for alphabet in alphabets:
            strings.append(string + alphabet)
    return strings

if __name__ == '__main__':
    DFAs: List[Dict[str, int | List[str] | List[List[str]]]]
    with open ('input.json', 'r') as file:
        DFAs = json.load(file)

    if is_isomorphic(DFAs['dfa_1'], DFAs['dfa_2']):
        print(f'DFA 1 and DFA 2 are isomorphic')
    else:
        print(f'DFA 1 and DFA 2 are not isomorphic')

    if is_isomorphic(DFAs['dfa_1'], DFAs['dfa_3']):
        print(f'DFA 1 and DFA 3 are isomorphic')
    else:
        print(f'DFA 1 and DFA 3 are not isomorphic')
    
    if is_isomorphic(DFAs['dfa_2'], DFAs['dfa_3']):
        print(f'DFA 2 and DFA 3 are isomorphic')
    else:
        print(f'DFA 2 and DFA 3 are not isomorphic')
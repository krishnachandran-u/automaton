import graphviz
from typing import List, Dict 

def draw_dfa(dfa: Dict[str, str | List[str] | List[List[str]]]):
    dot = graphviz.Digraph(node_attr={'shape': 'circle'})
    for state in dfa['states']:
        if state in dfa['final_states']:
            dot.node(state, shape='doublecircle')
        else:
            dot.node(state)

    dot.node("<>", shape='point')
    dot.edge("<>", dfa['start_state'])

    for transition in dfa['transitions']:
        dot.edge(transition[0], transition[2], label=transition[1])

    dot.render(f"images/{dfa['name']}", format='png', cleanup=True)
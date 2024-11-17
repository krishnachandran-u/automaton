import graphviz
from typing import List, Dict 
from regex import TreeNode
from type import DFA, NFA

def draw_dfa(dfa: DFA):
    dot = graphviz.Digraph(node_attr={'shape': 'circle', 'fontname': 'Courier Prime Bold'},
                           edge_attr={'fontname': 'Courier Prime Bold'}, 
                           graph_attr={'dpi': '300'})  

    for state in dfa['states']:
        if state in dfa['final_states']:
            dot.node(state, shape='doublecircle')
        else:
            dot.node(state)

    dot.node("@", shape='point', label='')
    dot.edge("@", dfa['start_state'])

    for transition in dfa['transitions']:
        dot.edge(transition[0], transition[2], label=transition[1])

    dot.render(f"images/{dfa['name']}", format='png', cleanup=True)

def draw_regexTree(tree: TreeNode):
    dot = graphviz.Digraph(node_attr={'shape': 'circle', 'fontname': 'Courier Prime Bold'},
                           edge_attr={'fontname': 'Courier Prime Bold'}, 
                           graph_attr={'dpi': '300'})  

    def draw_tree(node: TreeNode):
        dot.node(str(id(node)), label=node.value)
        if node.left is not None:
            draw_tree(node.left)
            dot.edge(str(id(node)), str(id(node.left)))
        if node.right is not None:
            draw_tree(node.right)
            dot.edge(str(id(node)), str(id(node.right)))

    draw_tree(tree)
    dot.render(f"images/{id(tree)}", format='png', cleanup=True)

def draw_nfa(nfa: NFA):
    dot = graphviz.Digraph(node_attr={'shape': 'circle', 'fontname': 'Courier Prime Bold'},
                           edge_attr={'fontname': 'Courier Prime Bold'}, 
                           graph_attr={'dpi': '300'})  

    for state in nfa['states']:
        if state in nfa['final_states']:
            dot.node(state, shape='doublecircle')
        else:
            dot.node(state)

    for start_state in nfa['start_states']:
        dot.node(f"{id(start_state)}", shape='point', label='')
        dot.edge(f"{id(start_state)}", start_state)

    for transition in nfa['transitions']:
        for end_state in transition[2]:
            dot.edge(transition[0], end_state, label=transition[1])

    dot.render(f"images/{nfa['name']}", format='png', cleanup=True)
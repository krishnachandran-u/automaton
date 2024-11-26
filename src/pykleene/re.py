from typing import TYPE_CHECKING
import graphviz

if TYPE_CHECKING:
    from pykleene.nfa import NFA
    from pykleene._helpers import BinaryTreeNode

class RE:
    OPERATORS = ['+', '.', '*']
    PARENTHESES = ['(', ')']
    PRECEDENCE = {
            '+': 1,  
            '.': 2, 
            '*': 3, 
            '(': 0, 
            ')': 0
    }

    def _isSymbol(char: str) -> bool:
        return char not in RE.OPERATORS and char not in RE.PARENTHESES

    def format(regex: str) -> str:
        formatted = []
        for i in range(len(regex) - 1):
            formatted.append(regex[i])
            if (RE._isSymbol(regex[i]) or regex[i] in [')', '*']) and (RE._isSymbol(regex[i + 1]) or regex[i + 1] == '(' ):
                formatted.append('.')
        formatted.append(regex[-1])
        return ''.join(formatted)

    def postfix(regex: str) -> str:
        stack = []
        postfix = []
        for char in regex:
            if char == '(':
                stack.append(char)
            elif char == ')':
                while stack[-1] != '(':
                    postfix.append(stack.pop())
                stack.pop()
            elif char in RE.PRECEDENCE:
                while stack and RE.PRECEDENCE[stack[-1]] >= RE.PRECEDENCE[char]:
                    postfix.append(stack.pop())
                stack.append(char)
            else:
                postfix.append(char)
        while stack:
            postfix.append(stack.pop())
        return ''.join(postfix)
    
    def expressionTree(regex: str) -> 'BinaryTreeNode':
        from pykleene._helpers import BinaryTreeNode 
        postfix = RE.postfix(RE.format(regex))
        stack: list[BinaryTreeNode] = []
        for char in postfix: 
            if char not in RE.OPERATORS:
                stack.append(BinaryTreeNode(leftChild=None, data=char, rightChild=None))
            else:
                if char == '*':
                    leftChild = stack.pop()
                    if leftChild.data in ['ε', 'φ']: # ε* = ε, φ* = ε
                        node = BinaryTreeNode(leftChild=None, data='ε', rightChild=None)
                    else:
                        node = BinaryTreeNode(leftChild=leftChild, data=char, rightChild=None) 
                elif char == '.':
                    rightChild = stack.pop()
                    leftChild = stack.pop()
                    if leftChild.data == 'φ' or rightChild.data == 'φ': # φ.anything = φ
                        node = BinaryTreeNode(leftChild=None, data='φ', rightChild=None)
                    elif leftChild.data == 'ε': # ε.anything = anything
                        node = rightChild
                    elif rightChild.data == 'ε':
                        node = leftChild
                    else:
                        node = BinaryTreeNode(leftChild=leftChild, data=char, rightChild=rightChild)
                elif char == '+':
                    rightChild = stack.pop()
                    leftChild = stack.pop()
                    if leftChild.data == 'φ': 
                        node = rightChild
                    elif rightChild.data == 'φ':
                        node = leftChild
                    elif leftChild.data == 'ε' and rightChild.data == 'ε':
                        node = BinaryTreeNode(leftChild=None, data='ε', rightChild=None)
                    else:
                        node = BinaryTreeNode(leftChild=leftChild, data=char, rightChild=rightChild)
                stack.append(node) 
        return stack.pop()

    def nfa(regex: str, method: str = 'regexTree') -> 'NFA':
        from pykleene.nfa import NFA
        from pykleene._helpers import BinaryTreeNode 

        def regexTreeToNfa(node: BinaryTreeNode, cnt: int = 0) -> tuple[NFA, int]:
            from copy import deepcopy
            leftNfa: NFA 
            rightNfa: NFA

            if node.leftChild is not None:
                leftNfa, cnt = regexTreeToNfa(node.leftChild, cnt)
            if node.rightChild is not None:
                rightNfa, cnt = regexTreeToNfa(node.rightChild, cnt)

            if RE._isSymbol(node.data):
                newNfa = NFA(
                    states = {f"q{cnt}", f"q{cnt + 1}"}, 
                    alphabet= {node.data} if node.data not in ['ε', 'φ'] else set(),
                    transitions = dict(),
                    startStates = {f"q{cnt}"},
                    finalStates = {f"q{cnt + 1}"}
                )
                cnt += 2
                if node.data != 'φ':
                    newNfa = newNfa.addTransition(f"q{cnt - 2}", node.data, f"q{cnt - 1}")
                else:
                    newNfa.transitions = dict()
                return newNfa, cnt

            elif node.data == '*':
                newNfa = deepcopy(leftNfa)
                newNfa = newNfa.addTransition(list(leftNfa.startStates)[0], 'ε', list(leftNfa.finalStates)[0])
                newNfa = newNfa.addTransition(list(leftNfa.finalStates)[0], 'ε', list(leftNfa.startStates)[0])
                return newNfa, cnt

            elif node.data == '+':
                newNfa = NFA(
                    states=leftNfa.states | rightNfa.states,
                    alphabet=leftNfa.alphabet | rightNfa.alphabet,
                    transitions=leftNfa.transitions | rightNfa.transitions,
                    startStates=leftNfa.startStates, 
                    finalStates=rightNfa.finalStates
                )

                newNfa = newNfa.addTransition(list(leftNfa.finalStates)[0], 'ε', list(rightNfa.finalStates)[0])
                newNfa = newNfa.addTransition(list(leftNfa.startStates)[0], 'ε', list(rightNfa.startStates)[0])
                return newNfa, cnt

            elif node.data == '.':
                newNfa = NFA(
                    states = leftNfa.states | rightNfa.states,
                    alphabet = leftNfa.alphabet | rightNfa.alphabet,
                    transitions = leftNfa.transitions | rightNfa.transitions,
                    startStates = leftNfa.startStates, 
                    finalStates = rightNfa.finalStates
                )

                newNfa = newNfa.addTransition(list(leftNfa.finalStates)[0], 'ε', list(rightNfa.startStates)[0])
                return newNfa, cnt

            else:
                raise ValueError(f"Invalid operator {node.data}")

        def regexPostfixToNfa(postfix: str) -> NFA:
            from copy import deepcopy
            stack: list[NFA] = []
            cnt: int = 0
            
            for char in postfix:
                if char not in RE.OPERATORS:  
                    newNfa = NFA(
                        states={f"q{cnt}", f"q{cnt + 1}"},
                        alphabet={char} if char not in ['ε', 'φ'] else set(),
                        transitions=dict(),
                        startStates={f"q{cnt}"},
                        finalStates={f"q{cnt + 1}"}
                    )
                    cnt += 2
                    if char != 'φ':
                        newNfa = newNfa.addTransition(f"q{cnt - 2}", char, f"q{cnt - 1}")
                    stack.append(newNfa)
                
                elif char == '*':  
                    leftNfa = stack.pop()
                    newNfa = deepcopy(leftNfa)
                    newNfa = newNfa.addTransition(list(leftNfa.startStates)[0], 'ε', list(rightNfa.finalStates)[0])
                    newNfa = newNfa.addTransition(list(leftNfa.finalStates)[0], 'ε', list(leftNfa.startStates)[0])
                    stack.append(newNfa)
                
                elif char == '+':  
                    rightNfa = stack.pop()
                    leftNfa = stack.pop()
                    newNfa = NFA(
                        states=leftNfa.states | rightNfa.states,
                        alphabet=leftNfa.alphabet | rightNfa.alphabet,
                        transitions=leftNfa.transitions | rightNfa.transitions,
                        startStates=leftNfa.startStates,
                        finalStates=rightNfa.finalStates
                    )
                    newNfa = newNfa.addTransition(list(leftNfa.finalStates)[0], 'ε', list(rightNfa.finalStates)[0])
                    newNfa = newNfa.addTransition(list(leftNfa.startStates)[0], 'ε', list(rightNfa.startStates)[0])
                    stack.append(newNfa)
                
                elif char == '.':  
                    rightNfa = stack.pop()
                    leftNfa = stack.pop()
                    newNfa = NFA(
                        states=leftNfa.states | rightNfa.states,
                        alphabet=leftNfa.alphabet | rightNfa.alphabet,
                        transitions=leftNfa.transitions | rightNfa.transitions,
                        startStates=leftNfa.startStates,
                        finalStates=rightNfa.finalStates
                    )
                    newNfa = newNfa.addTransition(list(leftNfa.finalStates)[0], 'ε', list(rightNfa.startStates)[0])
                    stack.append(newNfa)
                
                else:
                    raise ValueError(f"Invalid operator {char}")
            
            return stack.pop()
 
        if method == 'regexTree':
            return regexTreeToNfa(RE.expressionTree(RE.format(regex)))[0]

        if method == 'postfix':
            return regexPostfixToNfa(RE.postfix(RE.format(regex)))

        else:
            raise ValueError(f"Invalid method: {method}")
    
    def image(param, type: str = 'regexTree', dir: str = None, save: bool = False) -> None:
        from pykleene._config import graphvizConfig 
        from pykleene._helpers import BinaryTreeNode
        dot = graphviz.Digraph(**graphvizConfig)

        def drawRegexTree(node: BinaryTreeNode):
            dot.node(str(id(node)), node.data)
            if node.leftChild is not None:
                drawRegexTree(node.leftChild)
                dot.edge(str(id(node)), str(id(node.leftChild)))
            if node.rightChild is not None:
                drawRegexTree(node.rightChild)
                dot.edge(str(id(node)), str(id(node.rightChild)))

        if type == 'regexTree':
            drawRegexTree(param)
            dot.render(f"{dir}/<regexTree>{id(param)}", format='png', cleanup=True)

        else:
            raise ValueError(f"Invalid type: {type}")

  
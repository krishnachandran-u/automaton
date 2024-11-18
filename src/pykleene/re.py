from nfa import NFA
from _helpers import BinaryTreeNode 

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
    
    def expressionTree(regex: str) -> BinaryTreeNode:
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


  
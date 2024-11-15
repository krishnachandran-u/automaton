from __future__ import annotations
from typing import List

class TreeNode:
    left: TreeNode
    value: str
    right: TreeNode

    def __init__(self, leftNode: TreeNode = None, value: str = None, rightNode: TreeNode = None):
        self.left = leftNode
        self.value = value
        self.right = rightNode

def format_regex(regex: str) -> str:
    formatted = []
    operators_and_brackets = ['+', '.', '*', '(', ')']

    def append_dot() -> None:
        formatted.append('.')
    def is_symbol(char: str) -> bool:
        return char not in operators_and_brackets

    for i in range(len(regex) - 1):
        formatted.append(regex[i])
        if (is_symbol(regex[i]) or regex[i] in [')', '*']) and (is_symbol(regex[i + 1]) or regex[i + 1] == '(' ):
            append_dot()
    formatted.append(regex[-1])

    return ''.join(formatted)

def infix_to_postfix(regex: str):
    precedence = {
        '+': 1,  
        '.': 2, 
        '*': 3, 
        '(': 0, 
        ')': 0
    }
    stack = []
    postfix = []
    for char in regex:
        if char == '(':
            stack.append(char)
        elif char == ')':
            while stack[-1] != '(':
                postfix.append(stack.pop())
            stack.pop()
        elif char in precedence:
            while stack and precedence[stack[-1]] >= precedence[char]:
                postfix.append(stack.pop())
            stack.append(char)
        else:
            postfix.append(char)
    while stack:
        postfix.append(stack.pop())
    return ''.join(postfix)

def postfix_to_tree(postfix: str) -> TreeNode:
    stack: List[TreeNode] = []
    operators = ['+', '.', '*']
    for char in postfix: 
        if char not in operators:
            stack.append(TreeNode(leftNode=None, value=char, rightNode=None))
        else:
            if char == '*':
                leftNode = stack.pop()
                if leftNode.value in ['ε', 'φ']: # ε* = ε, φ* = ε
                    node = TreeNode(leftNode=None, value='ε', rightNode=None)
                else:
                    node = TreeNode(leftNode=leftNode, value=char, rightNode=None) 
            elif char == '.':
                rightNode = stack.pop()
                leftNode = stack.pop()
                if leftNode.value == 'φ' or rightNode.value == 'φ': # φ.anything = φ
                    node = TreeNode(leftNode=None, value='φ', rightNode=None)
                elif leftNode.value == 'ε': # ε.anything = anything
                    node = rightNode
                elif rightNode.value == 'ε':
                    node = leftNode
                else:
                    node = TreeNode(leftNode=leftNode, value=char, rightNode=rightNode)
            elif char == '+':
                rightNode = stack.pop()
                leftNode = stack.pop()
                if leftNode.value == 'φ': 
                    node = rightNode
                elif rightNode.value == 'φ':
                    node = leftNode
                elif leftNode.value == 'ε' and rightNode.value == 'ε':
                    node = TreeNode(leftNode=None, value='ε', rightNode=None)
                else:
                    node = TreeNode(leftNode=leftNode, value=char, rightNode=rightNode)
            stack.append(node) 
    return stack.pop()

def get_regexTree(regex: str) -> TreeNode:
    formatted_regex = format_regex(regex)
    postfix = infix_to_postfix(formatted_regex)
    return postfix_to_tree(postfix)

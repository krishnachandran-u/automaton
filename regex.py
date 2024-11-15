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
        if (is_symbol(regex[i]) or regex[i] in [')', '*']) and (is_symbol(regex[i + 1]) or regex[i + 1] == '(' ):
            append_dot()
        formatted.append(regex[i])
    formatted.append[regex[-1]]

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
    stack = []
    operators = ['+', '.', '*']
    for char in postfix: 
        if char not in operators:
            stack.append(TreeNode(leftNode=None, value=char, rightNode=None))
        else:
            if char == '*':
                node = TreeNode(leftNode=stack.pop(), value=char, rightNode=None)
            else:
                node = TreeNode(leftNode=stack.pop(), value=char, rightNode=stack.pop())
            stack.append(node) 
    return stack.pop()

"""
handle the case when there is epsilon and phi in the regex
"""

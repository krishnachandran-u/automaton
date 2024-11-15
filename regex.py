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
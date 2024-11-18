from typing import Any

class BinaryTreeNode:
    leftChild: 'BinaryTreeNode'
    data: Any
    rightChild: 'BinaryTreeNode'

    def __init__(self, leftChild: 'BinaryTreeNode' = None, data: Any = None, rightChild: 'BinaryTreeNode' = None):
        self.leftChild = leftChild
        self.data = data
        self.rightChild = rightChild
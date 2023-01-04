class Node:
    def __init__(self, data=None):
        self.data = data
        self.left =None
        self.right = None


class BinarySearchTree:
    def __init__(self):
        self.root = None
    
    def _insert_recursive(self,value,node):
        if value < node.data:
            if node.left is None:
                node.left = Node(value)
            else: #if the left node is not empty, that means it has substrees, meaning these should be checked recursively
                self._insert_recursive(value, node.left)
        elif value > node.date:
            if node.right is None:
                node.right = Node(value)
            else:
                self._insert_recursive(value, node.right)
        else: #if the value is equal the node.data, (do nothing because a tree shouldn't have duplicates)
            return

            
    
    def insert (self,value):
        if self.root is None: #empty tree
            self.root = Node(value)
        else:
            self._insert_recursive(value,self.root)

class Node:
    """
    A single node in the binary search tree.
    Holds a word and pointers to left/right children.
    """
    def __init__(self, word: str):
        self.word = word
        self.left = None
        self.right = None

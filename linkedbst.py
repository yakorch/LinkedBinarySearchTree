"""
File: linkedbst.py
Author: Ken Lambert
"""
import random
import timeit
from math import log

# from Laba12.Queue.abstractcollection import AbstractCollection
# from Laba13.binary_search_tree.bstnode import BSTNode
# from Laba12.Stack.linkedstack import LinkedStack
# from Laba12.Queue.linkedqueue import LinkedQueue


from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack
# # from linkedqueue import LinkedQueue


class LinkedBST(AbstractCollection):
    """A link-based binary search tree implementation."""

    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, sourceCollection)

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            str_res = ""
            if node != None:
                str_res += recurse(node.right, level + 1)
                str_res += "| " * level
                str_res += str(node.data) + "\n"
                str_res += recurse(node.left, level + 1)
            return str_res

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right != None:
                    stack.push(node.right)
                if node.left != None:
                    stack.push(node.left)

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        return None

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if node != None:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return iter(lyst)

    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        return None

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        return None

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) != None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""

        def recurse(node):
            if node is None:
                return None
            elif item == node.data:
                return node.data
            elif item < node.data:
                return recurse(node.left)
            else:
                return recurse(node.right)

        return recurse(self._root)

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        """Adds item to the tree."""

        # Helper function to search for item's position
        def recurse(node):
            # New item is less, go left until spot is found
            if item < node.data:
                if node.left is None:
                    node.left = BSTNode(item)
                else:
                    recurse(node.left)
            # New item is greater or equal,
            # go right until spot is found
            elif node.right is None:
                node.right = BSTNode(item)
            else:
                recurse(node.right)
                # End of recurse

        # Tree is empty, so new item goes at the root
        if self.isEmpty():
            self._root = BSTNode(item)
        # Otherwise, search for the item's spot
        else:
            recurse(self._root)
        self._size += 1

    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def lift_left_subtreetotop(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            current_node = top.left
            while not current_node.right == None:
                parent = current_node
                current_node = current_node.right
            top.data = current_node.data
            if parent == top:
                top.left = current_node.left
            else:
                parent.right = current_node.left

        # Begin main part of the method
        if self.isEmpty(): return None

        # Attempt to locate the node containing the item
        item_removed = None
        pre_root = BSTNode(None)
        pre_root.left = self._root
        parent = pre_root
        direction = 'L'
        current_node = self._root
        while not current_node == None:
            if current_node.data == item:
                item_removed = current_node.data
                break
            parent = current_node
            if current_node.data > item:
                direction = 'L'
                current_node = current_node.left
            else:
                direction = 'R'
                current_node = current_node.right

        # Return None if the item is absent
        if item_removed is None: return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if not (current_node.left is None or current_node.right is None):
            lift_left_subtreetotop(current_node)
        else:

            # Case 2: The node has no left child
            if current_node.left is None:
                new_child = current_node.right

                # Case 3: The node has no right child
            else:
                new_child = current_node.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = new_child
            else:
                parent.right = new_child

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = pre_root.left
        return item_removed

    def replace(self, item, new_item):
        """
        If item is in self, replaces it with newItem and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe is not None:
            if probe.data == item:
                old_вata = probe.data
                probe.data = new_item
                return old_вata
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def is_leaf(self, pos):
        """
        Checks if an edge is a leaf
        """
        return self.number_of_children(pos) == 0

    @staticmethod
    def number_of_children(pos: BSTNode):
        """
        Recursively calculates the number of children for some node 'pos'
        """

        def recurse(node: BSTNode):
            if node is None:
                return 0
            children = 2
            if node.left is None:
                children -= 1
            if node.right is None:
                children -= 1
            return children + recurse(node.left) + recurse(node.right)

        return recurse(pos)

    def height(self):
        """
        Return the height of tree
        :return: int
        """
        return self.height_help(self._root)

    def height_help(self, pos):
        """
        Helper function
        :param pos:
        :return:
        """
        return 1 + max(self.height_help(child) for child in
                       list(filter(lambda x: x is not None,
                                   [pos.left, pos.right]))) if not self.is_leaf(pos) else 0

    def is_balanced(self):
        """
        Return True if tree is balanced
        :return:
        """
        return self.height() < 2 * log(self._size + 1, 2) - 1

    def range_find(self, low, high):
        """
        Returns a list of the items in the tree, where low <= item <= high.
        """
        return [item for item in self.inorder() if low <= item <= high]

    def rebalance(self):
        """
        Balances the tree.
        :return:
        """
        sorted_values = list(sorted(self.inorder()))
        self.clear()

        def add_list(values: list) -> None:
            middle = len(values) // 2
            if middle == 0:
                if values:
                    self.add(values[0])
            else:
                self.add(values[middle])
                add_list(values[:middle])
                add_list(values[middle + 1:])

        add_list(sorted_values)

    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        return self.compare_items(item, "less")

    def compare_items(self, item, comp_method="more"):
        """
        Compares elems in a tree with item and returns the closest found
        """
        poss_values = []
        for value in self.inorder():
            if comp_method == "less":
                if item < value:
                    poss_values.append(value)
            else:
                if item > value:
                    poss_values.append(value)
        if comp_method == "less":
            return None if not poss_values else min(poss_values)
        return None if not poss_values else max(poss_values)

    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        return self.compare_items(item)

    @staticmethod
    def demo_bst(path):
        """
        Calculates the time for different methods of finding a word in a dictionary
        """
        # reading words from dictionary to a list
        with open(file=path, mode="r", encoding="utf-8") as file:
            words = file.readlines()

        # generates random words
        random_words = [random.choice(words) for _ in range(10 ** 4)]

        # time for searching 10 000 words in a list
        list_time = timeit.timeit("words.index(next(rand_words_iter))",
                                  globals={"rand_words_iter": iter(random_words), "words": words}, number=10 ** 4)

        unbalanced_tree = LinkedBST()
        less_words = words[:10 ** 3]  # because of recursion problem
        for word in less_words:
            unbalanced_tree.add(word)

        # time for an unbalanced tree, where elements added in the stupidest of ways
        unbalanced_tree_time = timeit.timeit("unbalanced_tree.find(next(random_words))",
                                             globals={"random_words": iter(random_words),
                                                      "unbalanced_tree": unbalanced_tree}, number=10 ** 4)

        shuffled_tree = LinkedBST()
        shuffled_words = random.sample(words, words.__len__())
        for word in shuffled_words:
            shuffled_tree.add(word)
        # time for a shuffled tree
        shuffle_tree_time = timeit.timeit("shuffled_tree.find(next(random_words))",
                                          globals={"random_words": iter(random_words),
                                                   "shuffled_tree": shuffled_tree}, number=10 ** 4)

        shuffled_tree.rebalance()
        # time for a balanced tree
        balanced_tree_time = timeit.timeit("balanced_tree.find(next(random_words))",
                                           globals={"random_words": iter(random_words),
                                                    "balanced_tree": shuffled_tree}, number=10 ** 4)

        print("Search of 10000 words using different methods:")
        print(f"List: {list_time.__round__(6)}")
        # multiplying by 240 for honesty of results, unbalanced tree had fewer words in it
        print(f"Unbalanced tree: {(240 * unbalanced_tree_time).__round__(6)}")
        print(f"Shuffled_tree: {shuffle_tree_time.__round__(6)}")
        print(f"Balanced_tree: {balanced_tree_time.__round__(6)}")

# LinkedBST().demo_bst("/Users/oksanakorch/Desktop/Python OP/Laby/Laba13/words.txt")

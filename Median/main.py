from bisect import bisect_left, bisect_right
from sys import stdout

from math import log
from random import shuffle

def is_leaf(node):
    return isinstance(node, RBLeaf)

class RBNode(object):
    """ Red Black Tree Internal Node (must have a value and !None children.) """

    def __init__(self, val, red=False, parent=None):
        if val is None:
            raise ValueError
        self.parent = parent
        self.red = red
        self.left = RBLeaf(self)
        self.right = RBLeaf(self)
        self.val = val

    def __cmp__(self, node):
        if node is None:
            return 1
        if not isinstance(node, RBNode):
            raise TypeError
        if self.val < node.val:
            return -1
        if self.val > node.val:
            return 1
        return 0

    def __str__(self):
        color = "B"
        if self.red:
            color = "R"
        return "%s%s" % (str(self.val), color)

    def color(self):
        if self.red:
            return "R"
        return "B"

    def grandparent(self):
        if self.parent:
            return self.parent.parent
        return None

    def sibling(self):
        if self.parent:
            if self is self.parent.left:
                return self.parent.right
            return self.parent.left
        return None

    def uncle(self):
        if self.parent:
            return self.parent.sibling()
        return None

class RBLeaf(RBNode):
    """ Red Black Leaf Node (black, val=None, left=right=None) """

    def __init__(self, parent=None):
        self.parent = parent
        self.red = False
        self.left = None
        self.right = None
        self.val = None

class RBTree(object):
    """ Red Black Tree object encapsulating tree operations. """

    def __init__(self):
        self.root = None

    def __iter__(self):
        return self.__inorder(self.root)

    # predecessor() would be a nice name, but that might not be a child,
    # and we need only children for the remove code, thus max_left().
    def __max_left(self, node):
        # If node is a leaf or if its left child is a leaf,
        # just return node.
        if is_leaf(node) or is_leaf(node.left):
            return node

        m = node.left
        while not is_leaf(m.right):
            m = m.right
        return m

    def __rotate_right(self, node):
        """ Rotate the tree right on node. """
        l = node.left
        if node.parent:
            if node is node.parent.right:
                node.parent.right = l
            else:
                node.parent.left = l
        l.parent = node.parent
        node.left = l.right
        if node.left:
            node.left.parent = node
        l.right = node
        node.parent = l
        if not node.grandparent():
            self.root = node.parent

    def __rotate_left(self, node):
        """ Rotate the tree left on node. """
        r = node.right
        if node.parent:
            if node is node.parent.right:
                node.parent.right = r
            else:
                node.parent.left = r
        r.parent = node.parent
        node.right = r.left
        if node.right:
            node.right.parent = node
        r.left = node
        node.parent = r
        if not node.grandparent():
            self.root = node.parent

    def __replace(self, parent, child):
        """Move a child into its parent's place."""

        if child.parent.left is child:
            child.parent.left = RBLeaf(child.parent)
        else:
            child.parent.right = RBLeaf(child.parent)

        if not parent.parent:
            self.root = child
        elif parent.parent.left is parent:
            parent.parent.left = child
        else:
            parent.parent.right = child

        child.parent = parent.parent
        if not is_leaf(child):
            child.left = parent.left
            child.left.parent = child
            child.right = parent.right
            child.right.parent = child

    def __inorder(self, node):
        node = self.root
        while node.left:
            node = node.left

        while True:
            yield node

            if node.right:
                node = node.right
                while node.left:
                    node = node.left
            else:
                while node.parent and node is node.parent.right:
                    node = node.parent
                node = node.parent

            if node is None:
                break

    def print_tree(self, node=None):
        """ Debugging routine to get a quick view of the tree. """

        if node is None:
            node = self.root
        print "%s" % (node)
        if node.left:
            self.print_tree(node.left)
        if node.right:
            self.print_tree(node.right)

    def insert(self, node):
        """ Add node to the tree and rebalance as necessary. """
        node.parent = None
        # New Root
        if not self.root:
            self.root = node
            return 1

        # Insert a Red node
        parent = self.root
        node.red = True
        ops = 0
        while not node.parent:
            ops = ops +1
            if node < parent:
                if not is_leaf(parent.left):
                    parent = parent.left
                    continue
                parent.left = node
            elif node > parent:
                if not is_leaf(parent.right):
                    parent = parent.right
                    continue
                parent.right = node
            else:
                raise ValueError
            node.parent = parent

        while True:
            p = node.parent

            # Case 1: Root Node
            if not p:
                node.red = False
                break

            # Case 2: Black parent
            if not p.red:
                break

            # Case 3: Parent and Uncle are Red
            u = node.uncle()
            if u.red:
                p.red = False
                u.red = False
                g = node.grandparent()
                g.red = True
                node = g
                continue

            # Case 4: Parent is Red and Uncle is Black
            #         left-right or right-left ancestry
            g = node.grandparent()
            if node is p.right and p is g.left:
                self.__rotate_left(p)
                node = node.left
            elif node is p.left and p is g.right:
                self.__rotate_right(p)
                node = node.right

            # Case 5: Parent is Red and Uncle is Black
            #         left-left or right-right ancestry
            g = node.grandparent()
            p = node.parent
            p.red = False
            g.red = True
            if node is p.left and p is g.left:
                self.__rotate_right(g)
            else: # node is p.right and p is g.right:
                self.__rotate_left(g)
            break

        return ops


    def find(self, val):
        node = self.root
        ops = 0
        while node and node.val != val:
            ops = ops +1
            if val > node.val:
                node = node.right
            else:
                node = node.left
            if is_leaf(node):
                node = None
                break
        return (node,ops)

    def remove(self, node):
        ops = 0

        # If the node to be removed has two non-leaf children, find the
        # preceeding in-order node (child) and replace the contents of the node
        # to be removed with that of the child. Then proceed to remove the child
        # from the tree.
        if not is_leaf(node.left) and not is_leaf(node.right):
            child = self.__max_left(node)
            node.val = child.val
            node = child

        # node has at _most_ one non-leaf child
        child = node.left
        if is_leaf(child):
            child = node.right
        self.__replace(node, child)

        # Removing a red node doesn't impact black node count in the path
        if node.red:
            return ops

        # node is black, if the child is red, change it to black, and the
        # black node count is preserved for this path
        if child.red:
            child.red = False
            return

        while True:
            # Case 1: node and child are both black
            #         if we deleted root, then black node count is preserved
            parent = child.parent
            if not parent:
                break

            # Black node count through child has been reduced by one

            # Case 2: if node's sibling is red, paint it black, paint parent
            #         red, and rotate left on parent. This balances the tree.
            sibling = child.sibling()
            if sibling.red:
                sibling.red = False
                parent.red = True
                if sibling is parent.right:
                    self.__rotate_left(parent)
                else:
                    self.__rotate_right(parent)
                sibling = child.sibling()

            # Sibling is black at this point due to Case 2, noting that
            # children of a red node must be black.

            # Case 3: if sibling's children and parent are black,
            #         painting sibling red balances the black node count at P,
            if not parent.red and\
               not sibling.left.red and not sibling.right.red:
                sibling.red = True
                child = parent
                # goto Case 1 with node is p
                continue

            # Case 4: if parent is red, sibling is black, if its children are
            #         black, paint sibling red and parent black to return the
            #         black node count to it's original value.
            if parent.red and\
               not sibling.left.red and not sibling.right.red:
                sibling.red = True
                parent.red = False
                break

            # Case 5: If sibling's children are black and red (not both red),
            #         prepare for Case 6 by ensuring the red child is left if
            #         the sibling is left, or right if the sibling is right.
            if sibling is parent.left and not is_leaf(sibling) and\
               not sibling.left.red:
                sibling.red = True
                sibling.right.red = False
                self.__rotate_left(sibling)
            elif sibling is parent.right and not is_leaf(sibling) and\
                 not sibling.right.red:
                sibling.red = True
                sibling.left.red = False
                self.__rotate_right(sibling)

            # Case 6: Balance the black count via a rotation on parent, and
            #         recoloring of parent, sibling, and the sibling's red
            #         child.
            sibling = child.sibling()
            sibling.red = parent.red
            parent.red = False
            if sibling is parent.right:
                sibling.right.red = False
                self.__rotate_left(parent)
            else:
                sibling.left.red = False
                self.__rotate_right(parent)
            break

        return ops

    def verify(self):
        result = True
        # 1) A node is either red or black.
        # 2) The root is black.
        if self.root.red:
            print "\n    ERROR: root is red"
            result = False
        if self.root.parent:
            print "\n    ERROR: root has a parent"
            result = False

        bcount = None
        for node in self:
            if node.red:
                # 3) All leaves are black.
                if is_leaf(node):
                    print "\n    ERROR: red leaf node"
                    result = False
                    continue
                    # 4) Both children of every red node are black.
                if node.left.red or node.right.red:
                    print "\n    ERROR: red node with red child"
                    result = False

            # Ensure the parent->child->parent links are valid
            if not is_leaf(node):
                if not node.left.parent is node:
                    print "\n    ERROR: %s->left(%s)->parent: %s" %\
                          (node, node.left, node.left.parent)
                    result = False
                if not node.right.parent is node:
                    print "\n    ERROR: %s->right(%s)->parent: %s" %\
                          (node, node.right, node.right.parent)
                    result = False

            # 5) Verify black count is consistent across leaves.
            if is_leaf(node):
                tmp = node
                count = 1
                while tmp.parent:
                    tmp = tmp.parent
                    if not tmp.red:
                        count = count + 1
                if bcount is None:
                    bcount = count
                elif count != bcount:
                    print "\n    ERROR: different black node count to leaf"
                    result = False
        return result

def successor(tree, x):

    #if x has right child, then retrieve the leftmost of its right branch
    if x.right:
        return self.minimum(x.right)
        #if x doesn't have right child and has no parent, then it's root and last node, so no successor
    if not x.p:
        return None
    parent = x.p
    #otherwise if x is a left child, then parent is its successor
    if x == parent.left:
        return parent
        #otherwise it x is a right child, then it is the last node of its parent's branch, so the successor will be its
    #parent's successor
    tmp = parent
    while tmp.p and tmp != tmp.p.left:
        tmp = tmp.p
    return tmp.p

    pass

def predecessor(tree, x):
    #if x has left child, then retrieve the rightmost of its left branch
    if x.left:
        return self.maximum(x.left)
        #if x doesn't have left child and has no parent, then it's root and the first node, so no predecessor
    if not x.p:
        return None
    parent = x.p
    #otherwise if x is a right child, then parent is its predecessor
    if x == parent.right:
        return parent
        #otherwise it x is a keft child, then it is the first node of its parent's branch, so the predecessor will be its
    #parent's predecessor
    tmp = parent
    while tmp.p and tmp != tmp.p.right:
        tmp = tmp.p
    return tmp.p
    pass

#test

tree = RBTree()

tree.insert(RBNode(1))
tree.insert(RBNode(2))
tree.insert(RBNode(1))

fd = open( "input00.txt" )
raw_input = fd.readline
#
##!/bin/python
#
#
#
## code snippet for illustrating input/output
#
N = int(raw_input())

s = []
x = []

for i in range(0, N):

    tmp = raw_input()
    a, b = [xx for xx in tmp.split(' ')]
    s.append(a)
    x.append(int(b))

auto_balanced_tree = RBTree()
center = None
size = 0
m = -1

def add(e):
    global auto_balanced_tree, size, center, m
    auto_balanced_tree.insertNode(e, None)
    size+=1
    if size == 1:
        center = auto_balanced_tree.root
        m = center.key
        return

    if e >= center.key: #case 1, the element is added to center's right
        if size % 2 == 0:
            #become even, center is not moved
            m = ( center.key + auto_balanced_tree.nextNode(center).key ) / 2.0
        else:
            #become odd, center is 1 step forward
            center = auto_balanced_tree.nextNode(center)
            m = center.key
    else: #case 2, the element is added to center's left
        if size % 2 == 0:
            #become even, center is 1 step backward
            old = center.key
            center = auto_balanced_tree.prevNode(center)
            m = (center.key + old) / 2.0
        else:
            #become odd, center is not moved
            m = center.key

def remove(e):
    global auto_balanced_tree, size, center, m
    if not size:
        raise ValueError

    node_to_delete = None
    if center and e == center.key: # if center has the same value as e, then remove center, this makes many things easier
        #since we don't have to judge wheter the node to remove is right or left to the center
        node_to_delete = center
    if not node_to_delete:
        node_to_delete = auto_balanced_tree.findNode(e)
    if not node_to_delete:
        raise ValueError #cannot find the node to delete

    size -= 1
    if center and id(node_to_delete) == id(center): #case 0, remove center
        if size % 2 == 0:
            new_center = auto_balanced_tree.prevNode(center)
        else:
            new_center = auto_balanced_tree.nextNode(center)
        auto_balanced_tree.deleteNode(center)
        center = new_center
        return

    auto_balanced_tree.deleteNode(node_to_delete)
    # e will be either greater or less than center.key, since the case equality is handled earlier
    if e > center.key : #case 1, the element removed is right to center
        if size % 2 == 0:
            #become even, center is 1 step backward
            old = center.key
            center = auto_balanced_tree.prevNode(center)
            m = (center.key + old) / 2.0
        else:
            #become odd, center is not moved
            m = center.key
    else: #case 2, the element removed is left to center
        if size % 2 == 0:
            #become even, center is not moved
            m = (center.key + auto_balanced_tree.nextNode(center).key) / 2.0
        else:
            #become odd, center is 1 step forward
            center = auto_balanced_tree.nextNode(center)
            m = center.key

def median():
    global auto_balanced_tree, size, center
    if not size:
        raise ValueError

    if m == int(m):
        print str(int(m))
    else:
        print m

for i in range(0, 1):
    try:
        if s[i] == 'a' :
            add(x[i])
        else:
            remove(x[i])
        median()
    except ValueError:
        print "Wrong!"
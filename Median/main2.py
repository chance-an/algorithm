class rbnode(object):
    """
    A node in a red black tree. See Cormen, Leiserson, Rivest, Stein 2nd edition pg 273.
    """

    def __init__(self, key):
        "Construct."
        self._key = key
        self._red = False
        self._left = None
        self._right = None
        self._p = None

    key = property(fget=lambda self: self._key, doc="The node's key")
    red = property(fget=lambda self: self._red, doc="Is the node red?")
    left = property(fget=lambda self: self._left, doc="The node's left child")
    right = property(fget=lambda self: self._right, doc="The node's right child")
    p = property(fget=lambda self: self._p, doc="The node's parent")

    def __str__(self):
        "String representation."
        return str(self.key)


    def __repr__(self):
        "String representation."
        return str(self.key)

#    def __eq__(self, other):
#        if other is None:
#            return False
#        return id(self) == id(other)

    def __nonzero__(self):
        return self.key is not None


class rbtree(object):
    """
    A red black tree. See Cormen, Leiserson, Rivest, Stein 2nd edition pg 273.
    """


    def __init__(self, create_node=rbnode):
        "Construct."

        self._nil = create_node(key=None)
        "Our nil node, used for all leaves."

        self._root = self.nil
        "The root of the tree."

        self._create_node = create_node
        "A callable that creates a node."


    root = property(fget=lambda self: self._root, doc="The tree's root node")
    nil = property(fget=lambda self: self._nil, doc="The tree's nil node")


    def search(self, key, x=None):
        """
        Search the subtree rooted at x (or the root if not given) iteratively for the key.

        @return: self.nil if it cannot find it.
        """
        if None == x:
            x = self.root
        while x != self.nil and key != x.key:
            if key < x.key:
                x = x.left
            else:
                x = x.right
        return x


    def minimum(self, x=None):
        """
        @return: The minimum value in the subtree rooted at x.
        """
        if None == x:
            x = self.root
        while x.left != self.nil:
            x = x.left
        return x


    def maximum(self, x=None):
        """
        @return: The maximum value in the subtree rooted at x.
        """
        if None == x:
            x = self.root
        while x.right != self.nil:
            x = x.right
        return x


    def insert_key(self, key):
        "Insert the key into the tree."
        self.insert_node(self._create_node(key=key))


    def insert_node(self, z):
        "Insert node z into the tree."
        y = self.nil
        x = self.root
        while x != self.nil:
            y = x
            if z.key < x.key:
                x = x.left
            else:
                x = x.right
        z._p = y
        if y == self.nil:
            self._root = z
        elif z.key < y.key:
            y._left = z
        else:
            y._right = z
        z._left = self.nil
        z._right = self.nil
        z._red = True
        self._insert_fixup(z)


    def _insert_fixup(self, z):
        "Restore red-black properties after insert."
        while z.p.red:
            if z.p == z.p.p.left:
                y = z.p.p.right
                if y.red:
                    z.p._red = False
                    y._red = False
                    z.p.p._red = True
                    z = z.p.p
                else:
                    if z == z.p.right:
                        z = z.p
                        self._left_rotate(z)
                    z.p._red = False
                    z.p.p._red = True
                    self._right_rotate(z.p.p)
            else:
                y = z.p.p.left
                if y.red:
                    z.p._red = False
                    y._red = False
                    z.p.p._red = True
                    z = z.p.p
                else:
                    if z == z.p.left:
                        z = z.p
                        self._right_rotate(z)
                    z.p._red = False
                    z.p.p._red = True
                    self._left_rotate(z.p.p)
        self.root._red = False


    def _left_rotate(self, x):
        "Left rotate x."
        y = x.right
        x._right = y.left
        if y.left != self.nil:
            y.left._p = x
        y._p = x.p
        if x.p == self.nil:
            self._root = y
        elif x == x.p.left:
            x.p._left = y
        else:
            x.p._right = y
        y._left = x
        x._p = y


    def _right_rotate(self, y):
        "Left rotate y."
        x = y.left
        y._left = x.right
        if x.right != self.nil:
            x.right._p = y
        x._p = y.p
        if y.p == self.nil:
            self._root = x
        elif y == y.p.right:
            y.p._right = x
        else:
            y.p._left = x
        x._right = y
        y._p = x


    def check_invariants(self):
        "@return: True iff satisfies all criteria to be red-black tree."

        def is_red_black_node(node):
            "@return: num_black"
            # check has _left and _right or neither
            if (node.left and not node.right) or (node.right and not node.left):
                return 0, False

            # check leaves are black
            if not node.left and not node.right and node.red:
                return 0, False

            # if node is red, check children are black
            if node.red and node.left and node.right:
                if node.left.red or node.right.red:
                    return 0, False

            # descend tree and check black counts are balanced
            if node.left and node.right:

                # check children's parents are correct
                if self.nil != node.left and node != node.left.p:
                    return 0, False
                if self.nil != node.right and node != node.right.p:
                    return 0, False

                # check children are ok
                left_counts, left_ok = is_red_black_node(node.left)
                if not left_ok:
                    return 0, False
                right_counts, right_ok = is_red_black_node(node.right)
                if not right_ok:
                    return 0, False

                # check children's counts are ok
                if left_counts != right_counts:
                    return 0, False
                return left_counts, True
            else:
                return 0, True

        num_black, is_ok = is_red_black_node(self.root)
        return is_ok and not self.root._red

        def delete_key(self, key):
            """
            Delete a key from the tree.

            @param key: the key you want to delete from the tree.
            @return: False if the key was not in the tree,
            otherwise True.
            """
        node = self.search(key)
        if node == self.nil:
            return False
        self.delete_node(node)
        return True

    def delete_key(self, key):
        """
Delete a key from the tree.

@param key: the key you want to delete from the tree.
@return: False if the key was not in the tree,
otherwise True.
"""
        node = self.search(key)
        if node == self.nil:
            return False
        self.delete_node(node)
        return True

    def delete_node(self, n):
        """
Delete a node from the tree.

@param n: the node you want to delete from the tree.
"""
        # The following source was "translated" from
        # this Java source:
        # http://en.literateprograms.org/Red-black_tree_(Java)
        if n.left != self.nil and n.right != self.nil:
            pred = self.maximum(n.left)
            n._key = pred.key
            n = pred

        assert n.left == self.nil or n.right == self.nil

        if n.right == self.nil:
            child = n.left
        else:
            child = n.right

        if not n.red:
            n._red = child.red
            self._deleteCase1(n)
        self._replaceNode(n, child)

        if self.root.red:
            self.root._red = False

    def _replaceNode(self, oldn, newn):
        if oldn.p == self.nil:
            self._root = newn
        else:
            if oldn == oldn.p.left:
                oldn.p._left = newn
            else:
                oldn.p._right = newn
        if newn != self.nil:
            newn._p = oldn.p

    def _deleteCase1(self, n):
        """ In this case, N has become the root node. The deletion
removed one black node from every path, so no properties
are violated.
"""
        if n.p == self.nil:
            return
        else:
            self._deleteCase2(n)

    def _deleteCase2(self, n):
        """ N has a red sibling. In this case we exchange the colors
of the parent and sibling, then rotate about the parent
so that the sibling becomes the parent of its former
parent. This does not restore the tree properties, but
reduces the problem to one of the remaining cases. """
        if self._sibling(n).red:
            n.p.red = True
            self._sibling(n)._red = False
            if n == n.p.left:
                self._left_rotate(n.p)
            else:
                self._right_rotate(n.p)
        self._deleteCase3(n)

    def _deleteCase3(self, n):
        """ In this case N's parent, sibling, and sibling's children
are black. In this case we paint the sibling red. Now
all paths passing through N's parent have one less black
node than before the deletion, so we must recursively run
this procedure from case 1 on N's parent.
"""
        tmp = self._sibling(n)
        if not n.p.red and not tmp.red and not tmp.left and not tmp.right:
            tmp._red = True
            self._deleteCase1(n.p)
        else:
            self._deleteCase4(n)

    def _deleteCase4(self, n):
        """ N's sibling and sibling's children are black, but its
parent is red. We exchange the colors of the sibling and
parent; this restores the tree properties.
"""
        tmp = self._sibling(n)
        if n.p.red and not tmp.red and not tmp.left.red and not tmp.right.red:
            tmp._red = True
            n.p._red = False
        else:
            self._deleteCase5(n)

    def _deleteCase5(self, n):
        """ There are two cases handled here which are mirror images
of one another:
N's sibling S is black, S's left child is red, S's
right child is black, and N is the left child of its
parent. We exchange the colors of S and its left
sibling and rotate right at S.

N's sibling S is black, S's right child is red,
S's left child is black, and N is the right child of
its parent. We exchange the colors of S and its right
sibling and rotate left at S.
Both of these function to reduce us to the situation
described in case 6. """
        tmp = self._sibling(n)

        if n == n.p.left and not tmp.red and tmp.left and not tmp.right:
            tmp._red = True
            tmp.left._red = False
            self._right_rotate(tmp)
        elif n == n.p.right and not tmp.red and tmp.right and not tmp.left:
            tmp._red = True
            tmp.right._red = False
            self._left_rotate(tmp)

        self._deleteCase6(n)

    def _deleteCase6(self, n):
        """ There are two cases handled here which are mirror images
of one another:
N's sibling S is black, S's right child is red, and N is
the left child of its parent. We exchange the colors of
N's parent and sibling, make S's right child black, then
rotate left at N's parent.
N's sibling S is black, S's left child is red, and N is
the right child of its parent. We exchange the colors of
N's parent and sibling, make S's left child black, then
rotate right at N's parent.
"""
        tmp = self._sibling(n)

        tmp._red = n.p.red
        n.p._red = False

        if n == n.p.left:
            assert tmp.right.red
            tmp.right._red = False
            self._left_rotate(n.p)
        else:
            assert tmp.left.red
            tmp.left._red = False
            self._right_rotate(n.p)

    def _sibling(self, n):
        assert n.p != self.nil
        if n == n.p.left:
            return n.p.right
        else:
            return n.p.left

    def successor(self, x):
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

    def predecessor(self, x):
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

#def write_tree_as_dot(t, f, show_nil=False):
#    "Write the tree in the dot language format to f."
#    def node_id(node):
#        return 'N%d' % id(node)
#
#    def node_color(node):
#        if node.red:
#            return "red"
#        else:
#            return "black"
#
#    def visit_node(node):
#        "Visit a node."
#        print >> f, "  %s [label=\"%s\", color=\"%s\"];" % (node_id(node), node, node_color(node))
#        if node.left:
#            if node.left != t.nil or show_nil:
#                visit_node(node.left)
#                print >> f, "  %s -> %s ;" % (node_id(node), node_id(node.left))
#        if node.right:
#            if node.right != t.nil or show_nil:
#                visit_node(node.right)
#                print >> f, "  %s -> %s ;" % (node_id(node), node_id(node.right))
#
#    print >> f, "// Created by rbtree.write_dot()"
#    print >> f, "digraph red_black_tree {"
#    visit_node(t.root)
#    print >> f, "}"


tree = rbtree()
for i in range(10):
    tree.insert_key(i)

#test infrastructure
#write_tree_as_dot(tree, stdout)
#node5 = tree.search(0)
#print tree.successor(node5)
#print tree.predecessor(node5)


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

auto_balanced_tree = rbtree()
center = None
size = 0
m = -1

def add(e):
    global auto_balanced_tree, size, center, m
    auto_balanced_tree.insert_key(e)
    size+=1
    if size == 1:
        center = auto_balanced_tree.root
        m = center.key
        return

    if e >= center.key: #case 1, the element is added to center's right
        if size % 2 == 0:
            #become even, center is not moved
            m = (center.key + auto_balanced_tree.successor(center).key) / 2.0
        else:
            #become odd, center is 1 step forward
            center = auto_balanced_tree.successor(center)
            m = center.key
    else: #case 2, the element is added to center's left
        if size % 2 == 0:
            #become even, center is 1 step backward
            old = center.key
            center = auto_balanced_tree.predecessor(center)
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
        node_to_delete = auto_balanced_tree.search(e)
    if not node_to_delete:
        raise ValueError #cannot find the node to delete

    size -= 1
    if center and id(node_to_delete) == id(center): #case 0, remove center
        if size % 2 == 0:
            new_center = auto_balanced_tree.predecessor(center)
        else:
            new_center = auto_balanced_tree.successor(center)
        auto_balanced_tree.delete_node(center)
        center = new_center
        return

    auto_balanced_tree.delete_node(node_to_delete)
    # e will be either greater or less than center.key, since the case equality is handled earlier
    if e > center.key : #case 1, the element removed is right to center
        if size % 2 == 0:
            #become even, center is 1 step backward
            old = center.key
            center = auto_balanced_tree.predecessor(center)
            m = (center.key + old) / 2.0
        else:
            #become odd, center is not moved
            m = center.key
    else: #case 2, the element removed is left to center
        if size % 2 == 0:
            #become even, center is not moved
            m = (center.key + auto_balanced_tree.successor(center).key) / 2.0
        else:
            #become odd, center is 1 step forward
            center = auto_balanced_tree.successor(center)
            m = center.key

def median():
    global auto_balanced_tree, size, center
    if not size:
        raise ValueError

    if m == int(m):
        print str(int(m))
    else:
        print m

for i in range(0, 5):
    try:
        if s[i] == 'a' :
            add(x[i])
        else:
            remove(x[i])
        median()
    except ValueError:
        print "Wrong!"
import random, math

# def random_data_generator (max_r):
#     for i in range(max_r):
#         yield random.randint(0, max_r)

class Node():
    def __init__(self, nombre, obj):
        self.nombre = nombre
        self.obj = obj
        self.parent = None
        self.leftChild = None
        self.rightChild = None
        self.height = 0

    def __str__(self):
        return str(self.nombre) + "(" + str(self.height) + ")"

    def is_leaf(self):
        return (self.height == 0)

    def max_children_height(self):
        if self.leftChild and self.rightChild:
            return max(self.leftChild.height, self.rightChild.height)
        elif self.leftChild and not self.rightChild:
            return self.leftChild.height
        elif not self.leftChild and self.rightChild:
            return self.rightChild.height
        else:
            return -1

    def balance (self):
            return (self.leftChild.height if self.leftChild else -1) - (self.rightChild.height if self.rightChild else -1)

class AVLTree():
    def __init__(self):
        self.rootNode = None
        self.elements_count = 0
        self.rebalance_count = 0
    def height(self):
        if self.rootNode:
            return self.rootNode.height
        else:
            return 0

    def rebalance (self, node_to_rebalance):
        self.rebalance_count += 1
        A = node_to_rebalance
        F = A.parent #allowed to be NULL
        if node_to_rebalance.balance() == -2:
            if node_to_rebalance.rightChild.balance() <= 0:
                """Rebalance, case RRC """
                B = A.rightChild
                C = B.rightChild
                assert (not A is None and not B is None and not C is None)
                A.rightChild = B.leftChild
                if A.rightChild:
                    A.rightChild.parent = A
                B.leftChild = A
                A.parent = B
                if F is None:
                    self.rootNode = B
                    self.rootNode.parent = None
                else:
                    if F.rightChild == A:
                        F.rightChild = B
                    else:
                        F.leftChild = B
                    B.parent = F
                self.recompute_heights (A)
                self.recompute_heights (B.parent)


            else:
                """Rebalance, case RLC """
                B = A.rightChild
                C = B.leftChild
                assert (not A is None and not B is None and not C is None)
                B.leftChild = C.rightChild
                if B.leftChild:
                    B.leftChild.parent = B
                A.rightChild = C.leftChild
                if A.rightChild:
                    A.rightChild.parent = A
                C.rightChild = B
                B.parent = C
                C.leftChild = A
                A.parent = C
                if F is None:
                    self.rootNode = C
                    self.rootNode.parent = None
                else:
                    if F.rightChild == A:
                        F.rightChild = C
                    else:
                        F.leftChild = C
                    C.parent = F
                self.recompute_heights (A)
                self.recompute_heights (B)


        else:
            assert(node_to_rebalance.balance() == +2)
            if node_to_rebalance.leftChild.balance() >= 0:
                B = A.leftChild
                C = B.leftChild
                """Rebalance, case LLC """
                assert (not A is None and not B is None and not C is None)
                A.leftChild = B.rightChild
                if (A.leftChild):
                    A.leftChild.parent = A
                B.rightChild = A
                A.parent = B
                if F is None:
                    self.rootNode = B
                    self.rootNode.parent = None
                else:
                    if F.rightChild == A:
                        F.rightChild = B
                    else:
                        F.leftChild = B
                    B.parent = F
                self.recompute_heights (A)
                self.recompute_heights (B.parent)
            else:
                B = A.leftChild
                C = B.rightChild
                """Rebalance, case LRC """
                assert (not A is None and not B is None and not C is None)
                A.leftChild = C.rightChild
                if A.leftChild:
                    A.leftChild.parent = A
                B.rightChild = C.leftChild
                if B.rightChild:
                    B.rightChild.parent = B
                C.leftChild = B
                B.parent = C
                C.rightChild = A
                A.parent = C
                if F is None:
                    self.rootNode = C
                    self.rootNode.parent = None
                else:
                    if (F.rightChild == A):
                        F.rightChild = C
                    else:
                        F.leftChild = C
                    C.parent = F
                self.recompute_heights (A)
                self.recompute_heights (B)

    def recompute_heights (self, start_from_node):
        changed = True
        node = start_from_node
        while node and changed:
            old_height = node.height
            node.height = (node.max_children_height() + 1 if (node.rightChild or node.leftChild) else 0)
            changed = node.height != old_height
            node = node.parent
    def add_as_child (self, parent_node, child_node):
        node_to_rebalance = None
        if child_node.id_fly < parent_node.id_fly:
            if not parent_node.leftChild:
                parent_node.leftChild = child_node
                child_node.parent = parent_node
                if parent_node.height == 0:
                    node = parent_node
                    while node:
                        node.height = node.max_children_height() + 1
                        if not node.balance () in [-1, 0, 1]:
                            node_to_rebalance = node
                            break #we need the one that is furthest from the root
                        node = node.parent
            else:
                self.add_as_child(parent_node.leftChild, child_node)
        else:
            if not parent_node.rightChild:
                parent_node.rightChild = child_node
                child_node.parent = parent_node
                if parent_node.height == 0:
                    node = parent_node
                    while node:
                        node.height = node.max_children_height() + 1
                        if not node.balance () in [-1, 0, 1]:
                            node_to_rebalance = node
                            break #we need the one that is furthest from the root
                        node = node.parent
            else:
                self.add_as_child(parent_node.rightChild, child_node)

        if node_to_rebalance:
            self.rebalance (node_to_rebalance)


    def insert (self, nombre, obj):
        new_node = Node(nombre, obj)
        if not self.rootNode:
            self.rootNode = new_node
            return True
        else:
            if not self.find(nombre):
                self.elements_count += 1
                self.add_as_child (self.rootNode, new_node)
                return True
            else:
                return False

    def find_smallest(self, start_node):
        node = start_node
        while node.leftChild:
            node = node.leftChild

    def inorder(self, node, retlst = []):
        if retlst is None:
            retlst = []
        if self.rootNode is not None:
            if node.leftChild:
                retlst = self.inorder(node.leftChild, retlst)
            retlst.append({'id_fly':node.id_fly, 'origin':node.origin, 'destiny':node.destiny, 'date_out':node.date_out, 'date_in':node.date_in, 'price_fc':node.price_fc, 'price_tc':node.price_tc, 'price_ec':node.price_ec, 'amount_fc':node.amount_fc, 'amount_tc':node.amount_tc, 'amount_ec':node.amount_ec, 'state':node.state}) #+= [node.id_fly]
            if node.rightChild:
                retlst = self.inorder(node.rightChild, retlst)
        return retlst

    def find(self, nombre):
        return self.find_in_subtree (self.rootNode, nombre )

    def searchItem(self, nombre):
        node = self.find_in_subtree (self.rootNode, nombre )
        return {'nombre': node.nombre, 'obj': node.obj}

    def update(self, nombre, obj):
        node = self.find_in_subtree(self.rootNode, nombre)
        node.nombre = nombre
        node.obj = obj
        return True

    def find_in_subtree(self, node, nombre):
        if node is None:
            return None # id_fly not found
        if nombre < node.nombre:
            return self.find_in_subtree(node.leftChild, nombre)
        elif nombre > node.nombre:
            return self.find_in_subtree(node.rightChild, nombre)
        else: # nombre is equal to node nombre
            return node


    def remove (self, nombre):
        # first find
        node = self.find(nombre)
        if not node is None:
            self.elements_count -= 1
            if node.is_leaf(): # nodo hoja se elimina
                self.remove_leaf(node)
            elif (bool(node.leftChild)) ^ (bool(node.rightChild)): # nodo es una rama con un hijo
                self.remove_branch (node)
            else: # nodo tiene 2 hijos hacer cambio
                assert (node.leftChild) and (node.rightChild)
                self.swap_with_successor_and_remove (node)


    def remove_leaf (self, node):
        parent = node.parent
        if (parent):
            if parent.leftChild == node:
                parent.leftChild = None
            else:
                assert (parent.rightChild == node)
                parent.rightChild = None
            self.recompute_heights(parent)
        else:
            self.rootNode = None
        del node
        # rebalance
        node = parent
        while (node):
            if not node.balance() in [-1, 0, 1]:
                self.rebalance(node)
            node = node.parent


    def remove_branch (self, node):
        parent = node.parent
        if (parent):
            if parent.leftChild == node:
                parent.leftChild = node.rightChild or node.leftChild
            else:
                assert (parent.rightChild == node)
                parent.rightChild = node.rightChild or node.leftChild
            if node.leftChild:
                node.leftChild.parent = parent
            else:
                assert(node.rightChild)
                node.rightChild.parent = parent
            self.recompute_heights(parent)
        del node
        # rebalance
        node = parent
        while (node):
            if not node.balance() in [-1, 0, 1]:
                self.rebalance(node)
            node = node.parent



    def swap_with_successor_and_remove (self, node):
        successor = self.find_smallest(node.rightChild)
        self.swap_nodes (node, successor)
        assert (node.leftChild is None)
        if node.height == 0:
            self.remove_leaf (node)
        else:
            self.remove_branch (node)


    def swap_nodes (self, node1, node2):
        assert (node1.height > node2.height)
        parent1 = node1.parent
        leftChild1 = node1.leftChild
        rightChild1 = node1.rightChild
        parent2 = node2.parent
        assert (not parent2 is None)
        assert (parent2.leftChild == node2 or parent2 == node1)
        leftChild2 = node2.leftChild
        assert (leftChild2 is None)
        rightChild2 = node2.rightChild

        # swap heights
        tmp = node1.height
        node1.height = node2.height
        node2.height = tmp

        if parent1:
            if parent1.leftChild == node1:
                parent1.leftChild = node2
            else:
                assert (parent1.rightChild == node1)
                parent1.rightChild = node2
            node2.parent = parent1
        else:
            self.rootNode = node2
            node2.parent = None

        node2.leftChild = leftChild1
        leftChild1.parent = node2
        node1.leftChild = leftChild2 # None
        node1.rightChild = rightChild2
        if rightChild2:
            rightChild2.parent = node1
        if not (parent2 == node1):
            node2.rightChild = rightChild1
            rightChild1.parent = node2

            parent2.leftChild = node1
            node1.parent = parent2
        else:
            node2.rightChild = node1
            node1.parent = node2

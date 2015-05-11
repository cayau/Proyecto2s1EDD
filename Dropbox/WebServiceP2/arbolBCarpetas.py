from __future__ import (nested_scopes, generators, division, absolute_import, with_statement,
                        print_function, unicode_literals)

from flask import Flask, request, render_template, json, jsonify
app = Flask(__name__)

class BTree(object):
  """A BTree implementation with search and insert functions. Capable of any order t."""

  #Inicio Node
  class Node(object):
    """A simple B-Tree Node."""

    def __init__(self, t):
      self.keys = []
      self.children = []
      self.leaf = True
      # t is the order of the parent B-Tree. Nodes need this value to define max size and splitting.
      self._t = t

    def __str__(self):
      cadena=str(self.keys)
      cadena2=str(self.children)
      cadena3 = cadena + cadena2
      return cadena3

    def split(self, parent, payload):
      """Split a node and reassign keys/children."""
      new_node = self.__class__(self._t)

      mid_point = self.size//2
      split_value = self.keys[mid_point]
      parent.add_key(split_value)

      # Add keys and children to appropriate nodes
      new_node.children = self.children[mid_point + 1:]
      self.children = self.children[:mid_point + 1]
      new_node.keys = self.keys[mid_point+1:]
      self.keys = self.keys[:mid_point]

      # If the new_node has children, set it as internal node
      if len(new_node.children) > 0:
        new_node.leaf = False

      parent.children = parent.add_child(new_node)
      if payload < split_value:
        return self
      else:
        return new_node

    @property
    def _is_full(self):
      ###################cambio estaba return self.size == 2 * self._t - 1 se convierte a return self.size == self._t - 1
      return self.size ==  self._t - 1

    @property
    def size(self):
      return len(self.keys)

    def add_key(self, value):
      """Add a key to a node. The node will have room for the key by definition."""
      self.keys.append(value)
      self.keys.sort()

    def add_child(self, new_node):
      """
      Add a child to a node. This will sort the node's children, allowing for children
      to be ordered even after middle nodes are split.

      returns: an order list of child nodes
      """
      i = len(self.children) - 1
      while i >= 0 and self.children[i].keys[0] > new_node.keys[0]:
        i -= 1
      return self.children[:i + 1]+ [new_node] + self.children[i + 1:]
   #Fin Node




##inicio def B-tree
  def __init__(self, t):
    """
    Create the B-tree. t is the order of the tree. Tree has no keys when created.
    This implementation allows duplicate key values, although that hasn't been checked
    strenuously.
    """
    self.codGraph = "digraph arbol{\n"
    self._t = t
    if self._t <= 1:
      raise ValueError("B-Tree must have a degree of 2 or more.")
    self.root = self.Node(t)


  def insertar(self, payload):
    """Insert a new key of value payload into the B-Tree."""
    node = self.root
    # Root is handled explicitly since it requires creating 2 new nodes instead of the usual one.
    if node._is_full:
      new_root = self.Node(self._t)
      new_root.children.append(self.root)
      new_root.leaf = False
      # node is being set to the node containing the ranges we want for payload insertion.
      node = node.split(new_root, payload)
      self.root = new_root
    while not node.leaf:
      i = node.size - 1
      while i > 0 and payload < node.keys[i] :
        i -= 1
      if payload > node.keys[i]:
        i += 1

      next = node.children[i]
      if next._is_full:
        node = next.split(node, payload)
      else:
        node = next
    # Since we split all full nodes on the way down, we can simply insert the payload in the leaf.
    node.add_key(payload)

  def search(self, value, node=None):
    """Return True if the B-Tree contains a key that matches the value."""
    if node is None:
      node = self.root
    if value in node.keys:
      return True
    elif node.leaf:
      # If we are in a leaf, there is no more to check.
      return False
    else:
      i = 0
      while i < node.size and value > node.keys[i]:
        i += 1
      return self.search(value, node.children[i])

  def getDot(self):
    dot = "digraph g { node [shape=record];"
    """Print an level-order representation."""
    this_level = [self.root]
    nivel=0
    while this_level:
      next_level = []
      output = ""
      pagina=0
      for node in this_level:
        if node.children:
          next_level.extend(node.children)

        i = 0
        aux = len(node.keys)
        for i in range(0,aux):
          if(i==0):output += "Nodo%d_%d[label=\"<P0>" %(nivel, pagina)
          output = output +"|"+ str(node.keys[i]) + "|<P%d>"% (i+1)
          if(i==aux-1):output += "\"]; "

        pagina += 1
      print(output)
      dot += output
      this_level = next_level
      nivel += 1

    """Print an level-order representation."""
    this_level = [self.root]
    nivel=0
    while this_level:
      next_level = []
      output = ""
      pagina=0
      aux2 = 0
      for node in this_level:
        if node.children:
          next_level.extend(node.children)

        i = 0
        aux = len(node.children)
        for i in range(0,aux):
          output += "Nodo%d_%d:P%d -> Nodo%d_%d; " %(nivel, pagina, i, nivel+1, aux2)
          aux2 +=1

        pagina += 1

      print(output)
      dot += output
      this_level = next_level
      nivel += 1

    dot += "}"
    print(dot)
    return dot

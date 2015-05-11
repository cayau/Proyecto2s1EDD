from arbolAVLArchivos import AVLTree
from arbolBCarpetas import BTree


class NodoRoot():
    def __init__(self):
        self.nombre = '/'
        self.archivos = AVLTree()
        self.carpetas = BTree(5)


class NodoUser(object):
    def __init__(self, cor, con, prev, next):
        self.correo = cor
        self.contrasena = con
        self.prev = prev
        self.next = next
        self.root = NodoRoot()


class DoubleListUser(object):
    head = None
    tail = None

    def append(self, cor, con):
        new_node = NodoUser(cor, con, None, None)
        if self.head is None:
            self.head = self.tail = new_node
            return True
        else:
            if not self.dat(cor):
                new_node.prev = self.tail
                new_node.next = None
                self.tail.next = new_node
                self.tail = new_node
                return True
            else:
                return False

    def remove(self, node_value):
        current_node = self.head

        while current_node is not None:
            if current_node.correo == node_value:
                # if it's not the first element
                if current_node.prev is not None:
                    current_node.prev.next = current_node.next
                    current_node.next.prev = current_node.prev
                else:
                    # otherwise we have no prev (it's None), head is the next one, and prev becomes None
                    self.head = current_node.next
                    current_node.next.prev = None

            current_node = current_node.next

    def show(self):
        current_node = self.head
        users = []
        while current_node is not None:
            users.append({'correo': current_node.correo, 'contra': current_node.contrasena})
            current_node = current_node.next
        return users

    def dat(self, node_value):
        encontrado = "false"
        current_node = self.head
        # print("Showing complete data from selected airport:")

        while current_node is not None and encontrado != "true":

            if current_node.correo == node_value:
                # print('aeropuerto encontrado')
                # print(current_node.identificador + " " +  current_node.nombre + " " +current_node.pais + " " + str(current_node.contrasena) )
                encontrado = "true"
                return True
            else:
                if current_node.next is None and encontrado != "true":
                    # print ("aeropuerto no encontrado")
                    return False

            current_node = current_node.next

    def getDot(self):
        dot = 'digraph g { node [shape=record]; rankdir=LR;'
        current_node = self.head
        i = 0
        while current_node is not None:
            dot += str('Nodo%d[label="<P0>|\'' + current_node.correo + '\'|<P1>"]; ') % (i)
            if (current_node.prev != None): dot += 'Nodo%d:P0 -> Nodo%d; ' % (i, i - 1)
            if (current_node.next != None): dot += 'Nodo%d:P1 -> Nodo%d; ' % (i, i + 1)
            dot += 'NodoRoot%d[label="root"]; '%(i)
            dot += 'Nodo%d -> NodoRoot%d; '%(i, i)
            current_node = current_node.next
            i += 1
        dot += '}'
        return dot
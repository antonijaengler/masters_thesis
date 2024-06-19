import string


class Node:
    def __init__(self, id: int = 0, s: float = 0, x: float = 0, y: float = 0, nodetype: string = "B", angle: float = 0, length: float = 0.0):  # used to be "A" type for the axiom
        self.id = id
        self.s = s
        self.x = x
        self.y = y
        self.nodetype = nodetype
        self.angle = angle
        self.length = length
        self.children = []
        self.junction = False

    def addChild(self, child):
        self.children.append(child)

    def printNode(self):
        return f'Node ' + self.nodetype + '(' + str(self.id) + ')' + ' at position (' + str(self.x) + ', ' + str(self.y) + ') heading ' + str(self.angle)


class Tree:
    def __init__(self, root: Node = None):
        self.root = root

    def printTree(self):
        return self.printTreeRecursive(self.root)

    def printTreeRecursive(self, node, level=0):
        if node is not None:
            print("  " * level + node.printNode())
            for child in node.children:
                self.printTreeRecursive(child, level + 1)

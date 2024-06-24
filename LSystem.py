import Tree
import math
import random


class LSystemGenerator:
    def __init__(self, rules, axiom, iterlimit: int = 1):
        self.rules = rules
        self.axiom = axiom
        self.iterlimit = iterlimit
        self.counter = 1

    def applyRules(self, node):
        randomrule = self.rules[random.randrange(0, len(self.rules))]
        changeangle = 180 / randomrule.spawncount
        #print(randomrule.printRule())
        if node.nodetype == randomrule.matchnodetype:
            node.nodetype = randomrule.changetotype
            node.length = randomrule.length
            for i in range(0, randomrule.spawncount):
                new_angle = randomrule.angle + node.angle
                new_x = randomrule.length * round(math.cos(math.radians(new_angle)), 15)
                new_y = randomrule.length * round(math.sin(math.radians(new_angle)), 15)
                newnode = Tree.Node(self.counter, 0, node.x + new_x, node.y + new_y, randomrule.spawntype, new_angle)
                node.addChild(newnode)
                randomrule.angle = randomrule.angle - changeangle
                self.counter += 1
            randomrule.angle += randomrule.spawncount * changeangle

    def processNode(self, node):
        for child in node.children:
            self.processNode(child)
        self.applyRules(node)
        return node

    def generateTree(self):
        start = self.axiom

        for iteration in range(0, self.iterlimit + 1):
            start = self.processNode(start)

        result = Tree.Tree(start)

        return result

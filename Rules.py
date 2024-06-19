import string


class Rule:
    def __init__(self, matchnodetype: string = "B", changetotype: string = "C", spawntype: string = "B", spawncount: int = 1, length: float = 1.0, angle: float = 0):  # used to be "A" for the axiom
        self.matchnodetype = matchnodetype
        self.changetotype = changetotype
        self.spawntype = spawntype
        self.spawncount = spawncount
        self.length = length
        self.angle = angle

    def printRule(self):
        return f'Found node type ' + self.matchnodetype + ', changed to ' + self.changetotype + '. ' \
                'Spawned node type ' + self.spawntype + ' ' + str(self.spawncount) + ' times with length: ' + str(self.length) + \
               ' and angle: ' + str(self.angle)


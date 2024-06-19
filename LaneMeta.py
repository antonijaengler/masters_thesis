class LaneOffset:
    def __init__(self, s, a, b, c, d):
        self.s = s
        self.a = a
        self.b = b
        self.c = c
        self.d = d

    def printSection(self, level):
        return level * "    " + f'<laneOffset s="{self.s}" a="{self.a}" b="{self.b}" c="{self.c}" d="{self.d}"/>\n'


class LaneSection:
    def __init__(self, s, lanes):
        self.s = s
        if lanes is not None:
            self.list_of_lanes = lanes
        else:
            self.list_of_lanes = []

    def printBegin(self, level):
        return level * "    " + f'<laneSection s="{self.s}">\n'

    def printEnd(self, level):
        return level * "    " + f'</laneSection>\n'

    def printSection(self, level):
        returnstring = self.printBegin(level)
        for lanes in self.list_of_lanes:
            returnstring += lanes.printLane(level + 1)
        returnstring += self.printEnd(level)

        return returnstring

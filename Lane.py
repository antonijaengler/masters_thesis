class Lane:
    def __init__(self, id, type, level, width, links=None):
        self.id = id
        self.type = type
        self.level = level
        self.width = width
        if links is None:
            self.links = []
        else:
            self.links = links

    def printBegin(self, level):
        return level * "    " + f'<lane id="{self.id}" type="{self.type}" level="{self.level}">\n'

    def printEnd(self, level):
        return level * "    " + f'</lane>\n'

    def printLane(self, level):
        returnstring = self.printBegin(level)
        for link in self.links:
            returnstring += self.links.printLink(level + 1)
        if self.width is not None:
            returnstring += self.width.printWidth(level + 1)
        returnstring += self.printEnd(level)
        return returnstring


class LeftLane:
    def __init__(self, lanes=None):
        self.lanes = lanes

    def printBegin(self, level):
        return level * "    " + f'<left>\n'

    def printEnd(self, level):
        return level * "    " + f'</left>\n'

    def printLane(self, level):
        returnstring = self.printBegin(level)
        for lane in self.lanes:
            returnstring += lane.printLane(level + 1)
        returnstring += self.printEnd(level)
        return returnstring


class CenterLane:
    def __init__(self, lanes=None):
        self.lanes = lanes

    def printBegin(self, level):
        return level * "    " + f'<center>\n'

    def printEnd(self, level):
        return level * "    " + f'</center>\n'

    def printLane(self, level):
        returnstring = self.printBegin(level)
        for lane in self.lanes:
            returnstring += lane.printLane(level + 1)
        returnstring += self.printEnd(level)
        return returnstring


class RightLane:
    def __init__(self, lanes=None):
        self.lanes = lanes

    def printBegin(self, level):
        return level * "    " + f'<right>\n'

    def printEnd(self, level):
        return level * "    " + f'</right>\n'

    def printLane(self, level):
        returnstring = self.printBegin(level)
        for lane in self.lanes:
            returnstring += lane.printLane(level + 1)
        returnstring += self.printEnd(level)
        return returnstring


class Lanes:
    def __init__(self, lanesections=None):
        if lanesections is not None:
            self.lanesections = lanesections
        else:
            self.lanesections = []

    def printBegin(self, level):
        return level * "    " + f'<lanes>\n'

    def printEnd(self, level):
        return level * "    " + f'</lanes>\n'

    def printLanes(self, level):
        returnstring = self.printBegin(level)
        for lanesection in self.lanesections:
            returnstring += lanesection.printSection(level + 1)
        returnstring += self.printEnd(level)
        return returnstring

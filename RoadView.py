# important for rendering!! without doesn't work

class PlanView:
    def __init__(self, geometries):
        if geometries is not None:
            self.geometries = geometries
        else:
            self.geometries = []

    def printBegin(self, level):
        return level * "    " + f'<planView>\n'

    def printEnd(self, level):
        return level * "    " + f'</planView>\n'

    def printView(self, level):
        returnstring = self.printBegin(level)
        for geometry in self.geometries:
            returnstring += geometry.printGeometry(level + 1)
        returnstring += self.printEnd(level)

        return returnstring


class Geometry:
    def __init__(self, s, x, y, hdg, length, line=None, arc=None):
        self.s = s
        self.x = x
        self.y = y
        self.hdg = hdg
        self.length = length
        self.line = line
        self.arc = arc

    def setLength(self, length):
        self.length = length

    def printBegin(self, level):
        return level * "    " + f'<geometry s="{round(self.s, 1)}" x="{self.x}" y="{self.y}" hdg="{self.hdg}" length="{self.length}">\n'

    def printEnd(self, level):
        return level * "    " + f'</geometry>\n'

    def printGeometry(self, level):
        returnstring = self.printBegin(level)
        if self.line is not None:
            returnstring += self.line.printLine(level + 1)
        if self.arc is not None:
            returnstring += self.arc.printArc(level + 1)
        returnstring += self.printEnd(level)

        return returnstring


class Line:
    def __init__(self):
        pass

    def printLine(self, level):
        return level * "    " + f'<line/>\n'


class Arc:
    def __init__(self, curvature: float):
        self.curvature = curvature

    def printArc(self, level):
        return level * "\t" + f'<arc curvature="{self.curvature}"/>\n'


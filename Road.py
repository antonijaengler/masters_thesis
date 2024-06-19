class Road():
    def __init__(self, name, lenght, id, junction, lanes, view, links):
        self.name = name
        self.length = lenght
        self.id = id
        self.junction = junction # -1 if it doesn't belong to any junction
        if links is not None:
            self.links = links
        else:
            self.links = None
        self.lanes_element = lanes
        self.view = view

    def printBegin(self, level):
        return level * "    " + f'<road name="{self.name}" length="{self.length}" id="{self.id}" junction="{self.junction}">\n'

    def printEnd(self, level):
        return level * "    " + f'</road>\n'

    def printRoad(self, level):
        returnstring = self.printBegin(level)
        for link in self.links:
            returnstring += link.printLink(level + 1)
        if self.view is not None:
            returnstring += self.view.printView(level + 1)
        for lanes in self.lanes_element:
            returnstring += lanes.printLanes(level + 1)
        returnstring += self.printEnd(level)

        return returnstring

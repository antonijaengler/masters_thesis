class OpenDRIVE:
    def __init__(self, roads, junctions):
        self.roads = roads
        self.junctions = junctions

    def addRoad(self, road):
        self.roads.append(road)

    def addJunction(self, junction):
        self.junctions.append(junction)

    def printBegin(self):
        return f'<OpenDRIVE>\n'

    def printEnd(self):
        return f'</OpenDRIVE>\n'

    def printOpenDrive(self):
        returnstring = self.printBegin()
        for road in self.roads:
            returnstring += road.printRoad(1)
        for junction in self.junctions:
            returnstring += junction.printJunction(1)
        returnstring += self.printEnd()

        return returnstring

class Junction:
    def __init__(self, id, name, connections):
        self.id = id
        self.name = name
        if connections is None:
            self.connections = []
        else:
            self.connections = connections

    def addConnection(self, connection):
        self.connections.append(connection)

    def printBegin(self, level):
        return level * "    " + f'<junction id="' + str(self.id) + '" name="' + self.name + '">\n'

    def printEnd(self, level):
        return level * "    " + f'</junction>\n'

    def printJunction(self, level):
        returnstring = self.printBegin(level)
        for connection in self.connections:
            returnstring += connection.printConnection(level + 1)
        returnstring += self.printEnd(level)

        return returnstring


class Connection:
    def __init__(self, id, incomingRoad, connectingRoad, contactPoint, lanelinks):
        self.id = id
        self.incomingRoad = incomingRoad
        self.connectingRoad = connectingRoad
        self.contactPoint = contactPoint
        if lanelinks is None:
            self.lanelinks = []
        else:
            self.lanelinks = lanelinks

    def printBegin(self, level):
        return level * "    " + f'<connection id="' + str(self.id) + '" incomingRoad="' + str(self.incomingRoad) + \
               '" connectingRoad="' + str(self.connectingRoad) + '" contactPoint="' + self.contactPoint + '">\n'

    def printEnd(self, level):
        return level * "    " + f'</connection>\n'

    def printConnection(self, level):
        returnstring = self.printBegin(level)
        for lanelink in self.lanelinks:
            returnstring += lanelink.printLaneLink(level + 1)
        returnstring += self.printEnd(level)
        return returnstring


class LaneLink:
    def __init__(self, fromnode, tonode):
        self.fromnode = fromnode
        self.tonode = tonode

    def printLaneLink(self, level):
        return level * "    " + f'<laneLink from="' + str(self.fromnode) + '" to="' + str(self.tonode) + '"/>\n'

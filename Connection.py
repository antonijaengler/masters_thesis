class Link:
    def __init__(self, predecessors=None, successors=None):
        if predecessors is not None:
            self.predecessors = predecessors
        else:
            self.predecessors = []
        if successors is not None:
            self.successors = successors
        else:
            self.successors = []

    def addPredecessor(self, predecessor):
        self.predecessors.append(predecessor)

    def addSuccessor(self, successor):
        self.successors.append(successor)

    def printBegin(self, level):
        return level * "    " + f'<link>\n'

    def printEnd(self, level):
        return level * "    " + f'</link>\n'

    def printLink(self, level):
        returnstring = self.printBegin(level)
        for predecessor in self.predecessors:
            returnstring += predecessor.printPredecessor(level + 1)
        for successor in self.successors:
            returnstring += successor.printSuccessor(level + 1)
        returnstring += self.printEnd(level)

        return returnstring


class Predecessor:
    def __init__(self, elemenetType, elementId, contactPoint):
        self.elementType = elemenetType
        self.elementId = elementId
        self.contactPoint = contactPoint

    def printPredecessor(self, level):
        if self.elementType is not None and self.contactPoint is not None:
            text = level * "    " + f'<predecessor elementType="{self.elementType}" elementId="{self.elementId}" ' \
                                f'contactPoint="{self.contactPoint}"/>\n'
        else:
            text = level * "    " + f'<predecessor id="{self.elementId}"/>\n'
        return text


class Successor:
    def __init__(self, elementType, elementId, contactPoint):
        self.elementType = elementType
        self.elementId = elementId
        self.contactPoint = contactPoint

    def printSuccessor(self, level):
        if self.elementType is not None and self.contactPoint is not None:
            text = level * "    " + f'<successor elementType="{self.elementType}" elementId="{self.elementId}" contactPoint="{self.contactPoint}"/>\n'
        else:
            text = level * "    " + f'<successor id="{self.elementId}"/>\n'
        return text

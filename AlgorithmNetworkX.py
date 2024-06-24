import Rules
import LSystem
import Tree
import RoadView
import Road
import OpenDRIVE
import Connection
import math
from itertools import combinations
import networkx
import matplotlib.pyplot as plt
import Graph
import Width
import Lane
import LaneMeta
import ConnectRoads
import time


def calculateCircle(t1, t2, alpha, node):
    distance = math.sqrt(math.pow(t2[0] - t1[0], 2) + math.pow(t2[1] - t1[1], 2))
    radius = (distance / 2) / (math.sin(alpha / 2))
    a = [(t2[0] - t1[0]) / 2, (t2[1] - t1[1]) / 2]
    distance_a = math.sqrt(math.pow(a[0], 2) + math.pow(a[1], 2))
    t0 = [t1[0] + a[0], t1[1] + a[1]]
    distance_b = math.sqrt(math.pow(radius, 2) - math.pow(distance_a, 2))
    center1 = [t0[0] - (distance_b * a[1]) / distance_a, t0[1] + (distance_b * a[0]) / distance_a]
    center2 = [t0[0] + (distance_b * a[1]) / distance_a, t0[1] - (distance_b * a[0]) / distance_a]
    distance_1 = math.sqrt(math.pow(center1[0] - node.x, 2) + math.pow(center1[1] - node.y, 2))
    distance_2 = math.sqrt(math.pow(center2[0] - node.x, 2) + math.pow(center2[1] - node.y, 2))
    if distance_1 < distance_2:
        center = center2
    else:
        center = center1

    return [center, radius]


def anglethreepoints(start, middle, end):
    a = math.sqrt(math.pow(end[0] - middle[0], 2) + math.pow(end[1] - middle[1], 2))
    b = math.sqrt(math.pow(start[0] - middle[0], 2) + math.pow(start[1] - middle[1], 2))
    c = math.sqrt(math.pow(end[0] - start[0], 2) + math.pow(end[1] - start[1], 2))

    alfa = math.acos((math.pow(a, 2) + math.pow(b, 2) - math.pow(c, 2)) / (2 * a * b))

    return alfa


def checkCollinear(point1, point2, point3):
    x1, y1 = point1
    x2, y2 = point2
    x3, y3 = point3

    # Calculate slopes
    slope1 = (y2 - y1) / (x2 - x1) if x2 - x1 != 0 else float('inf')
    slope2 = (y3 - y2) / (x3 - x2) if x3 - x2 != 0 else float('inf')

    # check if slopes are equal (or both infinite, indicating vertical line)
    if math.isnan(abs(slope1 - slope2)):
        return True
    else:
        return abs(slope1 - slope2) < 1e-10


def generateJunctionMesh(graph, opendrive):
    # find max id of edges
    counter = max([graph_network.edges[e]["id"] for e in graph_network.edges]) + 1
    numoflanes = 2

    # iterate through graph vertices
    for node in graph.nodes:
        # check if it is a junction
        if node.junction:
            junction = ConnectRoads.Junction(node.id, "junction" + str(node.id), None)
            index = 0
            # create roads between neighbouring vertices
            for neighbours in combinations(graph.edges([node]), 2):
                #print("Neighbours:", (neighbours[0][0].x, neighbours[0][0].y), (neighbours[0][1].x, neighbours[0][1].y),
                      #"\t", (neighbours[1][0].x, neighbours[1][0].y), (neighbours[1][1].x, neighbours[1][1].y))

                # calculate length and direction for the first edge
                length1 = math.sqrt(math.pow((neighbours[0][1].x - node.x), 2) + math.pow((neighbours[0][1].y - node.y), 2))
                direction1 = [(neighbours[0][1].x - node.x) / length1,
                             (neighbours[0][1].y - node.y) / length1]  # normalized

                # calculate length and direction for the second edge
                length2 = math.sqrt(math.pow((neighbours[1][1].x - node.x), 2) + math.pow((neighbours[1][1].y - node.y), 2))
                direction2 = [(neighbours[1][1].x - node.x) / length2,
                              (neighbours[1][1].y - node.y) / length2]  # normalized

                # calculate start and end of the road
                start = [node.x + 5 * direction1[0], node.y + 5 * direction1[1]]
                end = [node.x + 5 * direction2[0], node.y + 5 * direction2[1]]

                print("I'm at", start, "&", end, "with middle", [node.x, node.y])
                # check if it's a line or an arc
                if checkCollinear(start, [node.x, node.y], end):
                    print("These points are collinear!")
                    # calculate heading
                    heading = math.atan2((end[1] - start[1]), (end[0] - start[0]))

                    # calculate distance
                    distance = math.sqrt(math.pow(end[0] - start[0], 2) + math.pow(end[1] - start[1], 2))

                    # define geometry
                    line = RoadView.Line()
                    geometry1 = RoadView.Geometry(0.0, start[0], start[1], heading, distance, line)

                    length = distance
                else:
                    # calculate angle under which the lines intersect
                    alpha = math.pi - anglethreepoints(start, [node.x, node.y], end)
                    print("Angle is", alpha)

                    # calculate curvature for arc part of the road
                    center, radius = calculateCircle(start, end, alpha, node)
                    print("Starting curve at:", start, ", ending curve at:", end, ", middle at:", [node.x, node.y])
                    distancecurve = radius * alpha
                    curvature = 1 / radius

                    # calculate heading
                    heading = math.atan2((node.y - start[1]), (node.x - start[0]))
                    print("\tCenter of the curve is", center, "with heading=", heading)

                    # check if the turn is left or right
                    turn = (node.x - start[0]) * (end[1] - start[1]) - (node.y - start[1]) * (end[0] - start[0])
                    if turn < 0:
                        curvature = -curvature

                    # define geometry
                    arc = RoadView.Arc(curvature)
                    geometry1 = RoadView.Geometry(0.0, start[0], start[1], heading, distancecurve, arc=arc)

                    length = distancecurve

                # define lanes
                width = Width.Width(0.0, 4.0, 0.0, 0.0, 0.0)
                drivingLane = Lane.Lane(1, "driving", "false", width)
                leftLane = Lane.LeftLane([drivingLane])

                referenceLane = Lane.Lane(0, "none", "false", None)
                centerLane = Lane.CenterLane([referenceLane])

                drivingLane1 = Lane.Lane(-1, "driving", "false", width)
                rightLane = Lane.RightLane([drivingLane1])

                laneSection = LaneMeta.LaneSection(0.0, [leftLane, centerLane, rightLane])
                laneOffset = LaneMeta.LaneOffset(0.0, 0.0, 0.0, 0.0, 0.0)
                lanes = Lane.Lanes([laneOffset, laneSection])
                planView = RoadView.PlanView([geometry1])

                # define relationships
                link = Connection.Link()
                predecessor = Connection.Predecessor("road", graph.edges[neighbours[0]]['id'], "end")  #ili obrnuto??
                link.addPredecessor(predecessor)

                successor = Connection.Successor("road", graph.edges[neighbours[1]]['id'], "start")
                link.addSuccessor(successor)

                # for each lane
                innerlink1 = Connection.Link()
                predlink1 = Connection.Predecessor(None, 1, None)
                innerlink1.addPredecessor(predlink1)
                succlink1 = Connection.Successor(None, 1, None)
                innerlink1.addSuccessor(succlink1)
                drivingLane.addLink(innerlink1)

                innerlink_1 = Connection.Link()
                predlink_1 = Connection.Predecessor(None, -1, None)
                innerlink_1.addPredecessor(predlink_1)
                succlink_1 = Connection.Successor(None, -1, None)
                innerlink_1.addSuccessor(succlink_1)
                drivingLane1.addLink(innerlink_1)

                if length < 0:
                    print("Road length in junction:", length)
                    print("------------------------------------")
                road = Road.Road("Road " + str(counter), length, counter, node.id, [lanes], planView, [link])

                opendrive.addRoad(road)

                # create junction
                lanelink1 = ConnectRoads.LaneLink(1, 1)
                lanelink2 = ConnectRoads.LaneLink(-1, -1)

                connection1 = ConnectRoads.Connection(index, graph.edges[neighbours[0]]['id'], counter, "end", [lanelink1, lanelink2])
                connection2 = ConnectRoads.Connection(index + 1, graph.edges[neighbours[1]]['id'], counter, "end", [lanelink1, lanelink2])
                index += 2

                junction.addConnection(connection1)
                junction.addConnection(connection2)

                counter += 1

            opendrive.addJunction(junction)


def generateMesh(graph):
    opendrive = OpenDRIVE.OpenDRIVE([], [])

    # iterate through graph edges
    for edge in graph.edges:
        firstNode, secondNode = edge
        print("Processing edge:", graph.edges[edge]['id'], " = (", firstNode.id, "{", graph.degree[firstNode], "}", ",", secondNode.id, "{", graph.degree[secondNode], "}", ")")

        # process road segment
        line = RoadView.Line()
        x = firstNode.x
        y = firstNode.y
        length = math.sqrt(math.pow(secondNode.x - firstNode.x, 2) + math.pow(secondNode.y - firstNode.y, 2))
        print("Before junction road is long: ", length)
        if length < 1:
            print("\tFirst node:", x, y)
            print("\tSecond node:", secondNode.x, secondNode.y)
            print("---------------------------------------------------")
        direction = [(secondNode.x - firstNode.x) / length, (secondNode.y - firstNode.y) / length]  # normalized
        heading = math.atan2(direction[1], direction[0])
        print("Road is at angle", math.degrees(heading))

        # see if there is a junction on both sides of the edge
        if firstNode.junction:
            # move start of the road for 5 meters
            x = firstNode.x + 5 * direction[0]
            y = firstNode.y + 5 * direction[1]
            #print("Junction on node (", firstNode.id, ") :",  x, y)
            length -= 5
        if secondNode.junction:
            # move end of the road for 5 meters
            secondJunctionX = secondNode.x + 5 * direction[0]
            secondJunctionY = secondNode.y + 5 * direction[1]
            #print("Junction on node (", secondNode.id, ") :", secondJunctionX, secondJunctionY)
            length -= 5

        print("Road is long: ", length)
        geometry = RoadView.Geometry(firstNode.s, x, y, heading, length, line=line)  # firstNode.length, math.radians(secondNode.angle)
        width1 = Width.Width(0.0, 2.9e-1, 0.0, 0.0, 0.0)
        shoulderLane = Lane.Lane(2, "shoulder", "false", width1)
        width = Width.Width(0.0, 4.0, 0.0, 0.0, 0.0)
        drivingLane = Lane.Lane(1, "driving", "false", width)
        leftLane = Lane.LeftLane([shoulderLane, drivingLane])

        referenceLane = Lane.Lane(0, "none", "false", None)
        centerLane = Lane.CenterLane([referenceLane])

        width1 = Width.Width(0.0, 2.9e-1, 0.0, 0.0, 0.0)
        shoulderLane1 = Lane.Lane(-2, "shoulder", "false", width1)
        drivingLane1 = Lane.Lane(-1, "driving", "false", width)
        rightLane = Lane.RightLane([shoulderLane1, drivingLane1])

        laneSection = LaneMeta.LaneSection(0.0, [leftLane, centerLane, rightLane])
        laneOffset = LaneMeta.LaneOffset(0.0, 0.0, 0.0, 0.0, 0.0)
        lanes = Lane.Lanes([laneOffset, laneSection])
        planView = RoadView.PlanView([geometry])
        link = Connection.Link()
        lanelink1 = Connection.Link()
        lanelink2 = Connection.Link()
        lanelink_1 = Connection.Link()
        lanelink_2 = Connection.Link()

        # predecessors
        if firstNode.junction:
            predecessortype = "junction"
            predecessorconntactpoint = "start"
            predecessor = Connection.Predecessor(predecessortype, firstNode.id,
                                                 predecessorconntactpoint)
            link.addPredecessor(predecessor)
        else:
            for key in graph.adj[firstNode]:
                if key != secondNode:
                    predecessortype = "road"
                    predecessorconntactpoint = "end"
                    predecessor = Connection.Predecessor(predecessortype, graph.edges[firstNode, key]['id'], predecessorconntactpoint)
                    link.addPredecessor(predecessor)

                    # for every lane
                    predlink1 = Connection.Predecessor(None, 1, None)
                    lanelink1.addPredecessor(predlink1)
                    drivingLane.addLink(lanelink1)
                    predlink2 = Connection.Predecessor(None, 2, None)
                    lanelink2.addPredecessor(predlink2)
                    shoulderLane.addLink(lanelink2)
                    predlink_1 = Connection.Predecessor(None, -1, None)
                    lanelink_1.addPredecessor(predlink_1)
                    drivingLane1.addLink(lanelink_1)
                    predlink_2 = Connection.Predecessor(None, -2, None)
                    lanelink_2.addPredecessor(predlink_2)
                    shoulderLane1.addLink(lanelink_2)

        # successors
        if secondNode.junction:
            successortype = "junction"
            successorcontactpoint = "start"
            successor = Connection.Successor(successortype, secondNode.id, successorcontactpoint)
            link.addSuccessor(successor)
        else:
            for key in graph.adj[secondNode]:
                if key != firstNode:
                    successortype = "road"
                    successorcontactpoint = "start"
                    successor = Connection.Successor(successortype, graph.edges[secondNode, key]['id'], successorcontactpoint)
                    link.addSuccessor(successor)

                    # for every lane
                    succlink1 = Connection.Successor(None, 1, None)
                    lanelink1.addSuccessor(succlink1)
                    drivingLane.addLink(lanelink1)
                    succlink2 = Connection.Successor(None, 2, None)
                    lanelink2.addSuccessor(succlink2)
                    shoulderLane.addLink(lanelink2)
                    succlink_1 = Connection.Successor(None, -1, None)
                    lanelink_1.addSuccessor(succlink_1)
                    drivingLane1.addLink(lanelink_1)
                    succlink_2 = Connection.Successor(None, -2, None)
                    lanelink_2.addSuccessor(succlink_2)
                    shoulderLane1.addLink(lanelink_2)

        road = Road.Road("Road " + str(graph.edges[edge]['id']), length, graph.edges[edge]['id'], -1, [lanes], planView, [link])

        opendrive.addRoad(road)

    generateJunctionMesh(graph, opendrive)

    f = open("test2.xodr", "w")
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    f.write(opendrive.printOpenDrive())
    f.close()


if __name__ == '__main__':
    start_time = time.time()

    rule1 = Rules.Rule(length=100)
    rule2 = Rules.Rule("B", "C", "B", 2, 100, 90)
    rule3 = Rules.Rule("B", "C", "B", 3, 60, 20)
    rule4 = Rules.Rule("D", "C", "B", 2, 70, 70)
    rule5 = Rules.Rule("B", "C", "B", 2, 40, 90)

    root = Tree.Node()

    iterationlimit = 10

    generator = LSystem.LSystemGenerator([rule1, rule2], root, iterationlimit)
    tree = generator.generateTree()

    tree.printTree()

    graph = Graph.Graph()
    graph_network = graph.generateGraph(node=tree.root)
    networkx.draw(graph_network, pos=graph.getNodePositions(graph_network), node_color='red')
    graph.removeCloseNodes(graph_network, 20)
    print("Resulting nodes:", [n.id for n in graph_network.nodes])
    graph.solveIntersections(graph_network)
    print("Resulting edges:", [graph_network.edges[e]["id"] for e in graph_network.edges])
    print("Resulting nodes:", [n.id for n in graph_network.nodes])
    networkx.draw(graph_network, pos=graph.getNodePositions(graph_network), node_color='blue')
    graph.checkJunction(graph_network)

    generateMesh(graph_network)

    print("--- %s seconds ---" % (time.time() - start_time))

    plt.show()
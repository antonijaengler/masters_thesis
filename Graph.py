import math
import networkx
import Tree


class Graph:
    def __init__(self):
        self.counter = 0

    def generateGraph(self, node):
        graph = networkx.Graph()

        def generateGraphRecursive(node):
            graph.add_node(node)
            for child in node.children:
                graph.add_edge(node, child, id=self.counter)
                self.counter += 1
                generateGraphRecursive(child)

        generateGraphRecursive(node)

        return graph

    def getNodePositions(self, graph):
        positions = {}
        for node in graph.nodes:
            positions[node] = (node.x, node.y)

        return positions

    def checkJunction(self, graph):
        for node in graph.nodes:
            if graph.degree[node] >= 3:
                node.junction = True

    def solveIntersections(self, graph):
        print("Solving...")
        edges = list(graph.edges)
        nodesToAdd = {}
        for edge in graph.edges:
            edges.remove(edge)
            node1, node2 = edge
            for otheredge in edges:
                node3, node4 = otheredge
                D = (node2.x - node1.x) * (node3.y - node4.y) - (node3.x - node4.x) * (node2.y - node1.y)
                if D != 0:  # if they are not parallel, make new node
                    Ds = (node3.x - node1.x) * (node3.y - node4.y) - (node3.x - node4.x) * (node3.y - node1.y)
                    Dt = (node2.x - node1.x) * (node3.y - node1.y) - (node3.x - node1.x) * (node2.y - node1.y)
                    s = Ds / D
                    t = Dt / D
                    print("Making new node between", (node1.x, node1.y), ",", (node2.x, node2.y),
                          "and", (node3.x, node3.y), ",", (node4.x, node4.y))
                    if 0 <= s <= 1 and 0 <= t <= 1:
                        newx = node1.x + s * (node2.x - node1.x)
                        newy = node1.y + s * (node2.y - node1.y)
                        existingnode = [(abs(newx - n.x) > 1e-10, abs(newy - n.y) > 1e-10) for n in graph.nodes]
                        #print("New node", (newx, newy), ":", all(all(nodes) for nodes in existingnode))
                        if all(all(nodes) for nodes in existingnode):
                            newnode = Tree.Node(int(str(graph.edges[edge]["id"]) + str(graph.edges[otheredge]["id"])),
                                                0, newx, newy)
                            nodesToAdd[newnode] = [node1, node2, node3, node4]

        for intersection, neighbours in nodesToAdd.items():
            print("Intersection at", [intersection.x, intersection.y])
            graph.add_node(intersection)
            for neighbour in neighbours:
                # add appropriate edges
                graph.add_edge(intersection, neighbour, id=self.counter)
                self.counter += 1
            # remove existing edges
            print("Removing edge", (neighbours[0].x, neighbours[0].y), (neighbours[1].x, neighbours[1].y))
            print("Removing edge", (neighbours[2].x, neighbours[2].y), (neighbours[3].x, neighbours[3].y))
            if (neighbours[0], neighbours[1]) in graph.edges:  # whether the edge was maybe already deleted
                graph.remove_edge(neighbours[0], neighbours[1])
            if (neighbours[2], neighbours[3]) in graph.edges:
                graph.remove_edge(neighbours[2], neighbours[3])
        print("Intersections done!")

    def removeCloseNodes(self, graph, mindistance):
        nodes = list(graph.nodes)
        nodesToRemove = {}
        for node in graph.nodes:
            nodes.remove(node)
            nodesToRemove[node] = []
            print("Node at", node.x, ",", node.y)
            for othernode in nodes:
                # find nodes that are close to each other
                distance = math.sqrt(math.pow(node.x - othernode.x, 2) + math.pow(node.y - othernode.y, 2))
                if distance < mindistance:
                    print("Got you! ->", othernode.id, ":", [othernode.x, othernode.y])
                    nodesToRemove[node].append(othernode)

        print("Removing...")
        for key, value in nodesToRemove.items():
            if value:
                print("Removing node", key.id, "that is next to node", [v.id for v in value])
                neighbours = graph.adj[key]
                for v in value:
                    for n in neighbours:
                        if n not in graph.adj[v] and n != v:
                            print("Adding edge between", v.id, "and", n.id)
                            graph.add_edge(v, n, id=self.counter)
                            self.counter += 1
                graph.remove_node(key)
        print("Removing done!")

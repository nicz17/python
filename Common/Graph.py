"""
A simple Graph with nodes and edges.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2023 N. Zwahlen"
__version__ = "1.0.0"

import logging

class Node:
    """A Node for a Graph."""
    log = logging.getLogger('Node')

    def __init__(self, id: int, name: str) -> None:
        """Constructor with ID and name of the Node."""
        self.id = id
        self.name = name
        
    def __eq__(self, other): 
        if not isinstance(other, Node):
            # don't attempt to compare against unrelated types
            return NotImplemented
        return self.id == other.id

    def __hash__(self):
        return hash((self.name))

    def __str__(self):
        return f'Node {self.id} {self.name}'

class Edge:
    """An edge connecting two nodes."""
    log = logging.getLogger('Edge')

    def __init__(self, n1: Node, n2: Node) -> None:
        """Constructor with two nodes."""
        self.n1 = n1
        self.n2 = n2
    
    def __eq__(self, other): 
        if not isinstance(other, Edge):
            # don't attempt to compare against unrelated types
            return NotImplemented
        return (self.n1 == other.n1 and self.n2 == other.n2) or (self.n1 == other.n2 and self.n2 == other.n1)

    def __hash__(self):
        return hash((self.n1, self.n2)) + hash((self.n2, self.n1))

    def __str__(self):
        return f'Edge from {self.n1} to {self.n2}'


class Graph:
    """A Graph with nodes and edges."""
    log = logging.getLogger('Graph')

    def __init__(self) -> None:
        self.log.info('Graph constructor')
        self.nodes = []
        self.edges = set()

    def addNode(self, node: Node):
        """Add a Node to this Graph."""
        self.nodes.append(node)

    def addEdge(self, edge: Edge):
        """Add an Edge to this graph."""
        self.edges.add(edge)

    def dump(self):
        """Dump the Graph details to log."""
        self.log.info(self)
        for node in self.nodes:
            self.log.info('  %s', node)
        for edge in self.edges:
            self.log.info('  %s', edge)

    def toJson(self):
        data = []
        for edge in self.edges:
            dataEdge = []
            dataEdge.append(edge.n1.name)
            dataEdge.append(edge.n2.name)
            data.append(dataEdge)
        return data

    def __str__(self):
        return f'Graph with {len(self.nodes)} nodes and {len(self.edges)} edges'

def demoGraph():
    """Simple test and demo method for the Graph class."""
    graph = Graph()
    nodeA = Node(1, 'A')
    nodeB = Node(2, 'B')
    nodeC = Node(3, 'C')
    graph.addNode(nodeA)
    graph.addNode(nodeB)
    graph.addNode(nodeC)
    graph.addEdge(Edge(nodeA, nodeB))
    graph.addEdge(Edge(nodeB, nodeC))
    graph.addEdge(Edge(nodeC, nodeA))
    graph.dump()
    graph.log.info('JSON: %s', graph.toJson())

if __name__ == '__main__':
    logging.basicConfig(format="[%(levelname)s] %(message)s", 
        level=logging.DEBUG, handlers=[logging.StreamHandler()])
    demoGraph()
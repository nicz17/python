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

    def __init__(self, name: str) -> None:
        """Constructor with name of the Node."""
        self.name = name
        
    def __eq__(self, other): 
        if not isinstance(other, Node):
            # don't attempt to compare against unrelated types
            return NotImplemented
        return self.name == other.name

    def __hash__(self):
        return hash((self.name))

    def __str__(self):
        return f'Node {self.name}'

class Edge:
    """An edge connecting two nodes."""
    log = logging.getLogger('Edge')

    def __init__(self, v1: Node, v2: Node) -> None:
        """Constructor with two nodes."""
        self.v1 = v1
        self.v2 = v2
    
    def __eq__(self, other): 
        if not isinstance(other, Edge):
            # don't attempt to compare against unrelated types
            return NotImplemented
        return (self.v1 == other.v1 and self.v2 == other.v2) or (self.v1 == other.v2 and self.v2 == other.v1)

    def __hash__(self):
        return hash((self.v1, self.v2)) + hash((self.v2, self.v1))

    def __str__(self):
        return f'Edge from {self.v1} to {self.v2}'


class Graph:
    """A Graph with nodes and edges."""
    log = logging.getLogger('Graph')

    def __init__(self) -> None:
        self.log.info('Graph constructor')
        self.nodes = []
        self.edges = set()

    def addNode(self, v: Node):
        """Add a Node to this Graph."""
        self.nodes.append(v)

    def addEdge(self, edge: Edge):
        """Add an Edge to this graph."""
        self.edges.add(edge)

    def dump(self):
        """Dump the Graph details to log."""
        self.log.info(self)
        for Node in self.nodes:
            self.log.info('  %s', Node)
        for edge in self.edges:
            self.log.info('  %s', edge)

    def __str__(self):
        return f'Graph with {len(self.nodes)} nodes and {len(self.edges)} edges'

def demoGraph():
    """Simple test and demo method for the Graph class."""
    graph = Graph()
    nodeA = Node('A')
    nodeB = Node('B')
    nodeC = Node('C')
    graph.addNode(nodeA)
    graph.addNode(nodeB)
    graph.addNode(nodeC)
    graph.addEdge(Edge(nodeA, nodeB))
    graph.addEdge(Edge(nodeB, nodeC))
    graph.addEdge(Edge(nodeC, nodeA))
    graph.dump()

if __name__ == '__main__':
    logging.basicConfig(format="[%(levelname)s] %(message)s", 
        level=logging.DEBUG, handlers=[logging.StreamHandler()])
    demoGraph()
"""
A simple 2D triangle mesh generator.
The mesh is made of vertices connected by edges.
Three vertices and their edges make a triangular face.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2023 N. Zwahlen"
__version__ = "1.0.0"

import logging
import math

class Vertex:
    """A 2D vertex for a mesh."""
    log = logging.getLogger('Vertex')

    def __init__(self, x: float, y: float) -> None:
        """Constructor with x, y coordinates of the vertex."""
        self.x = x 
        self.y = y

    def dist(self, v):
        """Compute the euclidian distance to another vertex."""
        dx = self.x - v.x
        dy = self.y - v.y
        return math.sqrt(dx*dx + dy*dy)
        
    def __eq__(self, other): 
        if not isinstance(other, Vertex):
            # don't attempt to compare against unrelated types
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __str__(self):
        return f'Vertex {self.x}:{self.y}'

class Edge:
    """An edge connecting two vertices."""
    log = logging.getLogger('Edge')

    def __init__(self, v1: Vertex, v2: Vertex) -> None:
        """Constructor with two vertices."""
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


class Mesh:
    """A mesh with vertices and edges."""
    log = logging.getLogger('Mesh')

    def __init__(self) -> None:
        self.log.info('Mesh constructor')
        self.vertices = []
        self.edges = set()

    def addVertex(self, v: Vertex):
        """Add a vertex to this mesh."""
        self.vertices.append(v)

    def buildEdges(self):
        """Compute the edges of this mesh by combining vertices into triangles."""
        nVertices = len(self.vertices)
        self.log.info('Building edges for %d vertices', nVertices)
        self.edges.clear()

        if nVertices < 2:
            pass
        elif nVertices == 2:
            self.edges.add(Edge(self.vertices[0], self.vertices[1]))
        else:
            self.buildEdgesProximity()
            #self.buildEdgesCentered()

        self.log.info('Build result: %s', self)

    def buildEdgesCentered(self):
        """Build edges starting from the center and going outward."""
        center = self.getCenter()
        self.log.info('Building edges from the center %s', center)

        # Compute distance to center for each vertex
        for v in self.vertices:
            v.cdist = v.dist(center)

        # Order vertices by distance from center
        cenVert = sorted(self.vertices, key=lambda v: v.cdist)

        # Start with most central triangle
        self.edges.add(Edge(cenVert[0], cenVert[1]))
        self.edges.add(Edge(cenVert[0], cenVert[2]))
        self.edges.add(Edge(cenVert[1], cenVert[2]))

        # Connect the rest
        connected = [cenVert[0], cenVert[1], cenVert[2]]
        if len(cenVert) > 3:
            for i in range(3, len(cenVert)):
                v = cenVert[i]
                v1 = self.getClosestAmong(connected, v)
                v2 = self.getClosestAmong(connected, v1)
                self.edges.add(Edge(v, v1))
                self.edges.add(Edge(v, v2))
                connected.append(v)

    def buildEdgesProximity(self):
        """
        Connect each vertex to its 2 closest neighbours.
        Results in disjointed constellations.
        Could be used as a kind of clustering.
        """
        self.log.info('Building edges by proximity')
        for v in self.vertices:
            v2 = self.getClosest(v)
            v3 = self.getClosest(v, v2)
            if v2 is not None:
                self.edges.add(Edge(v, v2))
            if v3 is not None:
                self.edges.add(Edge(v, v3))
                if len(self.edges) < 3:
                    self.edges.add(Edge(v2, v3))

    def getClosest(self, v: Vertex, exc=None):
        """Find the closest vertex to the specified one, possibly ignoring another vertex."""
        result = None
        minDist = None
        for vertex in self.vertices:
            if v == vertex or exc == vertex:
                continue
            dist = v.dist(vertex)
            if minDist is None or dist < minDist:
                minDist = dist
                result = vertex
        return result

    def getClosestAmong(self, vertices, v: Vertex, exc=None):
        """Find the closest vertex to the specified one, possibly ignoring another vertex."""
        result = None
        minDist = None
        for vertex in vertices:
            if v == vertex or exc == vertex:
                continue
            dist = v.dist(vertex)
            if minDist is None or dist < minDist:
                minDist = dist
                result = vertex
        return result
    
    def getCenter(self):
        """Find the geometric center of the vertices."""
        nVertices = len(self.vertices)
        if nVertices < 1:
            return None
        sumX = 0.0
        sumY = 0.0
        for v in self.vertices:
            sumX += v.x
            sumY += v.y
        return Vertex(sumX/nVertices, sumY/nVertices)

    def dump(self):
        """Dump the mesh details to log."""
        self.log.info(self)
        for vertex in self.vertices:
            self.log.info('  %s', vertex)
        for edge in self.edges:
            self.log.info('  %s', edge)

    def __str__(self):
        return f'Mesh with {len(self.vertices)} vertices and {len(self.edges)} edges'

def demoMesh():
    """Simple test and demo method for the mesh class."""
    mesh = Mesh()
    mesh.addVertex(Vertex(0.0, 1.0))
    mesh.addVertex(Vertex(1.0, 0.0))
    mesh.addVertex(Vertex(1.0, 2.0))
    mesh.addVertex(Vertex(2.1, 1.0))
    mesh.buildEdges()
    mesh.dump()
    center = mesh.getCenter()
    mesh.log.info('Center: %s', center)

if __name__ == '__main__':
    logging.basicConfig(format="[%(levelname)s] %(message)s", 
        level=logging.DEBUG, handlers=[logging.StreamHandler()])
    demoMesh()
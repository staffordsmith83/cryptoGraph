from linkedLists import *
from adts_LLversion import *
import json
from copy import deepcopy
from DSAHeaps import *


class DSAGraphVertex:

    def __init__(self, label, value=None):
        self._label = label
        self._value = value
        self._edges = DSALinkedList()
        self._visited = False

    def setVisited(self):
        self._visited = True

    def clearVisited(self):
        self._visited = False

    def __repr__(self):
        return self._label


class DSAGraphEdge:
    def __init__(self, fromVertex, toVertex, weight=0.0):
        self.fromVertex = fromVertex
        self.toVertex = toVertex
        self.weight = weight
        self._visited = False

    def setVisited(self):
        self._visited = True

    def clearVisited(self):
        self._visited = False


def displayQueueLabels(queue):
    """Intended to be used in conjunction with the search functions that return a queue of vertices."""

    while not queue.isEmpty():
        v = queue.dequeue()
        print(v._label)


class DSAGraphWithEdges:
    """Non-directional graph. When adding an edge we add a reference in the links of both vertices"""

    def __init__(self):
        self._vertices = DSALinkedList()  # start with an empty list when first constructed
        self._edges = DSALinkedList()  # empty linked list for the edges too
        self.edgeCount = 0
        self.verticesCount = 0


    def addVertex(self, label):
        if self.hasVertex(label) is False:
            vertex = DSAGraphVertex(label)
            self._vertices.insertLast(vertex)
            self.verticesCount += 1

    def getVertex(self, label):
        result = None
        for i in self._vertices:
            if i._label == label:
                result = i

        if result is None:
            raise ValueError('The vertex does not exist')

        return result

    def addEdge(self, label1, label2, weight=0.0):
        """Do not confuse with .addEdge() method of individual vertices.
        Non directional graph, label1 <--> label2"""

        if self.hasVertex(label1) is False:
            self.addVertex(label1)

        if self.hasVertex(label2) is False:
            self.addVertex(label2)

        newEdge = DSAGraphEdge(label1, label2, weight)
        self._edges.insertLast(newEdge)

        self.edgeCount += 1

    def removeVertex(self, label):
        """ NEW METHOD SINCE CREATING THIS CLASS FOR THE PRACS"""
        """Will remove vertex and any edges that use it, and update the vertex and edge counts"""

        for v in self._vertices:
            if v._label == label:
                self._vertices.removeValue(v)   # remove that value from the linked list of vertices!
                self.verticesCount -= 1

        for e in self._edges:
            if e.fromVertex == label or e.toVertex == label:
                self._edges.removeValue(e)
                self.edgeCount -= 1


    def getEdge(self, fromVertex, toVertex):
        result = None
        for e in self._edges:
            if e.fromVertex == fromVertex and e.toVertex == toVertex:
                result = e

        if result is None:
            raise ValueError('The edge does not exist')

        return result

    def hasVertex(self, label):
        result = False
        for i in self._vertices:
            if i._label == label:
                result = True

        return result

    def getAdjacent(self, label):
        """Implementation changed with edge version of graph data structure.
        This may need renaming because this graph is now directional..."""
        adjacency_list = DSALinkedList()

        vertex = self.getVertex(label)
        if vertex is None:
            raise ValueError(f'There is no vertex with label {label}')

        else:
            for e in self._edges:
                if e.fromVertex == label:
                    adjacency_list.insertLast(self.getVertex(e.toVertex))

        return adjacency_list

    def getAdjacentEdges(self, label):
        """This method added for my modiified DSAGraph implementation
        to be used in the Cryptograph Application
        Returns a linkedlist of DSAEdge objects"""
        adjacent_edges_list = DSALinkedList()
        vertex = self.getVertex(label)
        if vertex is None:
            raise ValueError(f'There is no vertex with label {label}')

        else:
            for e in self._edges:
                if e.fromVertex == label:
                    adjacent_edges_list.insertLast(e)

        return adjacent_edges_list

    def isAdjacent(self, label1, label2):
        """This is directional"""
        result = False
        try:
            neighbours = self.getAdjacent(label1)
            for v in neighbours:
                if v._label == label2:
                    result = True

        except ValueError as ve:
            print(ve)

        return result

    def displayAsList(self):
        for v in self._vertices:
            print(f'{v._label}', end=", ")
        print('\n')

    def displayAsMatrix(self):
        """Not working... Stops printing the vertices after first one...had to use deepcopy...
        Maybe a problem with the iterator implementation in my LinkedLists class?"""
        vertices = deepcopy(self._vertices)
        for v in vertices:
            print(f'\n{v._label}:', end=" ")
            adjList = self.getAdjacent(v._label)

            for n in adjList:
                print(f'{n._label}', end=", ")

        print('\n')

    def displayEdges(self):
        for e in self._edges:
            print(f'{e.fromVertex} --> {e.toVertex}: {e.weight}')

    def searchDepthFirst(self):
        """NB This returns a queue of objects."""
        # mark all vertices as unvisited
        vertices = self._vertices
        for v in vertices:
            v.clearVisited()

        # establish the output container
        t = Queue()

        # pick one of the vertices to start with
        v = vertices.peekFirst()
        t.enqueue(v)
        v.setVisited()

        # make a traversal stack of items to check
        s = Stack()
        s.push(v)

        # while the stack is not empty:
        while not s.isEmpty():

            # while v has another vertex in its links to look at:
            v = s.top()
            if any(link._visited is False for link in self.getAdjacent(v._label)):

                for w in self.getAdjacent(v._label):

                    if not w._visited:
                        t.enqueue(w)
                        w.setVisited()

                        s.push(w)
                        v = w  # need to make the operation move to the links of w now
                        break  # stop going through the links of v now and switch to the links of w

            else:
                v = s.pop()  # only pop when we have gone through all items in that item.
        return t

    def searchBreadthFirst(self):
        """NB This returns a queue of objects."""
        # mark all vertices as unvisited
        vertices = self._vertices
        for v in vertices:
            v.clearVisited()

        # establish our output container
        t = Queue()

        # pick one of the vertices to start with
        v = vertices.peekFirst()
        t.enqueue(v)
        v.setVisited()

        # make a traversal queue that loads up items to check
        s = Queue()
        s.enqueue(v)

        # while the queue is not empty:
        while not s.isEmpty():

            # while v has another vertex in its links to look at:
            v = s.dequeue()
            # while any(link._visited is False for link in self.getAdjacent(v._label)):  # can this be made more efficient?

            for w in self.getAdjacent(v._label):

                if not w._visited:
                    t.enqueue(w)  # the output queue
                    w.setVisited()
                    # print(f'Putting {w._label} into the traverse queue')
                    s.enqueue(w)
                    # v = w  # need to make the operation move to the links of w now
                    # break  # stop going through the links of v now and switch to the links of w

        return t



    def readFromCsv(self, filepath):
        with open(filepath, 'r') as myCsv:
            for item in myCsv.readlines():
                label1, label2 = item.rstrip('\n').split(" ")

                self.addEdge(label1, label2)




if __name__ == "__main__":
    g = DSAGraphWithEdges()
    # g = DSAGraphWithEdges()

    testfile = 'test_vertices.al'
    g.readFromCsv(testfile)

    print(g.isAdjacent('G', 'F'))

    print('Our Graph as a list of vertices: ')
    # g.displayAsList()

    print('Our Graph as an adjacency matrix: ')
    g.displayAsMatrix()

    print('Running Depth First Search')
    dfs = g.searchDepthFirst()
    displayQueueLabels(dfs)

    print('Running Breadth First Search')
    bfs = g.searchBreadthFirst()
    displayQueueLabels(bfs)

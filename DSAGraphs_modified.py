from linkedLists import *
from adts_LLversion import *
import json

class DSAGraphVertex:

    def __init__(self, label, value=None):
        self._label = label
        self._value = value
        # self._edges = DSALinkedList() #edges keep track of links
        self._visited = False

    # def addEdge(self, vertex, attributes):
    #     self._links.insertLast(vertex)

    def setVisited(self):
        self._visited = True

    def clearVisited(self):
        self._visited = False

class DSAGraphEdge:
    def __init__(self, fromVertex, toVertex, weight=0.0):
        self.fromVertex = fromVertex
        self.toVertex = toVertex
        self.weight = weight



class DSAGraphWithEdges:
    """Non-directional graph. When adding an edge we add a reference in the links of both vertices"""

    def __init__(self):
        self._vertices = DSALinkedList()  # start with an empty list when first constructed
        self._edges = DSALinkedList()   # empty linked list for the edges too
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
        #
        # # Get the vertex objects, so that we can update their links
        # vertex1 = self.getVertex(label1)
        # vertex2 = self.getVertex(label2)
        #
        # # For undirected graph, add links to both vertices:
        # vertex1.addEdge(vertex2)
        # vertex2.addEdge(vertex1)
        #
        newEdge = DSAGraphEdge(label1, label2, weight)
        self._edges.insertLast(newEdge)
        
        self.edgeCount += 1

    def getEdge(self, fromVertex, toVertex):
        result = None
        for e in self._edges:
            if e.fromVertex == fromVertex and e.toVertex == toVertex:
                result = e

        if result is None:
            raise ValueError('The edge does not exist')

        return result

    def getEdgeWeightsFromBinance(self, binanceDataObject):
        with open(binanceDataObject.trades_filepath) as json_file:
            trades = json.load(json_file)  # trades is a list of dictionaries, one for each trading pair

            for e in self._edges:
                # symbol = e.fromVertex._label + e.toVertex._label
                symbol = self.getVertex(e.fromVertex)._label + self.getVertex(e.toVertex)._label

                for t in trades:
                    if t['symbol'] == symbol:
                        # set the weight!
                        e.weight = t['weightedAvgPrice']

    def hasVertex(self, label):
        result = False
        for i in self._vertices:
            if i._label == label:
                result = True

        return result

    def getAdjacent(self, label):
        adjacency_list = DSALinkedList()
        
        vertex = self.getVertex(label)
        if vertex is None:
            raise ValueError(f'There is no vertex with label {label}')

        else:
            for e in self._edges:
                if e.fromVertex == label:
                    adjacency_list.insertLast(self.getVertex(e.toVertex))
                    

    def isAdjacent(self, label1, label2):
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

    def displayAsMatrix(self):
        for v in self._vertices:
            print(f'\n{v._label}:', end="")
            for n in v._links:
                print(f'{n._label}, ', end="")
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
            if any(link._visited is False for link in v._links):

                for w in v._links:

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
            # while any(link._visited is False for link in v._links):  # can this be made more efficient?

            for w in v._links:

                if not w._visited:
                    t.enqueue(w)  # the output queue
                    w.setVisited()
                    # print(f'Putting {w._label} into the traverse queue')
                    s.enqueue(w)
                    # v = w  # need to make the operation move to the links of w now
                    # break  # stop going through the links of v now and switch to the links of w

        return t

    def displayQueueLabels(self, queue):
        """Intended to be used in conjunction with the search functions that return a queue of vertices."""

        while not queue.isEmpty():
            v = queue.dequeue()
            print(v._label)

    def readFromCsv(self, filepath):
        with open(filepath, 'r') as myCsv:
            for item in myCsv.readlines():
                label1, label2 = item.rstrip('\n').split(" ")

                self.addEdge(label1, label2)



if __name__ == "__main__":
    g = DSAGraphWithEdges()
    # g = DSAGraphWithEdges()


    testfile = 'prac6_sorted_order.al'
    g.readFromCsv(testfile)

    # print(g.isAdjacent('A', 'B'))

    # g.displayAsList()
    print('Our Graph as an adjacency matrix: ')
    g.displayAsMatrix()

    print('Running Depth First Search')
    dfs = g.searchDepthFirst()
    g.displayQueueLabels(dfs)

    g.displayAsMatrix()

    print('Running Breadth First Search')
    bfs = g.searchBreadthFirst()
    g.displayQueueLabels(bfs)

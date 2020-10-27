from copy import deepcopy    # TODO: reimplement to not use deepcopy

##########################################
# CLASSES
##########################################
# GRAPHS CLASSES
##########################################

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

##########################################
# LINKED LISTS CLASSES
##########################################

class DSAListNode:

    def __init__(self, value):
        """self.next should be the next DSAListNode object
        in line in the list"""
        self.value = value
        self.next = None
        self.previous = None


class DSALinkedList:

    def __init__(self):
        self.head = None

    def insertFirst(self, newValue):
        newNd = DSAListNode(newValue)

        if self.isEmpty():
            self.head = newNd

        else:
            self.head.previous = newNd      # add a previous ref to the top node
            newNd.next = self.head          # add a next ref to our new node (not inserted yet)
            self.head = newNd               # then reassign head to be the new node (shuffles items down)

    def insertLast(self, newValue):
        newNd = DSAListNode(newValue)

        if self.isEmpty():
            self.head = newNd

        else:
            currNd = self.head
            while currNd.next:  # check each item in list and set currNd to be the last node
                currNd = currNd.next

            # so we have traversed to the last node... what next?

            currNd.next = newNd             # assign the currently last node to point to the new node next...
            newNd.previous = currNd         # assign the new node to point back to the currently last node.
            # newNd is now added to the end!

    def isEmpty(self):
        return self.head is None

    def peekFirst(self):
        if self.isEmpty():
            raise ValueError('List is empty')
        else:
            return self.head.value

    def peekLast(self):
        if self.isEmpty():
            raise ValueError('List is empty')
        else:
            currNd = self.head
            while currNd.next:  # check each item in list and set currNd to be the last node
                currNd = currNd.next

            return currNd.value

    def removeFirst(self):
        if self.isEmpty():
            raise ValueError('List is empty')

        # check for one item list
        elif self.head is not None and self.head.next is None:
            nodeValue = self.head.value
            self.head = self.head.next      # in this case will set head to be None

        else:   # multi item list
            nodeValue = self.head.value
            self.head = self.head.next
            self.head.previous = None       # remove the previous ref as our second node is now our head

        return nodeValue

    def removeLast(self):
        if self.isEmpty():
            raise ValueError('List is empty')

        elif self.head.next is None:
            nodeValue = self.head.value
            self.head = None

        else:
            prevNd = None
            currNd = self.head

            while currNd.next is not None:
                prevNd = currNd
                currNd = currNd.next    # traverse to the second last node, to be able to drop its .next attribute

            prevNd.next = None          # cut off the tail of the list
            nodeValue = currNd.value

        return nodeValue


    def contains(self, searchValue):
        """Added this method 10/10/2020, useful when using this data structure for other purposes e.g. cryptoGraph"""

        for i in self:
            if i == searchValue:
                return True

        return False

    def removeValue(self, value):
        """ NEW METHOD SINCE CREATING THIS CLASS FOR THE PRACS"""
        """Based on a method from https://www.pythoncentral.io/find-remove-node-linked-lists/"""
        prev = None
        curr = self.head
        while curr:
            if curr.value == value:
                if prev:
                    prev.next = curr.next
                else:
                    self.head = curr.next
                return True

            prev = curr
            curr = curr.next

        return False


    def __iter__(self):

        self.cur = self.head
        return self

    def __next__(self):
        curval = None
        if self.cur == None:
            raise StopIteration
        else:
            curval = self.cur.value
            self.cur = self.cur.next
        return curval


class DSALinkedListDE:
    """Doubly Ended linked list implementation. added another instance attribute self.tail.
    Having this mens we never need to traverse through the list to find the end."""

    def __init__(self):
        self.head = None
        self.tail = None    # added for doubly-ended implementation

    def insertFirst(self, newValue):
        newNd = DSAListNode(newValue)

        if self.isEmpty():
            self.head = newNd
            self.tail = newNd   # doubly-ended
        else:
            self.head.previous = newNd      # add a previous ref to the top node
            newNd.next = self.head          # add a next ref to our new node (not inserted yet)
            self.head = newNd               # then reassign head to be the new node (shuffles items down)

    def insertLast(self, newValue):
        newNd = DSAListNode(newValue)

        if self.isEmpty():
            self.head = newNd
            self.tail = newNd  # doubly-ended
        else:
            self.tail.next = newNd             # assign the currently last node to point to the new node next...
            newNd.previous = self.tail        # assign the new node to point back to the currently last node.
            self.tail = newNd

    def isEmpty(self):
        return self.head is None

    def peekFirst(self):
        if self.isEmpty():
            raise ValueError('List is empty')
        else:
            return self.head.value

    def peekLast(self):
        if self.isEmpty():
            raise ValueError('List is empty')
        else:
            return self.tail.value

    def removeFirst(self):
        if self.isEmpty():
            raise ValueError('List is empty')

        elif self.head == self.tail:
            nodeValue = self.head.value
            self.head = None
            self.tail = None

        else:   # multi item list
            nodeValue = self.head.value
            self.head = self.head.next
            self.head.previous = None       # remove the previous ref as our second node is now our head

        return nodeValue

    def removeLast(self):
        if self.isEmpty():
            raise ValueError('List is empty')

        elif self.head == self.tail:
            nodeValue = self.head.value
            self.head = None
            self.tail = None

        else:
            nodeValue = self.tail.value
            self.tail = self.tail.previous

        return nodeValue

    def __iter__(self):

        self.cur = self.head
        return self

    def __next__(self):
        curval = None
        if self.cur == None:
            raise StopIteration
        else:
            curval = self.cur.value
            self.cur = self.cur.next
        return curval

    def removeValue(self, value):
        """ NEW METHOD SINCE CREATING THIS CLASS FOR THE PRACS"""
        """Based on a method from https://www.pythoncentral.io/find-remove-node-linked-lists/"""
        prev = None
        curr = self.head
        while curr:
            if curr.value == value:
                if prev:
                    prev.next(curr.next)
                else:
                    self.head = curr.next
                return True

            prev = curr
            curr = curr.next

        return False

###########################################
# STACKS AND QUEUES CLASSES
##########################################

class Stack:

    def __init__(self):  # the constructor
        self.items = DSALinkedList()

    def getCount(self):
        """ Return the count of items in the stack as an integer."""
        count = 0
        for i in self.items:    # uses the __iter__ method
            count = count + 1
        return count

    def isEmpty(self):
        """ Will return True if no items in the stack."""
        return self.items.isEmpty()

    def push(self, item):
        """Add another element, and increment the count"""
        # self.items.insertLast(item)
        self.items.insertFirst(item)        # add to and remove from the start of the list, more efficient!

    def pop(self):
        """Return the last element, zero it in stack, and decrement the count"""
        # return self.items.removeLast()
        return self.items.removeFirst()     # add to and remove from the start of the list, more efficient!

    def top(self):
        """Return the last element"""
        return self.items.peekFirst()


class Queue:
    """ Parent Class, no loading or unloading or peek methods Implemented."""

    def __init__(self, capacity=100, dtype=object):  # the constructor, with defaults
        self.items = DSALinkedList()

    def getCount(self):
        """ Return the count of items in the queue as an integer."""
        count = 0
        for i in self.items:  # uses the __iter__ method
            count = count + 1
        return count

    def isEmpty(self):
        """ Will return True if no items in the queue."""
        return self.items.isEmpty()

    def peek(self):
        """Return the front element."""
        return self.items.peekFirst()

    def enqueue(self, item):
        """Add another element at the back, and increment the count"""
        self.items.insertLast(item)

    def dequeue(self):
        """Return the front element, decrement the count, and shuffle everything down"""
        return self.items.removeFirst()


##########################################
# STATIC FUNCTIONS
##########################################

def displayQueueLabels(queue):
    """Intended to be used in conjunction with the search functions that return a queue of vertices."""

    while not queue.isEmpty():
        v = queue.dequeue()
        print(v._label)
##########################################
# CLASSES
##########################################
# GRAPHS CLASSES
##########################################

class DSAGraphVertex:
    """ Each instance describe a vertex in the graph.
    This class is adapted from the DSAGraph implementation for Practical 6."""

    def __init__(self, label, value=None):
        self._label = label
        self._value = value
        self._edges = SortableList()
        self.edgeCount = 0
        self._visited = False

    def setVisited(self):
        self._visited = True

    def clearVisited(self):
        self._visited = False

    def __repr__(self):
        return self._label


class DSAGraphEdge:
    """ Added v, p, and c default parameters, and added more attributes to store trade information for Cryptograph.
    self.weight stores the trade price."""

    def __init__(self, fromVertex, toVertex, weight=None, v=None, c=None):
        self.fromVertex = fromVertex
        self.toVertex = toVertex
        self.weight = weight
        self.volume24hr = v
        self.percentPriceChange24hr = c
        self._visited = False

    def setVisited(self):
        self._visited = True

    def clearVisited(self):
        self._visited = False


class DSAGraphWithEdges:
    """Non-directional graph. When adding an edge we add a reference in the links of both vertices.
    This class is adapted from the DSAGraph implementation for Practical 6."""

    def __init__(self):
        self._vertices = SortableList()  # use this modified implementation of a linkedList that can be sorted
        self._edges = SortableList()  # empty linked list for the edges too
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

    def addEdge(self, label1, label2, weight=None):
        """Do not confuse with .addEdge() method of individual vertices.
        Non directional graph, label1 <--> label2"""

        if self.hasVertex(label1) is False:
            self.addVertex(label1)

        if self.hasVertex(label2) is False:
            self.addVertex(label2)

        newEdge = DSAGraphEdge(label1, label2, weight)
        self._edges.insertLast(newEdge)

        self.edgeCount += 1

        # also increment the counter for the number of edges each vertex has
        leadingVertex = self.getVertex(label1)
        # TODO: do I need to maintain the list of edges for the vertex itself?
        leadingVertex.edgeCount += 1

    def removeVertex(self, label):
        """ NEW METHOD SINCE CREATING THIS CLASS FOR THE PRACS"""
        """Will remove vertex and any edges that use it, and update the vertex and edge counts"""

        # remove the edges first so we can still lookup vertices
        for e in self._edges:
            if e.fromVertex == label:
                self._edges.removeValue(e)
                self.edgeCount -= 1

            elif e.toVertex == label:
                self._edges.removeValue(e)
                self.edgeCount -= 1
                # also decrement the counter for the number of edges the leading vertex has
                leadingVertex = self.getVertex(label)
                leadingVertex.edgeCount -= 1

        # now remove the vertex
        for v in self._vertices:
            if v._label == label:
                self._vertices.removeValue(v)  # remove that value from the linked list of vertices!
                self.verticesCount -= 1

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
        """Implementation changed with edge version of graph data structure"""
        adjacency_list = SortableList()

        vertex = self.getVertex(label)
        if vertex is None:
            raise ValueError(f'There is no vertex with label {label}')

        else:
            for e in self._edges:
                if e.fromVertex == label:
                    adjacency_list.insertLast(self.getVertex(e.toVertex))

        return adjacency_list



##########################################
# LINKED LISTS CLASSES
##########################################

class DSAListNode:

    def __init__(self, value):
        """Building block for both linked list implementations in this module.
        Based on code from my submission for DSA Practical 4 - Linked Lists.
        self.next should be the next DSAListNode object
        in line in the list"""
        self.value = value
        self.next = None
        self.previous = None





class DSALinkedListDE:
    """Doubly Ended linked list implementation, based on my submission for DSA Practical 4 - Linked Lists.
    Added another instance attribute self.tail.
    Having this mens we never need to traverse through the list to find the end."""

    def __init__(self):
        self.head = None
        self.tail = None  # added for doubly-ended implementation

    def insertFirst(self, newValue):
        newNd = DSAListNode(newValue)

        if self.isEmpty():
            self.head = newNd
            self.tail = newNd  # doubly-ended
        else:
            self.head.previous = newNd  # add a previous ref to the top node
            newNd.next = self.head  # add a next ref to our new node (not inserted yet)
            self.head = newNd  # then reassign head to be the new node (shuffles items down)

    def insertLast(self, newValue):
        newNd = DSAListNode(newValue)

        if self.isEmpty():
            self.head = newNd
            self.tail = newNd  # doubly-ended
        else:
            self.tail.next = newNd  # assign the currently last node to point to the new node next...
            newNd.previous = self.tail  # assign the new node to point back to the currently last node.
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

        else:  # multi item list
            nodeValue = self.head.value
            self.head = self.head.next
            self.head.previous = None  # remove the previous ref as our second node is now our head

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
        """ NEW METHOD IMPLEMENTATION FOR Cryptograph.
        Based on a method from https://www.pythoncentral.io/find-remove-node-linked-lists/"""

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


class SortableList(DSALinkedListDE):
    """NEW IMPLEMENTATION FOR Cryptograph. TO be used to hold graph edges, or vertices. 
    These can then be sorted and returned in sorted order for display."""

    def sortByAttribute(self, attribute="edgeCount", order="high"):
        """
        For example:
        Allow the container of a graph's vertices to be sorted by the number of outward
        connections each of those vertices has. Wrapper for the
        mergeSort() method and its helper methods sortedMerge() and getMiddle()"""
        self.head = self.mergeSort(self.head, attribute, order)

    #################################
    # ADD SORTING METHODS THAT USE THE self.edgeCount ATTRIBUTE
    def sortedMerge(self, a, b, attribute, order):
        """ Adapted from https://www.geeksforgeeks.org/merge-sort-for-linked-list/"""
        result = None

        # BASE CASES
        if a is None:
            return b
        if b is None:
            return a

        # use Python's built-in getattr() method to retrieve the programmatically determined attribute
        aAttribute = getattr(a.value, attribute)
        bAttribute = getattr(b.value, attribute)

        # functionality to sort high-low or low-high
        if order == 'high':
            if aAttribute >= bAttribute:
                result = a
                result.next = self.sortedMerge(a.next, b, attribute, order)
            else:
                result = b
                result.next = self.sortedMerge(a, b.next, attribute, order)

        elif order == 'low':
            if aAttribute <= bAttribute:
                result = a
                result.next = self.sortedMerge(a.next, b, attribute, order)
            else:
                result = b
                result.next = self.sortedMerge(a, b.next, attribute, order)

        else:
            raise ValueError

        return result

    def mergeSort(self, h, attribute, order):
        """ Adapted from https://www.geeksforgeeks.org/merge-sort-for-linked-list/"""
        # BASE CASE: if the head is None
        if h is None or h.next is None:
            return h

        # Find the mid point of the list
        middle = self.getMiddle(h)
        nexttomiddle = middle.next

        # set the next of middle node to None
        middle.next = None

        # MergeSort left sublist
        left = self.mergeSort(h, attribute, order)

        # Mergesort the right sublist
        right = self.mergeSort(nexttomiddle, attribute, order)

        # merge the right and left
        sortedlist = self.sortedMerge(left, right, attribute, order)
        return sortedlist

    def getMiddle(self, head):
        """ Adapted from https://www.geeksforgeeks.org/merge-sort-for-linked-list/"""
        if head is None:
            return head

        slower = head
        faster = head

        while faster.next is not None and faster.next.next is not None:
            slower = slower.next
            faster = faster.next.next

        return slower

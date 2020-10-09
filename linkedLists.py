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

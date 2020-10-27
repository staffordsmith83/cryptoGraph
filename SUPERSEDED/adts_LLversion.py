import linkedLists


class Stack:

    def __init__(self):  # the constructor
        self.items = linkedLists.DSALinkedList()

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
        self.items = linkedLists.DSALinkedList()

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



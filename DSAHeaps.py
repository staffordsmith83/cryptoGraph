import numpy as np

import string, random


class DSAHeap:

    def __init__(self, maxSize):
        # TODO: is it good practise to initialize array with type DSAHeapEntry?
        # TODO: and give each heapEntry object default values of zero?
        # TODO: is np.zeros the correct method to use? What does 'zeros' mean if they
        # TODO: are not zeros but DSAHeapEntries?
        self.heapArray = np.zeros(shape=maxSize, dtype=object)
        # Other option maybe:
        # self.heapArray = np.full(shape=maxSize, dtype=DSAHeapEntry)
        self.count = 0

    def add(self, priority, object=None):
        """Extract the priority and value attributes from the heapItem object
        add the heapItem at the correct place in the heap tree.
        Start by putting it at the end, then trickle it up, by using
        arithmetic to get to its parent, until the parent is of equal or higher
        priority"""
        heapItem = DSAHeapEntry(priority, object)
        curIdx = self.count
        parentIdx = (curIdx - 1) / 2
        # insert item at the end
        self.heapArray[curIdx] = heapItem
        # trickle it up
        self._trickleUp(curIdx)

        # update the count
        self.count += 1

    def remove(self):
        """Always removes the highest priority item"""
        # copy the root element securely
        # root = deepcopy(self.heapArray[0])  # do we need a deep copy or create a fresh heapItem to be sure?
        root = self.heapArray[0]

        # move last element to head and trickle it down
        self.heapArray[0] = self.heapArray[self.count - 1]
        self.heapArray[self.count - 1] = 0
        self.count -= 1
        self._trickleDown(0)

        # update the count

        return root

    def _trickleUp(self, curIdx):
        parentIdx = (curIdx - 1) // 2  # make sure integer division
        if curIdx > 0:
            if self.heapArray[parentIdx].priority < self.heapArray[curIdx].priority:
                self.swap(parentIdx, curIdx)
                self._trickleUp(parentIdx)

    def _trickleDown(self, curIdx, totalItems=None):

        if not totalItems:
            totalItems = self.count

        lChildIdx = curIdx * 2 + 1
        rChildIdx = lChildIdx + 1

        # find the highest priority child, and make sure it is not the last
        if lChildIdx < (totalItems):  # as long as the lChild is not the last item, default to left child
            largeIdx = lChildIdx
            if rChildIdx < (totalItems):
                # but if the right child is not the end, and has more priority
                if self.heapArray[lChildIdx].priority < self.heapArray[rChildIdx].priority:
                    largeIdx = rChildIdx
            if self.heapArray[largeIdx].priority > self.heapArray[curIdx].priority:
                self.swap(largeIdx, curIdx)
                self._trickleDown(largeIdx)

    def swap(self, index1, index2):
        # temp = deepcopy(self.heapArray[index2])   # is this a copy on disk or just a reference?
        temp = self.heapArray[index2]
        self.heapArray[index2] = self.heapArray[index1]
        self.heapArray[index1] = temp

    def display(self):
        for i in range(self.count):
            item = self.remove()
            print(item)


class DSAHeapEntry:
    """Default priority is lowest possible python value"""
    def __init__(self, inPriority=float("-inf"), inValue=None):  # defaults in contructor

        self.priority = inPriority
        self.value = inValue

    def __repr__(self):
        return f'{self.value}: {self.priority}'


def randomChar():
    return random.choice(string.ascii_letters)


def heapSort(arrayToSort):
    """Takes an array of DSAHeap objects, and returns a sorted array of those objects"""
    ...

    myHeap = DSAHeap(maxSize=len(arrayToSort))

    for i in arrayToSort:
        myHeap.add(priority=i.priority, object=i.value)

    return myHeap.heapArray


def heapSortBasicArray(arrayToSort=np.random.randint(0, 99, 10)):
    """The first is to create a heap from an array of numbers,
    then remove all of the numbers from the heap and place them into a new array,
    then output the new array (which will be sorted)"""
    ...

    myHeap = DSAHeap(maxSize=len(arrayToSort))

    for i in arrayToSort:
        myHeap.add(priority=i)

    return myHeap.heapArray


if __name__ == "__main__":
    # arrayToSort = np.zeros(shape=6, dtype=object)
    #
    # arrayToSort[0] = DSAHeapEntry(99, 'a')
    # arrayToSort[1] = DSAHeapEntry(5, 'b')
    # arrayToSort[2] = DSAHeapEntry(3, 'c')
    # arrayToSort[3] = DSAHeapEntry(44, 'd')
    # arrayToSort[4] = DSAHeapEntry(6, 'e')
    # arrayToSort[5] = DSAHeapEntry(1, 'f')
    #
    # print(arrayToSort)
    #
    # # newHeap = heapify(arrayToSort, 6)
    #
    # # print(newHeap)
    #
    # # Testing heapSort()
    # h = heapSortBasicArray()
    # h.display()
    #
    # h2 = heapSort(arrayToSort)
    # h2.display()
    ...

#
# Data Structures and Algorithms COMP1002
#
# Python file to hold all sorting methods
#

import numpy as np


def bubbleSort(myArray):
    """ Takes an array of integers and exports a sorted array of integers"""
    arrayLength = len(myArray)
    for i in range(arrayLength - 1):  # should this be arrayLength not arrayLength-1?
        for ii in range(arrayLength - 1 - i):
            if myArray[ii] > myArray[ii + 1]:  # if item is greater than the next one in line
                temp = myArray[ii]  # switch the values in these two positions
                myArray[ii] = myArray[ii + 1]
                myArray[ii + 1] = temp

    return myArray  # may not be necessary as the function operates on the array itself, not a copy of it.


def insertionSort(myArray):
    # TODO: debug this to see if it is 'starting from last item' and going backwards. Works now but is it efficient?
    """ Takes an array of integers and exports a sorted array of integers"""
    for nn in range(1, len(myArray)):  # upper bound is non-inclusive
        ii = nn  # should this start at the last item, so ii = len(myArray)-1?
        while (ii > 0) and (myArray[ii - 1] > myArray[ii]):
            temp = myArray[ii]  # switch the values
            myArray[ii] = myArray[ii - 1]
            myArray[ii - 1] = temp

            ii = ii - 1

    return myArray  # may not be necessary as the function operates on the array itself, not a copy of it.


def selectionSort(myArray):
    for nn in range(0, len(myArray) - 1):  # dont check for last item, that should be already sorted.
        minIdx = nn
        for jj in range(nn + 1, len(myArray)):  # should upper bound be len(myArray)-1?
            if myArray[jj] < myArray[minIdx]:
                minIdx = jj

        temp = myArray[minIdx]  # switch the values
        myArray[minIdx] = myArray[nn]
        myArray[nn] = temp

    return myArray


def mergeSort(A):
    """ mergeSort - front-end for kick-starting the recursive algorithm"""
    leftIdx = 0
    rightIdx = len(A) - 1

    # Call the first of the recursive functions, on the full array
    _mergeSortRecurse(A, leftIdx, rightIdx)


def _mergeSortRecurse(A, leftIdx, rightIdx):
    if leftIdx < rightIdx:  # the base case is leftIdx = rightIdx, single value array
        midIdx = (leftIdx + rightIdx) // 2

        _mergeSortRecurse(A, leftIdx, midIdx)  # call the recursive function on the left half
        _mergeSortRecurse(A, midIdx + 1, rightIdx)  # call the recursive function on the right half

        _merge(A, leftIdx, midIdx, rightIdx)


def _merge(A, leftIdx, midIdx, rightIdx):
    tempLength = rightIdx - leftIdx + 1
    tempArr = np.zeros(tempLength)

    ii = leftIdx
    jj = midIdx + 1
    kk = 0

    while ii <= midIdx and jj <= rightIdx:
        if A[ii] <= A[jj]:
            tempArr[kk] = A[ii]
            ii += 1

        else:
            tempArr[kk] = A[jj]
            jj += 1

        kk += 1

    for ii in range(ii, midIdx + 1):  # range is not inclusive in python, so need +1
        tempArr[kk] = A[ii]
        kk += 1

    for jj in range(jj, rightIdx + 1):  # range is not inclusive in python, so need +1
        tempArr[kk] = A[jj]
        kk += 1

    for kk in range(leftIdx, rightIdx + 1):  # range is not inclusive in python, so need +1
        tempVal = kk - leftIdx
        A[kk] = tempArr[tempVal]


def quickSort(A):
    """ quickSort - front-end for kick-starting the recursive algorithm
    """
    ...


def quickSortRecurse(A, leftIdx, rightIdx):
    ...


def doPartitioning(A, leftIdx, rightIdx, pivotIdx):
    ...


if __name__ == '__main__':

    ...
    # testArray = np.random.randint(0, 93464, 3455)
    # # mergeSort(testArray)
    # # for i in testArray:
    # #     print(i)
    # print('NOW SORT IT OUT')
    # mergeSort(testArray)
    # for i in testArray:
    #     print(i)

    # To run test SortsTestHarness on my windows machine:
    # C:\Users\staff\miniconda3\envs\DSA\python.exe E:/MASTERS/DSA/Practical09/SortsTestHarness.py 10 mr


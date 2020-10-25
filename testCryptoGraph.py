import unittest
from cryptoGraph import *

#
# class MyTestCase(unittest.TestCase):
#     def test_something(self):
#         self.assertEqual(True, False)
#
#
if __name__ == '__main__':
    # unittest.main()
    binanceData = BinanceTradingData()
    fromAsset = 'BTC'
    toAsset = 'ETH'
    validTrades = binanceData.createSkeletonGraph()
    validTrades.loadEdgeWeightsFromCurrent(binanceData)
    # allPaths = validTrades.findPathsLL(fromAsset, toAsset)
    # searchRes1 = validTrades.searchDepthFirst()
    # validTrades.displayQueueLabels(searchRes1)
    #
    # searchRes2 = validTrades.searchDepthFirst(startNode='BTC')
    # validTrades.displayQueueLabels(searchRes2)

    # z = validTrades.targetedBreadthSearch(startNode='BTC', endNode='ETH')
    # displayQueueLabels(z)

    pathContainer = validTrades.getAllPaths(fromAsset, toAsset)
    for path in pathContainer:
        print(f'{path.head.value._label}->{path.tail.value._label}: cost={path.cost}')
    # price = validTrades.getSymbolPrice('ETHBTC')
    # print(price)
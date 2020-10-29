import unittest
from cryptoGraph import *
from unittest.mock import patch
from io import StringIO




# class MyTestCase(unittest.TestCase):
#
#     def test_usage_display(self):
#
#         expected = (
#         '______________________________\n'
#         'cryptoGraph usage information:\n'
#         '______________________________\n'
#         'No arguments: display usage information\n'
#         '-r flag: Report mode. Will ask for data files, and then print statistics\n'
#         '-i flag: Interactive mode. Menu for exploring trade and asset relationships\n\n'
#         )
#
#         with patch('sys.stdout', new=StringIO()) as fake_out:  # prepare to capture console output
#
#             cryptoGraph.main()  # call the method we are testing
#             self.assertEqual(fake_out.getvalue(), expected)






#
#
if __name__ == '__main__':
    # unittest.main()

    binanceData = BinanceTradingData()
    fromAsset = 'BTC'
    toAsset = 'ETH'
    validTrades = binanceData.createSkeletonGraph()
    print(validTrades)
    for v in validTrades._vertices:
        print(v.edgeCount)
    # validTrades.loadEdgeWeightsFromCurrent(binanceData)
    # # allPaths = validTrades.findPathsLL(fromAsset, toAsset)
    # # searchRes1 = validTrades.searchDepthFirst()
    # # validTrades.displayQueueLabels(searchRes1)
    # #
    # # searchRes2 = validTrades.searchDepthFirst(startNode='BTC')
    # # validTrades.displayQueueLabels(searchRes2)
    #
    # # z = validTrades.targetedBreadthSearch(startNode='BTC', endNode='ETH')
    # # displayQueueLabels(z)
    #
    # pathContainer = validTrades.getAllPaths(fromAsset, toAsset)
    # pathContainer.sortByPrice()
    # for path in pathContainer:
    #     print(f'{path.head.value._label}->{path.tail.value._label}: cost={path.cost}')
    # # price = validTrades.getSymbolPrice('ETHBTC')
    # # print(price)



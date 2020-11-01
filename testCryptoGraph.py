import unittest
import cryptoGraph
import dataStructures
from unittest.mock import patch
from io import StringIO
import requests
import sys
import os

#####################
# HELPER FUNCTIONS

def canAccessAPI():
    """Use this to determine if the program connect to the API. THis determines what the output will be
    of some methods that we want to test"""
    url = "https://api.binance.com/api/v3/ticker/price"
    timeout = 10
    try:
        requests.get(url, timeout=timeout)
        return True

    except (requests.ConnectionError, requests.Timeout) as exception:
        return False


# class BinanceTradingDataTest(unittest.TestCase):
#
#     def setUp(self):
#         """Setup a test object"""
#         trades_24hr_filepath = '24hr.json'
#         exchangeInfo_filepath = 'exchangeInfo.json'
#         localPrices_filepath = 'price.json'
#
#         self.b = cryptoGraph.BinanceTradingData(trades_24hr_filepath, exchangeInfo_filepath, localPrices_filepath)
#
#     def test_init(self):
#         """Test that the object variables are accessible after we initialise it"""
#         self.assertEqual(self.b.trades_24hr_filepath, '24hr.json')
#
#     def test_displayTradeDetails(self):
#         """test that an Index error is raised if we try to display a trade that doesnt exist"""
#         self.assertRaises(IndexError, lambda: self.b.displayTradeDetails('INVALID_SYMBOL'))
#
#         # test that we get the first part of the expected output from a trade that does exist
#         with patch('sys.stdout', new=StringIO()) as fake_out:  # prepare to capture console output
#
#             expected = 'symbol: ETHBTC'
#             self.b.displayTradeDetails('ETHBTC')  # call the method we are testing
#             self.assertIn(expected, fake_out.getvalue())
#
#     def test_displayTradeDetailsPriceChangeCalc(self):
#         """test that the price change calculation is performed, or error message displayed"""
#         with patch('sys.stdout', new=StringIO()) as fake_out:  # prepare to capture console output
#
#             expected1 = 'The latest price from the Binance API is'
#             expected2 = 'You cannot get up to date price information at this time.'
#             self.b.displayTradeDetails('ETHBTC')  # call the method we are testing
#
#             if canAccessAPI() is True:
#                 self.b.displayTradeDetails('ETHBTC')  # call the method we are testing
#                 self.assertIn(expected1, fake_out.getvalue())
#
#             elif canAccessAPI() is False:
#                 self.b.displayTradeDetails('ETHBTC')  # call the method we are testing
#                 self.assertIn(expected2, fake_out.getvalue())
#
#     def test_getAssetTrades(self):
#         """Test that a list of Assets is output to console"""
#         with patch('sys.stdout', new=StringIO()) as fake_out:  # prepare to capture console output
#
#             expected = 'USDT, TUSD, PAX, USDC, USDS, BUSD, NGN, ' \
#                        'RUB, TRY, EUR, ZAR, BKRW, IDRT, GBP, UAH, BIDR, AUD, DAI, '
#
#             assetTrades = self.b.getAssetTrades('BTC')  # call the method we are testing
#             for quoteAsset in assetTrades:
#                 print(quoteAsset, end=', ')
#
#             self.assertEqual(expected, fake_out.getvalue())
#
#
#     def test_createSkeletonGraph(self):
#         """Assert that the method creates a CryptoGraph object"""
#         self.assertIsInstance(self.b.createSkeletonGraph(), cryptoGraph.CryptoGraph)
#
#
# class CryptoGraphTest(unittest.TestCase):
#
#     def setUp(self):
#         """Setup two test objects"""
#         trades_24hr_filepath = '24hr.json'
#         exchangeInfo_filepath = 'exchangeInfo.json'
#         localPrices_filepath = 'price.json'
#         self.b = cryptoGraph.BinanceTradingData(trades_24hr_filepath, exchangeInfo_filepath, localPrices_filepath)
#         self.g = self.b.createSkeletonGraph()
#
#     def test_loadEdgeAttributesFrom24hr(self):
#         """Test loading the volume24hr attribute into the graph edges"""
#
#         # check that the volume24hr attributes are all None
#         for e in self.g._edges:
#             self.assertIsNone(e.volume24hr)
#
#         # run the method to fill the edge weights
#         self.g.loadEdgeAttributesFrom24hr(self.b)
#
#         # check that the edge weights are all filled
#         for e in self.g._edges:
#             self.assertIsNotNone(e.volume24hr)
#
#
#     def test_loadCostFromLocalJson(self):
#         """Test loading trade costs into graph"""
#
#         # check that the edge weights are all None
#         for e in self.g._edges:
#             self.assertIsNone(e.weight)
#
#         # run the method to fill the edge weights
#         self.g.loadCostFromLocalJson(self.b)
#
#         # check that the edge weights are all filled
#         for e in self.g._edges:
#             self.assertIsNotNone(e.weight)
#
#
#
#     def test_loadEdgeWeightsFromCurrent(self):
#         """EXTENSION: this will test if the costs can be added from a GET request to the Binance API.
#         Connection errors will not crash this method, exceptions handled by first checking connection
#         with helper function"""
#
#         if canAccessAPI() is True:
#             with patch('sys.stdout', new=StringIO()) as fake_out:  # prepare to capture console output
#                 self.g.loadEdgeWeightsFromCurrent()
#                 self.assertIn('Updated graph edge weights with most recent price from Binance', fake_out.getvalue())
#
#     def test_getAllPathsSuccess(self):
#         """Test that getAllPaths returns a SortableList of TradePaths"""
#         #first load the edge costs
#         self.g.loadCostFromLocalJson(self.b)
#
#         startNode = 'ETH'   # could test for all possible combinations of assets but is very time consuming
#         endNode = 'BTC'     # will test for success, and for failure
#         result = self.g.getAllPaths(startNode, endNode)
#         self.assertIsInstance(result, cryptoGraph.SortableList)             # check what is returned
#         self.assertIsInstance(result.peekFirst(), cryptoGraph.TradePath)    # check the type of first item in list
#
#
#     def test_getAllPathsFail(self):
#         """Test that getAllPaths returns an error message and handles exceptions when passed bad data"""
#         #first load the edge costs
#         self.g.loadCostFromLocalJson(self.b)
#
#         startNode = 'BADNAME'   # test for failure
#         endNode = 'BTC'
#
#         with patch('sys.stdout', new=StringIO()) as fake_out:  # prepare to capture console output
#             self.g.getAllPaths(startNode, endNode) # run the method
#             self.assertIn('At least one of those assets does not exist', fake_out.getvalue())
#
#     def test_getTopFiveSuccess(self):
#         """Test that getAllPaths returns a SortableList of TradePaths"""
#         #first load the edge costs
#         self.g.loadCostFromLocalJson(self.b)
#
#         startNode = 'ETH'   # could test for all possible combinations of assets but is very time consuming
#         endNode = 'BTC'     # will test for success, and for failure
#         result = self.g.getTopFiveTradePathsByCost(startNode, endNode)
#         self.assertIsInstance(result, cryptoGraph.SortableList)             # check what is returned
#         self.assertIsInstance(result.peekFirst().value, cryptoGraph.TradePath)    # check the type of first item in list
#
#
#     def test_getTopFiveFail(self):
#         """Test that getAllPaths returns an error message and handles exceptions when passed bad data"""
#         #first load the edge costs
#         self.g.loadCostFromLocalJson(self.b)
#
#         startNode = 'BADNAME'   # test for failure
#         endNode = 'BTC'
#
#         self.assertRaises(ValueError, lambda: self.g.getTopFiveTradePathsByCost(startNode, endNode))
#
# class TradePathTest(unittest.TestCase):
#
#     def setUp(self):
#         """Get an actual trade path by making a graph and doing traversal"""
#         trades_24hr_filepath = '24hr.json'
#         exchangeInfo_filepath = 'exchangeInfo.json'
#         localPrices_filepath = 'price.json'
#         self.b = cryptoGraph.BinanceTradingData(trades_24hr_filepath, exchangeInfo_filepath, localPrices_filepath)
#         self.g = self.b.createSkeletonGraph()
#         self.g.loadCostFromLocalJson(self.b)
#         self.pathBox = self.g.getAllPaths('ETH', 'BTC')
#         self.t = self.pathBox.peekFirst()
#
#     def test_setup_constructor(self):
#         """Test that the tradepath was initialised correctly"""
#         self.assertIsInstance(self.t, cryptoGraph.TradePath)
#
#     def test_costAttribute(self):
#         """Test that the cost attribute is accessible, and is the correct type"""
#         self.assertIsInstance(self.t.cost, float)
#
#     def test_calculateTotalCostSuccess(self):
#         """Test that the calculateTotalCost method returns the expected float value when run on the included data"""
#         # Run the calculateTotalCost method
#         self.t.calculateTotalCost(self.g)
#
#         # based upon the default trade data json files, this value should now be
#         self.assertAlmostEqual(0.02818916, self.t.cost)
#
#     def test_calculateTotalCostNoneValues(self):
#         """Test that the system can handle a path with None values.
#         This does not happen in the current implementation of the cryptoGraph program,
#         but the method should be able to handle this. What is you tried to calculate the cost
#         of a path before filling the attributes of the edges?"""
#
#         # Make a graph with no edge weights
#         skeletonGraph = self.b.createSkeletonGraph()
#
#         # Lets get one of the TradePath objects that would be returned from that
#         pathBox = skeletonGraph.getAllPaths('ETH', 'BTC')
#         t = pathBox.peekFirst()
#
#         # see what happens when we try to calculate the cost
#         t.calculateTotalCost(skeletonGraph)
#         with patch('sys.stdout', new=StringIO()) as fake_out:  # prepare to capture console output
#             t.calculateTotalCost(skeletonGraph)
#             self.assertIn('This edge has no weight recorded.', fake_out.getvalue())


class TestStaticMethods(unittest.TestCase):

    def setUp(self):
        """Get an actual trade path by making a graph and doing traversal"""
        trades_24hr_filepath = '24hr.json'
        exchangeInfo_filepath = 'exchangeInfo.json'
        localPrices_filepath = 'price.json'
        self.b = cryptoGraph.BinanceTradingData(trades_24hr_filepath, exchangeInfo_filepath, localPrices_filepath)
        self.g = self.b.createSkeletonGraph()
        self.g.loadCostFromLocalJson(self.b)
        self.pathBox = self.g.getAllPaths('ETH', 'BTC')
        self.t = self.pathBox.peekFirst()

    def test_APIGetRequests(self):
        """Test that we can get an up to date symbol price from the Binanace API"""
        if canAccessAPI() is True:
            self.assertIsInstance(cryptoGraph.getCurrentSymbolPrice('ETHBTC'), float)
            self.assertIsInstance(cryptoGraph.getAllSymbolPrices(), list)
        else:
            print("WARNING: Please connect to internet to test API GET request methods.")

    def test_getFirstXElements(self):
        """Test that this will return the first x elements in a linked list"""

        inList = cryptoGraph.SortableList()
        inList.insertLast('A')
        inList.insertLast('B')
        inList.insertLast('C')
        inList.insertLast('D')

        result = cryptoGraph.getFirstXElements(inList, 2)
        self.assertEqual('A', result.head.value.value)
        self.assertEqual('B', result.head.next.value.value)
        self.assertIsNone(result.head.next.next)

    def test_serialize_deserialize(self):
        """Test that serializing a file to disk, and deserializing it back to an object,
        works without errors, and the object type is correct"""
        tempOut = 'temp.p'
        sys.setrecursionlimit(10000)  # this is necessary for serialisation
        cryptoGraph.serialize(tempOut, self.g)

        readInObject = cryptoGraph.deserialize(tempOut)

        # Just check the type
        # Would be useful to implement the comparison methods __eq__() and __ne__() in the CryptoGraph class
        self.assertIsInstance(readInObject, cryptoGraph.CryptoGraph)

        # delete the temp file and reset the recursion limit
        os.remove(tempOut)
        sys.setrecursionlimit(1500)









if __name__ == '__main__':
    unittest.main()


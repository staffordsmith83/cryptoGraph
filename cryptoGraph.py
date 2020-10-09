import json
import DSAGraphs_modified
from linkedLists import *
from adts_LLversion import *


class CryptoGraph(DSAGraphs_modified.DSAGraphWithEdges):
    """Inherits from DSAGraph implementation developed by Stafford Smith for Practical 6,
    Data Structures and Algorithms unit, Curtin University, 2020.
    Changes are edge weights are now implemented, to store the exchange rates between
    cryptocurrencies"""
    ...


class CryptoGraphVertex(DSAGraphs_modified.DSAGraphVertex):
    """Inherits from DSAGraphVertex implementation developed by Stafford Smith for Practical 6,
    Data Structures and Algorithms unit, Curtin University, 2020"""
    ...
    # TODO cant find a way to change the implementation of GraphVertex from outside of the class.
    # DSADirecitonalGraph calls DSAGrashVertex, we need it to call our modified CryptoGraphVertex instead...
    # for now rewrite.


class BinanceTradingData:
    """Object that takes json data from Binance.com and creates an up to date snapshot
    of trading prices from the website.
    Data is currently offline but could be made to request up to date data with GET requests
    through the Binance REST API. Basically, an instance of this object holds the raw data,
    the methods to parse it, the methods to display it, and the methods to create a graph from it"""

    def __init__(self):
        # TODO: implement get data from API to initialize
        self.trades_filepath = 'binance_json/24hr.json'
        self.exchangeInfo_filepath = 'binance_json/exchangeInfo.json'

    def displayTradeDetails(self, tradeIdx=1, symbol='BTCETH'):
        """as per 'find and display trade details' requirement
        TODO modify this to operate on symbol names"""
        with open(self.trades_filepath) as json_file:
            trades = json.load(json_file)  # trades is a list of dictionaries, one for each trading pair

        for k, v in trades[tradeIdx].items():
            print(f'{k}: {v}')

    def createSkeletonGraph(self):
        with open(self.exchangeInfo_filepath) as json_file:
            ei = json.load(json_file)

        validTrades = DSAGraphs_modified.DSAGraphWithEdges()
        for symbol in ei['symbols']:

            if symbol["isSpotTradingAllowed"] is True:
                validTrades.addEdge(symbol['baseAsset'], symbol['quoteAsset'])
            elif symbol["isMarginTradingAllowed"] is True:
                validTrades.addEdge(symbol['baseAsset'], symbol['quoteAsset'])

        return validTrades

    #TODO: rewrite as a member of the graph class
    def pushEdgeWeightsToSkeleton(self, skeleton):
        with open(self.trades_filepath) as json_file:
            trades = json.load(json_file)  # trades is a list of dictionaries, one for each trading pair

            for e in skeleton._edges:
                symbol = e.fromVertex._label + e.toVertex._label

                for t in trades:
                    if t.symbol == symbol:
                        # set the weight!
                        e.weight = t.weightedAveragePrice


if __name__ == "__main__":
    latestBinanceData = BinanceTradingData()
    latestBinanceData.displayTradeDetails(tradeIdx=1)

    validTrades = latestBinanceData.createSkeletonGraph()
    # BinanceTradingData.pushEdgeWeightsToSkeleton(validTrades)
    validTrades.getEdgeWeightsFromBinance(latestBinanceData)

    # validTrades.displayAsMatrix()

    print(validTrades.verticesCount)
    print(validTrades.edgeCount)

    validTrades.displayEdges()
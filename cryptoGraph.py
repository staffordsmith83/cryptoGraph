import json
import DSAGraphs_modified
from linkedLists import *
from adts_LLversion import *

class Menu:
    def __init__(self, title, instructions=''):
        self.title = title
        self.instructions = instructions
        self.items = DSALinkedList()
        self.count = 0

    def addItem(self, menuItem):
        self.items.insertLast(menuItem)
        self.count += 1

    def display(self):
        print('\n__________________________________')
        print(self.title)
        print(self.instructions)
        for number, menuItem in enumerate(self.items):
            print(number, menuItem.name)


class MenuItem:
    def __init__(self, name, action):
        self.name = name
        self.action = action


class CryptoGraph(DSAGraphs_modified.DSAGraphWithEdges):
    """Inherits from DSAGraph implementation developed by Stafford Smith for Practical 6,
    Data Structures and Algorithms unit, Curtin University, 2020.
    This subclass adds a method to load edge weights from Binance trading data,
    the edge weights are a float datatype, that hold the average trading price from the last 24 hours."""

    def loadEdgeWeightsFromBinance(self, binanceDataObject):
        with open(binanceDataObject.trades_filepath) as json_file:
            trades = json.load(json_file)  # trades is a list of dictionaries, one for each trading pair

            for e in self._edges:
                # symbol = e.fromVertex._label + e.toVertex._label
                symbol = self.getVertex(e.fromVertex)._label + self.getVertex(e.toVertex)._label

                for t in trades:
                    if t['symbol'] == symbol:
                        # set the weight!
                        e.weight = t['weightedAvgPrice']


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

        validTrades = CryptoGraph()
        for symbol in ei['symbols']:

            if symbol["isSpotTradingAllowed"] is True:
                validTrades.addEdge(symbol['baseAsset'], symbol['quoteAsset'])
            elif symbol["isMarginTradingAllowed"] is True:
                validTrades.addEdge(symbol['baseAsset'], symbol['quoteAsset'])

        return validTrades


def loadData(binanceDataObject):

    validTrades = binanceDataObject.createSkeletonGraph()
    validTrades.loadEdgeWeightsFromBinance(binanceDataObject)

if __name__ == "__main__":
    # setup, should I just put this in init?
    latestBinanceData = BinanceTradingData()

    # setup the menu
    mainMenu = Menu(title='Welcome to cryptoGraph', instructions='Please select an operation:')
    mainMenu.addItem(MenuItem(name='Blank', action=None))
    mainMenu.addItem(MenuItem(name='Load Trade Data', action=loadData(latestBinanceData)))
    mainMenu.addItem(MenuItem(name='Display Trade Details', action=latestBinanceData.displayTradeDetails(tradeIdx=1)))

    # show the menu
    mainMenu.display()

    # TODO NEXT: user input and then execute actions from menu


    #
    # # validTrades.displayAsMatrix()
    #
    # print(validTrades.verticesCount)
    # print(validTrades.edgeCount)
    #
    # validTrades.displayEdges()
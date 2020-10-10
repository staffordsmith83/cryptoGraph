import json
import DSAGraphs_modified
from linkedLists import *
from adts_LLversion import *
import sys

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

    def findPaths(self, start, end, path=[]):
        # TODO: remove python list and use my LinkedList data container
        # TODO: add edge weights as a total
        path = path + [start]
        if start == end:
            return [path]
        if not self.hasVertex(start):
            return []
        paths = []
        for node in self.getAdjacent(start):
            if node._label not in path:
                newpaths = self.findPaths(node._label, end, path)
                for newpath in newpaths:
                    paths.append(newpath)
        return paths
        
    def findPathsLL(self, start, end, path=DSALinkedList()):
        """Build a list of symbols instead"""
        path.insertLast(start)
        if start == end:
            return path
        if not self.hasVertex(start):
            return None
        paths = DSALinkedList()
        for node in self.getAdjacent(start):
            if not path.contains(node._label):
                newpaths = self.findPathsLL(node._label, end, path)
                for newpath in newpaths:
                    paths.insertLast(newpath)
        # TODO: paths should be a llist or llists. We should be inserting the hole llist object at the end...
        # why is it returning a single level list?
        return paths


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

    def getAssetInfo(self, assetName):
        with open(self.exchangeInfo_filepath) as json_file:
            ei = json.load(json_file)

        assetPossibleTrades = DSALinkedList()
        for symbol in ei['symbols']:

            if symbol["baseAsset"] == assetName:
                assetPossibleTrades.insertLast(symbol["quoteAsset"])

        return assetPossibleTrades


def loadData(binanceDataObject):
    validTrades = binanceDataObject.createSkeletonGraph()
    validTrades.loadEdgeWeightsFromBinance(binanceDataObject)


def displayUsage():
    print(
        '______________________________\n'
        'cryptoGraph usage information:\n'
        '______________________________\n'
        'No arguments: display usage information\n'
        '-r flag: Report mode. Will ask for data files, and then print statistics\n'
        '-i flag: Interactive mode. Menu for exploring trade and asset relationships\n'
    )
    exit()


def runInteractiveMenu():
    user_choice = '0'
    while not user_choice == '9':
        print('\n\nINTERACTIVE MODE MENU')
        print('1. Load data')
        print('2. Find and display an asset')
        print('3. Find and display trade details')
        print('4. Find and display potential trade paths')
        print('5. Set asset filter')
        print('6. Asset overview')
        print('7. Trade overview')
        print('8. Save data (serialised)')
        print('9. Exit')

        user_choice = input('Please make a user_choice: ')

        if user_choice == '1':
            print('Loading latest Binance trading data from file')
            binanceData = BinanceTradingData()
        elif user_choice == '2':
            assetCode = input('Specify the asset code:')
            try:
                assetTrades = binanceData.getAssetInfo(assetCode)
                print(f'Possible trades for asset:{assetCode} are:')
                for quoteAsset in assetTrades:
                    print(quoteAsset, end=', ')
            except UnboundLocalError as ule:
                print(ule)
                print("Please run the 'Load data' option from the menu first.")
        elif user_choice == '3':
            fromAsset = input('Please specify the From Asset for your trade path:')
            toAsset = input('Please specify the To Asset for your trade path:')
            validTrades = binanceData.createSkeletonGraph()
            validTrades.loadEdgeWeightsFromBinance(binanceData)
            allPaths = validTrades.findPathsLL(fromAsset, toAsset)
            for path in allPaths:
                print(path)
            # print('\n________________________\n'
            #       f'There are {len(allPaths)} possible trade paths for this trade.') # no len for LL
        elif user_choice == '4':
            print('Do Something')
        else:
            print('I dont understand your user_choice.')



def runReportMode():
    ...


if __name__ == "__main__":

    # Handle commandline arguments

    if len(sys.argv) == 1:
        displayUsage()
    elif len(sys.argv) == 2:

        if sys.argv[1] == '-r':
            print('Report Mode')
        elif sys.argv[1] == '-i':
            runInteractiveMenu()
        else:
            print('Commandline argument not recognised')

    else:
        print('Incorrect number of arguments, refer to usage:')
        displayUsage()













    # TODO NEXT: user input and then execute actions from menu

    #
    # # validTrades.displayAsMatrix()
    #
    # print(validTrades.verticesCount)
    # print(validTrades.edgeCount)
    #
    # validTrades.displayEdges()

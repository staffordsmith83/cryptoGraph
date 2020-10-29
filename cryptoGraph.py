############################################
# IMPORTS
############################################


import json
import requests  # for web requests extended functionality only
import sys
from copy import deepcopy  # TODO: reimplement to not use deepcopy
import os
from dataStructures import *
import pickle


############################################
# CLASSES
############################################


class BinanceTradingData:
    """Object that takes json data from Binance.com and creates an up to date snapshot
    of trading prices from the website.
    Data is currently offline but could be made to request up to date data with GET requests
    through the Binance REST API. Basically, an instance of this object holds the raw data,
    the methods to parse it, the methods to display it, and the methods to create a graph from it"""

    def __init__(self,
                 trades_24hr_filepath='binance_json/24hr.json',
                 exchangeInfo_filepath='binance_json/exchangeInfo.json'
                 ):
        # TODO: implement get data from API to initialize
        self.trades_24hr_filepath = trades_24hr_filepath
        self.exchangeInfo_filepath = exchangeInfo_filepath

    def displayAllTradeDetails(self, tradeIdx=1, symbol='BTCETH'):
        """as per 'find and display trade details' requirement
        TODO modify this to operate on symbol names"""
        with open(self.trades_24hr_filepath) as json_file:
            trades = json.load(json_file)  # trades is a list of dictionaries, one for each trading pair

        for k, v in trades[tradeIdx].items():
            print(f'{k}: {v}')

    def displayTradeDetails(self, symbol):
        """as per 'find and display trade details' requirement
        TODO modify this to operate on symbol names"""
        with open(self.trades_24hr_filepath) as json_file:
            trades = json.load(json_file)  # trades is a list of dictionaries, one for each trading pair

            tradeCount = 0
            for i in trades:
                if i['symbol'] == symbol:
                    tradeDetails = i
                    tradeCount += 1

        if tradeCount == 0:
            raise IndexError('No trades for this symbol in the last 24 hours.')

        else:
            "Here is summary information for this trade symbol, over the last 24 hours"
            for k, v in tradeDetails.items():
                print(f'{k}: {v}')

        try:
            oldPrice = float(tradeDetails['weightedAvgPrice'])
            updatedPrice = getSymbolPrice(symbol)
            print(f'The latest price from the Binance API is: {updatedPrice}')
            priceDifference = (updatedPrice - oldPrice) / oldPrice * 100
            priceDifference = round(priceDifference, 2)
            if priceDifference < 0:
                print(
                    f'The current price is approximately {-priceDifference}% less than the last 24hr weighted average.')
            if priceDifference == 0:
                print(f'The current price is equal to the past 24hr weighted average.')
            if priceDifference > 0:
                print(
                    f'The current price is approximately {priceDifference}% more than the last 24hr weighted average.')


        except ValueError as ve:
            print(ve)

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

    def getAssetTrades(self, assetName):
        with open(self.exchangeInfo_filepath) as json_file:
            ei = json.load(json_file)

        assetPossibleTrades = DSALinkedList()
        for symbol in ei['symbols']:

            if symbol["baseAsset"] == assetName:
                assetPossibleTrades.insertLast(symbol["quoteAsset"])

        return assetPossibleTrades


class CryptoGraph(DSAGraphWithEdges):
    """Inherits from DSAGraph implementation developed by Stafford Smith for Practical 6,
    Data Structures and Algorithms unit, Curtin University, 2020.
    This subclass adds a method to load edge weights from Binance trading data,
    the edge weights are a float datatype, that hold the average trading price from the last 24 hours.
    """

    def loadEdgeAttributesFrom24hr(self, binanceDataObject):
        with open(binanceDataObject.trades_24hr_filepath) as json_file:
            trades = json.load(json_file)  # trades is a list of dictionaries, one for each trading pair

            for e in self._edges:
                # symbol = e.fromVertex._label + e.toVertex._label
                symbol = self.getVertex(e.fromVertex)._label + self.getVertex(e.toVertex)._label

                for t in trades:
                    if t['symbol'] == symbol:
                        # set the weight!
                        e.weight = float(t['weightedAvgPrice'])
                        e.volume24hr = float(t['volume'])
                        e.percentPriceChange24hr = float(t['priceChangePercent'])

    def loadEdgeWeightsFromCurrent(self):
        prices = getAllSymbolPrices()

        for e in self._edges:
            # symbol = e.fromVertex._label + e.toVertex._label
            symbol = self.getVertex(e.fromVertex)._label + self.getVertex(e.toVertex)._label

            for t in prices:
                if t['symbol'] == symbol:
                    # set the weight!
                    e.weight = t['price']

    def getAllPaths(self, startNode, endNode):
        path = TradePath()
        pathContainer = SortableList()
        try:
            u = self.getVertex(startNode)
            d = self.getVertex(endNode)

            for v in self._vertices:
                v.clearVisited()

            self._getAllPathsRec(u, d, path, pathContainer)

            print('Found all Paths')
            return pathContainer

        except ValueError as ve:
            print('One of those assets does not exist')

    def _getAllPathsRec(self, u, d, path, pathContainer):
        # TODO: implement without using deepcopy
        u.setVisited()
        path.insertLast(u)

        if u._label == d._label:  # if we have got to the destination vertex
            completePath = deepcopy(
                path)  # problem here with mutable path object! Using deepcopy but perhaps reimplement
            completePath.calculateTotalCost(self)
            pathContainer.insertLast(completePath)  # add this complete path to the self.tempPaths attribute NOT WORKING

            # TODO: replace this with a method that calculates the path cost, and stores it in the object.
            # TODO: Then retrieve the whole container, sort it by cost order, and print top 10 lowest cost paths.
            # self.displayPathAndCost(path)


        else:
            for i in self.getAdjacent(u._label):  # get adjacent takes the label

                if not i._visited:
                    self._getAllPathsRec(i, d, path, pathContainer)

        path.removeLast()
        u.clearVisited()

    def displayPathAndCost(self, path):
        commission = 0.001
        pathstring = ''
        pathcost = 1
        fromLabel = None  # the first toLabel will be the label of the head
        toLabel = path.head.value._label
        for i in path:

            if fromLabel is None:
                # print('this is the first node, moving to the next one in the list to get the first edge')
                fromLabel = toLabel  # increment so that the from Label is now the first list item
                pathstring = i._label
            else:
                pathstring = f'{pathstring} > {i._label}'
                fromLabel = toLabel
                toLabel = i._label
                cost = float(self.getEdgeValue(fromLabel, i._label))
                if cost == 0.0:
                    print('Be careful, no edge weight recorded for this trade')
                    cost = 1.0

                pathcost = pathcost * cost
                pathcost = pathcost - pathcost * commission  # ignore commission for now

        print(f'{pathstring} cost = {pathcost}')

        print('\n')

    def getEdgeValue(self, fromVertex, toVertex, attribute='weight'):

        e = self.getEdge(fromVertex, toVertex)
        if attribute == 'weight':
            return e.weight

    def getTopFiveTradePathsByCost(self, fromAsset, toAsset):

        pathContainer = self.getAllPaths(fromAsset, toAsset)
        if pathContainer is not None:
            pathContainer.sortByAttribute(attribute='cost', order='low')
            topFiveByCost = getFirstXElements(pathContainer, 5)

            return topFiveByCost


    def __repr__(self):
        return f'Cryptograph with {self.edgeCount} edges, and {self.verticesCount} vertices'


class TradePath(DSALinkedListDE):
    def __init__(self):
        self.head = None
        self.tail = None  # added for doubly-ended implementation
        self.cost = 0

    def calculateTotalCost(self, tradeGraph):

        commission = 0.001
        # pathstring = ''
        pathcost = 1
        fromLabel = None  # the first toLabel will be the label of the head
        toLabel = self.head.value._label
        for i in self:

            if fromLabel is None:
                fromLabel = toLabel  # increment so that the from Label is now the first list item

            else:
                fromLabel = toLabel
                toLabel = i._label
                # TODO next line may be inefficient... are we searching all edges in the graph, or is it targeted?
                cost = float(tradeGraph.getEdgeValue(fromLabel, i._label))
                if cost == 0.0:
                    raise ValueError('Be careful, no edge weight recorded for this trade')

                pathcost = pathcost * cost
                # pathcost = pathcost - pathcost * commission  # ignore commission for now

        # Now set the self.cost attribute to be our calculated total cost!
        self.cost = pathcost




############################################
# STATIC METHODS/ FUNCTIONS
############################################

def getSymbolPrice(symbol):
    """Takes a trade symbol as a string, and performs a GET request.
    Return the current trade price as a float"""
    baseUrl = 'https://api.binance.com/api/v3/ticker/price?symbol='
    requestUrl = baseUrl + symbol
    print("Making Web Request for Latest Price Info...")
    resp = requests.get(requestUrl)
    if resp.status_code != 200:
        # This means something went wrong.
        raise ValueError
    print("Latest Price Info Received from Binance API")
    return float(resp.json()['price'])


def getAllSymbolPrices():
    """Returns all current trade prices"""
    requestUrl = 'https://api.binance.com/api/v3/ticker/price'
    print("Making Web Request for Latest Price Info...")

    try:
        resp = requests.get(requestUrl)
        if resp.status_code != 200:
            # This means something went wrong.
            raise ValueError
        print("Latest Price Info Received from Binance API")
        return resp.json()

    except ConnectionError as ce:
        print('Could not connect to internet' + str(ce))


def getFirstXElements(inList, x):
    outList = DSALinkedListDE()
    currNode = inList.head
    for i in range(x):
        currNode = _getFirstXElementsRec(currNode, outList)

    return outList


def _getFirstXElementsRec(currNode, outList):
    outList.insertLast(currNode)
    currNode = currNode.next

    return currNode


def loadData(binanceDataObject):
    validTrades = binanceDataObject.createSkeletonGraph()
    validTrades.loadEdgeAttributesFrom24hr(binanceDataObject)


def serialize(path, myObject):
    print("Saving Object to File...")
    try:
        with open(path, "wb") as dataFile:
            pickle.dump(myObject, dataFile)
    except IOError:
        print("Error: problem pickling object!")


def deserialize(path):
    print("Reading Object from File...")
    try:
        with open(path, "rb") as dataFile:
            inObject = pickle.load(dataFile)
    except IOError:
        print("Error: Object file does not exist!")

    return inObject



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


def runInteractiveMenu(binanceData=None):
    user_choice = '0'
    while not user_choice == '13':
        print('\n\nINTERACTIVE MODE MENU')
        print('1. Load data from user specified files')
        print('2. Update price data to latest using Binance API')
        print('3. Find and display an asset')
        print('4. Find and display trade details')
        print('5. Find and display potential trade paths')
        print('6. Find the top 5 trade paths by cost')
        print('7. Set asset filter')
        print('8. Asset overview')
        print('9. Trade overview')
        print('10. Check for Possible Profitable Trade Paths...')
        print('11. Save data (serialised)')
        print('12. Reload graph from saved serialised graph object')
        print('13. Exit')

        user_choice = input('Please make a user_choice: ')
        #######################################
        if user_choice == '1':

            # TODO: use user input lines instead of predetermined paths
            # trades_24hr_filepath = input("Specify the path to the 24hr trades json file")
            # exchangeInfo_filepath = input("Specify the path to the exchange info json file")

            trades_24hr_filepath = 'binance_json/24hr.json'
            exchangeInfo_filepath = 'binance_json/exchangeInfo.json'

            print('Loading Binance trading data from file')
            binanceData = BinanceTradingData(trades_24hr_filepath, exchangeInfo_filepath)
            print('Building graph data structure using vertices from exchange info json file...')
            validTrades = binanceData.createSkeletonGraph()
            print('DONE')
            print('Loading trade attributes from 24hr json file...')
            validTrades.loadEdgeAttributesFrom24hr(binanceData)
            print('DONE')

        #######################################

        elif user_choice == '2':
            try:
                validTrades.loadEdgeWeightsFromCurrent()
                print('Updated graph edge weights with most recent price from Binance')

            except UnboundLocalError as ule:
                print(ule)
                print("Please run the 'Load data' option from the menu first.")

            except ConnectionError as ce:
                print('Could not connect to internet' + str(ce))

        #######################################

        elif user_choice == '3':
            assetCode = input('Specify the asset code:')
            try:
                assetTrades = binanceData.getAssetTrades(assetCode)
                print(f'Possible trades for asset:{assetCode} are:')
                for quoteAsset in assetTrades:
                    print(quoteAsset, end=', ')

            except UnboundLocalError as ule:
                print(ule)
                print("Please run the 'Load data' option from the menu first.")

        #######################################

        elif user_choice == '4':
            fromAsset = input('Please specify the From Asset for your trade pair:')
            toAsset = input('Please specify the To Asset for your trade pair:')
            tradeSymbol = fromAsset + toAsset
            try:
                binanceData.displayTradeDetails(symbol=tradeSymbol)

            except IndexError as ie:
                print(ie)

        #######################################

        elif user_choice == '5':
            fromAsset = input('Please specify the From Asset for your trade path:')
            toAsset = input('Please specify the To Asset for your trade path:')
            try:
                pathContainer = validTrades.getAllPaths(fromAsset, toAsset)
                for path in pathContainer:
                    # print(f'{path.head.value._label}->{path.tail.value._label}: cost={path.cost}')
                    for v in path:
                        print(v._label + '>', end='')
                    print(path.cost)

            except UnboundLocalError as ule:
                print(ule)
                print("Please run the 'Load data' option from the menu first.")

        #######################################

        elif user_choice == '6':
            fromAsset = input('Please specify the From Asset for your trade path:')
            toAsset = input('Please specify the To Asset for your trade path:')

            try:
                topFiveByCost = validTrades.getTopFiveTradePathsByCost(fromAsset, toAsset)

                print('Here are the top 5 paths, lowest in price:')
                for path in topFiveByCost:
                    for v in path.value:
                        print(v._label + '>', end='')
                    print(path.value.cost)

            except UnboundLocalError as ule:
                print(ule)
                print("Please run the 'Load data' option from the menu first.")


        #######################################

        elif user_choice == '7':
            # TODO: NOT WORKING, 'DSAListNode object is not callable' error or something...

            # Do not build valid trades everytime, or we lose previous exclusions!

            excludeAsset = ' '
            while not excludeAsset == '':
                excludeAsset = input(
                    'Enter an Asset Code to remove it from the available options, hit return to finish:')

                if validTrades.hasVertex(excludeAsset):
                    validTrades.removeVertex(excludeAsset)
                    print(f'Asset {excludeAsset} removed from the Graph')


        #######################################

        elif user_choice == '8':
            """Asset Overview, we do not have very much information, 
            so provide a summary which ones have the most possible trades"""

            try:
                candidateAssets = validTrades._vertices
                candidateAssets.sortByAttribute(attribute='edgeCount', order='high')

                print('Here are the top 5 assets for number of outward allowable trades:')
                assetCount = 0
                for asset in candidateAssets:
                    assetCount += 1
                    print(f'Asset: {asset._label}, Number of Edges: {asset.edgeCount}')
                    if assetCount >= 5:
                        break


            except UnboundLocalError as ule:
                print(ule)
                print("Please run the 'Load data' option from the menu first.")

        #######################################

        elif user_choice == '9':
            # TODO: put the following in a function that the choice calls
            """Trade overview, lists:
            The top 10 highest volume of trades for last 24hrs,
            The top 10 highest avg weighted price for the last 24hrs.
            The top 10 highest for price change over last 24hrs
            This could be stored in edges...
            self.volume24hr
            self.avgPrice24hr
            self.percentPriceChange24hr
            """
            candidateTrades = validTrades._edges
            candidateTrades.sortByAttribute(attribute="volume24hr", order="high")
            highestVolumeTrades = getFirstXElements(candidateTrades, 5)

            print('Here are the top 5 trades by volume in the last 24hrs:')
            for t in highestVolumeTrades:
                print(t.value.fromVertex, t.value.toVertex, t.value.volume24hr)

            candidateTrades.sortByAttribute(attribute="percentPriceChange24hr", order="high")
            highestChangeTrades = getFirstXElements(candidateTrades, 5)

            print('Here are the top 5 trades by percentage price change in the last 24hrs:')
            for t in highestChangeTrades:
                print(t.value.fromVertex, t.value.toVertex, t.value.percentPriceChange24hr)


        #######################################

        elif user_choice == '10':
            # TODO: Maximum recursion depth exceeded here
            """For the 10 trades with highest volume in the last 24hrs, report if an indirect trade route exists that
            is cheaper than the direct trade route."""

            print('WARNING: This operation is processor intensive, and will take some time. Please be patient.')
            try:

                for trade in highestVolumeTrades:
                    fromLabel = trade.value.fromVertex
                    toLabel = trade.value.toVertex
                    symbol = fromLabel + toLabel

                    topFiveByCost = validTrades.getTopFiveTradePathsByCost(trade.value.fromVertex, trade.value.toVertex)
                    # topFiveByCost = validTrades.getTopFiveTradePathsByCost('ETH', 'BTC')

                    if topFiveByCost.peekFirst().value.cost != trade.value.weight:
                        print("ALERT: Possible Profitable Trade Path...")
                        print('Here are the top 5 paths, lowest in price:')
                        for path in topFiveByCost:
                            for v in path.value:
                                print(v._label + '>', end='')
                            print(path.value.cost)

            except UnboundLocalError as ule:
                print('Please try running the trade overview function first')



        #######################################

        elif user_choice == '11':
            """Save the trade graph by serialisation. Also save the binance data object?"""
            if not os.path.exists('data'):
                os.makedirs('data')
            graph_outFilename = 'data/latestGraph.p'
            serialize(graph_outFilename, validTrades)
            print(f'Saved trades graph object to {graph_outFilename}')

            ...

        #######################################

        elif user_choice == '12':

            print("Replacing trading graph object with last saved version...")
            try:
                validTrades = deserialize(graph_outFilename)

            except UnboundLocalError as e:
                print('Please ensure there is a saved trade graph to reload...')


        #######################################

        elif user_choice == '13':

            print("Ending Session")

            sys.exit()

        #######################################

        else:
            print('I dont understand your user_choice.')


def runReportMode():
    """Takes two commandline arguments <asset_file> and <trade_file>.
    Then runs statistics on the dataset and outputs."""

    # TODO
    ...


############################################
# MAIN FUNCTION
############################################


def main():
    # Up the recursion limit
    sys.setrecursionlimit(10000)

    # Handle commandline arguments

    if len(sys.argv) == 1:
        displayUsage()
    elif len(sys.argv) == 2:

        if sys.argv[1] == '-r':
            runReportMode()
        elif sys.argv[1] == '-i':
            runInteractiveMenu()
        else:
            print('Commandline argument not recognised')

    else:
        print('Incorrect number of arguments, refer to usage:')
        displayUsage()


############################################
# RUN IT...
############################################

if __name__ == "__main__":
    main()

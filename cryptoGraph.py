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


    def getAllPaths(self, startNode, endNode, path=DSALinkedList()):

        try:
            u = self.getVertex(startNode)
            d = self.getVertex(endNode)

            for v in self._vertices:
                v.clearVisited()

            self.getAllPathsRec(u, d, path)

            print('Found all Paths')

        except ValueError as ve:
            print('One of those assets does not exist')



    def getAllPathsRec(self, u, d, path):

        u.setVisited()
        path.insertLast(u)

        if u._label == d._label:                # if we have got to the destination vertex
            self.tempPaths.insertLast(path)     # add this complete path to the self.tempPaths attribute NOT WORKING
            self.displayPathEdges(path)
        else:
            for i in self.getAdjacent(u._label):  # get adjacent takes the label

                if not i._visited:
                    self.getAllPathsRec(i, d, path)

        path.removeLast()
        u.clearVisited()

    def displayPathEdges(self, path):
        commission = 0.001
        pathstring = ''
        pathcost = 0
        fromLabel = path.head.value._label  # the first toLabel will be the label of the head
        for i in path:

            pathstring = f'{pathstring} > {i._label}'
            # if i == path.head:
            #     ...
            # else:
            #     cost = self.getEdgeValue(fromLabel, i._label)
            #
            #     pathcost = pathcost * cost
            #     pathcost = pathcost - pathcost * commission
            #
            #     fromLabel = i._label

        print(f'{pathstring} cost = {pathcost}')

        print('\n')

    def getEdgeValue(self, fromVertex, toVertex, attribute='weight'):

        e = self.getEdge(fromVertex, toVertex)
        if attribute == 'weight':
            return e.weight

    def targetedBreadthSearch(self, startNode, endNode):
        """NB This returns a queue of objects."""
        # mark all vertices as unvisited
        vertices = self._vertices
        for v in vertices:
            v.clearVisited()

        # establish our output container
        t = Queue()

        # pick one of the vertices to start with
        v = self.getVertex(startNode)
        e = self.getVertex(endNode)
        # mark the source node as visited and enqueue it
        t.enqueue(v)
        v.setVisited()

        # make a traversal queue that loads up items to check
        q = Queue()
        q.enqueue(v)

        # while the queue is not empty:
        while not q.isEmpty():
            # while v has another vertex in its links to look at:
            v = q.dequeue()

            if v == e:
                t.enqueue(v)
                print('Found the end node')
                return t

            else:
                for w in self.getAdjacent(v._label):
                    if not w._visited:
                        t.enqueue(w)  # the output queue
                        w.setVisited()

                        q.enqueue(w)

        return t

    def targetedDepthSearch(self, startNode):
        """NB This returns a queue of objects."""
        # mark all vertices as unvisited
        vertices = self._vertices
        for v in vertices:
            v.clearVisited()

        # establish the output container
        t = Queue()

        # pick one of the vertices to start with
        v = self.getVertex(startNode)
        # mark the source node as visited and enqueue it
        t.enqueue(v)
        v.setVisited()

        # make a traversal stack of items to check
        s = Stack()
        s.push(v)

        # while the stack is not empty:
        while not s.isEmpty():

            # while v has another vertex in its links to look at:
            v = s.top()
            if any(link._visited is False for link in self.getAdjacent(v._label)):

                for w in self.getAdjacent(v._label):

                    if not w._visited:
                        t.enqueue(w)
                        w.setVisited()

                        s.push(w)
                        v = w  # need to make the operation move to the links of w now
                        break  # stop going through the links of v now and switch to the links of w

            else:
                v = s.pop()  # only pop when we have gone through all items in that item.
        return t

    def __repr__(self):
        return f'Cryptograph with {self.edgeCount} edges, and {self.verticesCount} vertices'


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

    def displayAllTradeDetails(self, tradeIdx=1, symbol='BTCETH'):
        """as per 'find and display trade details' requirement
        TODO modify this to operate on symbol names"""
        with open(self.trades_filepath) as json_file:
            trades = json.load(json_file)  # trades is a list of dictionaries, one for each trading pair

        for k, v in trades[tradeIdx].items():
            print(f'{k}: {v}')

    def displayTradeDetails(self, symbol):
        """as per 'find and display trade details' requirement
        TODO modify this to operate on symbol names"""
        with open(self.trades_filepath) as json_file:
            trades = json.load(json_file)  # trades is a list of dictionaries, one for each trading pair

            tradeCount = 0
            for i in trades:
                if i['symbol'] == symbol:
                    tradeDetails = i
                    tradeCount += 1

        if tradeCount == 0:
            raise IndexError('No trades for this symbol in the last 24 hours.')

        else:
            # print(f'In the last 24 hours there have been {tradeCount} trades for the trade {symbol}.'
            #       f'The last recorded trade has the following information:')

            for k, v in tradeDetails.items():
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

class GraphPath(DSALinkedListDE):
    """ Inherits from DSALInkedLists but adds an instance attribute of totalCost
    Specialised to contain cryptoGraph edge objects"""
    def __init__(self):
        self.head = None
        self.tail = None  # added for doubly-ended implementation
        self.totalCost = 0


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


def runInteractiveMenu(binanceData=None):
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
            print('Building graph data structure')
            validTrades = binanceData.createSkeletonGraph()
            validTrades.loadEdgeWeightsFromBinance(binanceData)
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
            fromAsset = input('Please specify the From Asset for your trade pair:')
            toAsset = input('Please specify the To Asset for your trade pair:')
            tradeSymbol = fromAsset + toAsset
            try:
                tradeDetails = binanceData.displayTradeDetails(symbol=tradeSymbol)

            except IndexError as ie:
                print(ie)

        elif user_choice == '4':
            fromAsset = input('Please specify the From Asset for your trade path:')
            toAsset = input('Please specify the To Asset for your trade path:')
            # try:
            validTrades.getAllPathEdges(fromAsset, toAsset)
            print(validTrades.tempPaths)
            # except UnboundLocalError as ule:
            #     print(ule)
            #     print("Please run the 'Load data' option from the menu first.")


        elif user_choice == '5':
            # Do not build valid trades everytime, or we lose previous exclusions!
            # validTrades = binanceData.createSkeletonGraph()

            excludeAsset = ' '
            while not excludeAsset == '':
                excludeAsset = input('Enter an Asset Code to remove it from the available options, hit return to finish:')

                if validTrades.hasVertex(excludeAsset):
                    validTrades.removeVertex(excludeAsset)
                    print(f'Asset {excludeAsset} removed from the Graph')

            # load the edge weights last so we're only doing it for the ones we need to
            # validTrades.loadEdgeWeightsFromBinance(binanceData)








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


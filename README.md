# cryptoGraph
A python program to analyse cryptocurrency trading data. Done as part of Data Structures and Algorithms unit at Curitn University.

For input data, the software uses either local .json files containing data pulled from the Binance API, or provides a means for the user to request up to date information using the Binance API. The data is loaded into a vanilla implementation of a graph data structure, to facilitate least cost path analysis between tradeable cryptocurrencies. Summaries and path analyses can be performed, and the main objects can be serialized to file.



_______________________________

## Included in this folder:

    1   cryptoGraph.py - This is the main program, with the main code, and has extra classes. Some custom class definitions that inherit from the more general class definitions in dataStructures.py.

    2   dataStructures.py - Contains modified implementations of data structures developed for the Curtin University of Technology unit Data Structures and Algorithms COMP5008, done as part of a GDip in Geospatial Intelligence course.

    3   testCryptoGraph.py - Unit testing framework for the methods in cryptoGraph.py. The classes and methods in dataStructures.py are assumed to be tested.

    4   README.md - this file, in markdown format, to be readable on GitHub.

    5   .gitignore - for obvious reasons.

    6   binance_json/24hr.json - a data file containing 
    
    7   binance_json/exchangeInfo.json

    8   Report.pdf

    9   Coversheet.pdf
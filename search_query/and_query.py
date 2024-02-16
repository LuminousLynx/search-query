from __future__ import annotations

from search_query.node import Node
from search_query.query import Query
from search_query.tree import Tree


class AND_Query(Query):
    def __init__(self, qs, nestedQueries, searchField):
        self.qs = qs
        self.nestedQueries = nestedQueries
        self.searchField = searchField
        self.qt = Tree(Node("AND", True))
        self.buildQueryTree()
        if(self.validTreeStructure(self.qt.root)):
            self.qt.removeAllMarks()
            for nq in nestedQueries:
                nq.qt.removeAllMarks()
            print("Valid Tree")
        else:
            print("else was executed")
            raise Exception("Error: Invalid Tree Structure")
        if self.validateInput(qs, nestedQueries) is False:
            raise Exception("Error: Invalid Input")
        
    
    
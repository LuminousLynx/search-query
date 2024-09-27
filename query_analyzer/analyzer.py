#!/usr/bin/env python
"""Tool for analyzing yield of queries"""

import typing

from search_query.query import Query
from search_query.parser_base import QueryListParser
from search_query.constants import PLATFORM
from search_query.constants import Operators

class query_analyzer:
    '''Analyzer class, provides basic methods for converting query to list, connection to UI and controlling API access'''

    def __init__(self, 
                 query: Query, 
                 database: str) -> None:
        '''initialization for query analyzer'''

        self.query = query
        self.database = database

        self.parser = QueryListParser


    def to_string(self) -> str:
        return self.query.to_string(syntax = self.database)
    

    def convert_query_to_str_list(self, 
                                  query: Query, 
                                  pos: int, 
                                  query_dict: dict = {}) -> list:
        '''Method to parse the query object into a list with all parts as strings'''

        




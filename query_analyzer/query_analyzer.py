#!/usr/bin/env python
"""Tool for analyzing yield of queries"""

import typing

from search_query.query import Query
from search_query.constants import PLATFORM
from search_query.constants import Operators

# pylint: disable=line-too-long

class query_analyzer:
    '''Analyzer class, provides basic functions for converting query to list, query yield analysis, and UI display'''

    # add: self.ui as conection point to user interface
    # global variable as it doesn't need to be changed even if called repeatedly
    # add module: ui

    def __init__(self, 
                 query: Query, 
                 ) -> None:
        '''Initialization for query analyzer'''
        self.query = query

    def analyze_yield(self) -> None:
        '''Main function for yield analysis'''

        query_list = self.parse_query_to_list(query=self.query, current_pos=0)
        
        # TO DO: save yields in list of dicts with query strings and yield as kv pairs
        # how to test yield w/o access to certain databases?
        # add functions/module: estimating yield from samples, retrieving and saving yield for every entry in list
        # add module: interpreter of results that can give suggestions to user 
        # pass query/yield dict to ui

    def parse_query_to_list(self, 
                            query: Query, 
                            current_pos: int = 0,
                            query_list: typing.List[Query] = [],
                            ) -> list[Query]:
        '''Function to recursively parse the query and all its subqueries into a list'''

        if current_pos == 0:
            query_list.append(query)

        if query.operator:
            for child in query.children:
                query_list.append(child)
            
        current_pos += 1

        if current_pos < len(query_list):
            query_list = self.parse_query_to_list(query=query_list[current_pos], current_pos=current_pos, query_list=query_list)
        
        return query_list

                






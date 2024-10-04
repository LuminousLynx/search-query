#!/usr/bin/env python
"""Tool for analyzing yield of queries"""

import typing

from search_query.query import Query
from search_query.constants import PLATFORM
from search_query.constants import Operators
from analyzer_ui import AnalyzerUI
from yield_collector import YieldCollector
from query_advisor import QueryAdvisor

# pylint: disable=line-too-long

class QueryAnalyzer:
    '''Analyzer class, provides basic functions for converting query to list, query yield analysis, and UI display'''

    def __init__(self) -> None:
        '''Initializing Query Analyzer'''
        self.UI = AnalyzerUI()
        self.collector = YieldCollector()
        self.advisor = QueryAdvisor()


    def analyze_yield(self, query: Query, platform: PLATFORM) -> None:
        '''Main function for yield analysis'''
        
        # Make query list with all subqueries
        query_list = self.parse_query_to_list(query=query)

        # Collect yields of all terms into list
        yield_list = self.collector.collect(query_list=query_list, platform=platform)

        # Create suggestions for query refinement based on yields in list
        suggestions = self.advisor.create_suggestions(yield_list=yield_list)

        # Display subqueries, yields and suggestions to user via the UI
        data = {"list": yield_list, "suggestions": suggestions}
        self.UI.run_UI(data=data)


    def parse_query_to_list(self, 
                            query: Query, 
                            current_pos: int = 0,
                            query_list: typing.Optional[typing.List[Query]] = None,
                        ) -> typing.List[Query]:
        '''Function to recursively parse the query and all its subqueries into a list'''

        if query_list is None:
            query_list = []

        if current_pos == 0:
            query_list.append(query)

        if query.operator:
            for child in query.children:
                query_list.append(child)
            
        current_pos += 1

        if current_pos < len(query_list):
            query_list = self.parse_query_to_list(query=query_list[current_pos], current_pos=current_pos, query_list=query_list)
        
        return query_list

                






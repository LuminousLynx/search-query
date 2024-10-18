#!/usr/bin/env python
"""Tool for analyzing yield of queries"""

from search_query.query import Query

from search_query.query_analyzer.analyzer_ui import AnalyzerUI
from search_query.query_analyzer.yield_collector import YieldCollector
from search_query.query_analyzer.query_advisor import QueryAdvisor

# pylint: disable=line-too-long

class QueryAnalyzer:
    '''Main Analyzer class. Initializes UI, YieldCollector and QueryAdvisor, calls Methods for yield analysis'''


    def __init__(self) -> None:
        '''Initializing Query Analyzer'''
        self.UI = AnalyzerUI()
        self.collector = YieldCollector()
        self.advisor = QueryAdvisor()


    def analyze_yield(self, query: Query, platform: str) -> None:
        '''Main function for yield analysis'''
        
        # Make query list with all subqueries
        query_list = self.parse_query_to_list(query=query)
        print("[INFO] Query list parsed successfully.")

        # Collect yields of all terms into list
        print("[INFO] Collecting yields.")
        yield_list = self.collector.collect(query_list=query_list, platform=platform)
        print("[INFO] Yields collected successfully.")

        # Create suggestions for query refinement based on yields in list
        suggestions = self.advisor.create_suggestions(yield_list=yield_list)
        print("[INFO] Suggestions created successfully.")

        # Display subqueries, yields and suggestions to user via the UI
        print("[INFO] Displaying results to user.")
        data = {"list": yield_list, "suggestions": suggestions}
        self.UI.run_UI(data=data)


    def parse_query_to_list(self, query: Query, current_pos: int = 0) -> list:
        '''Function to parse the query and all its subqueries into a list'''

        parsed_queries = []

        if current_pos == 0:
            parsed_queries.append(query)

        while current_pos < len(parsed_queries):
            query = parsed_queries[current_pos]

            if query.operator:
                for child in query.children:
                    parsed_queries.append(child)
            
            current_pos += 1
        
        return parsed_queries
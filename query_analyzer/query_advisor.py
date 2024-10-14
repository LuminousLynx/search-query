#!/usr/bin/env python
"""Class for generating suggestions based on query yields from list"""

import typing

from search_query.query import Query
from search_query.and_query import AndQuery
from search_query.not_query import NotQuery
from search_query.or_query import OrQuery

from query_analyzer.analyzer_constants import SUGGESTIONS
from query_analyzer.analyzer_constants import YIELD

# pylint: disable=line-too-long

class QueryAdvisor():
    """Class for generating suggestions based on query yields from list; includes helper methods"""
    def __init__(self) -> None:
        '''Constructor for QueryAdvisor class'''
        self.suggestions = typing.List[str]

    def create_suggestions(self, yield_list: typing.List[typing.Dict]) -> typing.List[str]:
        '''Method for creating suggestions and interpreting analysis of subterm yields.'''

        main_query_yield = self.get_yield_by_query(yield_list=yield_list, query=self.get_query_by_index(yield_list=yield_list, index=0))

        if YIELD.is_in_optimal_range(main_query_yield):
            self.suggestions.append(SUGGESTIONS.OK.value)

        elif YIELD.is_high(main_query_yield):
            self.suggestions.append(SUGGESTIONS.LITTLE_TOO_HIGH.value)
            self.suggestions.append("\n")
            problem_area = self.identify_high_yield(yield_list=yield_list)
            self.suggestions.append("\n-> ".join(query.to_string() for query in problem_area))

        elif YIELD.is_low(main_query_yield):
            self.suggestions.append(SUGGESTIONS.LITTLE_TOO_LOW.value)
            self.suggestions.append("\n")
            problem_area = self.identify_low_yield(yield_list=yield_list)
            self.suggestions.append("\n-> ".join(query.to_string() for query in problem_area))

        elif YIELD.is_dynamite(main_query_yield):
            self.suggestions.append(SUGGESTIONS.TOO_HIGH.value)
            problem_area = self.identify_high_yield(yield_list=yield_list)
            self.suggestions.append("\n-> ".join(query.to_string() for query in problem_area))

        elif YIELD.is_restrictive(main_query_yield):
            self.suggestions.append(SUGGESTIONS.TOO_LOW.value)
            problem_area = self.identify_low_yield(yield_list=yield_list)
            self.suggestions.append("\n-> ".join(query.to_string() for query in problem_area))
        
        return self.suggestions


    def identify_high_yield(self, yield_list: typing.List[typing.Dict]) -> typing.List[Query]:
        '''Method for identifying problematic areas in queries with high yield'''
        
        problem_found = False
        root_query = self.get_query_by_index(yield_list=yield_list, index=0)
        problem_area = typing.List[Query]

        while not problem_found:

            problem_area.append(root_query)
            if len(problem_area) > 3:
                problem_area.pop(0)

            if root_query.operator:
                children_list = self.create_children_list(yield_list=yield_list, query=root_query)
                if isinstance(AndQuery, root_query):
                    max_yield_child = self.get_query_with_max_yield(yield_list=children_list)
                    root_query = max_yield_child
                elif isinstance(OrQuery, root_query):
                    for child in children_list:
                        if not (YIELD.is_high(child["yield"]) or YIELD.is_dynamite(child["yield"])):
                            children_list.remove(child)
                    if len(children_list) > 0:
                        max_yield_child = self.get_query_with_max_yield(yield_list=children_list)
                        root_query = max_yield_child
                    else:
                        problem_found = True
                elif isinstance(NotQuery, root_query):
                        problem_found = True
            else:
                problem_found = True

        self.add_specific_suggestion(problem_area=problem_area, problem="high yield")       
        return problem_area
    

    def identify_low_yield(self, yield_list: typing.List[typing.Dict]) -> typing.List[Query]:
        '''Method for identifying problematic areas in queries with low yield'''
        
        problem_found = False
        root_query = self.get_query_by_index(yield_list=yield_list, index=0)
        problem_area = typing.List[Query]

        while not problem_found:

            problem_area.append(root_query)
            if len(problem_area) > 3:
                problem_area.pop(0)

            if root_query.operator:
                children_list = self.create_children_list(yield_list=yield_list, query=root_query)
                if isinstance(AndQuery, root_query):
                    for child in children_list:
                        if not (YIELD.is_low(child["yield"]) or YIELD.is_restrictive(child["yield"])):
                            children_list.remove(child)
                    if len(children_list) > 0:
                        min_yield_child = self.get_query_with_min_yield(yield_list=children_list)
                        root_query = min_yield_child
                    else:
                        problem_found = True
                elif isinstance(OrQuery, root_query):
                    min_yield_child = self.get_query_with_min_yield(yield_list=children_list)
                    root_query = min_yield_child
                elif isinstance(NotQuery, root_query):
                        problem_found = True
            else:
                problem_found = True

        self.add_specific_suggestion(problem_area=problem_area, problem="low yield")       
        return problem_area


    def add_specific_suggestion(self, problem_area: typing.List[Query], problem: str) -> None:
        '''Method for adding specific suggestion from constants.SUGGESTIONS based on problem area analysis'''
        
        if problem == "high yield":
            if isinstance(OrQuery, problem_area[-1]):
                self.suggestions.append(SUGGESTIONS.TOO_HIGH_ONLY_OR.value)
            elif isinstance(NotQuery, problem_area[-1]) or problem_area.count(AndQuery) > 1:
                self.suggestions.append(SUGGESTIONS.TOO_HIGH_SOFT_RESTRICTION.value)
            else:
                self.suggestions.append(SUGGESTIONS.TOO_HIGH_NO_RESTRICTION.value)

        elif problem == "low yield":
            if isinstance(AndQuery, problem_area[-1]):
                self.suggestions.append(SUGGESTIONS.TOO_LOW_ONLY_AND.value)
            elif isinstance(NotQuery, problem_area[-1]) or problem_area.count(OrQuery) > 1:
                self.suggestions.append(SUGGESTIONS.TOO_LOW_SOFT_EXTENSION.value)
            else:
                self.suggestions.append(SUGGESTIONS.TOO_LOW_NO_EXTENSION.value)
    
    
    # Helper methods

    def get_query_by_index(self, yield_list: typing.List[typing.Dict], index: int) -> Query:
        '''Helper method for extracting specific query from yield list'''

        query = yield_list[index]["query"]
        return query
    
    def get_yield_by_query(self, yield_list: typing.List[typing.Dict], query: Query) -> int:
        '''Helper method for extracting yield by query from yield list'''

        for item in yield_list:
            if item["query"] == query:
                return item["yield"]
        return None
    
    def get_query_with_max_yield(self, yield_list: typing.List[typing.Dict]) -> Query:
        '''Helper method for extracting query with highest yield from yield list'''

        max_yield = max(item["yield"] for item in yield_list)
        query = next(item["query"] for item in yield_list if item["yield"] == max_yield)   
        return query
    
    def get_query_with_min_yield(self, yield_list: typing.List[typing.Dict]) -> Query:	
        '''Helper method for extracting query with lowest yield from yield list'''

        min_yield = min(item["yield"] for item in yield_list)
        query = next(item["query"] for item in yield_list if item["yield"] == min_yield) 
        return query
    
    def create_children_list(self, yield_list: typing.List[typing.Dict], query: Query) -> typing.List[typing.Dict]:
        '''Helper method for creating list of children and their yield from a query'''
        
        children_list = []

        for child in query.children:
            children_list.append({"query": child, "yield": self.get_yield_by_query(yield_list=yield_list, query=child)})
        return children_list
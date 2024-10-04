#!/usr/bin/env python
"""Class for generating suggestions based on query yields from list"""

import typing

from search_query.query import Query
from search_query.and_query import AndQuery
from search_query.not_query import NotQuery
from search_query.or_query import OrQuery

from search_query.constants import PLATFORM
from search_query.constants import Operators
from search_query.constants import SUGGESTIONS
from search_query.constants import YIELD

class QueryAdvisor():

    def __init__(self) -> None:
        self.suggestions = typing.List[str]

    def create_suggestions(self, yield_list: typing.List[typing.Dict]) -> typing.List[str]:
        '''Method for creating suggestions and interpreting analysis of subterm yields.'''

        main_query_yield = yield_list[0]["yield"]

        if YIELD.is_in_optimal_range(main_query_yield):
            self.suggestions.append(SUGGESTIONS.OK.value)

        elif YIELD.is_high(main_query_yield):
            self.suggestions.append(SUGGESTIONS.LITTLE_TOO_HIGH.value)
            self.suggestions.append("\n")
            query = self.identify_high_yield(yield_list=yield_list)
            self.suggestions.append(query.to_string())

        elif YIELD.is_low(main_query_yield):
            self.suggestions.append(SUGGESTIONS.LITTLE_TOO_LOW.value)
            self.suggestions.append("\n")
            query = self.identify_low_yield(yield_list=yield_list)
            self.suggestions.append(query.to_string())

        elif YIELD.is_dynamite(main_query_yield):
            self.suggestions.append(SUGGESTIONS.TOO_HIGH.value)
            query = self.identify_high_yield(yield_list=yield_list)
            self.suggestions.append(query.to_string())

        elif YIELD.is_restrictive(main_query_yield):
            self.suggestions.append(SUGGESTIONS.TOO_LOW.value)
            query = self.identify_low_yield(yield_list=yield_list)
            self.suggestions.append(query.to_string())
        
        return self.suggestions


    def identify_high_yield(self, yield_list: typing.List[typing.Dict]) -> Query:

        problem_found = False
        root_query = self.get_query_by_index(yield_list=yield_list, index=0)

        while not problem_found:

            if root_query.operator:
                children_list = self.create_children_list(yield_list=yield_list, query=root_query)

                # wenn AND: max yield child nehmen, auf kinder untersuchen
                max_yield_child = self.get_query_with_max_yield(yield_list=children_list)

                # wenn OR: schauen, ob kinder jeweils in optimaler yield range liegen. Wenn ja, root_query zurückgeben, wenn nein, kinder die drüber sind untersuchen

                # wenn NOT: root-query zurückgeben und Vorschlag: entweder NOT-Teil erweitern oder vorderen Teil einschränken






            else:
                return root_query
    

    def identify_low_yield(self, yield_list: typing.List[typing.Dict]) -> Query:

        # TODO: Implement
        pass


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
    
    def create_children_list(self, yield_list: typing.List[typing.Dict], query: Query) -> typing.List[typing.Dict]:
        '''Helper method for creating list of children and their yield from a query'''
        
        children_list = []

        for child in query.children:
            children_list.append({"query": child, "yield": self.get_yield_by_query(yield_list=yield_list, query=child)})

        return children_list
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
        pass

    def create_suggestions(self, yield_list: typing.List[typing.Dict]) -> list[str]:
        '''Method for creating suggestions and interpreting analysis of subterm yields.'''

        suggestions = []
        main_query_yield = yield_list[0]["yield"]

        if YIELD.is_in_optimal_range(main_query_yield):
            suggestions.append(SUGGESTIONS.OK.value)

        elif YIELD.is_high(main_query_yield):
            suggestions.append(SUGGESTIONS.LITTLE_TOO_HIGH.value)
            suggestions.append("\n")

            query = self.identify_slightly_high_yield(yield_list=yield_list)
            suggestions.append(query.to_string())

        elif YIELD.is_low(main_query_yield):
            suggestions.append(SUGGESTIONS.LITTLE_TOO_LOW.value)
            suggestions.append("\n")

            query = self.identify_slightly_low_yield(yield_list=yield_list)
            suggestions.append(query.to_string())

        elif YIELD.is_dynamite(main_query_yield):
            query = self.identify_high_yield(yield_list=yield_list, suggestions=suggestions)
            suggestions.append(query.to_string())

        elif YIELD.is_restrictive(main_query_yield):
            query = self.identify_low_yield(yield_list=yield_list, suggestions=suggestions)
            suggestions.append(query.to_string())

        return suggestions


    def identify_slightly_high_yield(self, yield_list: typing.List[typing.Dict]) -> Query:

        # TODO: Implement
        pass

    def identify_slightly_low_yield(self, yield_list: typing.List[typing.Dict]) -> Query:

        # TODO: Implement
        pass

    def identify_high_yield(self, yield_list: typing.List[typing.Dict], suggestions: typing.List[str]) -> Query:

        # TODO: Implement
        pass

    def identify_low_yield(self, yield_list: typing.List[typing.Dict], suggestions: typing.List[str]) -> Query:

        # TODO: Implement
        pass

#!/usr/bin/env python
"""Class for collecting yields of (sub)queries"""

import typing
import re
import math

from collections import Counter

from search_query.query import Query
from search_query.and_query import AndQuery
from search_query.not_query import NotQuery
from search_query.or_query import OrQuery

from search_query.constants import PLATFORM
from search_query.constants import Operators

import random   # for testing purposes, remove in final version

# pylint: disable=line-too-long

class YieldCollector():
    '''Provides methods for collecting the yields of a query and its subqueries'''

    def __init__(self) -> None:
        pass


    def collect(self, query_list: typing.List[Query], platform: PLATFORM) -> typing.List[typing.Dict]:
        '''Main Method that gets called from the query analyzer class. Decides on method of yield collection and runs it.'''

        if platform == PLATFORM.WOS.value:
            yield_list = self.collect_wos(query_list=query_list)
        elif platform == PLATFORM.PUBMED.value:
            yield_list = self.collect_pubmed(query_list=query_list)
        elif platform == PLATFORM.EBSCO.value:
            yield_list = self.collect_ebsco(query_list=query_list)
        else:
            yield_list = self.collect_estimated(query_list=query_list)
        
        return yield_list
    

    def collect_wos(self, query_list: typing.List[Query]) -> typing.List[typing.Dict]:
        '''Method for collecting yields from Web of Science platform'''
        
        yield_list = []

        for query in query_list:
            # query_yield = TODO: implement yield collection for WOS
            query_yield = random.randint(10, 10000) # default value generator for testing
            yield_list = self.add_to_yield_list(yield_list=yield_list, query=query, query_yield=query_yield)

        return yield_list
    

    def collect_pubmed(self, query_list: typing.List[Query]) -> typing.List[typing.Dict]:
        '''Method for collecting yields from PubMed platform'''
        
        yield_list = []

        for query in query_list:
            # query_yield = TODO: implement yield collection for PubMed
            query_yield = random.randint(10, 10000) # default value generator for testing
            yield_list = self.add_to_yield_list(yield_list=yield_list, query=query, query_yield=query_yield)

        return yield_list


    def collect_ebsco(self, query_list: typing.List[Query]) -> typing.List[typing.Dict]:
        '''Method for collecting yields from EBSCO platform'''
        
        yield_list = []

        for query in query_list:
            # query_yield = TODO: implement yield collection for EBSCO
            query_yield = random.randint(10, 10000) # default value generator for testing
            yield_list = self.add_to_yield_list(yield_list=yield_list, query=query, query_yield=query_yield)

        return yield_list
    

    def collect_estimated(self, query_list: typing.List[Query], api: str) -> typing.List[typing.Dict]:
        '''Method for collecting estimated yields for APIs that do not support boolean queries'''
        
        yield_list = []
        complex_query_list = []

        # first, collect yields of single expression queries and save complex queries for later
        for query in query_list:
            if not query.operator:
                # query_yield = TODO: call method for trivial query of respective platform
                query_yield = random.randint(10, 10000) # default value generator for testing
                yield_list = self.add_to_yield_list(yield_list=yield_list, query=query, query_yield=query_yield)
            else:
                complex_query_list.append(query)

        # second, collect yields of complex queries, starting from the simplest ones, because the yield of their children is already known
        complex_query_list.reverse()
        for query in complex_query_list:

            if isinstance(query, OrQuery):
                children_yield_list = [{"query": child, "yield": self.get_yield_by_query(yield_list=yield_list, query=child)} for child in query.children]
                query_yield = sum([child["yield"] for child in children_yield_list])
                yield_list = self.add_to_yield_list(yield_list=yield_list, query=query, query_yield=query_yield)

            elif isinstance(query, AndQuery):
                children_samples = typing.List[typing.List[str]]
                for child in query.children:
                    children_samples.extend(self.get_doi_samples(query=child, api=api))

                # secure data quality by removing non-DOI entries
                for doi in children_samples:
                    if not self.matches_doi_pattern(doi):
                        children_samples.remove(doi)

                unique_dois = set(children_samples)
                doi_frequencies = Counter(children_samples)
                shared_dois = [element for element, count in doi_frequencies.items() if count == len(query.children)]
                shared_doi_percentage = len(shared_dois) / len(unique_dois)

                query_yield = math.ceil(shared_doi_percentage * sum([self.get_yield_by_query(yield_list=yield_list, query=child) for child in query.children]))
                yield_list = self.add_to_yield_list(yield_list=yield_list, query=query, query_yield=query_yield)

            elif isinstance(query, NotQuery):
                # TODO: Implement
                pass

        return yield_list

    # Helper methods

    def add_to_yield_list(self, yield_list: typing.List[typing.Dict], query: Query, query_yield: int) -> typing.List[typing.Dict]:
        '''Helper method for adding query and its yield to the yield list'''
        
        return yield_list.append({"query": query, "yield": query_yield})
    

    def get_yield_by_query(self, yield_list: typing.List[typing.Dict], query: Query) -> int:
        '''Helper method for extracting yield by query from yield list'''

        for item in yield_list:
            if item["query"] == query:
                return item["yield"]
        return None
    
    
    def get_doi_samples(self, query: Query, api: str) -> typing.List[str]:
        '''Helper method for collecting a sample of 50 DOIs to estimate complex query yield'''

        # TODO: Implement: collecting DOIs and adding them to a list
        pass


    def matches_doi_pattern(self, doi: str) -> bool:
        '''Helper method for checking if a string matches the DOI pattern'''

        doi_pattern = r"10.\d{4,9}/[-._;()/:A-Z0-9]+"
        return re.match(doi_pattern, doi)

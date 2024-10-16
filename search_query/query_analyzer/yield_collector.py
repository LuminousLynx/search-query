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

# pylint: disable=line-too-long

class YieldCollector():
    '''Provides methods for collecting the yields of a query and its subqueries'''

    def __init__(self) -> None:
        pass


    def collect(self, query_list: typing.List[Query], platform: str) -> typing.List[typing.Dict]:
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
        
        yield_list = typing.List[typing.Dict]

        for query in query_list:
            query_yield = 10 #TODO: implement yield collection for WOS
            yield_list = self.add_to_yield_list(yield_list=yield_list, query=query, query_yield=query_yield)

        return yield_list
    

    def collect_pubmed(self, query_list: typing.List[Query]) -> typing.List[typing.Dict]:
        '''Method for collecting yields from PubMed platform'''
        
        yield_list = typing.List[typing.Dict]

        for query in query_list:
            query_yield = 10 #TODO: implement yield collection for PubMed
            yield_list = self.add_to_yield_list(yield_list=yield_list, query=query, query_yield=query_yield)

        return yield_list


    def collect_ebsco(self, query_list: typing.List[Query]) -> typing.List[typing.Dict]:
        '''Method for collecting yields from EBSCO platform'''
        
        yield_list = typing.List[typing.Dict]

        for query in query_list:
            query_yield = 10 #TODO: implement yield collection for EBSCO
            yield_list = self.add_to_yield_list(yield_list=yield_list, query=query, query_yield=query_yield)

        return yield_list
    

    def collect_estimated(self, query_list: typing.List[Query], api: str) -> typing.List[typing.Dict]:
        '''Method for collecting estimated yields for APIs that do not support boolean queries'''
        
        yield_list = typing.List[typing.Dict]
        doi_list = typing.List[typing.Dict]
        complex_query_list = typing.List[Query]

        # first, collect yields of single expression queries and save complex queries for later
        for query in query_list:
            if not query.operator:
                query_results = self.get_query_results(query=query, api=api)
                
                # secure data quality by removing non-DOI entries
                query_results["dois"] = self.validate_doi_list(doi_list=query_results["dois"])
                
                # add dois and yield to respective lists
                yield_list = self.add_to_yield_list(yield_list=yield_list, query=query, query_yield=query_results["yield"])
                doi_list = self.add_to_doi_list(doi_list=doi_list, query=query, dois=query_results["dois"])
            else:
                complex_query_list.append(query)

        # second, estimate yields of complex queries, starting from the simplest ones, because the yield and doi samples of their children are already known
        complex_query_list.reverse()
        for query in complex_query_list:

            # check if query has already been collected and skip if it has
            if query in [item["query"] for item in yield_list]:
                continue

            if isinstance(query, OrQuery):
                query_results = self.collect_or_estimated(query=query, doi_list=doi_list)

            elif isinstance(query, AndQuery):
                query_results = self.collect_and_estimated(yield_list=yield_list, query=query, doi_list=doi_list)

            elif isinstance(query, NotQuery):
                query_results = self.collect_not_estimated(yield_list=yield_list, query=query, complex_query_list=complex_query_list, api=api)

                # set yield of NOT query to 0, because it wouldn't make sense to actually collect it
                yield_list = self.add_to_yield_list(yield_list=yield_list, query=query, query_yield=0)

                # enter yield and doi sample of parent query into respective lists
                yield_list = self.add_to_yield_list(yield_list=yield_list, query=self.get_parent_query(query=query, complex_query_list=complex_query_list), query_yield=query_results["yield"])
                doi_list = self.add_to_doi_list(doi_list=doi_list, query=self.get_parent_query(query=query, complex_query_list=complex_query_list), dois=query_results["dois"])

                # skip to next iteration
                continue
            
            yield_list = self.add_to_yield_list(yield_list=yield_list, query=query, query_yield=query_results["yield"])
            doi_list = self.add_to_doi_list(doi_list=doi_list, query=query, dois=query_results["dois"])

        return yield_list.reverse()
    

    def collect_or_estimated(self, query: Query, doi_list: typing.List[typing.Dict] = None) -> typing.List[typing.Dict]:
        '''Method for collecting estimated yields and DOI samples for OR queries'''

        children_doi_list = [{"query": child, "dois": self.get_doi_by_query(doi_list=doi_list, query=child)} for child in query.children]
        no_duplicate_sample = set([item for sublist in [child["dois"] for child in children_doi_list] for item in sublist])
        return {"yield": len(no_duplicate_sample), "dois": no_duplicate_sample}


    def collect_and_estimated(self, yield_list: typing.List[typing.Dict], query: Query, doi_list: typing.List[typing.Dict] = None) -> typing.List[typing.Dict]:
        '''Method for collecting estimated yields and DOI samples for AND queries'''

        children_doi_list = [{"query": child, "dois": self.get_doi_by_query(doi_list=doi_list, query=child)} for child in query.children]

        no_duplicate_sample = set(children_doi_list)
        doi_frequencies = Counter(children_doi_list)
        shared_dois = [element for element, count in doi_frequencies.items() if count == len(query.children)]
        shared_doi_percentage = len(shared_dois) / len(no_duplicate_sample)

        return {"yield": math.ceil(shared_doi_percentage * sum([self.get_yield_by_query(yield_list=yield_list, query=child) for child in query.children])), "dois": shared_dois}


    def collect_not_estimated(self, yield_list: typing.List[typing.Dict], query: Query, complex_query_list: typing.List[Query], doi_list: typing.List[typing.Dict] = None) -> typing.List[typing.Dict]:
        '''Method for collecting estimated yields and DOI samples for queries containing NOT queries'''

        # As it would not make much sense to calculate the yield of a NOT query, this method calculates the yield of the parent query and returns both doi list and yield.
        # In the main method, both yield_list and doi_list are updated accordingly. 

        parent_query = self.get_parent_query(query=query, complex_query_list=complex_query_list)
        sibling_queries = parent_query.children.remove(query)

        if isinstance(parent_query, OrQuery):
            sibling_doi_list = [{"query": sibling, "dois": self.get_doi_by_query(doi_list=doi_list, query=sibling)} for sibling in sibling_queries]
            sibling_sample = set([item for sublist in [sibling["dois"] for sibling in sibling_doi_list] for item in sublist])
            query_yield = len(sibling_sample)
        
        elif isinstance(parent_query, AndQuery):
            sibling_doi_list = [{"query": sibling, "dois": self.get_doi_by_query(doi_list=doi_list, query=sibling)} for sibling in sibling_queries]
            doi_frequencies = Counter(sibling_doi_list)
            sibling_sample = [element for element, count in doi_frequencies.items() if count == len(sibling_queries)]
            query_yield = math.ceil(len(sibling_sample) / len(sibling_doi_list) * sum([self.get_yield_by_query(yield_list=yield_list, query=sibling) for sibling in sibling_queries]))
            
        this_sample = self.get_doi_by_query(doi_list=doi_list, query=query)

        for doi in sibling_sample:
            if doi in this_sample:
                sibling_sample.remove(doi)

        return {"yield": query_yield, "dois": sibling_sample}

        


    # Helper methods

    def add_to_yield_list(self, yield_list: typing.List[typing.Dict], query: Query, query_yield: int) -> typing.List[typing.Dict]:
        '''Helper method for adding query and its yield to the yield list'''
        
        return yield_list.append({"query": query, "yield": query_yield})


    def add_to_doi_list(self, doi_list: typing.List[typing.Dict], query: Query, dois: typing.List[str]) -> typing.List[typing.Dict]:
        '''Helper method for adding query and its DOIs to the DOI list'''

        return doi_list.append({"query": query, "dois": dois})
    

    def get_yield_by_query(self, yield_list: typing.List[typing.Dict], query: Query) -> int:
        '''Helper method for extracting yield by query from yield list'''

        for item in yield_list:
            if item["query"] == query:
                return item["yield"]
        return None


    def get_doi_by_query(self, doi_list: typing.List[typing.Dict], query: Query) -> typing.List[str]:
        '''Helper method for extracting DOIs by query from DOI list'''

        for item in doi_list:
            if item["query"] == query:
                return item["dois"]
        return None


    def get_parent_query(self, query: Query, complex_query_list: typing.List[Query]) -> Query:
        '''Helper method for getting the parent query of a subquery '''

        for complex_query in complex_query_list:
            if query in complex_query.children:
                return complex_query
        return None
    
    
    def get_query_results(self, query: Query, api: str) -> typing.List[str]:
        '''Helper method for collecting a sample of DOIs to estimate complex query yield'''

        # TODO: Implement: collecting at most 200 DOIs and adding them to a list, also from complex queries themselves (recursion)
        pass
    

    def validate_doi_list(self, doi_list: typing.List[str]) -> typing.List[str]:
        '''Helper method for validating a list of DOIs'''

        return [doi for doi in doi_list if self.matches_doi_pattern(doi)]


    def matches_doi_pattern(self, doi: str) -> bool:
        '''Helper method for checking if a string matches the DOI pattern'''

        doi_pattern = r"10.\d{4,9}/[-._;()/:A-Z0-9]+"
        return re.match(doi_pattern, doi)
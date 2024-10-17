#!/usr/bin/env python
"""Class for accessing search source APIs implemented in CoLRev and retrieving yield from queries"""

from search_query.query import Query

import typing

import colrev

class ColrevCollector():
    '''Class for collecting yields of queries from CoLRev'''

    def __init__(self) -> None:
        pass

    def collect(self, query_list: typing.List[Query], api: str) -> typing.List[typing.Dict]:
        # TODO: Implement
        pass

    def collect_pubmed(self, query: Query) -> typing.Dict:
        # TODO: Implement
        pass

    def collect_crossref(self, query: Query) -> typing.Dict:
        # TODO: Implement
        pass
#!/usr/bin/env python
"""Class for collecting yields of (sub)queries"""

import typing

from search_query.query import Query
from search_query.and_query import AndQuery
from search_query.not_query import NotQuery
from search_query.or_query import OrQuery

from search_query.constants import PLATFORM
from search_query.constants import Operators

class YieldCollector():
    '''Provides methods for collecting the yields of a query and its subqueries'''

    def __init__(self) -> None:
        pass

    def collect(self, query_list: typing.List[Query], platform: PLATFORM) -> list[dict]:
        '''Main Method that gets called from the query analyzer class. Decides on method of yield collection and runs yield collection.'''

        # TODO: Implement
        pass

#!/usr/bin/env python
"""Class for accessing search source APIs implemented in CoLRev and retrieving yield from queries"""

from search_query.query import Query

import typing
import re
import requests

from colrev.packages.pubmed.src.pubmed_api import *
from colrev.packages.crossref.src.crossref_api import *

class ColrevCollector():
    '''Class for collecting yields of queries from CoLRev'''

    def __init__(self) -> None:
        pass

    def collect(self, query: Query, api: str) -> typing.Dict:
        '''Main method for connection to colrev. Passes the query to the correct endpoint and returns the yield (and the doi sample, depending on the endpoint)'''

        if "pubmed" in api.lower():
            yield_dict = self.collect_pubmed(query=query)
        elif "crossref" in api.lower():
            yield_dict = self.collect_crossref(query=query)
        
        return yield_dict
    

    def collect_pubmed(self, query: Query) -> typing.Dict:
        '''Method for collecting yields from the PubMed API'''

        pubmed_api = PubmedAPI()

        pubmed_query = query.to_string(syntax="pubmed").replace(" ", "+")

        results = pubmed_api._get_pubmed_ids(query=pubmed_query, retstart=0, page=0)

        return {"yield": results["totalResults"]}


    def collect_crossref(self, query: Query) -> typing.Dict:

        query_string = query.to_string()
        query_string = re.sub(r'\[.*\]', '', query_string)

        url = f"https://api.crossref.org/works?query="+query_string+"&rows=1000"

        crossref_endpoint = Endpoint(request_url=url)

        # TODO: Implement Crossref API call with CoLRev
        pass
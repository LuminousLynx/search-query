#!/usr/bin/env python
"""Class for accessing search source APIs implemented in CoLRev and retrieving yield from queries"""

from search_query.query import Query


import re
import requests

from colrev.packages.pubmed.src.pubmed_api import PubmedAPI
from colrev.packages.crossref.src.crossref_api import Endpoint

class ColrevCollector():
    '''Class for collecting yields of queries from CoLRev'''

    def __init__(self) -> None:
        pass

    def collect(self, query: Query, api: str) -> dict:
        '''Main method for connection to colrev. Passes the query to the correct endpoint and returns the yield (and the doi sample, depending on the endpoint)'''

        if "pubmed" in api.lower():
            yield_dict = self.collect_pubmed(query=query)
        elif "crossref" in api.lower():
            yield_dict = self.collect_crossref(query=query)
        
        return yield_dict
    

    def collect_pubmed(self, query: Query) -> dict:
        '''Method for collecting yields from the PubMed API'''

        session = requests.Session()
        pubmed_api = PubmedAPI(parameters={}, email="", session=session)

        if query.operator:
            query_string = query.to_string(syntax="pubmed")
        else:
            query_string = query.to_string()
        query_string = re.sub(r'\[.{2}\]', '', query_string)
        query_string = query_string.replace(" ", "+")
        print("Searching: ", query_string)

        pubmed_query = str("https://pubmed.ncbi.nlm.nih.gov/?term=")+query_string

        try:
            results = pubmed_api._get_pubmed_ids(query=pubmed_query, retstart=0, page=1)
        except IndexError:
            print("No results found for query: ", query.to_string())
            results = {"totalResults": 0}

        return {"yield": results["totalResults"]}


    def collect_crossref(self, query: Query) -> dict:

        query_string = query.to_string()
        query_string = re.sub(r'\[.{2}\]', '', query_string)

        url = str("https://api.crossref.org/works?query="+query_string)

        crossref_endpoint = Endpoint(request_url=url)

        result_yield = crossref_endpoint.get_nr()
        result_sample = crossref_endpoint.get_dois()
        
        return {"yield": result_yield, "sample": result_sample}
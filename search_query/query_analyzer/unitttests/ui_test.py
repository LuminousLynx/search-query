#!/usr/bin/env python
'''Test for UI class in query analyzer'''

from search_query.query_analyzer.analyzer_ui import AnalyzerUI
from search_query.and_query import AndQuery
from search_query.or_query import OrQuery
from search_query.query import Query

from search_query.query_analyzer.analyzer_constants import SUGGESTIONS
from search_query.constants import Fields


import typing

# pylint: disable=line-too-long

# simulate query for UI test
data = {}
data["list"] = typing.List[typing.Dict]
data["suggestions"] = typing.List[str]

query00 = Query("test0", search_field=Fields.ABSTRACT)
query01 = Query("test1", search_field=Fields.ABSTRACT)
query02 = Query("test2", search_field=Fields.ABSTRACT)
query03 = Query("test3", search_field=Fields.ABSTRACT)
query04 = Query("test4", search_field=Fields.ABSTRACT)
query05 = Query("test5", search_field=Fields.ABSTRACT)

query1 = OrQuery([query00, query04, query05], search_field=Fields.ABSTRACT)
query2 = OrQuery([query01, query03], search_field=Fields.ABSTRACT)
query3 = AndQuery([query1, query02, query2], search_field=Fields.ABSTRACT)

# random yields for testing
query_list = [{"query": query3, "yield": 204}, {"query": query1, "yield": 2232}, {"query": query02, "yield": 341}, 
              {"query": query2, "yield": 123}, {"query": query00, "yield": 123}, {"query": query04, "yield": 123}, {"query": query05, "yield": 123}, {"query": query01, "yield": 123}, {"query": query03, "yield": 123}]
data["list"] = query_list

# random suggestions and query string for testing
data["suggestions"] = [SUGGESTIONS.TOO_HIGH_NO_RESTRICTION.value, SUGGESTIONS.TOO_HIGH_SOFT_RESTRICTION.value, SUGGESTIONS.TOO_HIGH_ONLY_OR.value]
data["suggestions"].append("-> "+"\n-> ".join(query["query"].to_string("pubmed") for query in data["list"] if query["query"].operator))
data["suggestions"].append("-> "+"\n-> ".join(query["query"].to_string() for query in data["list"] if not query["query"].operator))

ui = AnalyzerUI()
ui.run_UI(data=data)
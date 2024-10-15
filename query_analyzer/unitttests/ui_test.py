#!/usr/bin/env python
'''Test for UI class in query analyzer'''

from query_analyzer.analyzer_ui import AnalyzerUI
from search_query.and_query import AndQuery
from search_query.or_query import OrQuery

# pylint: disable=line-too-long

# simulate query for UI test
data = {}
data["list"] = []
data["suggestions"] = []

query1 = OrQuery(["test0", "test4", "test5"], search_field="Abstract")
query2 = OrQuery(["test1", "test2"], search_field="Abstract")
query3 = AndQuery([query1, query2], search_field="Abstract")

query_list = [{"query": query3, "yield": 204}, {"query": query2, "yield": 2232}, {"query": query1, "yield": 341}]
data["list"] = query_list

for a in range(5):
    data["suggestions"].append("test" * (a+1))

ui = AnalyzerUI()
ui.run_UI(data=data)
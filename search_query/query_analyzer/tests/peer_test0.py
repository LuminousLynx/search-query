#!/usr/bin/env python
"""Integration test number 0 for the query analyzer"""

'''
Welcome, fellow human! I'm glad you volunteered to help me evaluate my program. 
    
This is an integration test for the query analyzer. If you have any questions regarding this program, please check out the anayzer_README file or fell free to ask me. 

If not: Great! Let's run the program and find out if it works for you! 

Your mission, should you choose to accept it, is to...
    ...run this python file. It will analyze the yield of the original query and display the results in a GUI window. 
    There, it will give you recommendations on how to improve the query. Close the window, improve the query in this file according to the recommendations and run the file again.
    Your target yield for the main query is between 200 and 2000. 

    Good Luck! 

This machine will self-destruct in 5 seconds.

...4...

...3...

...2...

Just kidding. Or am I?

...1...
'''

from search_query.query import Query
from search_query.and_query import AndQuery
from search_query.or_query import OrQuery
from search_query.not_query import NotQuery

from search_query.query_analyzer.query_analyzer import QueryAnalyzer

# pylint: disable=line-too-long
# flake8: noqa: E501

'''
Original query: 
(instrument[tiab] OR instruments[tiab] OR Measurement[tiab] OR Measurements[tiab] OR Measures[tiab] OR Measure[tiab] OR scale[tiab] OR scales[tiab] OR validate[tiab] OR validation[tiab] OR validates[tiab] OR validated[tiab] OR validity[tiab])
AND 
NOT (bisexual[tiab] OR "transgender"[tiab]) NOT ("animals"[MeSH] NOT "humans"[MeSH]))
'''

# Define the terms
terms1 = [
    Query('instrument'),
    Query('instruments'),
    Query('Measurement'),
    Query('Measurements'),
    Query('Measures'),
    Query('Measure'),
    Query('scale'),
    Query('scales'),
    Query('validate'),
    Query('validation'),
    Query('validates'),
    Query('validated'),
    Query('validity')
]

terms2 = [
    Query('bisexual'),
    Query('"transgender"')
]

terms3 = [
    Query('"animals"'),
    Query('"humans"')
]

# Build the query
query = AndQuery(
    [OrQuery(terms1, search_field="tiab"),
    NotQuery(
        [OrQuery(terms2, search_field="tiab"), NotQuery(terms3, search_field="MeSH")],
        search_field="tiab"
    )],
    search_field="tiab"
)

if __name__ == "__main__":
    analyzer = QueryAnalyzer()
    analyzer.analyze_yield(query, "colrev.pubmed")
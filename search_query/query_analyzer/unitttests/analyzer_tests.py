from __future__ import annotations
from search_query.query_analyzer.query_analyzer import QueryAnalyzer
from search_query.query import Query

#!/usr/bin/env python3
"""Tests for QueryAnalyzer."""


def test_parse_query_to_list() -> None:
    """Test parse_query_to_list method of QueryAnalyzer."""

    analyzer = QueryAnalyzer()

    # Mock data
    query = Query(operator="AND", children=[Query(), Query()])

    # Call the method
    result = analyzer.parse_query_to_list(query=query)

    # Assertions
    assert result == [query, query.children[0], query.children[1]]
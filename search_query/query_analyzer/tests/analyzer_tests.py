from __future__ import annotations
import pytest
from search_query.query_analyzer.query_analyzer import QueryAnalyzer
from search_query.query import Query

class TestQueryAnalyzer:
    def setup_method(self):
        """Setup for each test method."""
        self.analyzer = QueryAnalyzer()

    def test_parse_query_to_list(self):
        """Test parse_query_to_list method of QueryAnalyzer."""

        # Mock data
        query = Query(operator="AND", children=[Query(), Query()])

        # Call the method
        result = self.analyzer.parse_query_to_list(query=query)

        # Assertions
        assert result == [query, query.children[0], query.children[1]]
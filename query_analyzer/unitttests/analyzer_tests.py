from __future__ import annotations
from unittest.mock import MagicMock
from query_analyzer import QueryAnalyzer
from search_query.query import Query
from analyzer_ui import AnalyzerUI
from yield_collector import YieldCollector
from query_advisor import QueryAdvisor

#!/usr/bin/env python3
"""Tests for QueryAnalyzer."""




def test_analyze_yield() -> None:
    """Test analyze_yield method of QueryAnalyzer."""

    # Mock dependencies
    mock_ui = MagicMock(spec=AnalyzerUI)
    mock_collector = MagicMock(spec=YieldCollector)
    mock_advisor = MagicMock(spec=QueryAdvisor)

    # Create instance of QueryAnalyzer with mocked dependencies
    analyzer = QueryAnalyzer()
    analyzer.UI = mock_ui
    analyzer.collector = mock_collector
    analyzer.advisor = mock_advisor

    # Mock data
    query = Query(operator="AND", children=[Query(), Query()])
    platform = "test_platform"
    mock_yield_list = ["yield1", "yield2"]
    mock_suggestions = ["suggestion1", "suggestion2"]

    # Set return values for mocks
    mock_collector.collect.return_value = mock_yield_list
    mock_advisor.create_suggestions.return_value = mock_suggestions

    # Call the method
    analyzer.analyze_yield(query=query, platform=platform)

    # Assertions
    mock_collector.collect.assert_called_once_with(query_list=[query, query.children[0], query.children[1]], platform=platform)
    mock_advisor.create_suggestions.assert_called_once_with(yield_list=mock_yield_list)
    mock_ui.run_UI.assert_called_once_with(data={"list": mock_yield_list, "suggestions": mock_suggestions})


def test_parse_query_to_list() -> None:
    """Test parse_query_to_list method of QueryAnalyzer."""

    analyzer = QueryAnalyzer()

    # Mock data
    query = Query(operator="AND", children=[Query(), Query()])

    # Call the method
    result = analyzer.parse_query_to_list(query=query)

    # Assertions
    assert result == [query, query.children[0], query.children[1]]
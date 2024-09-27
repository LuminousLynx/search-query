#!/usr/bin/env python
"""Tests for search query analysis"""
import unittest

from search_query.and_query import AndQuery
from search_query.not_query import NotQuery
from search_query.or_query import OrQuery
from search_query.query import SearchField
from search_query.constants import Fields

# pylint: disable=line-too-long
# flake8: noqa: E501


class AnalyzerTest(unittest.TestCase):
    """Testing class for query translator"""

    def setUp(self) -> None:
        self.query_robot = NotQuery(["robot*"], search_field=SearchField(Fields.TITLE))
        self.query_ai = OrQuery(
            [
                '"AI"',
                '"Artificial Intelligence"',
                '"Machine Learning"',
                self.query_robot,
            ],
            search_field=SearchField(
                Fields.TITLE,
            ),
        )
        self.query_health = OrQuery(
            ['"health care"', "medicine"],
            search_field=SearchField(Fields.TITLE),
        )
        self.query_ethics = OrQuery(
            ["ethic*", "moral*"], search_field=SearchField(Fields.ABSTRACT)
        )
        self.query_complete = AndQuery(
            [self.query_ai, self.query_health, self.query_ethics],
            search_field=SearchField(Fields.TITLE),
        )

    def print_query(self) -> None:
        print(self.query_complete.to_string())

if __name__ == "__main__":
    unittest.main()

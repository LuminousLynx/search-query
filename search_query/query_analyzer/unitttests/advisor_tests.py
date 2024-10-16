import pytest
from query_analyzer.query_advisor import QueryAdvisor
from search_query.query import Query
from search_query.and_query import AndQuery
from search_query.not_query import NotQuery
from search_query.or_query import OrQuery
from query_analyzer.analyzer_constants import SUGGESTIONS, YIELD

class TestQueryAdvisor:

    @pytest.fixture
    def advisor(self):
        return QueryAdvisor()

    def test_create_suggestions(self, advisor):
        yield_list = [
            {"query": Query(), "yield": 50},
            {"query": Query(), "yield": 30},
            {"query": Query(), "yield": 70}
        ]
        suggestions = advisor.create_suggestions(yield_list)
        assert isinstance(suggestions, list)

    def test_identify_high_yield(self, advisor):
        yield_list = [
            {"query": AndQuery(), "yield": 100},
            {"query": OrQuery(), "yield": 90},
            {"query": NotQuery(), "yield": 80}
        ]
        problem_area = advisor.identify_high_yield(yield_list)
        assert isinstance(problem_area, list)

    def test_identify_low_yield(self, advisor):
        yield_list = [
            {"query": AndQuery(), "yield": 10},
            {"query": OrQuery(), "yield": 20},
            {"query": NotQuery(), "yield": 5}
        ]
        problem_area = advisor.identify_low_yield(yield_list)
        assert isinstance(problem_area, list)

    def test_add_specific_suggestion(self, advisor):
        problem_area = [AndQuery(), OrQuery(), NotQuery()]
        advisor.add_specific_suggestion(problem_area, "high yield")
        assert isinstance(advisor.suggestions, list)

    def test_get_query_by_index(self, advisor):
        yield_list = [
            {"query": Query(), "yield": 50},
            {"query": Query(), "yield": 30}
        ]
        query = advisor.get_query_by_index(yield_list, 1)
        assert isinstance(query, Query)

    def test_get_yield_by_query(self, advisor):
        query = Query()
        yield_list = [
            {"query": query, "yield": 50},
            {"query": Query(), "yield": 30}
        ]
        yield_value = advisor.get_yield_by_query(yield_list, query)
        assert yield_value == 50

    def test_get_query_with_max_yield(self, advisor):
        yield_list = [
            {"query": Query(), "yield": 50},
            {"query": Query(), "yield": 70}
        ]
        query = advisor.get_query_with_max_yield(yield_list)
        assert isinstance(query, Query)

    def test_get_query_with_min_yield(self, advisor):
        yield_list = [
            {"query": Query(), "yield": 50},
            {"query": Query(), "yield": 30}
        ]
        query = advisor.get_query_with_min_yield(yield_list)
        assert isinstance(query, Query)

    def test_create_children_list(self, advisor):
        query = Query()
        query.children = [Query(), Query()]
        yield_list = [
            {"query": query.children[0], "yield": 50},
            {"query": query.children[1], "yield": 30}
        ]
        children_list = advisor.create_children_list(yield_list, query)
        assert isinstance(children_list, list)
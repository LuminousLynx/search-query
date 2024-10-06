#!/usr/bin/env python
"""Constants for search-query"""
# pylint: disable=too-few-public-methods
# pylint: disable=line-too-long
from enum import Enum

# noqa: E501


class PLATFORM(Enum):
    """Database identifier"""

    WOS = "wos"
    PUBMED = "pubmed"
    EBSCO = "ebsco"
    STRUCTURED = "structured"
    PRE_NOTATION = "pre_notation"


class Operators:
    """Operators"""

    AND = "AND"
    OR = "OR"
    NOT = "NOT"
    NEAR = "NEAR"


class Fields:
    """Search fields"""

    TITLE = "ti"
    ALL = "all"
    ABSTRACT = "ab"
    AUTHOR_KEYWORDS = "au"

    @classmethod
    def all(cls) -> list:
        """Return all fields as a list."""
        return [
            value
            for key, value in vars(cls).items()
            if not key.startswith("_") and not callable(value) and key not in ["all"]
        ]


# The PLATFORM_FIELD_MAP contains the current mapping of standard Fields to the
# syntax of the databases. If a field is not present in the map, it is assumed
# that the field is not supported by the database.
# If multiple options exist for valid database syntax, only the most common
# option is included in the map. Less common options are replaced in the parser.
# For instance, pubmed recommends [mh]. However, [mesh] is also valid and is replaced
# in the parser.
PLATFORM_FIELD_MAP = {
    # fields from
    # https://webofscience.help.clarivate.com/en-us/Content/wos-core-collection/woscc-search-field-tags.htm
    PLATFORM.WOS: {
        Fields.ALL: "ALL=",
        Fields.ABSTRACT: "AB=",
        Fields.TITLE: "TI=",
    },
    # fields from https://pubmed.ncbi.nlm.nih.gov/help/
    PLATFORM.PUBMED: {
        Fields.ALL: "[all]",
        Fields.TITLE: "[ti]",
        Fields.ABSTRACT: "[ab]",
    },
    # fields from https://connect.ebsco.com/s/article/Searching-with-Field-Codes?language=en_US
    PLATFORM.EBSCO: {
        Fields.TITLE: "TI ",
    },
}

# For convenience, modules can use the following to translate fields to a DB
PLATFORM_FIELD_TRANSLATION_MAP = {
    db: {v: k for k, v in fields.items()} for db, fields in PLATFORM_FIELD_MAP.items()
}

PLATFORM_COMBINED_FIELDS_MAP = {
    PLATFORM.PUBMED: {
        "[tiab]": [Fields.TITLE, Fields.ABSTRACT],
    },
}


class YIELD(Enum):
    '''Yield ranges for query analyzer, based on PRISMA statement'''

    UPPER_LIMIT = 2500
    UPPER_OPTIMUM = 2000
    LOWER_OPTIMUM = 200
    LOWER_LIMIT = 50

    # For further development: Implement a method for the user to choose their own desired yield range. Naturally, this Enum then should be relocated outside of the constants module 
    # as it would not be a constant anymore.

    @classmethod
    def is_in_optimal_range(y: int) -> bool:
        return y in range(YIELD.LOWER_OPTIMUM.value, YIELD.UPPER_OPTIMUM.value+1)
    
    @classmethod
    def is_low(y: int) -> bool:
        return y in range(YIELD.LOWER_LIMIT.value, YIELD.LOWER_OPTIMUM.value)
    
    @classmethod
    def is_high(y: int) -> bool:
        return y in range(YIELD.UPPER_OPTIMUM.value, YIELD.UPPER_LIMIT.value)
    
    @classmethod
    def is_restrictive(y: int) -> bool:
        return y <= YIELD.LOWER_LIMIT.value
    
    @classmethod
    def is_dynamite(y: int) -> bool:
        return y >= YIELD.UPPER_LIMIT.value
    

class SUGGESTIONS(Enum):
    '''Suggestions for different query faults'''

    TOO_HIGH_NO_RESTRICTION = "This part of your query yields a large number of results. This might originate from missing restrictions with AND or NOT operators. I suggest restrictions: "
    TOO_HIGH_SOFT_RESTRICTION = "This part of your query yields a large number of results. The restrictions you implemented with AND or NOT operators might not be tight enough: "
    TOO_HIGH_ONLY_OR = "The yield of your subterms is satisfactory, but extending them with OR operators might cause a problem. Try omitting unnecessary OR connections: "

    TOO_LOW_NO_EXTENSION = "I suggest extending the following term with OR operators: "
    TOO_LOW_SOFT_EXTENSION = "The extensions you implemented with OR operators might not be sufficient. I suggest extending your query here: "
    TOO_LOW_ONLY_AND = "The yield of your subterms is satisfactory. Connecting them with AND operators reduces the yield too much. Try omitting too restrictive AND connections: "

    LITTLE_TOO_HIGH = "The yield of your query might be a little high for conducting a systematic review. Here is my analysis: "
    LITTLE_TOO_LOW = "Your query might yield just too few results for a systematic review. Here is my analysis: "
    TOO_HIGH = "The yield of your query is too high for conducting a systematic review. Here is my analysis: "
    TOO_LOW = "Your query yields too few results for a systematic review. Here is my analysis: "
    
    OK = "The yield of your query is within the suggested range. Ut bene succedat! "

    # This class can be extended to further improve useability of the query analyzer


class ExitCodes:
    """Exit codes"""

    SUCCESS = 0
    FAIL = 1


class Colors:
    """Colors for CLI printing"""

    RED = "\033[91m"
    GREEN = "\033[92m"
    ORANGE = "\033[93m"
    BLUE = "\033[94m"
    END = "\033[0m"

#!/usr/bin/env python
"""Constants for search query analyzer"""
# pylint: disable=too-few-public-methods
# pylint: disable=line-too-long
from enum import Enum
import random 

# noqa: E501

class YIELD(Enum):
    '''Yield ranges for query analyzer, based on PRISMA statement'''

    UPPER_LIMIT = 2500
    UPPER_OPTIMUM = 2000
    LOWER_OPTIMUM = 200
    LOWER_LIMIT = 50

    # For further development: Implement a method for the user to choose their own desired yield range. Naturally, this Enum then should be relocated outside of the constants module 
    # as it would not be a constant anymore.

    @staticmethod
    def is_in_optimal_range(y: int) -> bool:
        return y in range(YIELD.LOWER_OPTIMUM.value, YIELD.UPPER_OPTIMUM.value+1)
    
    @staticmethod
    def is_low(y: int) -> bool:
        return y in range(YIELD.LOWER_LIMIT.value, YIELD.LOWER_OPTIMUM.value)
    
    @staticmethod
    def is_high(y: int) -> bool:
        return y in range(YIELD.UPPER_OPTIMUM.value, YIELD.UPPER_LIMIT.value)
    
    @staticmethod
    def is_restrictive(y: int) -> bool:
        return y <= YIELD.LOWER_LIMIT.value
    
    @staticmethod
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

    # This class can be extended to further improve useability of the query analyzer.


class CHESSPIECE:
    '''Chesspiece symbols for query visualization'''
    @staticmethod
    def randomChessPiece() -> str:
        chessPieces = (
        u"\u2654",
        u"\u2655",
        u"\u2656",
        u"\u2657",
        u"\u2658",
        u"\u2659"
        )
        return chessPieces[random.randint(0, len(chessPieces)-1)]
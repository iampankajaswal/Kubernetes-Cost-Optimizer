from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class QueryType(str, Enum):
    INSTANT = "instant"
    RANGE = "range"


@dataclass(slots=True)
class PromQLQuery:
    """
    Represents a PromQL query.

    This object is passed around the application instead of
    passing raw PromQL strings.
    """

    name: str
    expression: str
    description: str
    query_type: QueryType = QueryType.INSTANT

    def __str__(self) -> str:
        return self.expression

# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""Custom exceptions for ``stsynphot`` to raise."""

# SYNPHOT
from synphot.exceptions import SynphotError

__all__ = [
    "AmbiguousObsmode",
    "GenericASTTraversalPruningException",
    "GraphtabError",
    "IncompleteObsmode",
    "ParameterOutOfBounds",
    "ParserError",
    "UnusedKeyword",
]


class ParserError(SynphotError):
    """Exceptions for language parser."""


class GenericASTTraversalPruningException(ParserError):
    """SPARK AST traversal pruning exception."""


class ParameterOutOfBounds(SynphotError):
    """Exceptions for catalog problems."""


class GraphtabError(SynphotError):
    """Exceptions to do with graph table traversal."""


class UnusedKeyword(GraphtabError):
    """Unused keyword is not allowed in graph table."""


class IncompleteObsmode(GraphtabError):
    """Incomplete observation mode is not allowed in graph table."""


class AmbiguousObsmode(GraphtabError):
    """Ambiguous observation mode is not allowed in graph table."""


class PixscaleNotFoundError(SynphotError):
    """Undefined pixel scale for a given observation mode."""

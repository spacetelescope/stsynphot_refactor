# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""Custom exceptions for `stsynphot` to raise."""
from __future__ import absolute_import, division, print_function

# SYNPHOT
try:
    from synphot.exceptions import SynphotError
except ImportError:  # This is so RTD would build successfully
    pass

__all__ = ['ParserError', 'GenericASTTraversalPruningException',
           'ParameterOutOfBounds', 'GraphtabError', 'UnusedKeyword',
           'IncompleteObsmode', 'AmbiguousObsmode']


class ParserError(SynphotError):
    """Exceptions for language parser."""
    pass


class GenericASTTraversalPruningException(ParserError):
    """SPARK AST traversal pruning exception."""
    pass


class ParameterOutOfBounds(SynphotError):
    """Exceptions for catalog problems."""
    pass


class GraphtabError(SynphotError):
    """Exceptions to do with graph table traversal."""
    pass


class UnusedKeyword(GraphtabError):
    """Unused keyword is not allowed in graph table."""
    pass


class IncompleteObsmode(GraphtabError):
    """Incomplete observation mode is not allowed in graph table."""
    pass


class AmbiguousObsmode(GraphtabError):
    """Ambiguous observation mode is not allowed in graph table."""
    pass

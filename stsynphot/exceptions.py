# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""Custom exceptions for stsynphot to raise."""
from __future__ import division, print_function

# SYNPHOT
from synphot.synexceptions import SynphotError


class ParameterOutOfBounds(SynphotError):
    """Exceptions for catalog problems."""
    pass


# Do we need these???

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

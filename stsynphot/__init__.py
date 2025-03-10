# Licensed under a 3-clause BSD style license - see LICENSE.rst
try:
    from .version import version as __version__
except ImportError:
    __version__ = ''

# STSYNPHOT UI
from .config import getref, showref, conf  # noqa
from .spectrum import band, ebmvx, Vega  # noqa
from .catalog import grid_to_spec  # noqa
from .spparser import parse_spec  # noqa

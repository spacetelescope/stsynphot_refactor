# Licensed under a 3-clause BSD style license - see LICENSE.rst

# Set up the version
from pkg_resources import get_distribution, DistributionNotFound

try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:
    # package is not installed
    __version__ = 'unknown'

# STSYNPHOT UI
from .config import getref, showref, conf  # noqa
from .spectrum import band, ebmvx, Vega  # noqa
from .catalog import grid_to_spec  # noqa
from .spparser import parse_spec  # noqa

# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""This is an Astropy affiliated package."""

# Affiliated packages may add whatever they like to this file, but
# should keep this content at the top.
# ----------------------------------------------------------------------------
from ._astropy_init import *
# ----------------------------------------------------------------------------

#--------------#
# STSYNPHOT UI #
#--------------#
from .config import getref, showref
from .spectrum import band, ebmvx
from .spparser import parse_spec

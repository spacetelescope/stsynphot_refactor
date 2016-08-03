"""Adapted from ``astrolib/pysynphot/from_commissioning/stis/test1.py``."""
from __future__ import absolute_import, division, print_function

# LOCAL
from ..utils import CommCase


class Test1101(CommCase):
    obsmode = 'stis,ccd'
    spectrum = 'rn(unit(1,flam),band(johnson,v),15.0,vegamag)'

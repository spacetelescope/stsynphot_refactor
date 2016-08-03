"""Adapted from ``astrolib/pysynphot/from_commissioning/acs/test1.py``."""
from __future__ import absolute_import, division, print_function

# LOCAL
from ..utils import CommCase


class Test472(CommCase):
    obsmode = 'acs,hrc,coron,fr388n#3880'
    spectrum = 'rn(unit(1.0,flam),band(johnson,v),15,vegamag)'

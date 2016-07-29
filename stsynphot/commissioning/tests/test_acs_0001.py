"""Adapted from ``astrolib/pysynphot/from_commissioning/acs/test1.py``."""
from __future__ import absolute_import, division, print_function

# LOCAL
from ..utils import CommCase

# EXAMPLES (REMOVE WHEN DONE)
#
# import os
# from astropy.utils.data import get_pkg_data_filename
# from ..utils import use_pysynphot
#
#
# @use_pysynphot
# def test_acs_local():
#     """Some test using ASTROLIB and package data."""
#     filename = get_pkg_data_filename(os.path.join('data', 'earthshine.fits'))
#     assert filename.endswith('earthshine.fits')


class Test472(CommCase):
    obsmode = 'acs,hrc,coron,fr388n#3880'
    spectrum = 'rn(unit(1.0,flam),band(johnson,v),15,vegamag)'

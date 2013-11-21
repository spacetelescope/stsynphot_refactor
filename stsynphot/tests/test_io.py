# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""Test io.py module.

.. note:: read_*() functions are tested in other modules where they are used.

"""
from __future__ import absolute_import, division, print_function, unicode_literals

# STDLIB
import os

# THIRD-PARTY
import numpy as np

# ASTROPY
from astropy.tests.helper import pytest

# SYNPHOT
from synphot import exceptions as synexceptions

# LOCAL
from .. import config, stio


class TestIRAFConvert(object):
    """Test IRAF filename conversions."""
    def setup_class(self):
        os.environ['MYTESTPATH'] = '/path1/path2/'

    @pytest.mark.parametrize(
        ('in_str', 'ans'),
        [('mypath/image.fits', 'mypath/image.fits'),
         ('$MYTESTPATH/image.fits', '/path1/path2/image.fits'),
         ('CRREFER$image.fits', os.path.join(config.ROOTDIR(), 'image.fits')),
         ('mtab$image.fits', os.path.join(config.MTABDIR(), 'image.fits')),
         ('crGrid$image.fits', os.path.join(config.CATDIR(), 'image.fits')),
         ('crgridgs$image.fits',
          os.path.join(config.CATDIR(), 'gunnstryker', 'image.fits')),
         ('crgridjac$image.fits',
          os.path.join(config.CATDIR(), 'jacobi', 'image.fits')),
         ('crgridbk$image.fits',
          os.path.join(config.CATDIR(), 'bkmodels', 'image.fits')),
         ('crgridk93$image.fits',
          os.path.join(config.CATDIR(), 'k93models', 'image.fits')),
         ('crgridbz77$image.fits',
          os.path.join(config.CATDIR(), 'bz77', 'image.fits')),
         ('cracscomp$image.fits',
          os.path.join(config.ROOTDIR(), 'comp', 'acs', 'image.fits'))])
    def test_irafconvert(self, in_str, ans):
        out_str = stio.irafconvert(in_str)
        assert out_str == ans

    def test_irafconvert_data(self):
        out_str = stio.irafconvert('synphot$detectors.dat')
        assert out_str.endswith('data/detectors.dat')

    def test_exceptions(self):
        with pytest.raises(TypeError):
            out_str = stio.irafconvert(1)

        with pytest.raises(KeyError):
            out_str = stio.irafconvert('dummydummy$image.fits')

    def teardown_class(self):
        del os.environ['MYTESTPATH']


def test_read_table_exception():
    """Test data type check for FITS table read."""
    # Set INNODE to str (should be int)
    with pytest.raises(synexceptions.SynphotError):
        data = stio._read_table(
            config.GRAPHTABLE(), 1,
            {'COMPNAME': np.str, 'KEYWORD': np.str, 'INNODE': np.str,
             'OUTNODE': np.int, 'THCOMPNAME': np.str, 'COMMENT': np.str})

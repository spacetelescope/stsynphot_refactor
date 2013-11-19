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
from astropy.utils.data import get_pkg_data_filename

# SYNPHOT
from synphot import exceptions as synexceptions

# LOCAL
from .. import config, io


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
        out_str = io.irafconvert(in_str)
        assert out_str == ans

    def test_irafconvert_data(self):
        out_str = io.irafconvert('synphot$detectors.dat')
        assert out_str.endswith('data/detectors.dat')

    def test_exceptions(self):
        with pytest.raises(TypeError):
            out_str = io.irafconvert(1)

        with pytest.raises(KeyError):
            out_str = io.irafconvert('dummydummy$image.fits')

    def teardown_class(self):
        del os.environ['MYTESTPATH']


class TestGetLatestFile(object):
    """Test getting latest file."""
    def test_ftp(self):
        """Remote FTP path."""
        config.setdir(root='ftp://ftp.stsci.edu/cdbs/')

        template = os.path.join(config.MTABDIR(), 'n*tmg.fits')
        ans = os.path.join(config.MTABDIR(), 'n9i1408hm_tmg.fits')
        filename = io.get_latest_file(template, raise_error=True)
        assert filename == ans

        config.setdir()

    def test_local(self):
        """Local data path."""
        template = io.irafconvert('synphot$wavecats/cos_nuv_g285m_*.txt')
        ans = 'data/wavecats/cos_nuv_g285m_3094.txt'
        filename = io.get_latest_file(template, raise_error=True)
        assert filename.endswith(ans)

    def test_not_found(self):
        template = io.irafconvert('synphot$*dummy')

        # Warning only
        filename = io.get_latest_file(template)
        assert filename == ''

        # Raise error
        with pytest.raises(IOError):
            filename = io.get_latest_file(template, raise_error=True)


def test_read_table_exception():
    """Test data type check for FITS table read."""
    # Set INNODE to str (should be int)
    with pytest.raises(synexceptions.SynphotError):
        data = io._read_table(
            config.GRAPHTABLE(), 1,
            {'COMPNAME': np.str, 'KEYWORD': np.str, 'INNODE': np.str,
             'OUTNODE': np.int, 'THCOMPNAME': np.str, 'COMMENT': np.str})

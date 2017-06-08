# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""Test io.py module.

.. note::

    ``read_*()`` functions are tested in other modules where they are used.

"""
from __future__ import absolute_import, division, print_function

# STDLIB
import os

# THIRD-PARTY
import numpy as np
import pytest

# ASTROPY
from astropy.tests.helper import remote_data
from astropy.utils.data import _find_pkg_data_path, get_pkg_data_filename

# SYNPHOT
from synphot import exceptions as synexceptions

# LOCAL
from .. import stio
from ..config import conf


class TestIRAFConvert(object):
    """Test IRAF filename conversions."""
    def setup_class(self):
        os.environ['MYTESTPATH'] = '/path1/path2/'

    @pytest.mark.parametrize(
        ('in_str', 'ans'),
        [('mypath/image.fits', 'mypath/image.fits'),
         ('$MYTESTPATH//image.fits', '/path1/path2/image.fits'),
         ('CRREFER$image.fits', os.path.join(conf.rootdir, 'image.fits')),
         ('mtab$image.fits', os.path.join(conf.rootdir, 'mtab', 'image.fits'))
         ])
    def test_irafconvert(self, in_str, ans):
        out_str = stio.irafconvert(in_str)
        assert out_str == ans

    def test_irafconvert_data(self):
        out_str = stio.irafconvert('synphot$detectors.dat')
        assert out_str.endswith(os.path.join('data', 'detectors.dat'))

    def test_exceptions(self):
        with pytest.raises(TypeError):
            out_str = stio.irafconvert(1)
        with pytest.raises(KeyError):
            out_str = stio.irafconvert('dummydummy$image.fits')

    def teardown_class(self):
        del os.environ['MYTESTPATH']


class TestGetLatestFile(object):
    """Test getting latest file."""
    def setup_class(self):
        self.datadir = _find_pkg_data_path('data')

    @remote_data
    def test_ftp(self):
        """Remote FTP path."""
        template = 'ftp://ftp.stsci.edu/cdbs/mtab/OLD_FILES/n*tmg.fits'
        ans = 'ftp://ftp.stsci.edu/cdbs/mtab/OLD_FILES/n9i1408hm_tmg.fits'
        filename = stio.get_latest_file(template, raise_error=True)
        assert filename == ans

    def test_local(self):
        """Local data path."""
        template = os.path.join(self.datadir, '*tmg.fits')
        ans = os.path.join(self.datadir, 'tables_tmg.fits')
        filename = stio.get_latest_file(template, raise_error=True)
        assert filename == ans

    def test_bogus(self):
        """Bogus data path."""
        filename = stio.get_latest_file(
            os.path.join('foo', 'foo', '*tmg.fits'))
        assert filename == ''

    def test_no_files(self):
        """Real path with no files."""
        template = os.path.join(self.datadir, '*dummy')

        # Warning only
        filename = stio.get_latest_file(template)
        assert filename == ''

        # Raise error
        with pytest.raises(IOError):
            filename = stio.get_latest_file(template, raise_error=True)


def test_read_table_exception():
    """Test data type check for FITS table read."""
    tabname = get_pkg_data_filename(os.path.join('data', 'tables_tmg.fits'))

    # Set INNODE to str (should be int)
    with pytest.raises(synexceptions.SynphotError):
        data = stio._read_table(
            tabname, 1,
            {'COMPNAME': np.str, 'KEYWORD': np.str, 'INNODE': np.str,
             'OUTNODE': np.int, 'THCOMPNAME': np.str, 'COMMENT': np.str})

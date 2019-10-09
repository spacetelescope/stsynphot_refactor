# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""Test io.py module.

.. note::

    ``read_*()`` functions are tested in other modules where they are used.

"""

# STDLIB
import os
import warnings

# THIRD-PARTY
import numpy as np
import pytest

# ASTROPY
from astropy.utils.data import _find_pkg_data_path, get_pkg_data_filename
from astropy.utils.exceptions import AstropyUserWarning

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
            stio.irafconvert(1)
        with pytest.raises(KeyError):
            stio.irafconvert('dummydummy$image.fits')

    def teardown_class(self):
        del os.environ['MYTESTPATH']


class TestGetLatestFile(object):
    """Test getting latest file."""
    def setup_class(self):
        self.datadir = _find_pkg_data_path('data')

    @pytest.mark.remote_data
    def test_http(self):
        """Remote HTTP path."""
        path = 'http://ssb.stsci.edu/cdbs_open/cdbs/mtab/OLD_FILES/'
        with warnings.catch_warnings():
            # Warning issued from html5lib 1.0.1
            warnings.filterwarnings(
                'ignore', message=r'.*Using or importing the ABC.*',
                category=DeprecationWarning)
            filename = stio.get_latest_file(
                path + 'n*tmg.fits', raise_error=True)
        assert filename == path + 'n9i1408hm_tmg.fits'

    def test_local(self):
        """Local data path."""
        template = os.path.join(self.datadir, '*tmg.fits')
        ans = os.path.join(self.datadir, 'tables_tmg.fits')
        filename = stio.get_latest_file(template, raise_error=True)
        assert filename == ans

    def test_bogus(self):
        """Bogus data path."""
        with pytest.warns(AstropyUserWarning, match=r'No files found'):
            filename = stio.get_latest_file(
                os.path.join('foo', 'foo', '*tmg.fits'))
        assert filename == ''

    def test_no_files(self):
        """Real path with no files."""
        template = os.path.join(self.datadir, '*dummy')

        # Warning only
        with pytest.warns(AstropyUserWarning, match=r'No files found'):
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
        stio._read_table(
            tabname, 1,
            {'COMPNAME': np.str_, 'KEYWORD': np.str_, 'INNODE': np.str_,
             'OUTNODE': np.int64, 'THCOMPNAME': np.str_, 'COMMENT': np.str_})

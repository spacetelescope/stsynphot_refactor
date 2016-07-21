"""Adapted from ``astrolib/pysynphot/from_commissioning/acs/test1.py``."""
from __future__ import absolute_import, division, print_function

# STDLIB
import os

# ASTROPY
from astropy.tests.helper import pytest, remote_data
from astropy.utils.data import get_pkg_data_filename

# LOCAL
from .. import HAS_PYSYNPHOT


@pytest.mark.skipif('not HAS_PYSYNPHOT')
def test_acs_local():
    """Some test against ASTROLIB using package data."""
    filename = get_pkg_data_filename(os.path.join('data', 'earthshine.fits'))
    assert filename.endswith('earthshine.fits')


@pytest.mark.skipif('not HAS_PYSYNPHOT')
@remote_data
def test_acs_remote():
    """Some test against ASTROLIB using remote data
    (including Central Storage)."""
    pass

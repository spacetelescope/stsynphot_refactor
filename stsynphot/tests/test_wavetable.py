# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""Test wavetable.py module."""

# THIRD-PARTY
import numpy as np
import pytest

# ASTROPY
from astropy import units as u

# LOCAL
from .. import exceptions
from ..wavetable import WAVECAT


@pytest.mark.parametrize(
    ('obsmode', 'ans'),
    [('nicmos,3,f220m', '(7000.0,29996.0,1.0)'),
     ('acs,hrc,f550m', WAVECAT['acs,hrc']),
     ('stis,ccd,g750m', WAVECAT['stis,g750m']),
     ('stis,fuvmama,g140l,s52x2', WAVECAT['stis,g140l']),
     ('stis,nuvmama,e230h,c2263,s02x02', WAVECAT['stis,e230h,c2263'])])
def test_getitem(obsmode, ans):
    """Waveset catalog access."""
    assert WAVECAT[obsmode] == ans


def test_getitem_exceptions():
    """Waveset catalog exceptions."""
    with pytest.raises(KeyError):
        WAVECAT['johnson,v']
    with pytest.raises(exceptions.AmbiguousObsmode):
        WAVECAT['acs,wfc1,wfc2']


def test_load_waveset_file():
    """Load waveset from file."""
    par, wave = WAVECAT.load_waveset('acs,wfc1')
    assert par.endswith('wavecats/acs.dat')
    assert wave.unit == u.AA
    np.testing.assert_allclose([wave.value[0], wave.value[-1]], [1000, 11000])


@pytest.mark.parametrize(
    ('obsmode', 'ncoeff', 'ans'),
    [('stis,g230l', 3, [1568, 3184]),
     ('wfc3,uvis2,g280', 4, [1850, 9998])])
def test_load_waveset_coeff(obsmode, ncoeff, ans):
    """Load waveset from coefficients."""
    par, wave = WAVECAT.load_waveset(obsmode)
    assert len(par[1:-1].split(',')) == ncoeff
    assert wave.unit == u.AA
    np.testing.assert_allclose([wave.value[0], wave.value[-1]], ans)

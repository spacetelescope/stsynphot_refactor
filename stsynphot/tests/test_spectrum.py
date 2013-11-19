# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""Test spectrum.py module."""
from __future__ import absolute_import, division, print_function, unicode_literals

# THIRD-PARTY
import numpy as np

# SYNPHOT
from synphot import reddening
from synphot import spectrum as synspectrum

# LOCAL
from .. import config, spectrum


def test_vega():
    """Test that Vega spectrum is loaded properly."""
    # Failed load
    spectrum.load_vega('dummyfile')
    assert spectrum.Vega is None

    # Software default
    spectrum.load_vega(area=config.PRIMARY_AREA(), encoding='binary')
    assert isinstance(spectrum.Vega, synspectrum.SourceSpectrum)


def test_ebmvx():
    """Test extinction curve and related cache."""
    ec_mwavg = spectrum.ebmvx('mwavg', 0.3)
    assert isinstance(ec_mwavg, reddening.ExtinctionCurve)
    assert isinstance(spectrum._REDLAWS['mwavg'], reddening.ReddeningLaw)

    for m in ('gal3', None):
        ec_test = spectrum.ebmvx(m, 0.3)
        np.testing.assert_array_equal(ec_test.thru.value, ec_mwavg.thru.value)

    spectrum.reset_cache()
    assert spectrum._REDLAWS == {}

"""Utility functions for commissioning tests."""
from __future__ import absolute_import, division, print_function

# STDLIB
import sys

# THIRD-PARTY
import numpy as np
from numpy.testing import assert_allclose

# ASTROPY
from astropy.tests.helper import pytest, remote_data

# ASTROLIB
try:
    import pysynphot as S
    from pysynphot.spparser import parse_spec as old_parse_spec
except ImportError:
    HAS_PYSYNPHOT = False
else:
    HAS_PYSYNPHOT = True

# LOCAL
from synphot import Observation
from ..config import conf
from ..spectrum import band
from ..spparser import parse_spec

use_pysynphot = pytest.mark.skipif('not HAS_PYSYNPHOT')

__all__ = ['use_pysynphot', 'count_outliers', 'CommCase']


def count_outliers(data, sigma=3.0):
    """Count outliers in given data.

    This is as defined in similar method in ``SpecCase``
    in ``astrolib/pysynphot/from_commissioning/conv_base.py``.

    Parameters
    ----------
    data : ndarray
        Result differences to be analyzed.

    sigma : float
        Values outside this number of sigma of std. dev.
        around mean are considered outliers.

    Returns
    -------
    n_outliers : int
        Number of outlier data points.

    """
    return np.count_nonzero(abs(data) > (data.mean() + sigma * data.std()))


@use_pysynphot
@remote_data
class CommCase(object):
    """Base class for commissioning tests."""
    obsmode = None  # Observation mode string
    spectrum = None  # SYNPHOT-like string to construct spectrum

    # Default tables are the latest available as of 2016-07-25.
    tables = {'graphtable': 'mtab$07r1502mm_tmg.fits',
              'comptable': 'mtab$07r1502nm_tmc.fits',
              'thermtable': 'mtab$tae17277m_tmt.fits'}

    def setup_class(self):
        """Subclass needs to define ``obsmode`` and ``spectrum``
        class variables for this to work.

        """
        if not HAS_PYSYNPHOT:
            raise ImportError(
                'ASTROLIB PYSYNPHOT must be installed to run these tests')

        # Make sure both software use the same graph and component tables.

        conf.graphtable = self.tables['graphtable']
        conf.comptable = self.tables['comptable']
        conf.thermtable = self.tables['thermtable']

        S.setref(graphtable=self.tables['graphtable'],
                 comptable=self.tables['comptable'],
                 thermtable=self.tables['thermtable'])

        # Construct spectra for both software.

        self.sp = parse_spec(self.spectrum)
        self.bp = band(self.obsmode)

        # Astropy version has no prior knowledge of instrument-specific
        # binset, so it has to be set explicitly.
        if hasattr(self.bp, 'binset'):
            self.obs = Observation(self.sp, self.bp, binset=self.bp.binset)
        else:
            self.obs = Observation(self.sp, self.bp)

        self.spref = old_parse_spec(self.spectrum)
        self.bpref = S.ObsBandpass(self.obsmode)
        self.obsref = S.Observation(self.spref, self.bpref)

        # Ensure we are comparing in the same flux unit
        self.spref.convert(self.sp._internal_flux_unit.name)
        self.obsref.convert(self.obs._internal_flux_unit.name)

    @staticmethod
    def _get_new_wave(sp):
        """Astropy version does not assume a default waveset
        (you either have it or you don't). This is a convenience
        method to duck-type ASTROLIB waveset behavior.
        """
        wave = sp.waveset
        if wave is None:
            wave = conf.waveset_array
        else:
            wave = wave.value
        return wave

    # TODO: Make this more reliable?
    @staticmethod
    def _get_flux_atol(flux, factor=2.0, max_no_atol=1e-4):
        """Reasonable limit for atol for flux comparison.
        For example, max flux of 1e-16 will give atol of 1e-32.
        Max flux of 1e-4 or higher will use default atol of 0.

        """
        y = abs(max(flux))

        if y >= max_no_atol:
            flux_atol = 0
        else:
            flux_atol = 10 ** (np.log10(y) * factor)

        # No point going below system limit.
        if flux_atol < sys.float_info.min:
            flux_atol = sys.float_info.min

        return flux_atol

    def test_spec(self, thresh=0.01):
        """Test source spectrum in PHOTLAM."""
        wave = self._get_new_wave(self.sp)
        assert_allclose(wave, self.spref.wave, rtol=thresh)

        flux = self.sp(wave).value
        flux_atol = self._get_flux_atol(flux)
        assert_allclose(flux, self.spref.flux, rtol=thresh, atol=flux_atol)

    def test_thru(self, thresh=0.01, thru_atol=1e-8):
        """Test bandpass. Throughput is always between 0 and 1."""
        wave = self._get_new_wave(self.bp)
        assert_allclose(wave, self.bpref.wave, rtol=thresh)

        thru = self.bp(wave).value
        assert_allclose(thru, self.bpref.throughput, rtol=thresh,
                        atol=thru_atol)

    def test_obs(self, thresh=0.01):
        """Test observation."""

        # Astropy version does not assume a default waveset
        # (you either have it or you don't). If there is no
        # waveset, use ASTROLIB values for flux comparison.
        if self.sp.waveset is None or self.bp.waveset is None:
            wave = self.obsref.wave

        # If there is a valid waveset, compare it as well.
        else:
            wave = self.obs.waveset.value
            assert_allclose(wave, self.obsref.wave, rtol=thresh)

            # Binned data comparison has to happen here because
            # they cannot be resampled.
            binset = self.obs.binset.value
            binflux = self.obs.binflux.value
            flux_atol = self._get_flux_atol(binflux)
            assert_allclose(binset, self.obsref.binwave, rtol=thresh)
            assert_allclose(binflux, self.obsref.binflux, rtol=thresh,
                            atol=flux_atol)

        flux = self.obs(wave).value
        flux_atol = self._get_flux_atol(flux)
        assert_allclose(flux, self.obsref.flux, rtol=thresh, atol=flux_atol)

    def test_countrate(self, thresh=0.01):
        """Test observation countrate calculations."""
        ans = self.obsref.countrate()

        # Astropy version does not assume a default area.
        val = self.obs.countrate(conf.area).value

        assert_allclose(val, ans, rtol=thresh)

    def test_efflam(self, thresh=0.01):
        """Test observation effective wavelength."""
        ans = self.obsref.efflam()
        val = self.obs.effective_wavelength().value
        assert_allclose(val, ans, rtol=thresh)

    def teardown_class(self):
        """Reset config for both software."""
        for cfgname in self.tables:
            conf.reset(cfgname)

        S.setref()


class ThermCase(CommCase):
    """Commissioning tests with thermal component."""

    def test_therm_spec(self, thresh=0.01):
        """Test bandpass thermal spectrum."""
        thspref = self.bpref.obsmode.ThermalSpectrum()
        thsp = self.bp.obsmode.thermal_spectrum()

        # Make sure comparing same unit
        thspref.convert(thsp._internal_flux_unit.name)

        # waveset not expected to be same here, so just compare flux
        flux = thsp(thspref.wave).value
        assert_allclose(flux, thspref.flux, rtol=thresh)

    def test_thermback(self, thresh=0.01):
        """Test bandpass thermal background."""
        ans = self.bpref.thermback()
        val = self.bp.thermback().value

        assert_allclose(val, ans, rtol=thresh)

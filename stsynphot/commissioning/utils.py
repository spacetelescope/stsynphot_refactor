"""Utility functions for commissioning tests."""

# STDLIB
import os
import sys
from collections import Iterable

# THIRD-PARTY
import numpy as np
import pytest
from numpy.testing import assert_allclose

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

# Currently, this is here because only commissioning tests are considered
# slow. If there are slow tests in the core unit tests, we can move this
# one level higher.
try:
    slow = pytest.mark.skipif(not pytest.config.getoption('--slow'),
                              reason='need --slow option to run')
except AttributeError:  # Not using pytest
    slow = pytest.mark.skipif(True, reason='need --slow option to run')

__all__ = ['use_pysynphot', 'slow', 'count_outliers', 'CommCase', 'ThermCase']


def count_outliers(data, sigma=3.0):
    """Count outliers in given data.

    This is as defined in similar method in ``SpecCase``
    in ``astrolib/pysynphot/from_commissioning/conv_base.py``.

    .. note:: This is not used but kept for reference.

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
@slow
@pytest.mark.remote_data
class CommCase:
    """Base class for commissioning tests."""
    obsmode = None  # Observation mode string
    spectrum = None  # SYNPHOT-like string to construct spectrum
    force = None

    # Default tables are the latest available as of 2016-07-25.
    tables = {
        'graphtable': os.path.join('mtab$OLD_FILES', '07r1502mm_tmg.fits'),
        'comptable': os.path.join('mtab$OLD_FILES', '07r1502nm_tmc.fits'),
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
            self.obs = Observation(self.sp, self.bp, force=self.force,
                                   binset=self.bp.binset)
        else:
            self.obs = Observation(self.sp, self.bp, force=self.force)

        # Astropy version does not assume a default waveset
        # (you either have it or you don't). If there is no
        # waveset, no point comparing obs waveset against ASTROLIB.
        if self.sp.waveset is None or self.bp.waveset is None:
            self._has_obswave = False
        else:
            self._has_obswave = True

        self.spref = old_parse_spec(self.spectrum)
        self.bpref = S.ObsBandpass(self.obsmode)
        self.obsref = S.Observation(self.spref, self.bpref, force=self.force)

        # Ensure we are comparing in the same units
        self.bpref.convert(self.bp._internal_wave_unit.name)
        self.spref.convert(self.sp._internal_wave_unit.name)
        self.spref.convert(self.sp._internal_flux_unit.name)
        self.obsref.convert(self.obs._internal_wave_unit.name)
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

    def _assert_allclose(self, actual, desired, rtol=1e-07,
                         atol=sys.float_info.min):
        """``assert_allclose`` only report percentage but we
        also want to know some extra info conveniently."""
        if isinstance(actual, Iterable):
            ntot = len(actual)
        else:
            ntot = 1

        n = np.count_nonzero(
            abs(actual - desired) > atol + rtol * abs(desired))
        msg = (f'obsmode: {self.obsmode}\n'
               f'spectrum: {self.spectrum}\n'
               f'(mismatch {n}/{ntot})')
        assert_allclose(actual, desired, rtol=rtol, atol=atol, err_msg=msg)

    # TODO: Confirm whether non-default atol is acceptable.
    #       Have to use this value to avoid AssertionError for very
    #       small non-zero flux values like 1.8e-26 to 2e-311.
    def _compare_nonzero(self, new, old, thresh=0.01, atol=1e-29):
        """Compare normally when results from both are non-zero."""
        i = (new != 0) & (old != 0)

        # Make sure non-zero atol is not too high, otherwise just let it fail.
        if atol > (thresh * min(new.max(), old.max())):
            atol = sys.float_info.min

        self._assert_allclose(new[i], old[i], rtol=thresh, atol=atol)

    def _compare_zero(self, new, old, thresh=0.01):
        """Special handling for comparison when one of the results
        is zero. This is because ``rtol`` will not work."""
        i = ((new == 0) | (old == 0)) & (new != old)
        try:
            self._assert_allclose(new[i], old[i], rtol=thresh)
        except AssertionError as e:
            pytest.xfail(str(e))  # TODO: Will revisit later

    def test_band_wave(self, thresh=0.01):
        """Test bandpass waveset."""
        wave = self._get_new_wave(self.bp)
        self._assert_allclose(wave, self.bpref.wave, rtol=thresh)

    def test_spec_wave(self, thresh=0.01):
        """Test source spectrum waveset."""
        wave = self._get_new_wave(self.sp)

        # TODO: Failure due to different wavesets for blackbody; Ignore?
        try:
            self._assert_allclose(wave, self.spref.wave, rtol=thresh)
        except (AssertionError, ValueError):
            self._has_obswave = False  # Skip obs waveset tests
            if 'bb(' in self.spectrum:
                pytest.xfail('Blackbody waveset implementations are different')
            elif 'unit(' in self.spectrum:
                pytest.xfail('Flat does not use default waveset anymore')
            else:
                raise

    def test_obs_wave(self, thresh=0.01):
        """Test observation waveset."""
        if not self._has_obswave:  # Nothing to test
            return

        # Native
        wave = self.obs.waveset.value

        # TODO: Failure due to different wavesets for blackbody; Ignore?
        try:
            self._assert_allclose(wave, self.obsref.wave, rtol=thresh)
        except (AssertionError, ValueError):
            if 'bb(' in self.spectrum:
                pytest.xfail('Blackbody waveset implementations are different')
            elif 'unit(' in self.spectrum:
                self._has_obswave = False  # Skip binned flux test
                pytest.xfail('Flat does not use default waveset anymore')
            else:
                raise

        # Binned
        binset = self.obs.binset.value
        self._assert_allclose(binset, self.obsref.binwave, rtol=thresh)

    @pytest.mark.parametrize('thrutype', ['zero', 'nonzero'])
    def test_band_thru(self, thrutype, thresh=0.01):
        """Test bandpass throughput, which is always between 0 and 1."""
        wave = self.bpref.wave
        thru = self.bp(wave).value

        if thrutype == 'zero':
            self._compare_zero(thru, self.bpref.throughput, thresh=thresh)
        else:  # nonzero
            self._compare_nonzero(thru, self.bpref.throughput, thresh=thresh)

    @pytest.mark.parametrize('fluxtype', ['zero', 'nonzero'])
    def test_spec_flux(self, fluxtype, thresh=0.01):
        """Test flux for source spectrum in PHOTLAM."""
        wave = self.spref.wave
        flux = self.sp(wave).value

        if fluxtype == 'zero':
            self._compare_zero(flux, self.spref.flux, thresh=thresh)
        else:  # nonzero
            self._compare_nonzero(flux, self.spref.flux, thresh=thresh)

    @pytest.mark.parametrize('fluxtype', ['zero', 'nonzero'])
    def test_obs_flux(self, fluxtype, thresh=0.01):
        """Test flux for observation in PHOTLAM."""
        wave = self.obsref.wave
        flux = self.obs(wave).value

        # Native
        if fluxtype == 'zero':
            self._compare_zero(flux, self.obsref.flux, thresh=thresh)
        else:  # nonzero
            self._compare_nonzero(flux, self.obsref.flux, thresh=thresh)

        if not self._has_obswave:  # Do not compare binned flux
            return

        # Binned (cannot be resampled)
        binflux = self.obs.binflux.value
        if fluxtype == 'zero':
            self._compare_zero(binflux, self.obsref.binflux, thresh=thresh)
        else:  # nonzero
            try:
                self._compare_nonzero(binflux, self.obsref.binflux,
                                      thresh=thresh)
            except AssertionError as e:
                if 'unit(' in self.spectrum:
                    pytest.xfail('Flat does not use default waveset anymore:\n'
                                 f'{repr(e)}')
                else:
                    raise

    def test_countrate(self, thresh=0.01):
        """Test observation countrate calculations."""
        ans = self.obsref.countrate()

        # Astropy version does not assume a default area.
        val = self.obs.countrate(conf.area).value

        self._assert_allclose(val, ans, rtol=thresh)

    def test_efflam(self, thresh=0.01):
        """Test observation effective wavelength."""
        ans = self.obsref.efflam()
        val = self.obs.effective_wavelength().value
        self._assert_allclose(val, ans, rtol=thresh)

    def teardown_class(self):
        """Reset config for both software."""
        for cfgname in self.tables:
            conf.reset(cfgname)

        S.setref()


class ThermCase(CommCase):
    """Commissioning tests with thermal component."""

    @pytest.mark.parametrize('fluxtype', ['zero', 'nonzero'])
    def test_therm_spec(self, fluxtype, thresh=0.01):
        """Test bandpass thermal spectrum."""
        thspref = self.bpref.obsmode.ThermalSpectrum()
        thsp = self.bp.obsmode.thermal_spectrum()

        # Make sure comparing same units
        thspref.convert(thsp._internal_wave_unit.name)
        thspref.convert(thsp._internal_flux_unit.name)

        # waveset not expected to be same here, so just compare flux
        flux = thsp(thspref.wave).value
        if fluxtype == 'zero':
            self._compare_zero(flux, thspref.flux, thresh=thresh)
        else:  # nonzero
            # TODO: Is the refactored version really better?
            try:
                self._compare_nonzero(flux, thspref.flux, thresh=thresh)
            except AssertionError:
                pytest.xfail('New thermal spectrum samples better')

    def test_thermback(self, thresh=0.01):
        """Test bandpass thermal background."""
        ans = self.bpref.thermback()
        val = self.bp.thermback().value

        self._assert_allclose(val, ans, rtol=thresh)

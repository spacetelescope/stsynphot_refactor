# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""Test spectrum.py module."""
from __future__ import absolute_import, division, print_function, unicode_literals

# STDLIB
import os
import shutil
import tempfile

# THIRD-PARTY
import numpy as np

# ASTROPY
from astropy import units as u
from astropy.io import fits
from astropy.tests.helper import pytest
from astropy.utils.data import get_pkg_data_filename

# SYNPHOT
from synphot import analytic, reddening, units
from synphot import exceptions as synexceptions
from synphot import spectrum as synspectrum
from synphot.utils import trapezoid_integration

# LOCAL
from .. import config, observationmode, spectrum


GT_FILE = get_pkg_data_filename('data/tables_tmg.fits')
CP_FILE = get_pkg_data_filename('data/tables_tmc.fits')
TH_FILE = get_pkg_data_filename('data/tables_tmt.fits')


class TestInterpolateSpectrum(object):
    """Test spectrum interpolation."""
    def setup_class(self):
        self.comp_path = os.path.join(config.ROOTDIR(), 'comp')
        self.fname_acs = os.path.join(
            self.comp_path, 'acs', 'acs_wfc_aper_002_syn.fits[aper#]')
        self.fname_cos = os.path.join(
            self.comp_path, 'cos', 'cos_mcp_g140lc1230_mjd_013_syn.fits[mjd#]')
        self.fname_ramp = os.path.join(
            self.comp_path, 'acs', 'acs_fr656n_005_syn.fits[fr656n#]')
        self.fname_stis = os.path.join(
            self.comp_path, 'stis', 'stis_nm16_mjd_010_syn.fits[MJD#]')
        self.wave_stis = [1049, 2250, 3500, 4750, 6000, 7250, 8500, 9750, 11000]

    def test_no_interp_first_col(self):
        """Test whether the algorithm grabs the correct column
        when the input value is the first column (no interpolation required)
        and there is no THROUGHPUT (default) column present, meaning that the
        interpolation column starts at column 1.

        """
        sp = spectrum.interpolate_spectral_element(self.fname_acs, 0)
        np.testing.assert_array_equal(
            sp.wave.value,
            [3500, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 11000])
        np.testing.assert_allclose(
            sp.thru.value,
            [0.28, 0.22, 0.20999999, 0.22, 0.22, 0.2, 0.15000001, 0.1, 0.04])
        assert 'acs_wfc_aper_002_syn.fits#0' in sp.metadata['expr']

    def test_no_interp_has_err_col(self):
        """Test whether the algorithm grabs the correct column
        when the input value is a column (no interpolation required) and
        an ERROR column is present.

        """
        sp = spectrum.interpolate_spectral_element(self.fname_stis, 51252)
        np.testing.assert_array_equal(sp.wave.value[::25], self.wave_stis)
        np.testing.assert_allclose(
            sp.thru.value[:10],
            [0, 0.965065, 0.965065, 0.965065, 0.963328, 0.976245, 0.983497,
             0.984206, 0.976436, 0.963131])

    def test_interp_mjd(self):
        """Test whether the algorithm gets the correct throughput table
        when input value does not correspond to a column and interpolation
        is required.

        """
        sp = spectrum.interpolate_spectral_element(self.fname_stis, 51000)
        np.testing.assert_array_equal(sp.wave.value[::25], self.wave_stis)
        np.testing.assert_allclose(
            sp.thru.value[:10],
            [0, 0.97830353, 0.97830353, 0.97830353, 0.97722476, 0.98524689,
             0.98975077, 0.99019109, 0.98536552, 0.97710241])
        assert sp.thru.value[0] == sp.thru.value[-1]

    @pytest.mark.parametrize(
        ('interpval', 'ans'),
        [(40000, [0, 0.10225279, 0.06328997, 0.02321319, 0.00536039, 0]),
         (60000, [0, 0.09322135, 0.04873522, 0.01732031, 0.00407352, 0])])
    def test_extrap_mjd(self, interpval, ans):
        """Test extrapolation without using default column."""
        sp = spectrum.interpolate_spectral_element(self.fname_cos, interpval)
        np.testing.assert_allclose(sp.thru.value[400:3000:500], ans, rtol=1e-5)

    def test_interp_ramp(self):
        """Test ramp filter interpolation with wavelength shift."""
        sp = spectrum.interpolate_spectral_element(self.fname_ramp, 6480)
        np.testing.assert_allclose(
            sp.wave.value[:100:10],
            [3499.99902344, 5686, 5736, 5786, 5836, 5886, 5936, 5986, 6036,
             6086])
        np.testing.assert_allclose(
            sp.thru.value[:100:10],
            [5.88854514e-07, 1.00120149e-06, 1.00202179e-06, 1.00353753e-06,
             1.00710832e-06, 1.03335088e-06, 1.34637005e-06, 3.78240595e-06,
             1.53430929e-05, 5.09230156e-05])

    def test_default_ramp(self):
        """Test ramp filter using default THROUGHPUT with warning."""
        sp = spectrum.interpolate_spectral_element(self.fname_ramp, -5)
        np.testing.assert_array_equal(sp.thru, 0)
        assert sp.warnings['DefaultThroughput']

    def test_exceptions(self):
        # Invalid filename format
        with pytest.raises(synexceptions.SynphotError):
            sp = spectrum.interpolate_spectral_element('dummy.fits', -5)

        # Invalid interpolation column name
        with pytest.raises(synexceptions.SynphotError):
            sp = spectrum.interpolate_spectral_element(
                os.path.join(self.comp_path, 'acs',
                             'acs_wfc_aper_002_syn.fits[mjd#]'), 51252)

        # Cannot extrapolate and no default throughput
        with pytest.raises(synexceptions.ExtrapolationNotAllowed):
            sp = spectrum.interpolate_spectral_element(self.fname_acs, -5)


class TestObservationSpectralElement(object):
    """Test ObservationSpectralElement and band() convenience function."""
    def setup_class(self):
        self.outdir = tempfile.mkdtemp()
        self.obs = spectrum.band(
            'acs,hrc,f555w', graphtable=GT_FILE, comptable=CP_FILE)
        self.sp = analytic.flat_spectrum(
            'flam', area=self.obs.primary_area).to_spectrum(self.obs.wave)

    def test_attributes(self):
        assert isinstance(self.obs, synspectrum.SpectralElement)
        assert isinstance(self.obs.obsmode, observationmode.ObservationMode)
        assert str(self.obs) == 'acs,hrc,f555w'
        assert len(self.obs) == 6
        assert self.obs.primary_area.value == config.PRIMARY_AREA()
        np.testing.assert_array_equal(
            [self.obs.binwave.value[0], self.obs.binwave.value[-1]],
            [1000, 11000])

    def test_config_primary_area(self):
        """Changing config after init should have no effect"""
        config.setref(area=1)
        assert config.PRIMARY_AREA() == 1
        assert self.obs.primary_area.value != 1
        config.setref()

    def test_other_graph_table(self):
        """Using the graph table with PRIMAREA."""
        gt_file = get_pkg_data_filename('data/tables_primarea_tmg.fits')
        obs = spectrum.band(
            'acs,hrc,f555w', graphtable=gt_file, comptable=CP_FILE)

        # Primary area should be from graph table
        assert obs.primary_area.value == 100

        # Unit response
        a = obs.unit_response()
        b = units.HC / (100 * trapezoid_integration(
            obs.wave.value, obs.thru.value * obs.wave.value))
        np.testing.assert_allclose(a.value, b.value)

    @pytest.mark.parametrize(
        ('obsmode', 'ans'),
        [('acs,hrc,f555w', 2.9788972414188295e-19),
         ('acs,sbc,f125lp', 1.7218083497870695e-17),
         ('acs,wfc1,f555w,f814w', 1.7485647715025005e-13),
         ('cos,boa,fuv,g130m,c1309', 3.8108219824401987e-15),
         ('stis,ccd,f25ndq1,a2d4,mjd#55555', 3.0597787848106823e-18),
         ('wfc3,ir,f140w', 1.4737148727216957e-20),
         ('wfc3,uvis1,f395n', 5.9433862614148255e-18),
         ('wfc3,uvis2,fq924n', 6.1632709911742462e-18),
         ('wfpc2,1,a2d7,f300w,cont#49892.0', 6.3011E-17),
         ('wfpc2,f555w', 4.8967453103320938e-19)])
    def test_uresp(self, obsmode, ans):
        """Unit response for different detector settings."""
        obs = spectrum.band(obsmode, graphtable=GT_FILE, comptable=CP_FILE)
        np.testing.assert_allclose(obs.unit_response().value, ans, rtol=1e-4)

    def test_countrate(self):
        c = self.obs.countrate(self.sp)
        assert c.unit == u.count / (u.s * units.AREA)
        np.testing.assert_allclose(c.value, 3.357E+18, rtol=1e-5)

        # Invalid source spectrum
        with pytest.raises(synexceptions.SynphotError):
            c = self.obs.countrate(1)

    def test_thermback(self):
        obs = spectrum.band(
            'wfc3,ir,f153m', graphtable=GT_FILE, comptable=CP_FILE)
        bg = obs.thermback(thermtable=TH_FILE)
        assert bg.unit == u.count / u.s / u.pix
        np.testing.assert_allclose(bg.value, 5.9774451061328011e-2, rtol=5e-3)

        # ACS has no thermal background
        with pytest.raises(NotImplementedError):
            bg = self.obs.thermback(thermtable=TH_FILE)

    @pytest.mark.parametrize(
        ('cenwave', 'out_unit', 'ans'),
        [(u.Quantity(500, u.nm), u.nm, [499.9, 500.1]),
         (5000, u.AA, [4999, 5001])])
    def test_wave_range(self, cenwave, out_unit, ans):
        w1, w2 = self.obs.wave_range(cenwave, 2, mode='none')
        assert w1.unit == w2.unit == out_unit
        np.testing.assert_allclose([w1.value, w2.value], ans)

    def test_pixel_range(self):
        npix = self.obs.pixel_range(
            u.Quantity([499.95, 500.05], u.nm), mode='round')
        assert npix == 1

    def test_std_filter(self):
        obs1 = spectrum.band('johnson,v')
        obs2 = synspectrum.SpectralElement.from_filter('johnson_v')
        np.testing.assert_allclose(obs1.thru.value, obs2.thru.value)

    def test_no_obsmode(self):
        """Spectrum without obsmode."""
        obs = spectrum.ObservationSpectralElement([1000, 9000], [1, 1])
        assert obs.obsmode is None
        assert obs.binwave is None
        assert len(obs) == 0

        with pytest.raises(synexceptions.SynphotError):
            a = obs.countrate(self.sp)

        with pytest.raises(synexceptions.SynphotError):
            a = obs.thermback(thermtable=TH_FILE)

        with pytest.raises(synexceptions.UndefinedBinset):
            a = obs.wave_range(5000, 2)

        with pytest.raises(synexceptions.UndefinedBinset):
            a = obs.pixel_range([4000, 5000])

    def test_write_fits(self):
        outfile = os.path.join(self.outdir, 'outspec1.fits')
        self.obs.to_fits(outfile, trim_zero=False, pad_zero_ends=False)

        # Read it back in
        with fits.open(outfile) as pf:
            assert (pf[1].header['grftable'] ==
                    os.path.basename(self.obs.obsmode.gtname))
            assert (pf[1].header['cmptable'] ==
                    os.path.basename(self.obs.obsmode.ctname))

        obs = synspectrum.SpectralElement.from_file(outfile)
        np.testing.assert_allclose(obs.wave.value, self.obs.wave.value)
        np.testing.assert_allclose(obs.thru.value, self.obs.thru.value)

    def teardown_class(self):
        shutil.rmtree(self.outdir)


class TestEbmvx(object):
    """Test extinction curve and related cache."""
    def setup_class(self):
        self.ec_mwavg = spectrum.ebmvx('mwavg', 0.3)

    def test_mwavg(self):
        """No check on data quality, which is dependent on reference file."""
        assert isinstance(self.ec_mwavg, reddening.ExtinctionCurve)
        assert isinstance(spectrum._REDLAWS['mwavg'], reddening.ReddeningLaw)

    @pytest.mark.parametrize('m', ['gal3', None])
    def test_dummy(self, m):
        ec_test = spectrum.ebmvx(m, 0.3)
        np.testing.assert_array_equal(
            ec_test.thru.value, self.ec_mwavg.thru.value)

    def teardown_class(self):
        spectrum.reset_cache()
        assert spectrum._REDLAWS == {}


class TestVega(object):
    """Test that Vega spectrum is loaded properly."""
    def test_default(self):
        assert isinstance(spectrum.Vega, synspectrum.SourceSpectrum)

    def test_failed_load(self):
        spectrum.load_vega('dummyfile')
        assert spectrum.Vega is None

# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""Test spectrum.py module."""

# STDLIB
import os
import shutil
import tempfile
import warnings

# THIRD-PARTY
import numpy as np
import pytest

# ASTROPY
from astropy import units as u
from astropy.io import fits
from astropy.modeling.models import Const1D
from astropy.utils.data import get_pkg_data_filename
from astropy.utils.exceptions import AstropyUserWarning

# SYNPHOT
from synphot import units
from synphot import exceptions as synexceptions
from synphot.models import ConstFlux1D
from synphot.spectrum import SourceSpectrum, SpectralElement

# LOCAL
from .. import spectrum
from ..config import conf
from ..exceptions import PixscaleNotFoundError
from ..stio import irafconvert

GT_FILE = get_pkg_data_filename(os.path.join('data', 'tables_tmg.fits'))
CP_FILE = get_pkg_data_filename(os.path.join('data', 'tables_tmc.fits'))
TH_FILE = get_pkg_data_filename(os.path.join('data', 'tables_tmt.fits'))


@pytest.mark.remote_data
class TestInterpolateSpectrum:
    """Test spectrum interpolation."""
    def setup_class(self):
        self.fname_acs = irafconvert(
            'cracscomp$acs_wfc_aper_002_syn.fits[aper#]')
        self.fname_cos = irafconvert(
            'crcoscomp$cos_mcp_g140lc1230_mjd_013_syn.fits[mjd#]')
        self.fname_ramp = irafconvert(
            'cracscomp$acs_fr656n_005_syn.fits[fr656n#]')
        self.fname_stis = irafconvert(
            'crstiscomp$stis_nm16_mjd_010_syn.fits[MJD#]')
        self.wave_stis = [1049, 2250, 3500, 4750, 6000, 7250, 8500, 9750,
                          11000]

    def test_no_interp_first_col(self):
        """Test whether the algorithm grabs the correct column
        when the input value is the first column (no interpolation required)
        and there is no THROUGHPUT (default) column present, meaning that the
        interpolation column starts at column 1.

        """
        sp = spectrum.interpolate_spectral_element(self.fname_acs, 0)
        w = [3500, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 11000]
        np.testing.assert_allclose(sp.waveset.value, w)
        np.testing.assert_allclose(
            sp(w).value,
            [0.28, 0.22, 0.20999999, 0.22, 0.22, 0.2, 0.15000001, 0.1, 0.04])
        assert 'acs_wfc_aper_002_syn.fits#0' in sp.meta['expr']

    def test_no_interp_has_err_col(self):
        """Test whether the algorithm grabs the correct column
        when the input value is a column (no interpolation required) and
        an ERROR column is present.

        """
        sp = spectrum.interpolate_spectral_element(self.fname_stis, 51252)
        np.testing.assert_allclose(sp.waveset[::25].value, self.wave_stis)
        np.testing.assert_allclose(
            sp(sp.waveset[:10]).value,
            [0, 0.965065, 0.965065, 0.965065, 0.963328, 0.976245, 0.983497,
             0.984206, 0.976436, 0.963131])

    def test_interp_mjd(self):
        """Test whether the algorithm gets the correct throughput table
        when input value does not correspond to a column and interpolation
        is required.

        """
        sp = spectrum.interpolate_spectral_element(self.fname_stis, 51000)
        np.testing.assert_array_equal(sp.waveset[::25].value, self.wave_stis)
        np.testing.assert_allclose(
            sp(sp.waveset[:10]).value,
            [0, 0.97830353, 0.97830353, 0.97830353, 0.97722476, 0.98524689,
             0.98975077, 0.99019109, 0.98536552, 0.97710241])
        assert sp(sp.waveset[0]) == sp(sp.waveset[-1])

    @pytest.mark.parametrize(
        ('interpval', 'ans'),
        [(40000, [0, 0.10225279, 0.06328997, 0.02321319, 0.00536039, 0]),
         (60000, [0, 0.09322135, 0.04873522, 0.01732031, 0.00407352, 0])])
    def test_extrap_mjd(self, interpval, ans):
        """Test extrapolation without using default column."""
        sp = spectrum.interpolate_spectral_element(self.fname_cos, interpval)
        w = sp.waveset[400:3000:500]
        np.testing.assert_allclose(sp(w).value, ans, rtol=1e-5)

    def test_interp_ramp(self):
        """Test ramp filter interpolation with wavelength shift."""
        sp = spectrum.interpolate_spectral_element(self.fname_ramp, 6480)
        w = sp.waveset[:100:10]
        np.testing.assert_allclose(
            w.value,
            [3499.99902344, 5686, 5736, 5786, 5836, 5886, 5936, 5986, 6036,
             6086])
        np.testing.assert_allclose(
            sp(w).value,
            [5.88854514e-07, 1.00120149e-06, 1.00202179e-06, 1.00353753e-06,
             1.00710832e-06, 1.03335088e-06, 1.34637005e-06, 3.78240595e-06,
             1.53430929e-05, 5.09230156e-05])

    def test_default_ramp(self):
        """Test ramp filter using default THROUGHPUT with warning."""
        with pytest.warns(AstropyUserWarning,
                          match=r'Extrapolation not allowed'):
            sp = spectrum.interpolate_spectral_element(self.fname_ramp, -5)
        np.testing.assert_array_equal(sp(sp.waveset), 0)
        assert sp.warnings['DefaultThroughput']

    def test_exceptions(self):
        # Invalid filename format
        with pytest.raises(synexceptions.SynphotError):
            spectrum.interpolate_spectral_element('dummy.fits', -5)

        # Invalid interpolation column name
        with pytest.raises(synexceptions.SynphotError):
            spectrum.interpolate_spectral_element(
                irafconvert('cracscomp$acs_wfc_aper_002_syn.fits[mjd#]'),
                51252)

        # Cannot extrapolate and no default throughput
        with pytest.raises(synexceptions.ExtrapolationNotAllowed):
            spectrum.interpolate_spectral_element(self.fname_acs, -5)


@pytest.mark.remote_data
class TestObservationSpectralElement:
    """Test ``ObservationSpectralElement`` and ``band()``."""
    def setup_class(self):
        self.outdir = tempfile.mkdtemp()
        self.obs = spectrum.band(
            'acs,hrc,f555w', graphtable=GT_FILE, comptable=CP_FILE)
        self.sp = SourceSpectrum(ConstFlux1D, amplitude=1 * units.FLAM)

    def test_attributes(self):
        assert (str(self.obs.obsmode) == self.obs.meta['expr'] ==
                'acs,hrc,f555w')
        assert len(self.obs) == 6
        assert self.obs.area.value == conf.area
        np.testing.assert_array_equal(
            self.obs.waveset[::self.obs.waveset.size - 1].value, [500, 30010])
        np.testing.assert_array_equal(
            self.obs.binset[::self.obs.binset.size - 1].value, [1000, 11000])

    def test_config_primary_area(self):
        """Changing config after init should have no effect"""
        conf.area = 1
        assert conf.area == 1 and self.obs.area.value != 1
        conf.reset('area')

    def test_no_zero_bound(self):
        with pytest.warns(UserWarning, match=r'Unbounded throughput'):
            result = self.obs.bounded_by_zero(wavelengths=[5000, 6000])
        assert not result

    def test_other_graph_table(self):
        """Using the graph table with PRIMAREA."""
        gt_file = get_pkg_data_filename(
            os.path.join('data', 'tables_primarea_tmg.fits'))
        obs = spectrum.band(
            'acs,hrc,f555w', graphtable=gt_file, comptable=CP_FILE)

        # Primary area should be from graph table
        assert obs.area.value == 100

        x = obs.waveset.value
        y = obs(obs.waveset).value

        # Unit response
        a = obs.unit_response(obs.area)
        b = units.HC * 0.01 / abs(np.trapz(x * y, x=x))
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
        with warnings.catch_warnings():
            warnings.filterwarnings(
                'ignore', message=r'.*not valid flux unit.*',
                category=AstropyUserWarning)
            obs = spectrum.band(
                obsmode, graphtable=GT_FILE, comptable=CP_FILE)

        np.testing.assert_allclose(
            obs.unit_response(obs.area).value, ans, rtol=1e-4)

    def test_thermback(self):
        obs = spectrum.band(
            'wfc3,ir,f153m', graphtable=GT_FILE, comptable=CP_FILE)
        bg = obs.thermback(thermtable=TH_FILE)
        np.testing.assert_allclose(
            bg, 5.9774451061328011e-2 * (u.count / u.s / u.pix), rtol=5e-3)

        # ACS has no thermal background
        with pytest.raises(NotImplementedError):
            bg = self.obs.thermback(thermtable=TH_FILE)

    @pytest.mark.parametrize(
        ('cenwave', 'ans'),
        [(500 * u.nm, [499.9, 500.1] * u.nm),
         (5000, [4999, 5001] * u.AA)])
    def test_binned_waverange(self, cenwave, ans):
        np.testing.assert_allclose(
            self.obs.binned_waverange(cenwave, 2, mode='none'), ans)

    def test_binned_pixelrange(self):
        assert self.obs.binned_pixelrange(
            [499.95, 500.05] * u.nm, mode='round') == 1

    def test_std_filter(self):
        obs1 = spectrum.band('johnson,v')
        obs2 = SpectralElement.from_filter('johnson_v', encoding='binary')
        w = obs1.waveset
        np.testing.assert_allclose(obs1(w), obs2(w))

        # No pixel scale
        with pytest.raises(PixscaleNotFoundError):
            obs1.thermback()

        # No binset
        with pytest.raises(synexceptions.UndefinedBinset):
            obs1.binned_waverange(5000, 2)
        with pytest.raises(synexceptions.UndefinedBinset):
            obs1.binned_pixelrange([5000, 5002])

    def test_no_obsmode(self):
        """Spectrum without obsmode."""
        with pytest.raises(synexceptions.SynphotError):
            spectrum.ObservationSpectralElement(Const1D, amplitude=1)

    def test_write_fits(self):
        outfile = os.path.join(self.outdir, 'outspec1.fits')
        self.obs.to_fits(outfile, trim_zero=False, pad_zero_ends=False)

        # Read it back in
        with fits.open(outfile) as pf:
            assert (pf[1].header['grftable'] ==
                    os.path.basename(self.obs.obsmode.gtname))
            assert (pf[1].header['cmptable'] ==
                    os.path.basename(self.obs.obsmode.ctname))

        obs = SpectralElement.from_file(outfile)
        w = self.obs.waveset
        np.testing.assert_allclose(obs.waveset, w)
        np.testing.assert_allclose(obs(w), self.obs(w))

    def test_disabled_methods(self):
        with pytest.raises(NotImplementedError):
            self.obs.taper()
        with pytest.raises(NotImplementedError):
            self.obs.from_file('dummy.fits')
        with pytest.raises(NotImplementedError):
            self.obs.from_filter('johnson_v')

    def teardown_class(self):
        shutil.rmtree(self.outdir)


@pytest.mark.remote_data
class TestEbmvx:
    """Test extinction curve and related cache."""
    def setup_class(self):
        self.ec_mwavg = spectrum.ebmvx('mwavg', 0.3)

        # https://github.com/spacetelescope/synphot_refactor/issues/129
        self.w = np.squeeze(self.ec_mwavg.model.points)

        self.y = self.ec_mwavg(self.w)

    def test_mwavg(self):
        """No check on data quality, which is dependent on reference file."""
        assert spectrum._REDLAWS['mwavg'].meta['expr'] == 'mwavg'

    @pytest.mark.parametrize('m', ['gal3', None])
    def test_dummy(self, m):
        """Dummy values should default to 'mwavg'."""
        ec_test = spectrum.ebmvx(m, 0.3)
        np.testing.assert_array_equal(ec_test(self.w), self.y)

    def teardown_class(self):
        spectrum.reset_cache()
        assert spectrum._REDLAWS == {}


def test_vega_dummy():
    """Test that Vega spectrum is loaded properly."""
    # Dummy
    with pytest.warns(AstropyUserWarning,
                      match=r'Failed to load Vega spectrum'):
        spectrum.load_vega(vegafile='dummyfile.fits', encoding='binary')
    assert spectrum.Vega is None


@pytest.mark.remote_data
def test_vega_default():
    """Test that Vega spectrum is loaded properly."""
    # Default
    spectrum.load_vega(encoding='binary')
    assert 'Vega' in spectrum.Vega.meta['expr']

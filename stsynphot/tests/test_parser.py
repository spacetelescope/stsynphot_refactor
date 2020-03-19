# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""Test spparser.py module, which uses spark.py.

.. note::

    Only testing to see if the parser makes the right kind of
    objects. Quality of the data is tested in other modules.

"""

# STDLIB
import os

# THIRD-PARTY
import pytest
from astropy import units as u
from astropy.tests.helper import assert_quantity_allclose
from astropy.utils.exceptions import AstropyUserWarning
from numpy.testing import assert_allclose

# SYNPHOT
from synphot import exceptions as synexceptions
from synphot import units
from synphot.models import (BlackBodyNorm1D, Box1D, ConstFlux1D, Empirical1D,
                            GaussianFlux1D, PowerLawFlux1D)
from synphot.reddening import ExtinctionCurve
from synphot.spectrum import SourceSpectrum, SpectralElement

# LOCAL
from .. import catalog, exceptions, observationmode, spectrum, spparser
from ..config import conf
from ..stio import resolve_filename


def _single_functioncall(sp, ans_cls, ans_model, ans_name, ans_z=0):
    assert isinstance(sp, ans_cls)

    # Do not check composite model
    if ans_model is not None:
        assert isinstance(sp.model, ans_model)

    if ans_name:
        assert sp.meta['expr'] == ans_name
    if ans_z is not None:
        assert_allclose(sp.z, ans_z)


def _compare_spectra(sp1, sp2):
    """Test that two spectra are basically equivalent."""
    if sp1.waveset is None:
        assert sp2.waveset is None
        w = [100, 5000, 11000] * u.AA
    else:
        w = sp1.waveset
        assert_quantity_allclose(w, sp2.waveset)
    assert_quantity_allclose(sp1(w), sp2(w))
    assert_quantity_allclose(sp1.integrate(wavelengths=w),
                             sp2.integrate(wavelengths=w))
    assert type(sp1.model.__class__) == type(sp2.model.__class__)
    if hasattr(sp1, 'z'):
        assert sp1.z == sp2.z


def test_unit_1_flam():
    sp1 = spparser.parse_spec('unit(1, flam)')
    _single_functioncall(sp1, SourceSpectrum, ConstFlux1D, 'unit(1.0,flam)')

    sp2 = SourceSpectrum(ConstFlux1D, amplitude=1 * units.FLAM)
    _compare_spectra(sp1, sp2)


def test_bb_5000():
    sp1 = spparser.parse_spec('bb(5000)')
    _single_functioncall(sp1, SourceSpectrum, BlackBodyNorm1D, 'bb(5000.0)')

    sp2 = SourceSpectrum(BlackBodyNorm1D, temperature=5000 * u.K)
    _compare_spectra(sp1, sp2)


def test_powerlaw_5000_1_flam():
    sp1 = spparser.parse_spec('pl(5000, 1, flam)')
    _single_functioncall(
        sp1, SourceSpectrum, PowerLawFlux1D, 'pl(5000.0,1.0,flam)')

    sp2 = SourceSpectrum(PowerLawFlux1D, amplitude=1 * units.FLAM,
                         x_0=5000 * u.AA, alpha=-1)
    _compare_spectra(sp1, sp2)


def test_box_5000_1():
    sp1 = spparser.parse_spec('box(5000, 1)')
    _single_functioncall(sp1, SpectralElement, Box1D, 'box(5000.0,1.0)',
                         ans_z=None)

    sp2 = SpectralElement(Box1D, amplitude=1, x_0=5000 * u.AA, width=1 * u.AA)
    _compare_spectra(sp1, sp2)


def test_em_5000_25_1_flam():
    sp1 = spparser.parse_spec('em(5000, 25, 1, flam)')
    _single_functioncall(
        sp1, SourceSpectrum, GaussianFlux1D, 'em(5000, 25, 1, FLAM)')

    f = 1 * (units.FLAM * u.AA)  # Integrated flux
    sp2 = SourceSpectrum(
        GaussianFlux1D, mean=5000 * u.AA, fwhm=25 * u.AA, total_flux=f)
    _compare_spectra(sp1, sp2)


def test_rn_bb_box_abmag():
    sp1 = spparser.parse_spec('rn(bb(5000), box(5000, 10), 17, abmag)')
    _single_functioncall(sp1, SourceSpectrum, None,
                         'rn(bb(5000.0),box(5000.0,10.0),17.0,abmag)')

    bb = SourceSpectrum(BlackBodyNorm1D, temperature=5000 * u.K)
    box = SpectralElement(Box1D, amplitude=1, x_0=5000 * u.AA, width=10 * u.AA)
    sp2 = bb.normalize(17 * u.ABmag, band=box)
    _compare_spectra(sp1, sp2)


def test_z_null():
    """ETC junk spectrum results in flat spectrum with no redshift."""
    sp1 = spparser.parse_spec('z(null, 0.1)')
    _single_functioncall(sp1, SourceSpectrum, ConstFlux1D, 'z(null,0.1)')

    sp2 = SourceSpectrum(ConstFlux1D, amplitude=1 * units.PHOTLAM)
    _compare_spectra(sp1, sp2)


def test_z_em():
    sp1 = spparser.parse_spec('z(em(5000, 25, 1, flam), 0.1)')
    _single_functioncall(
        sp1, SourceSpectrum, None, 'z(em(5000, 25, 1, FLAM),0.1)', ans_z=0.1)

    f = 1 * (units.FLAM * u.AA)  # Integrated flux
    sp2 = SourceSpectrum(
        GaussianFlux1D, mean=5000 * u.AA, fwhm=25 * u.AA, total_flux=f)
    sp2.z = 0.1
    _compare_spectra(sp1, sp2)


@pytest.mark.remote_data
def test_remote_spec_vegafile():
    sp1 = spparser.parse_spec('spec(crcalspec$alpha_lyr_stis_007.fits)')
    _single_functioncall(sp1, SourceSpectrum, Empirical1D,
                         'spec(crcalspec$alpha_lyr_stis_007.fits)')

    sp2 = SourceSpectrum.from_file(resolve_filename(
        os.environ['PYSYN_CDBS'], 'calspec', 'alpha_lyr_stis_007.fits'))
    _compare_spectra(sp1, sp2)


@pytest.mark.remote_data
def test_remote_band_v():
    sp1 = spparser.parse_spec('band(v)')
    _single_functioncall(
        sp1, spectrum.ObservationSpectralElement, Empirical1D, 'band(v)',
        ans_z=None)

    sp2 = SpectralElement.from_filter('johnson_v')
    _compare_spectra(sp1, sp2)


@pytest.mark.remote_data
def test_remote_icat_k93():
    sp1 = spparser.parse_spec('icat(k93models, 5000, 0.5, 0)')
    _single_functioncall(sp1, SourceSpectrum, Empirical1D,
                         'k93models(T_eff=5000,metallicity=0.5,log_g=0)')

    sp2 = catalog.grid_to_spec('k93models', 5000, 0.5, 0)
    _compare_spectra(sp1, sp2)


@pytest.mark.remote_data
def test_remote_ebmvx_mwavg():
    sp1 = spparser.parse_spec('ebmvx(0.3, mwavg)')
    _single_functioncall(
        sp1, ExtinctionCurve, Empirical1D, 'ebmvx(0.3,mwavg)', ans_z=None)

    sp2 = spectrum.ebmvx('mwavg', 0.3)
    _compare_spectra(sp1, sp2)


@pytest.mark.remote_data
def test_remote_rn_calspec_box():
    sp1 = spparser.parse_spec(
        'rn(crcalspec$gd71_mod_005.fits, box(5000, 10), 17, vegamag)')
    _single_functioncall(
        sp1, SourceSpectrum, None,
        'rn(crcalspec$gd71_mod_005.fits,box(5000.0,10.0),17.0,vegamag)')

    gd71 = SourceSpectrum.from_file(resolve_filename(
        os.environ['PYSYN_CDBS'], 'calspec', 'gd71_mod_005.fits'))
    box = SpectralElement(Box1D, amplitude=1, x_0=5000 * u.AA, width=10 * u.AA)
    sp2 = gd71.normalize(17 * units.VEGAMAG, band=box, vegaspec=spectrum.Vega)
    _compare_spectra(sp1, sp2)


@pytest.mark.remote_data
def test_remote_rn_icat_k93():
    sp1 = spparser.parse_spec(
        'rn(icat(k93models, 5000, 0.5, 0), '
        'cracscomp$acs_f814w_hrc_006_syn.fits, 17, obmag)')
    _single_functioncall(
        sp1, SourceSpectrum, None,
        'rn(k93models(T_eff=5000,metallicity=0.5,log_g=0),'
        'cracscomp$acs_f814w_hrc_006_syn.fits,17.0,obmag)')

    k93 = catalog.grid_to_spec('k93models', 5000, 0.5, 0)
    bp = SpectralElement.from_file(resolve_filename(
        os.environ['PYSYN_CDBS'], 'comp', 'acs', 'acs_f814w_hrc_006_syn.fits'))
    sp2 = k93.normalize(17 * units.OBMAG, band=bp, area=conf.area)
    _compare_spectra(sp1, sp2)


@pytest.mark.remote_data
def test_remote_rn_powerlaw():
    sp1 = spparser.parse_spec('rn(pl(5000, 1, flam), band(v), 1, photlam)')
    _single_functioncall(sp1, SourceSpectrum, None,
                         'rn(pl(5000.0,1.0,flam),band(v),1.0,photlam)')

    pl = SourceSpectrum(PowerLawFlux1D, amplitude=1 * units.FLAM,
                        x_0=5000 * u.AA, alpha=-1)
    bp = SpectralElement.from_filter('johnson_v')
    sp2 = pl.normalize(1 * units.PHOTLAM, band=bp)
    _compare_spectra(sp1, sp2)


@pytest.mark.remote_data
def test_remote_rn_unit_1_flam():
    sp1 = spparser.parse_spec(
        'rn(unit(1,flam), band(acs, wfc1, fr388n#3881.0), 10, abmag)')
    _single_functioncall(
        sp1, SourceSpectrum, None,
        'rn(unit(1.0,flam),band(acs,wfc1,fr388n#3881.0),10.0,abmag)')

    constsp = SourceSpectrum(ConstFlux1D, amplitude=1 * units.FLAM)
    bp = spectrum.band('acs, wfc1, fr388n#3881.0')
    sp2 = constsp.normalize(10 * u.ABmag, band=bp)
    _compare_spectra(sp1, sp2)


@pytest.mark.remote_data
def test_remote_rn_calspec_u():
    sp1 = spparser.parse_spec(
        'rn(crcalspec$bd_75d325_stis_002.fits, band(u), 9.5, vegamag) * '
        'band(fos, blue, 4.3, g160l)')
    # NOTE: No expr for this combo.
    _single_functioncall(sp1, SourceSpectrum, None, '')

    bd75 = SourceSpectrum.from_file(resolve_filename(
        os.environ['PYSYN_CDBS'], 'calspec', 'bd_75d325_stis_002.fits'))
    bp_u = SpectralElement.from_filter('johnson_u')
    bd75_norm = bd75.normalize(
        9.5 * units.VEGAMAG, band=bp_u, vegaspec=spectrum.Vega)
    bp_fos = spectrum.band('fos, blue, 4.3, g160l')
    sp2 = bd75_norm * bp_fos
    _compare_spectra(sp1, sp2)


@pytest.mark.remote_data
def test_remote_z_vega():
    sp1 = spparser.parse_spec('z(crcalspec$alpha_lyr_stis_007.fits, 0.1)')
    _single_functioncall(sp1, SourceSpectrum, None,
                         'z(crcalspec$alpha_lyr_stis_007.fits,0.1)', ans_z=0.1)

    sp2 = SourceSpectrum.from_file(resolve_filename(
        os.environ['PYSYN_CDBS'], 'calspec', 'alpha_lyr_stis_007.fits'))
    sp2.z = 0.1
    _compare_spectra(sp1, sp2)


@pytest.mark.remote_data
class TestRenormPartialOverlap:
    """Test handling of ``rn(...)`` syntax for partial overlap."""
    def setup_class(self):
        self.fname = resolve_filename(
            conf.rootdir, 'etc', 'source', 'qso_fos_001.dat')

    def test_partial(self):
        """Warning only."""
        input_str = f'rn({self.fname}, band(johnson, u), 15, abmag)'
        with pytest.warns(AstropyUserWarning,
                          match=r'Spectrum is not defined everywhere'):
            sp = spparser.parse_spec(input_str)
        assert isinstance(sp, SourceSpectrum)
        assert 'force_renorm' in sp.warnings

        name = sp.meta['expr']
        assert (name.startswith('rn(') and
                name.endswith('qso_fos_001.dat,band(johnson,u),15.0,abmag)'))

    def test_disjoint(self):
        """Raise error."""
        input_str = f'rn({self.fname}, band(johnson, v), 15, abmag)'
        with pytest.raises(synexceptions.DisjointError):
            spparser.parse_spec(input_str)


@pytest.mark.remote_data
class TestEnvVar:
    """Test syntax using PYSYN_CDBS environment variable."""
    def setup_class(self):
        self.old_path = os.environ.get('PYSYN_CDBS')
        if self.old_path is None:
            os.environ['PYSYN_CDBS'] = conf.rootdir

    def test_double_slash(self):
        sp = spparser.parse_spec(
            'spec($PYSYN_CDBS//calspec/gd71_mod_005.fits)')
        assert isinstance(sp, SourceSpectrum)
        assert isinstance(sp.model, Empirical1D)

    def teardown_class(self):
        if self.old_path is None:
            del os.environ['PYSYN_CDBS']


@pytest.mark.parametrize(
    'input_str',
    ['foo(1)',
     'unit(1, nm)',
     'unit(1, vegamag)',
     'pl(5000, 1, nm)',
     'pl(5000, 1, vegamag)',
     'em(5000, 25, 1, nm)',
     'rn(bb(5000), foo(v), 17, obmag)',
     'rn(unit(1, flam), band(stis, ccd, g430m, c4451, 52X0.2), 10, abmag)',
     'rn(unit(1, flam), band(stis, ccd, mirror, 50CCD), 10, abmag)',
     'ebmvx(0.3, foo)'])
def test_parser_exception(input_str):
    """Test syntax that raises ParserError."""
    with pytest.raises(exceptions.ParserError):
        spparser.parse_spec(input_str)


class TestTokens:
    """Test underlying parser engine."""
    def setup_class(self):
        self.scanner = spparser.Scanner()

    @pytest.mark.parametrize(
        ('token_type', 'token_str'),
        [('FLOAT', '.1'),
         ('FLOAT', '1.1'),
         ('FLOAT', '1.'),
         ('FLOAT', '1'),
         ('FLOAT', '.1e+1'),
         ('FLOAT', '1.1e+1'),
         ('FLOAT', '1.e+1'),
         ('FLOAT', '1e+1'),
         ('FLOAT', '.1e-1'),
         ('FLOAT', '1.1e-1'),
         ('FLOAT', '1.e-1'),
         ('FLOAT', '1e-1'),
         ('FLOAT', '.1e1'),
         ('FLOAT', '1.1e1'),
         ('FLOAT', '1.e1'),
         ('FLOAT', '1e1'),
         ('IDENTIFIER', '/'),
         ('IDENTIFIER', 'xyzzy'),
         ('IDENTIFIER', 'xy20zzy'),
         ('IDENTIFIER', 'xyzzy20'),
         ('IDENTIFIER', '/a/b/c'),
         ('IDENTIFIER', 'foo$bar'),
         ('IDENTIFIER', 'a/b'),
         ('IDENTIFIER', '/a/b/c/foo.fits'),
         ('IDENTIFIER', 'C:/a/b/c/foo.fits')])
    def test_single_token_1(self, token_type, token_str):
        t = self.scanner.tokenize(token_str)
        assert (t[0].type, t[0].attr) == (token_type, token_str)

    @pytest.mark.parametrize(
        ('token_str', 'ans'),
        [('(', ('LPAREN', None)),
         (')', ('RPAREN', None)),
         (',', (',', None)),
         ('+', ('+', None)),
         ('*', ('*', None)),
         ('@foolist', ('FILELIST', 'foolist'))])
    def test_single_token_2(self, token_str, ans):
        t = self.scanner.tokenize(token_str)
        assert (t[0].type, t[0].attr) == ans

    @pytest.mark.parametrize(
        ('input_str', 'ans'),
        [('50CCD',
          [('FLOAT', '50'),
           ('IDENTIFIER', 'CCD')]),
         ('500X0.2',
          [('FLOAT', '500'),
           ('IDENTIFIER', 'X0.2')]),
         ('spec($PYSYN_CDBS//calspec/gd71_mod_005.fits)',
          [('IDENTIFIER', 'spec'),
           ('LPAREN', None),
           ('IDENTIFIER', '$PYSYN_CDBS//calspec/gd71_mod_005.fits'),
           ('RPAREN', None)]),
         ('spec(earthshine.fits) * 0.5 + '
          'rn(spec(Zodi.fits), band(johnson, v), 22.7, vegamag) + '
          '(spec(el1215a.fits) + spec(el1302a.fits) + spec(el1356a.fits) + '
          'spec(el2471a.fits)) * 0.5',
          [('IDENTIFIER', 'spec'),
           ('LPAREN', None),
           ('IDENTIFIER', 'earthshine.fits'),
           ('RPAREN', None),
           ('*', None),
           ('FLOAT', '0.5'),
           ('+', None),
           ('IDENTIFIER', 'rn'),
           ('LPAREN', None),
           ('IDENTIFIER', 'spec'),
           ('LPAREN', None),
           ('IDENTIFIER', 'Zodi.fits'),
           ('RPAREN', None),
           (',', None),
           ('IDENTIFIER', 'band'),
           ('LPAREN', None),
           ('IDENTIFIER', 'johnson'),
           (',', None),
           ('IDENTIFIER', 'v'),
           ('RPAREN', None),
           (',', None),
           ('FLOAT', '22.7'),
           (',', None),
           ('IDENTIFIER', 'vegamag'),
           ('RPAREN', None),
           ('+', None),
           ('LPAREN', None),
           ('IDENTIFIER', 'spec'),
           ('LPAREN', None),
           ('IDENTIFIER', 'el1215a.fits'),
           ('RPAREN', None),
           ('+', None),
           ('IDENTIFIER', 'spec'),
           ('LPAREN', None),
           ('IDENTIFIER', 'el1302a.fits'),
           ('RPAREN', None),
           ('+', None),
           ('IDENTIFIER', 'spec'),
           ('LPAREN', None),
           ('IDENTIFIER', 'el1356a.fits'),
           ('RPAREN', None),
           ('+', None),
           ('IDENTIFIER', 'spec'),
           ('LPAREN', None),
           ('IDENTIFIER', 'el2471a.fits'),
           ('RPAREN', None),
           ('RPAREN', None),
           ('*', None),
           ('FLOAT', '0.5')]),
         ('spec(earthshine.fits) * 0.5 + '
          'rn(spec(Zodi.fits), band(johnson, v), 22.7, vegamag) + '
          '(spec(el1215a.fits) * 0.1 + spec(el1302a.fits) * 0.066666667 + '
          'spec(el1356a.fits) * 0.0060 + spec(el2471a.fits) * 0.0050)',
          [('IDENTIFIER', 'spec'),
           ('LPAREN', None),
           ('IDENTIFIER', 'earthshine.fits'),
           ('RPAREN', None),
           ('*', None),
           ('FLOAT', '0.5'),
           ('+', None),
           ('IDENTIFIER', 'rn'),
           ('LPAREN', None),
           ('IDENTIFIER', 'spec'),
           ('LPAREN', None),
           ('IDENTIFIER', 'Zodi.fits'),
           ('RPAREN', None),
           (',', None),
           ('IDENTIFIER', 'band'),
           ('LPAREN', None),
           ('IDENTIFIER', 'johnson'),
           (',', None),
           ('IDENTIFIER', 'v'),
           ('RPAREN', None),
           (',', None),
           ('FLOAT', '22.7'),
           (',', None),
           ('IDENTIFIER', 'vegamag'),
           ('RPAREN', None),
           ('+', None),
           ('LPAREN', None),
           ('IDENTIFIER', 'spec'),
           ('LPAREN', None),
           ('IDENTIFIER', 'el1215a.fits'),
           ('RPAREN', None),
           ('*', None),
           ('FLOAT', '0.1'),
           ('+', None),
           ('IDENTIFIER', 'spec'),
           ('LPAREN', None),
           ('IDENTIFIER', 'el1302a.fits'),
           ('RPAREN', None),
           ('*', None),
           ('FLOAT', '0.066666667'),
           ('+', None),
           ('IDENTIFIER', 'spec'),
           ('LPAREN', None),
           ('IDENTIFIER', 'el1356a.fits'),
           ('RPAREN', None),
           ('*', None),
           ('FLOAT', '0.0060'),
           ('+', None),
           ('IDENTIFIER', 'spec'),
           ('LPAREN', None),
           ('IDENTIFIER', 'el2471a.fits'),
           ('RPAREN', None),
           ('*', None),
           ('FLOAT', '0.0050'),
           ('RPAREN', None)]),
         ('spec(earthshine.fits) * 0.5 + '
          'rn(spec(Zodi.fits), band(johnson, v), 22.7, vegamag) + '
          '(spec(el1215a.fits) + spec(el1302a.fits) + spec(el1356a.fits) + '
          'spec(el2471a.fits))',
          [('IDENTIFIER', 'spec'),
           ('LPAREN', None),
           ('IDENTIFIER', 'earthshine.fits'),
           ('RPAREN', None),
           ('*', None),
           ('FLOAT', '0.5'),
           ('+', None),
           ('IDENTIFIER', 'rn'),
           ('LPAREN', None),
           ('IDENTIFIER', 'spec'),
           ('LPAREN', None),
           ('IDENTIFIER', 'Zodi.fits'),
           ('RPAREN', None),
           (',', None),
           ('IDENTIFIER', 'band'),
           ('LPAREN', None),
           ('IDENTIFIER', 'johnson'),
           (',', None),
           ('IDENTIFIER', 'v'),
           ('RPAREN', None),
           (',', None),
           ('FLOAT', '22.7'),
           (',', None),
           ('IDENTIFIER', 'vegamag'),
           ('RPAREN', None),
           ('+', None),
           ('LPAREN', None),
           ('IDENTIFIER', 'spec'),
           ('LPAREN', None),
           ('IDENTIFIER', 'el1215a.fits'),
           ('RPAREN', None),
           ('+', None),
           ('IDENTIFIER', 'spec'),
           ('LPAREN', None),
           ('IDENTIFIER', 'el1302a.fits'),
           ('RPAREN', None),
           ('+', None),
           ('IDENTIFIER', 'spec'),
           ('LPAREN', None),
           ('IDENTIFIER', 'el1356a.fits'),
           ('RPAREN', None),
           ('+', None),
           ('IDENTIFIER', 'spec'),
           ('LPAREN', None),
           ('IDENTIFIER', 'el2471a.fits'),
           ('RPAREN', None),
           ('RPAREN', None)])])
    def test_composite_token(self, input_str, ans):
        t = self.scanner.tokenize(input_str)
        for expect, actual in zip(ans, t):
            assert (actual.type, actual.attr) == expect


def teardown_module():
    """Clear all cache."""
    catalog.reset_cache()
    observationmode.reset_cache()
    spectrum.reset_cache()

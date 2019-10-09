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
from astropy.utils.exceptions import AstropyUserWarning

# SYNPHOT
from synphot import exceptions as synexceptions
from synphot.models import (Box1D, ConstFlux1D, Empirical1D, Gaussian1D,
                            PowerLawFlux1D)
from synphot.reddening import ExtinctionCurve
from synphot.spectrum import SourceSpectrum, SpectralElement

# LOCAL
from .. import catalog, exceptions, observationmode, spectrum, spparser
from ..config import conf


def _single_functioncall(input_str, ans_cls, ans_model):
    sp = spparser.parse_spec(input_str)
    assert isinstance(sp, ans_cls)

    # Do not check composite model
    if ans_model is not None:
        assert isinstance(sp.model, ans_model)


@pytest.mark.parametrize(
    ('input_str', 'ans_cls', 'ans_model'),
    [('unit(1, flam)', SourceSpectrum, ConstFlux1D),
     ('bb(5000)', SourceSpectrum, None),
     ('pl(5000, 1, flam)', SourceSpectrum, PowerLawFlux1D),
     ('box(5000, 1)', SpectralElement, Box1D),
     ('em(5000, 25, 1, flam)', SourceSpectrum, Gaussian1D),
     ('rn(bb(5000), box(5000, 10), 17, abmag)', SourceSpectrum, None),
     ('z(null, 0.1)', SourceSpectrum, ConstFlux1D),
     ('z(em(5000, 25, 1, flam), 0.1)', SourceSpectrum, None)])
def test_single_functioncall(input_str, ans_cls, ans_model):
    """Test parser function calls."""
    _single_functioncall(input_str, ans_cls, ans_model)


@pytest.mark.remote_data
@pytest.mark.parametrize(
    ('input_str', 'ans_cls', 'ans_model'),
    [('spec(crcalspec$alpha_lyr_stis_007.fits)', SourceSpectrum, Empirical1D),
     ('band(v)', spectrum.ObservationSpectralElement, Empirical1D),
     ('icat(k93models, 5000, 0.5, 0)', SourceSpectrum, None),
     ('ebmvx(0.3, mwavg)', ExtinctionCurve, Empirical1D),
     ('rn(crcalspec$gd71_mod_005.fits, box(5000, 10), 17, vegamag)',
      SourceSpectrum, None),
     ('rn(icat(k93models, 5000, 0.5, 0), '
      'cracscomp$acs_f814w_hrc_006_syn.fits, 17, obmag)',
      SourceSpectrum, None),
     ('rn(pl(5000, 1, flam), band(v), 1, photlam)',
      SourceSpectrum, None),
     ('rn(unit(1,flam), band(acs, wfc1, fr388n#3881.0), 10, abmag)',
      SourceSpectrum, None),
     ('rn(crcalspec$bd_75d325_stis_002.fits, band(u), 9.5, vegamag) * '
      'band(fos, blue, 4.3, g160l)', SourceSpectrum, None),
     ('z(crcalspec$alpha_lyr_stis_007.fits, 0.1)', SourceSpectrum, None)])
def test_single_functioncall_remote(input_str, ans_cls, ans_model):
    """Test parser function calls with remote data."""
    _single_functioncall(input_str, ans_cls, ans_model)


@pytest.mark.remote_data
class TestRenormPartialOverlap(object):
    """Test handling of ``rn(...)`` syntax for partial overlap."""
    def setup_class(self):
        self.fname = os.path.join(
            conf.rootdir, 'etc', 'source', 'qso_fos_001.dat')

    def test_partial(self):
        """Warning only."""
        input_str = 'rn({0}, band(johnson, u), 15, abmag)'.format(self.fname)
        with pytest.warns(AstropyUserWarning,
                          match=r'Spectrum is not defined everywhere'):
            sp = spparser.parse_spec(input_str)
        assert isinstance(sp, SourceSpectrum)
        assert 'force_renorm' in sp.warnings

    def test_disjoint(self):
        """Raise error."""
        input_str = 'rn({0}, band(johnson, v), 15, abmag)'.format(self.fname)
        with pytest.raises(synexceptions.DisjointError):
            spparser.parse_spec(input_str)


@pytest.mark.remote_data
class TestEnvVar(object):
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


class TestTokens(object):
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

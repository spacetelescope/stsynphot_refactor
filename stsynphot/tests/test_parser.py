# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""Test spparser.py module, which uses spark.py.

.. note::

    Only testing to see if the parser makes the right kind of
    objects. Quality of the data is tested in other modules.

"""
from __future__ import absolute_import, division, print_function, unicode_literals

# STDLIB
import os

# ASTROPY
from astropy import units as u
from astropy.tests.helper import pytest

# SYNPHOT
from synphot import analytic, reddening
from synphot import exceptions as synexceptions
from synphot import spectrum as synspectrum

# LOCAL
from .. import catalog, config, exceptions, observationmode, spectrum, spparser


_DEFAULT_AREA = config.PRIMARY_AREA()


def test_unit_and_area():
    """Test unit(...) syntax and also config changes."""
    sp = spparser.parse_spec('unit(1, flam)')
    assert isinstance(sp, analytic.Const1DSpectrum)
    assert sp.primary_area == _DEFAULT_AREA

    # Non-default area
    config.setref(area=1)
    sp = spparser.parse_spec('unit(1, flam)')
    assert sp.primary_area == 1

    # Restore default
    config.setref()


@pytest.mark.parametrize(
    ('input_str', 'ans_cls'),
    [('bb(5000)', analytic.BlackBody1DSpectrum),
     ('pl(5000, 1, flam)', analytic.PowerLaw1DSpectrum),
     ('box(5000, 1)', analytic.Box1DSpectrum),
     ('spec(crcalspec$alpha_lyr_stis_005.fits)', synspectrum.SourceSpectrum),
     ('band(v)', spectrum.ObservationSpectralElement),
     ('em(5000, 25, 1, flam)', analytic.Gaussian1DSpectrum),
     ('icat(k93models, 5000, 0.5, 0)', synspectrum.SourceSpectrum),
     ('ebmvx(0.3, mwavg)', reddening.ExtinctionCurve),
     ('z(null, 0.1)', analytic.Const1DSpectrum),
     ('z(crcalspec$alpha_lyr_stis_005.fits, 0.1)', synspectrum.SourceSpectrum),
     ('z(em(5000, 25, 1, flam), 0.1)', synspectrum.SourceSpectrum),
     ('rn(crcalspec$gd71_mod_005.fits, box(5000, 10), 17, vegamag)',
      synspectrum.SourceSpectrum),
     ('rn(bb(5000), box(5000, 10), 17, abmag)', synspectrum.SourceSpectrum),
     ('rn(icat(k93models, 5000, 0.5, 0), cracscomp$acs_f814w_hrc_006_syn.fits, '
      '17, obmag)', synspectrum.SourceSpectrum),
     ('rn(pl(5000, 1, flam), band(v), 1, photlam)',
      synspectrum.SourceSpectrum),
     ('rn(unit(1,flam), band(acs, wfc1, fr388n#3881.0), 10, abmag)',
      synspectrum.SourceSpectrum),
     ('rn(crcalspec$bd_75d325_stis_002.fits, band(u), 9.5, vegamag) * '
      'band(fos, blue, 4.3, g160l)', synspectrum.SourceSpectrum)])
def test_single_functioncall(input_str, ans_cls):
    """Test other function calls."""
    sp = spparser.parse_spec(input_str)
    assert isinstance(sp, ans_cls)

    if isinstance(sp, synspectrum.BaseSpectrum):
        assert sp.warnings == {}
        assert sp.primary_area.value == _DEFAULT_AREA
    else:
        assert sp.primary_area == _DEFAULT_AREA


class TestRenormPartialOverlap(object):
    """Test handling of rn(...) syntax for partial overlap."""
    def setup_class(self):
        self.fname = os.path.join(
            config.ROOTDIR(), 'etc', 'source', 'qso_fos_001.dat')

    def test_partial(self):
        """Warning only."""
        input_str = 'rn({0}, band(johnson, u), 15, abmag)'.format(self.fname)
        sp = spparser.parse_spec(input_str)
        assert isinstance(sp, synspectrum.SourceSpectrum)
        assert 'force_renorm' in sp.warnings

    def test_disjoint(self):
        """Raise error."""
        input_str = 'rn({0}, band(johnson, v), 15, abmag)'.format(self.fname)
        with pytest.raises(synexceptions.DisjointError):
            sp = spparser.parse_spec(input_str)


class TestEnvVar(object):
    """Test syntax using PYSYN_CDBS environment variable."""
    def setup_class(self):
        self.old_path = os.environ.get('PYSYN_CDBS')
        if self.old_path is None:
            os.environ['PYSYN_CDBS'] = config.ROOTDIR()

    def test_double_slash(self):
        sp = spparser.parse_spec('spec($PYSYN_CDBS//calspec/gd71_mod_005.fits)')
        assert isinstance(sp, synspectrum.SourceSpectrum)

    def teardown_class(self):
        if self.old_path is None:
            del os.environ['PYSYN_CDBS']


@pytest.mark.parametrize(
    'input_str',
    ['unit(1,nm)',
     'pl(5000, 1, nm)',
     'em(5000, 25, 1, nm)',
     'ebmvx(0.3, foo)',
     'foo(1)',
     'rn(bb(5000), foo(v), 17, obmag)',
     'rn(unit(1, flam), band(stis, ccd, g430m, c4451, 52X0.2), 10, abmag)',
     'rn(unit(1, flam), band(stis, ccd, mirror, 50CCD), 10, abmag)'])
def test_parser_exception(input_str):
    """Test syntax that raises ParserError."""
    with pytest.raises(exceptions.ParserError):
        sp = spparser.parse_spec(input_str)


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

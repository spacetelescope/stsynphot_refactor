"""This module contains ACS/HRC commissioning tests.
Adapted from ``astrolib/pysynphot/from_commissioning/acs/test1.py``,
``astrolib/pysynphot/from_commissioning/acs/test2.py``, and most of
``astrolib/pysynphot/from_commissioning/acs/test3.py``.
"""
from __future__ import absolute_import, division, print_function

# STDLIB
import os
import shutil

# THIRD-PARTY
from astropy.tests.helper import pytest
from astropy.utils.data import get_pkg_data_filename

# LOCAL
from ..utils import CommCase

# Local test data
datafiles = ['earthshine.fits', 'el1215a.fits', 'el1302a.fits', 'el1356a.fits',
             'el2471a.fits', 'Zodi.fits']


def setup_module(module):
    """Copy test data to working directory so ``parse_spec`` works
    properly for both ``stsynphot`` and ASTROLIB PYSYNPHOT."""
    for datafile in datafiles:
        src = get_pkg_data_filename(os.path.join('data', datafile))
        shutil.copyfile(src, datafile)


def teardown_module(module):
    """Clean up test data in working directory."""
    for datafile in datafiles:
        os.remove(datafile)


class Test472(CommCase):
    obsmode = 'acs,hrc,coron,fr388n#3880'
    spectrum = 'rn(unit(1.0,flam),band(johnson,v),15,vegamag)'


class Test473(Test472):
    spectrum = 'rn(unit(1.0,flam),band(johnson,v),5,vegamag)'


class Test474(Test472):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)')

    # TODO: Revisit failure on only one data point; Insignificant?
    @pytest.mark.parametrize('fluxtype', ['zero', 'nonzero'])
    def test_obs_flux(self, fluxtype, thresh=0.01):
        try:
            super(Test474, self).test_obs_flux(fluxtype, thresh=thresh)
        except AssertionError as e:
            if fluxtype == 'nonzero':
                pytest.xfail(str(e))
            else:
                raise


class Test475(Test474):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),30.0,vegamag)')


class Test476(Test474):
    spectrum = 'spec(earthshine.fits)*0.5+spec(Zodi.fits)*1.0'


class Test477(Test474):
    spectrum = 'spec(earthshine.fits)*0.5+spec(Zodi.fits)*1.25'


class Test478(Test474):
    spectrum = 'spec(earthshine.fits)*0.5+spec(Zodi.fits)*2.0'


class Test479(Test474):
    spectrum = 'spec(earthshine.fits)*0.5+spec(Zodi.fits)*4.0'


class Test480(CommCase):
    obsmode = 'acs,hrc,f220w'
    spectrum = '$PYSYN_CDBS/calspec/g191b2b_mod_004.fits'


class Test481(Test480):
    spectrum = '$PYSYN_CDBS/calspec/gd153_mod_004.fits'


class Test482(Test480):
    spectrum = '$PYSYN_CDBS/calspec/gd71_mod_005.fits'


# Duplicate of Test480 and the syntax already tested in Test507
# class Test483(Test480):
#    spectrum = 'crcalspec$g191b2b_mod_004.fits'


class Test484(Test480):
    spectrum = 'rn(unit(1.0,flam),box(5500.0,1.0),1e-18,flam)'


class Test485(Test480):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)+(spec(el1215a.fits)+'
                'spec(el1302a.fits)+spec(el1356a.fits)+spec(el2471a.fits))')


class Test486(CommCase):
    obsmode = 'acs,hrc,f250w'
    spectrum = '$PYSYN_CDBS/calspec/g191b2b_mod_004.fits'


class Test487(Test486):
    spectrum = '$PYSYN_CDBS/calspec/gd153_mod_004.fits'


# Duplicate of Test490 and syntax already tested in Test482
# class Test488(Test486):
#    spectrum = '$PYSYN_CDBS/calspec/gd71_mod_005.fits'


class Test489(Test486):
    spectrum = 'rn(unit(1.0,flam),box(5500.0,1.0),1e-18,flam)'


class Test490(Test486):
    spectrum = 'spec($PYSYN_CDBS/calspec/gd71_mod_005.fits)'


class Test491(Test486):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)+(spec(el1215a.fits)+'
                'spec(el1302a.fits)+spec(el1356a.fits)+spec(el2471a.fits))')


class Test492(CommCase):
    obsmode = 'acs,hrc,f330w'
    spectrum = '$PYSYN_CDBS/calspec/g191b2b_mod_004.fits'


class Test493(Test492):
    spectrum = '$PYSYN_CDBS/calspec/gd153_mod_004.fits'


class Test494(Test492):
    spectrum = '$PYSYN_CDBS/calspec/gd71_mod_005.fits'


class Test495(Test492):
    spectrum = 'rn(unit(1.0,flam),box(5500.0,1.0),1.0e-17,flam)'


class Test496(Test492):
    spectrum = 'rn(unit(1.0,flam),box(5500.0,1.0),1e-18,flam)'


# Duplicate of Test494 and syntax already tested in Test490
# class Test497(Test492):
#    spectrum = 'spec($PYSYN_CDBS/calspec/gd71_mod_005.fits)'


class Test498(Test492):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)+(spec(el1215a.fits)+'
                'spec(el1302a.fits)+spec(el1356a.fits)+spec(el2471a.fits))')


class Test499(CommCase):
    obsmode = 'acs,hrc,f344n'
    spectrum = '$PYSYN_CDBS/calspec/g191b2b_mod_004.fits'


class Test500(Test499):
    spectrum = '$PYSYN_CDBS/calspec/gd153_mod_004.fits'


class Test501(Test499):
    spectrum = '$PYSYN_CDBS/calspec/gd71_mod_005.fits'


class Test502(Test499):
    spectrum = 'rn(unit(1.0,flam),box(5500.0,1.0),1e-18,flam)'


class Test503(Test499):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)+(spec(el1215a.fits)+'
                'spec(el1302a.fits)+spec(el1356a.fits)+spec(el2471a.fits))')


# Duplicate of Test507 and syntax already tested in Test499
# class Test504(CommCase):
#    obsmode = 'acs,hrc,f435w'
#    spectrum = '$PYSYN_CDBS/calspec/g191b2b_mod_004.fits'


class Test505(CommCase):
    obsmode = 'acs,hrc,f435w'
    spectrum = '$PYSYN_CDBS/calspec/gd153_mod_004.fits'


class Test506(Test505):
    spectrum = '$PYSYN_CDBS/calspec/gd71_mod_005.fits'


class Test507(Test505):
    spectrum = 'crcalspec$g191b2b_mod_004.fits'


class Test508(Test505):
    spectrum = 'rn(unit(1.0,flam),box(5500.0,1.0),1e-18,flam)'


class Test509(Test505):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)+(spec(el1215a.fits)+'
                'spec(el1302a.fits)+spec(el1356a.fits)+spec(el2471a.fits))')


class Test510(CommCase):
    obsmode = 'acs,hrc,f475w'
    spectrum = '$PYSYN_CDBS/calspec/g191b2b_mod_004.fits'


class Test511(Test510):
    spectrum = '$PYSYN_CDBS/calspec/gd153_mod_004.fits'


class Test512(Test510):
    spectrum = '$PYSYN_CDBS/calspec/gd71_mod_005.fits'


class Test513(Test510):
    spectrum = 'rn(unit(1.0,flam),box(5500.0,1.0),1e-18,flam)'


class Test514(Test510):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)+(spec(el1215a.fits)+'
                'spec(el1302a.fits)+spec(el1356a.fits)+spec(el2471a.fits))')


class Test515(CommCase):
    obsmode = 'acs,hrc,f502n'
    spectrum = '$PYSYN_CDBS/calspec/g191b2b_mod_004.fits'


class Test516(Test515):
    spectrum = '$PYSYN_CDBS/calspec/gd153_mod_004.fits'


class Test517(Test515):
    spectrum = '$PYSYN_CDBS/calspec/gd71_mod_005.fits'


class Test518(Test515):
    spectrum = 'rn(unit(1.0,flam),box(5500.0,1.0),1e-18,flam)'


class Test519(Test515):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)+(spec(el1215a.fits)+'
                'spec(el1302a.fits)+spec(el1356a.fits)+spec(el2471a.fits))')


class Test520(CommCase):
    obsmode = 'acs,hrc,f550m'
    spectrum = '$PYSYN_CDBS/calspec/g191b2b_mod_004.fits'


class Test521(Test520):
    spectrum = '$PYSYN_CDBS/calspec/gd153_mod_004.fits'


class Test522(Test520):
    spectrum = '$PYSYN_CDBS/calspec/gd71_mod_005.fits'


class Test523(Test520):
    spectrum = 'rn(unit(1.0,flam),box(5500.0,1.0),1e-18,flam)'


class Test524(Test520):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)+(spec(el1215a.fits)+'
                'spec(el1302a.fits)+spec(el1356a.fits)+spec(el2471a.fits))')


class Test525(CommCase):
    obsmode = 'acs,hrc,f555w'
    spectrum = '$PYSYN_CDBS/calspec/g191b2b_mod_004.fits'


class Test526(Test525):
    spectrum = '$PYSYN_CDBS/calspec/gd153_mod_004.fits'


class Test527(Test525):
    spectrum = '$PYSYN_CDBS/calspec/gd71_mod_005.fits'


class Test528(Test525):
    spectrum = 'rn(bb(10000),band(johnson,v),20,vegamag)'


class Test529(Test525):
    spectrum = 'rn(icat(k93models,5770,0.0,4.5),band(johnson,v),20,vegamag)'


class Test530(Test525):
    spectrum = 'rn(pl(4000.0,-1.0,flam),band(johnson,v),20,vegamag)'


class Test531(Test525):
    spectrum = 'rn(unit(1.0,flam),band(johnson,v),15,vegamag)'


class Test532(Test525):
    spectrum = 'rn(unit(1.0,flam),box(5500.0,1.0),1e-18,flam)'


class Test533(Test525):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)')


class Test534(Test525):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)+(spec(el1215a.fits)+'
                'spec(el1302a.fits)+spec(el1356a.fits)+spec(el2471a.fits))')


class Test535(CommCase):
    obsmode = 'acs,hrc,f555w,coron'
    spectrum = 'rn(unit(1.0,flam),band(johnson,v),0,vegamag)'


class Test536(Test535):
    spectrum = 'rn(unit(1.0,flam),band(johnson,v),10,vegamag)'


# UNTIL HERE - test2.py Test537

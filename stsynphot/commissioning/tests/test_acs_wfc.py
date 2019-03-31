"""This module contains ACS/WFC commissioning tests.
Adapted from ``astrolib/pysynphot/from_commissioning/acs/test5.py``,
``astrolib/pysynphot/from_commissioning/acs/test6.py``, and
``astrolib/pysynphot/from_commissioning/acs/test7.py``.

.. note::

    ``astrolib/pysynphot/from_commissioning/acs/test4.py`` was disabled.
    Therefore, Test658 to Test671 were not ported over.

    WFC1 and WFC2 have the same throughput curves.
    Therefore, testing for WFC1 alone is sufficient.

"""

# STDLIB
import os
import shutil

# THIRD-PARTY
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


class Test672(CommCase):
    obsmode = 'acs,wfc1,f502n'
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)+(spec(el1215a.fits)+'
                'spec(el1302a.fits)+spec(el1356a.fits)+spec(el2471a.fits))')


class Test673(CommCase):
    obsmode = 'acs,wfc1,f550m'
    spectrum = '$PYSYN_CDBS/calspec/g191b2b_mod_004.fits'


class Test674(Test673):
    spectrum = '$PYSYN_CDBS/calspec/gd153_mod_004.fits'


class Test675(Test673):
    spectrum = '$PYSYN_CDBS/calspec/gd71_mod_005.fits'


class Test676(Test673):
    spectrum = 'rn(unit(1.0,flam),box(5500.0,1.0),1e-18,flam)'


class Test677(Test673):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)+(spec(el1215a.fits)+'
                'spec(el1302a.fits)+spec(el1356a.fits)+spec(el2471a.fits))')


class Test678(CommCase):
    obsmode = 'acs,wfc1,f555w'
    spectrum = '$PYSYN_CDBS/calspec/g191b2b_mod_004.fits'


class Test679(Test678):
    spectrum = '$PYSYN_CDBS/calspec/gd153_mod_004.fits'


class Test680(Test678):
    spectrum = '$PYSYN_CDBS/calspec/gd71_mod_005.fits'


class Test681(Test678):
    spectrum = 'rn(bb(10000),band(johnson,v),20,vegamag)'


class Test682(Test678):
    spectrum = 'rn(icat(k93models,5770,0.0,4.5),band(johnson,v),20,vegamag)'


class Test683(Test678):
    spectrum = 'rn(pl(4000.0,-1.0,flam),band(johnson,v),20,vegamag)'


class Test684(Test678):
    spectrum = 'rn(unit(1.0,flam),band(johnson,v),15,vegamag)'


class Test685(Test678):
    spectrum = 'rn(unit(1.0,flam),band(johnson,v),22,vegamag)'


class Test686(Test678):
    spectrum = 'rn(unit(1.0,flam),box(5500.0,1.0),1e-18,flam)'


# Duplicate of Test680 and syntax already tested in Test490
# class Test687(Test678):
#    spectrum = 'spec($PYSYN_CDBS/calspec/gd71_mod_005.fits)'


class Test688(Test678):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)')


class Test689(Test678):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)+(spec(el1215a.fits)+'
                'spec(el1302a.fits)+spec(el1356a.fits)+spec(el2471a.fits))')


class Test690(CommCase):
    obsmode = 'acs,wfc1,f555w,pol_v'
    spectrum = 'rn(unit(1.0,flam),band(johnson,v),22,vegamag)'


class Test691(Test690):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)')


class Test692(CommCase):
    obsmode = 'acs,wfc1,f606w'
    spectrum = '$PYSYN_CDBS/calspec/g191b2b_mod_004.fits'


class Test693(Test692):
    spectrum = '$PYSYN_CDBS/calspec/gd153_mod_004.fits'


class Test694(Test692):
    spectrum = '$PYSYN_CDBS/calspec/gd71_mod_005.fits'


class Test695(Test692):
    spectrum = 'rn(unit(1.0,flam),box(5500.0,1.0),1e-18,flam)'


class Test696(Test692):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)+(spec(el1215a.fits)+'
                'spec(el1302a.fits)+spec(el1356a.fits)+spec(el2471a.fits))')


class Test697(CommCase):
    obsmode = 'acs,wfc1,f625w'
    spectrum = '$PYSYN_CDBS/calspec/g191b2b_mod_004.fits'


class Test698(Test697):
    spectrum = '$PYSYN_CDBS/calspec/gd153_mod_004.fits'


class Test699(Test697):
    spectrum = '$PYSYN_CDBS/calspec/gd71_mod_005.fits'


class Test700(Test697):
    spectrum = 'rn(unit(1.0,flam),box(5500.0,1.0),1e-18,flam)'


class Test701(Test697):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)')


class Test702(Test697):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)+(spec(el1215a.fits)+'
                'spec(el1302a.fits)+spec(el1356a.fits)+spec(el2471a.fits))')


class Test703(CommCase):
    obsmode = 'acs,wfc1,f658n'
    spectrum = '$PYSYN_CDBS/calspec/g191b2b_mod_004.fits'


class Test704(Test703):
    spectrum = '$PYSYN_CDBS/calspec/gd153_mod_004.fits'


class Test705(Test703):
    spectrum = '$PYSYN_CDBS/calspec/gd71_mod_005.fits'


class Test706(Test703):
    spectrum = 'rn(unit(1.0,flam),box(5500.0,1.0),1e-18,flam)'


class Test707(Test703):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)+(spec(el1215a.fits)+'
                'spec(el1302a.fits)+spec(el1356a.fits)+spec(el2471a.fits))')


class Test708(CommCase):
    obsmode = 'acs,wfc1,f660n'
    spectrum = '$PYSYN_CDBS/calspec/g191b2b_mod_004.fits'


class Test709(Test708):
    spectrum = '$PYSYN_CDBS/calspec/gd153_mod_004.fits'


class Test710(Test708):
    spectrum = '$PYSYN_CDBS/calspec/gd71_mod_005.fits'


class Test711(Test708):
    spectrum = 'rn(unit(1.0,flam),box(5500.0,1.0),1e-18,flam)'


class Test712(Test708):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)+(spec(el1215a.fits)+'
                'spec(el1302a.fits)+spec(el1356a.fits)+spec(el2471a.fits))')


class Test713(CommCase):
    obsmode = 'acs,wfc1,f775w'
    spectrum = '$PYSYN_CDBS/calspec/g191b2b_mod_004.fits'


class Test714(Test713):
    spectrum = '$PYSYN_CDBS/calspec/gd153_mod_004.fits'


class Test715(Test713):
    spectrum = '$PYSYN_CDBS/calspec/gd71_mod_005.fits'


class Test716(Test713):
    spectrum = 'rn(unit(1.0,flam),box(5500.0,1.0),1e-18,flam)'


class Test717(Test713):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)+(spec(el1215a.fits)+'
                'spec(el1302a.fits)+spec(el1356a.fits)+spec(el2471a.fits))')


class Test718(CommCase):
    obsmode = 'acs,wfc1,f814w'
    spectrum = '$PYSYN_CDBS/calspec/g191b2b_mod_004.fits'


class Test719(Test718):
    spectrum = '$PYSYN_CDBS/calspec/gd153_mod_004.fits'


class Test720(Test718):
    spectrum = '$PYSYN_CDBS/calspec/gd71_mod_005.fits'


class Test721(Test718):
    spectrum = 'rn(unit(1.0,flam),box(5500.0,1.0),1e-18,flam)'


class Test722(Test718):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)+(spec(el1215a.fits)+'
                'spec(el1302a.fits)+spec(el1356a.fits)+spec(el2471a.fits))')


class Test723(CommCase):
    obsmode = 'acs,wfc1,f850lp'
    spectrum = '$PYSYN_CDBS/calspec/g191b2b_mod_004.fits'


class Test724(Test723):
    spectrum = '$PYSYN_CDBS/calspec/gd153_mod_004.fits'


class Test725(Test723):
    spectrum = '$PYSYN_CDBS/calspec/gd71_mod_005.fits'


class Test726(Test723):
    spectrum = 'rn(unit(1.0,flam),box(5500.0,1.0),1e-18,flam)'


class Test727(Test723):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)')


class Test728(Test723):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)+(spec(el1215a.fits)+'
                'spec(el1302a.fits)+spec(el1356a.fits)+spec(el2471a.fits))')


class Test729(CommCase):
    obsmode = 'acs,wfc1,f892n'
    spectrum = '$PYSYN_CDBS/calspec/g191b2b_mod_004.fits'


class Test730(Test729):
    spectrum = '$PYSYN_CDBS/calspec/gd153_mod_004.fits'


class Test731(Test729):
    spectrum = '$PYSYN_CDBS/calspec/gd71_mod_005.fits'


class Test732(Test729):
    spectrum = 'rn(unit(1.0,flam),box(5500.0,1.0),1e-18,flam)'


class Test733(Test729):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)+(spec(el1215a.fits)+'
                'spec(el1302a.fits)+spec(el1356a.fits)+spec(el2471a.fits))')


class Test734(CommCase):
    obsmode = 'acs,wfc1,fr1016n#10000'
    spectrum = 'rn(unit(1.0,flam),box(5500.0,1.0),1.e-15,flam)'


class Test735(Test734):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)')


class Test736(CommCase):
    obsmode = 'acs,wfc1,fr388n#3880'
    spectrum = 'em(3880.0,10.0,1.0E-16,flam)'


class Test737(Test736):
    spectrum = 'rn(bb(10000),band(johnson,v),20,vegamag)'


class Test738(Test736):
    spectrum = 'rn(icat(k93models,15400,0.0,3.9),band(johnson,v),15,vegamag)'


class Test739(Test736):
    spectrum = 'rn(icat(k93models,3500,0.0,4.6),band(johnson,v),15,vegamag)'


class Test740(Test736):
    spectrum = 'rn(icat(k93models,44500,0.0,5.0),band(johnson,v),15,vegamag)'


class Test741(Test736):
    spectrum = 'rn(icat(k93models,4850,0.0,1.1),band(johnson,v),15,vegamag)'


class Test742(Test736):
    spectrum = 'rn(icat(k93models,5770,0.0,4.5),band(johnson,v),15,vegamag)'


class Test743(Test736):
    spectrum = 'rn(icat(k93models,5770,0.0,4.5),band(johnson,v),20,vegamag)'


class Test744(Test736):
    spectrum = 'rn(pl(4000.0,-1.0,flam),band(johnson,v),20,vegamag)'


class Test745(Test736):
    spectrum = 'rn(unit(1.0,flam),band(johnson,v),15,vegamag)'


class Test746(Test736):
    spectrum = 'rn(unit(1.0,flam),band(johnson,v),22,vegamag)'


# Duplicate of Test748 and syntax already tested in Test587
# class Test747(Test736):
#    spectrum = 'rn(unit(1.0,flam),box(5500.0,1.0),1.E-15,flam)'


class Test748(Test736):
    spectrum = 'rn(unit(1.0,flam),box(5500.0,1.0),1.e-15,flam)'


class Test749(Test736):
    spectrum = 'spec($PYSYN_CDBS/calspec/g191b2b_mod_004.fits)'


class Test750(Test736):
    spectrum = 'spec($PYSYN_CDBS/calspec/gd71_mod_005.fits)'


class Test751(Test736):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)')


class Test752(CommCase):
    obsmode = 'acs,wfc1,fr388n#3881'
    spectrum = 'rn(unit(1.0,flam),band(johnson,v),15,vegamag)'


class Test753(Test752):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)')


class Test754(CommCase):
    obsmode = 'acs,wfc1,fr423n#4230'
    spectrum = 'rn(unit(1.0,flam),box(5500.0,1.0),1.e-15,flam)'


class Test755(Test754):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)')


class Test756(CommCase):
    obsmode = 'acs,wfc1,fr459m#4590'
    spectrum = 'rn(unit(1.0,flam),band(johnson,v),22,vegamag)'


class Test757(Test756):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)')


class Test758(CommCase):
    obsmode = 'acs,wfc1,fr459m#4620'
    spectrum = 'rn(unit(1.0,flam),box(5500.0,1.0),1.e-15,flam)'


class Test759(Test758):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)')


class Test760(CommCase):
    obsmode = 'acs,wfc1,fr462n#4620'
    spectrum = 'rn(unit(1.0,flam),box(5500.0,1.0),1.e-15,flam)'


class Test761(Test760):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)')


class Test762(CommCase):
    obsmode = 'acs,wfc1,fr505n#5000'
    spectrum = 'rn(unit(1.0,flam),box(5500.0,1.0),1.e-15,flam)'


class Test763(Test762):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)')


class Test764(CommCase):
    obsmode = 'acs,wfc1,fr551n#5500'
    spectrum = 'rn(unit(1.0,flam),box(5500.0,1.0),1.e-15,flam)'


class Test765(Test764):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)')


class Test766(CommCase):
    obsmode = 'acs,wfc1,fr601n#6000'
    spectrum = 'rn(unit(1.0,flam),box(5500.0,1.0),1.e-15,flam)'


class Test767(Test766):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)')


class Test768(CommCase):
    obsmode = 'acs,wfc1,fr647m#6470'
    spectrum = 'rn(unit(1.0,flam),box(5500.0,1.0),1.e-15,flam)'


class Test769(Test768):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)')


class Test770(CommCase):
    obsmode = 'acs,wfc1,fr656n#6500'
    spectrum = 'rn(unit(1.0,flam),box(5500.0,1.0),1.e-15,flam)'


class Test771(Test770):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)')


class Test772(CommCase):
    obsmode = 'acs,wfc1,fr716n#7100'
    spectrum = 'rn(unit(1.0,flam),box(5500.0,1.0),1.e-15,flam)'


class Test773(Test772):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)')


class Test774(CommCase):
    obsmode = 'acs,wfc1,fr782n#7900'
    spectrum = 'rn(unit(1.0,flam),box(5500.0,1.0),1.e-15,flam)'


class Test775(Test774):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)')


class Test776(CommCase):
    obsmode = 'acs,wfc1,fr853n#8500'
    spectrum = 'rn(unit(1.0,flam),box(5500.0,1.0),1.e-15,flam)'


class Test777(Test776):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)')


class Test778(CommCase):
    obsmode = 'acs,wfc1,fr914m#9000'
    spectrum = 'rn(unit(1.0,flam),box(5500.0,1.0),1.e-15,flam)'


class Test779(Test778):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)')


class Test780(CommCase):
    obsmode = 'acs,wfc1,fr931n#9300'
    spectrum = 'rn(unit(1.0,flam),box(5500.0,1.0),1.e-15,flam)'


class Test781(Test780):
    obsmode = 'acs,wfc1,fr931n#9300'
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)')


class Test782(CommCase):
    obsmode = 'acs,wfc1,g800l'
    spectrum = 'em(6500.0,10.0,1.0E-16,flam)'


class Test783(Test782):
    spectrum = 'rn(bb(10000),band(johnson,v),20,vegamag)'


class Test784(Test782):
    spectrum = 'rn(icat(k93models,5770,0.0,4.5),band(johnson,v),20,vegamag)'


class Test785(Test782):
    spectrum = 'rn(pl(4000.0,-1.0,flam),band(johnson,v),20,vegamag)'


class Test786(Test782):
    spectrum = 'rn(unit(1.0,flam),band(johnson,v),15,vegamag)'


class Test787(Test782):
    spectrum = 'rn(unit(1.0,flam),box(5500.0,1.0),1.5e-16,flam)'


class Test788(Test782):
    spectrum = 'spec($PYSYN_CDBS/calspec/gd71_mod_005.fits)'


class Test789(Test782):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)')


class Test790(Test782):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)+(spec(el1215a.fits)+'
                'spec(el1302a.fits)+spec(el1356a.fits)+spec(el2471a.fits))')

"""This module contains ACS/HRC commissioning tests.
Adapted from ``astrolib/pysynphot/from_commissioning/acs/test1.py``,
``astrolib/pysynphot/from_commissioning/acs/test2.py``, and most of
``astrolib/pysynphot/from_commissioning/acs/test3.py``.
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


class Test472(CommCase):
    obsmode = 'acs,hrc,coron,fr388n#3880'
    spectrum = 'rn(unit(1.0,flam),band(johnson,v),15,vegamag)'


class Test473(Test472):
    spectrum = 'rn(unit(1.0,flam),band(johnson,v),5,vegamag)'


class Test474(Test472):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)')


class Test475(Test472):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),30.0,vegamag)')


class Test476(Test472):
    spectrum = 'spec(earthshine.fits)*0.5+spec(Zodi.fits)*1.0'


class Test477(Test472):
    spectrum = 'spec(earthshine.fits)*0.5+spec(Zodi.fits)*1.25'


class Test478(Test472):
    spectrum = 'spec(earthshine.fits)*0.5+spec(Zodi.fits)*2.0'


class Test479(Test472):
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


class Test537(Test535):
    spectrum = 'rn(unit(1.0,flam),band(johnson,v),15,vegamag)'


class Test538(Test535):
    spectrum = 'rn(unit(1.0,flam),band(johnson,v),5,vegamag)'


class Test539(Test535):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)')


class Test540(CommCase):
    obsmode = 'acs,hrc,f606w'
    spectrum = '$PYSYN_CDBS/calspec/g191b2b_mod_004.fits'


class Test541(Test540):
    spectrum = '$PYSYN_CDBS/calspec/gd153_mod_004.fits'


class Test542(Test540):
    spectrum = '$PYSYN_CDBS/calspec/gd71_mod_005.fits'


class Test543(Test540):
    spectrum = 'rn(unit(1.0,flam),box(5500.0,1.0),1e-18,flam)'


class Test544(Test540):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)+(spec(el1215a.fits)+'
                'spec(el1302a.fits)+spec(el1356a.fits)+spec(el2471a.fits))')


class Test545(CommCase):
    obsmode = 'acs,hrc,f625w'
    spectrum = '$PYSYN_CDBS/calspec/g191b2b_mod_004.fits'


class Test546(Test545):
    spectrum = '$PYSYN_CDBS/calspec/gd153_mod_004.fits'


class Test547(Test545):
    spectrum = '$PYSYN_CDBS/calspec/gd71_mod_005.fits'


class Test548(Test545):
    spectrum = 'rn(unit(1.0,flam),box(5500.0,1.0),1e-18,flam)'


class Test549(Test545):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)+(spec(el1215a.fits)+'
                'spec(el1302a.fits)+spec(el1356a.fits)+spec(el2471a.fits))')


class Test550(CommCase):
    obsmode = 'acs,hrc,f658n'
    spectrum = '$PYSYN_CDBS/calspec/g191b2b_mod_004.fits'


class Test551(Test550):
    spectrum = '$PYSYN_CDBS/calspec/gd153_mod_004.fits'


class Test552(Test550):
    spectrum = '$PYSYN_CDBS/calspec/gd71_mod_005.fits'


class Test553(Test550):
    spectrum = 'rn(unit(1.0,flam),box(5500.0,1.0),1e-18,flam)'


class Test554(Test550):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)+(spec(el1215a.fits)+'
                'spec(el1302a.fits)+spec(el1356a.fits)+spec(el2471a.fits))')


class Test555(CommCase):
    obsmode = 'acs,hrc,f660n'
    spectrum = '$PYSYN_CDBS/calspec/g191b2b_mod_004.fits'


class Test556(Test555):
    spectrum = '$PYSYN_CDBS/calspec/gd153_mod_004.fits'


class Test557(Test555):
    spectrum = '$PYSYN_CDBS/calspec/gd71_mod_005.fits'


class Test558(CommCase):
    obsmode = 'acs,hrc,f775w'
    spectrum = '$PYSYN_CDBS/calspec/g191b2b_mod_004.fits'


class Test559(Test558):
    spectrum = '$PYSYN_CDBS/calspec/gd153_mod_004.fits'


class Test560(Test558):
    spectrum = '$PYSYN_CDBS/calspec/gd71_mod_005.fits'


# Duplicate of Test558 and syntax already tested in Test507.
# class Test561(Test558):
#    spectrum = 'crcalspec$g191b2b_mod_004.fits'


class Test562(Test558):
    spectrum = 'rn(unit(1.0,flam),box(5500.0,1.0),1e-18,flam)'


class Test563(Test558):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)+(spec(el1215a.fits)+'
                'spec(el1302a.fits)+spec(el1356a.fits)+spec(el2471a.fits))')


class Test564(CommCase):
    obsmode = 'acs,hrc,f814w'
    spectrum = '$PYSYN_CDBS/calspec/g191b2b_mod_004.fits'


class Test565(Test564):
    spectrum = '$PYSYN_CDBS/calspec/gd153_mod_004.fits'


class Test566(Test564):
    spectrum = '$PYSYN_CDBS/calspec/gd71_mod_005.fits'


# Duplicate of Test564 and syntax already tested in Test507.
# class Test567(Test564):
#    spectrum = 'crcalspec$g191b2b_mod_004.fits'


class Test568(CommCase):
    obsmode = 'acs,hrc,f850lp'
    spectrum = '$PYSYN_CDBS/calspec/g191b2b_mod_004.fits'


class Test569(Test568):
    spectrum = '$PYSYN_CDBS/calspec/gd153_mod_004.fits'


class Test570(Test568):
    spectrum = '$PYSYN_CDBS/calspec/gd71_mod_005.fits'


class Test571(Test568):
    spectrum = 'rn(unit(1.0,flam),box(5500.0,1.0),1e-18,flam)'


class Test572(Test568):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)+(spec(el1215a.fits)+'
                'spec(el1302a.fits)+spec(el1356a.fits)+spec(el2471a.fits))')


class Test573(CommCase):
    obsmode = 'acs,hrc,f892n'
    spectrum = '$PYSYN_CDBS/calspec/g191b2b_mod_004.fits'


class Test574(Test573):
    spectrum = '$PYSYN_CDBS/calspec/gd153_mod_004.fits'


class Test575(Test573):
    spectrum = '$PYSYN_CDBS/calspec/gd71_mod_005.fits'


class Test576(Test573):
    spectrum = 'rn(unit(1.0,flam),box(5500.0,1.0),1e-18,flam)'


class Test577(Test573):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)+(spec(el1215a.fits)+'
                'spec(el1302a.fits)+spec(el1356a.fits)+spec(el2471a.fits))')


class Test578(CommCase):
    obsmode = 'acs,hrc,fr388n#3880'
    spectrum = 'rn(bb(10000),band(johnson,v),20,vegamag)'


class Test579(Test578):
    spectrum = 'rn(icat(k93models,15400,0.0,3.9),band(johnson,v),15,vegamag)'


class Test580(Test578):
    spectrum = 'rn(icat(k93models,3500,0.0,4.6),band(johnson,v),15,vegamag)'


class Test581(Test578):
    spectrum = 'rn(icat(k93models,44500,0.0,5.0),band(johnson,v),15,vegamag)'


class Test582(Test578):
    spectrum = 'rn(icat(k93models,4850,0.0,1.1),band(johnson,v),15,vegamag)'


class Test583(Test578):
    spectrum = 'rn(icat(k93models,5770,0.0,4.5),band(johnson,v),15,vegamag)'


class Test584(Test578):
    spectrum = 'rn(icat(k93models,5770,0.0,4.5),band(johnson,v),20,vegamag)'


class Test585(Test578):
    spectrum = 'rn(pl(4000.0,-1.0,flam),band(johnson,v),20,vegamag)'


class Test586(Test578):
    spectrum = 'rn(unit(1.0,flam),band(johnson,v),15,vegamag)'


class Test587(Test578):
    spectrum = 'rn(unit(1.0,flam),box(5500.0,1.0),1.E-15,flam)'


# Duplicate of Test587 and syntax already tested in Test571
# class Test588(Test578):
#    spectrum = 'rn(unit(1.0,flam),box(5500.0,1.0),1.e-15,flam)'


class Test589(Test578):
    spectrum = 'spec($PYSYN_CDBS/calspec/g191b2b_mod_004.fits)'


class Test590(Test578):
    spectrum = 'spec($PYSYN_CDBS/calspec/gd71_mod_005.fits)'


class Test591(Test578):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)')


class Test592(CommCase):
    obsmode = 'acs,hrc,fr459m#4590'
    spectrum = 'rn(unit(1.0,flam),band(johnson,v),22,vegamag)'


class Test593(Test592):
    spectrum = 'rn(unit(1.0,flam),box(5500.0,1.0),1.e-15,flam)'


class Test594(Test592):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)')


class Test595(CommCase):
    obsmode = 'acs,hrc,fr459m#4592'
    spectrum = 'rn(unit(1.0,flam),band(johnson,v),15,vegamag)'


class Test596(Test595):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)')


class Test597(CommCase):
    obsmode = 'acs,hrc,fr505n#5050'
    spectrum = 'rn(unit(1.0,flam),box(5500.0,1.0),1.e-15,flam)'


class Test598(Test597):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)')


class Test599(CommCase):
    obsmode = 'acs,hrc,fr656n#6560'
    spectrum = 'rn(unit(1.0,flam),box(5500.0,1.0),1.e-15,flam)'


class Test600(Test599):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)')


class Test601(CommCase):
    obsmode = 'acs,hrc,g800l'
    spectrum = 'em(6500.0,10.0,1.0E-16,flam)'


class Test602(Test601):
    spectrum = 'rn(bb(10000),band(johnson,v),20,vegamag)'


class Test603(Test601):
    spectrum = 'rn(icat(k93models,5770,0.0,4.5),band(johnson,v),20,vegamag)'


class Test604(Test601):
    spectrum = 'rn(pl(4000.0,-1.0,flam),band(johnson,v),20,vegamag)'


class Test605(Test601):
    spectrum = 'rn(unit(1.0,flam),band(johnson,v),15,vegamag)'


class Test606(Test601):
    spectrum = 'rn(unit(1.0,flam),box(5500.0,1.0),1.5e-16,flam)'


class Test607(Test601):
    spectrum = 'spec($PYSYN_CDBS/calspec/gd71_mod_005.fits)'


class Test608(Test601):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)')


class Test609(Test601):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)+(spec(el1215a.fits)+'
                'spec(el1302a.fits)+spec(el1356a.fits)+spec(el2471a.fits))')


class Test610(CommCase):
    obsmode = 'acs,hrc,pr200l'
    spectrum = 'em(4000.0,10.0,1.0E-16,flam)'


class Test611(Test610):
    spectrum = 'rn(bb(10000),band(johnson,v),20,vegamag)'


class Test612(Test610):
    spectrum = 'rn(icat(k93models,5770,0.0,4.5),band(johnson,v),20,vegamag)'


class Test613(Test610):
    spectrum = 'rn(pl(4000.0,-1.0,flam),band(johnson,v),20,vegamag)'


class Test614(Test610):
    spectrum = 'rn(unit(1.0,flam),band(johnson,v),15,vegamag)'


class Test615(Test610):
    spectrum = 'rn(unit(1.0,flam),box(5500.0,1.0),1.5e-16,flam)'


class Test616(Test610):
    spectrum = 'spec($PYSYN_CDBS/calspec/gd71_mod_005.fits)'


class Test617(Test610):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)')


class Test618(Test610):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)+(spec(el1215a.fits)+'
                'spec(el1302a.fits)+spec(el1356a.fits)+spec(el2471a.fits))')

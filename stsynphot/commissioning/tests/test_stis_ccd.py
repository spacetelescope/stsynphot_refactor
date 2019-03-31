"""This module contains STIS/CCD commissioning tests.
Adapted from ``astrolib/pysynphot/from_commissioning/stis/test*.py``.
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
             'el2471a.fits', 'qso_template.fits', 'Zodi.fits']


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


class Test1101(CommCase):
    obsmode = 'stis,ccd'
    spectrum = 'rn(unit(1,flam),band(johnson,v),15.0,vegamag)'


class Test1102(CommCase):
    obsmode = 'stis,ccd,50ccd'
    spectrum = 'rn(icat(k93models,44500,0.0,5.0),band(johnson,v),10,vegamag)'


class Test1103(Test1102):
    spectrum = 'rn(icat(k93models,44500,0.0,5.0),band(johnson,v),20,vegamag)'


class Test1104(Test1102):
    spectrum = 'rn(icat(k93models,5770,0.0,4.5),band(johnson,v),28,vegamag)'


class Test1105(Test1102):
    spectrum = ('rn(spec($PYSYN_CDBS/calspec/agk_81d266_stis_001.fits),'
                'band(johnson,v),10,vegamag)')
    force = 'extrap'


class Test1106(Test1102):
    spectrum = 'rn(unit(1.0,flam),band(johnson,v),15,vegamag)'


class Test1107(Test1102):
    spectrum = 'spec($PYSYN_CDBS/calspec/agk_81d266_stis_001.fits)'
    force = 'extrap'


class Test1108(Test1102):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)')


class Test1109(Test1102):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)+(spec(el1215a.fits)+'
                'spec(el1302a.fits)+spec(el1356a.fits)+spec(el2471a.fits))')


class Test1110(CommCase):
    obsmode = 'stis,ccd,f25nd5'
    spectrum = 'rn(icat(k93models,44500,0.0,5.0),band(johnson,v),4,vegamag)'


class Test1111(Test1110):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)+(spec(el1215a.fits)+'
                'spec(el1302a.fits)+spec(el1356a.fits)+spec(el2471a.fits))')


class Test1112(CommCase):
    obsmode = 'stis,ccd,f28x50lp'
    spectrum = 'rn(icat(k93models,5860,0.0,4.4),band(johnson,v),5,vegamag)'


class Test1113(Test1112):
    spectrum = 'spec($PYSYN_CDBS/calspec/agk_81d266_stis_001.fits)'
    force = 'extrap'


class Test1114(CommCase):
    obsmode = 'stis,ccd,f28x50lp'
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)')


class Test1115(Test1114):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)+(spec(el1215a.fits)+'
                'spec(el1302a.fits)+spec(el1356a.fits)+spec(el2471a.fits))')


class Test1116(CommCase):
    obsmode = 'stis,ccd,f28x50oii'
    spectrum = 'spec($PYSYN_CDBS/calspec/agk_81d266_stis_001.fits)'


class Test1117(Test1116):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)')


class Test1118(CommCase):
    obsmode = 'stis,ccd,f28x50oiii'
    spectrum = 'spec($PYSYN_CDBS/calspec/agk_81d266_stis_001.fits)'
    force = 'extrap'


class Test1119(CommCase):
    obsmode = 'stis,ccd,f28x50oiii'
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)')


class Test1120(CommCase):
    obsmode = 'stis,ccd,g230lb'
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)')


class Test1121(Test1120):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)+(spec(el1215a.fits)+'
                'spec(el1302a.fits)+spec(el1356a.fits)+spec(el2471a.fits))')


class Test1122(CommCase):
    obsmode = 'stis,ccd,g230lb,s52x2'
    spectrum = 'rn(icat(k93models,44500,0.0,5.0),band(johnson,v),22,vegamag)'


class Test1123(Test1122):
    spectrum = 'spec($PYSYN_CDBS/calspec/agk_81d266_stis_001.fits)'


class Test1124(CommCase):
    obsmode = 'stis,ccd,g230mb,c1995'
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)+(spec(el1215a.fits)+'
                'spec(el1302a.fits)+spec(el1356a.fits)+spec(el2471a.fits))')


class Test1125(CommCase):
    obsmode = 'stis,ccd,g230mb,c1995,s52x2'
    spectrum = 'spec($PYSYN_CDBS/calspec/agk_81d266_stis_001.fits)'


class Test1126(CommCase):
    obsmode = 'stis,ccd,g430l'
    spectrum = 'em(4300.0,1.0,1.0E-12,flam)'


class Test1127(Test1126):
    spectrum = 'rn(icat(k93models,5860,0.0,4.4),band(johnson,v),5,vegamag)'


class Test1128(Test1126):
    spectrum = ('rn(spec(Zodi.fits),band(johnson,v),23.3,vegamag)+'
                '(spec(el1215a.fits)*0.2+spec(el1302a.fits)*0.01333333333+'
                'spec(el1356a.fits)*0.012+spec(el2471a.fits)*0.01)')


class Test1129(Test1126):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)')


class Test1130(Test1126):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)+(spec(el1215a.fits)+'
                'spec(el1302a.fits)+spec(el1356a.fits)+spec(el2471a.fits))')


class Test1131(CommCase):
    obsmode = 'stis,ccd,g430l,s52x2'
    spectrum = 'rn(icat(k93models,44500,0.0,5.0),band(johnson,v),23.5,vegamag)'


class Test1132(Test1131):
    spectrum = ('rn(spec($PYSYN_CDBS/calspec/agk_81d266_stis_001.fits),'
                'band(johnson,v),10,vegamag)')


class Test1133(Test1131):
    spectrum = 'spec($PYSYN_CDBS/calspec/agk_81d266_stis_001.fits)'


class Test1134(CommCase):
    obsmode = 'stis,ccd,g430m,c4194'
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)')


class Test1135(Test1134):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)+(spec(el1215a.fits)+'
                'spec(el1302a.fits)+spec(el1356a.fits)+spec(el2471a.fits))')


class Test1136(CommCase):
    obsmode = 'stis,ccd,g430m,c4194,s52x2'
    spectrum = 'em(4300.0,1.0,1.0E-12,flam)'


class Test1137(Test1136):
    spectrum = 'spec($PYSYN_CDBS/calspec/agk_81d266_stis_001.fits)'


class Test1138(CommCase):
    obsmode = 'stis,ccd,g750l,c7751'
    spectrum = ('rn(spec(Zodi.fits),band(johnson,v),22.7,vegamag)+'
                '(spec(el1215a.fits)*0.2+spec(el1302a.fits)*0.01333333333+'
                'spec(el1356a.fits)*0.012+spec(el2471a.fits)*0.01)')


class Test1139(Test1138):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.1,vegamag)+(spec(el1215a.fits)+'
                'spec(el1302a.fits)+spec(el1356a.fits)+spec(el2471a.fits))')


class Test1140(Test1138):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)')


class Test1141(Test1138):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)+(spec(el1215a.fits)+'
                'spec(el1302a.fits)+spec(el1356a.fits)+spec(el2471a.fits))')


class Test1142(Test1138):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),23.3,vegamag)+(spec(el1215a.fits)+'
                'spec(el1302a.fits)+spec(el1356a.fits)+spec(el2471a.fits))')


class Test1143(Test1138):
    spectrum = ('spec(earthshine.fits)+rn(spec(Zodi.fits),band(johnson,v),'
                '22.7,vegamag)+(spec(el1215a.fits)+spec(el1302a.fits)+'
                'spec(el1356a.fits)+spec(el2471a.fits))*2.0')


class Test1144(CommCase):
    obsmode = 'stis,ccd,g750l,c7751,s52x02'
    spectrum = 'rn(z(spec(qso_template.fits),0.03),band(johnson,v),18,vegamag)'
    force = 'extrap'


class Test1145(CommCase):
    obsmode = 'stis,ccd,g750l,c7751,s52x02'
    spectrum = 'rn(z(spec(qso_template.fits),1.0),band(johnson,v),18,vegamag)'


class Test1146(Test1145):
    spectrum = 'rn(z(spec(qso_template.fits),3.0),band(johnson,v),18,vegamag)'


class Test1147(CommCase):
    obsmode = 'stis,ccd,g750l,c7751,s52x2'
    spectrum = 'rn(icat(k93models,44500,0.0,5.0),band(johnson,v),23,vegamag)'


class Test1148(Test1147):
    spectrum = 'rn(icat(k93models,44500,0.0,5.0),band(johnson,v),24.5,vegamag)'


class Test1149(Test1147):
    spectrum = 'spec($PYSYN_CDBS/calspec/agk_81d266_stis_001.fits)'
    force = 'extrap'


class Test1150(CommCase):
    obsmode = 'stis,ccd,g750m,c7283'
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)+(spec(el1215a.fits)+'
                'spec(el1302a.fits)+spec(el1356a.fits)+spec(el2471a.fits))')


class Test1151(CommCase):
    obsmode = 'stis,ccd,g750m,c7283,s52x2'
    spectrum = 'spec($PYSYN_CDBS/calspec/agk_81d266_stis_001.fits)'


class Test1152(CommCase):
    obsmode = 'stis,ccd,s03x005nd'
    spectrum = 'rn(icat(k93models,44500,0.0,5.0),band(johnson,v),4,vegamag)'


class Test1153(Test1152):
    spectrum = 'rn(unit(1.0,flam),band(johnson,v),15,vegamag)'


class Test1154(Test1152):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)')


class Test1155(Test1152):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)+(spec(el1215a.fits)+'
                'spec(el1302a.fits)+spec(el1356a.fits)+spec(el2471a.fits))')


class Test1205(CommCase):
    obsmode = 'stis,g230lb,ccd,s52x2'
    spectrum = '$PYSYN_CDBS/calspec/g191b2b_mod_004.fits'


class Test1206(Test1205):
    spectrum = '$PYSYN_CDBS/calspec/gd153_mod_004.fits'


class Test1207(Test1205):
    spectrum = '$PYSYN_CDBS/calspec/gd71_mod_005.fits'


class Test1208(CommCase):
    obsmode = 'stis,g430l,ccd,s52x2'
    spectrum = '$PYSYN_CDBS/calspec/g191b2b_mod_004.fits'


class Test1209(Test1208):
    spectrum = '$PYSYN_CDBS/calspec/gd153_mod_004.fits'


class Test1210(Test1208):
    spectrum = '$PYSYN_CDBS/calspec/gd71_mod_005.fits'


class Test1211(CommCase):
    obsmode = 'stis,g750l,ccd,s52x2'
    spectrum = '$PYSYN_CDBS/calspec/g191b2b_mod_004.fits'


class Test1212(Test1211):
    spectrum = '$PYSYN_CDBS/calspec/gd153_mod_004.fits'


class Test1213(Test1211):
    spectrum = '$PYSYN_CDBS/calspec/gd71_mod_005.fits'

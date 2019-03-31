"""This module contains STIS/FUVMAMA commissioning tests.
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
             'el2471a.fits', 'ngc1068_template.fits', 'Zodi.fits']


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


class Test1156(CommCase):
    obsmode = 'stis,fuvmama,25mama'
    spectrum = 'rn(icat(k93models,44500,0.0,5.0),band(johnson,v),18.5,vegamag)'


class Test1157(Test1156):
    spectrum = 'rn(icat(k93models,44500,0.0,5.0),band(johnson,v),20,vegamag)'


class Test1158(Test1156):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)+(spec(el1215a.fits)+'
                'spec(el1302a.fits)+spec(el1356a.fits)+spec(el2471a.fits))')


class Test1159(CommCase):
    obsmode = 'stis,fuvmama,e140h,c1416'
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)+(spec(el1215a.fits)+'
                'spec(el1302a.fits)+spec(el1356a.fits)+spec(el2471a.fits))')


class Test1160(CommCase):
    obsmode = 'stis,fuvmama,e140h,c1416,s02x02'
    spectrum = 'spec($PYSYN_CDBS/calspec/bd_28d4211_stis_001.fits)'


class Test1161(CommCase):
    obsmode = 'stis,fuvmama,e140m,c1425'
    spectrum = ('rn(spec(Zodi.fits),band(johnson,v),23.3,vegamag)+'
                '(spec(el1215a.fits)*0.2+spec(el1302a.fits)*0.01333333333+'
                'spec(el1356a.fits)*0.012+spec(el2471a.fits)*0.01)')


class Test1162(Test1161):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)+(spec(el1215a.fits)+'
                'spec(el1302a.fits)+spec(el1356a.fits)+spec(el2471a.fits))')


class Test1163(Test1161):
    spectrum = ('spec(earthshine.fits)+rn(spec(Zodi.fits),band(johnson,v),'
                '23.3,vegamag)+(spec(el1215a.fits)+spec(el1302a.fits)+'
                'spec(el1356a.fits)+spec(el2471a.fits))*2.0')


class Test1164(CommCase):
    obsmode = 'stis,fuvmama,e140m,c1425,s02x006'
    spectrum = 'em(1425.0,0.043487548828125,1.0E-10,flam)'


class Test1165(Test1164):
    spectrum = 'em(1425.0,1.0,1.0E-10,flam)'


class Test1166(CommCase):
    obsmode = 'stis,fuvmama,e140m,c1425,s02x02'
    spectrum = 'rn(icat(k93models,11900,0.0,4.0),band(johnson,v),10,vegamag)'


class Test1167(Test1166):
    spectrum = 'rn(icat(k93models,11900,0.0,4.0),band(johnson,v),6,vegamag)'


class Test1168(Test1166):
    spectrum = 'rn(icat(k93models,11900,0.0,4.0),band(johnson,v),7,vegamag)'


class Test1169(Test1166):
    spectrum = 'rn(icat(k93models,44500,0.0,5.0),band(johnson,v),22,vegamag)'


class Test1170(Test1166):
    spectrum = 'spec($PYSYN_CDBS/calspec/bd_28d4211_stis_001.fits)'


class Test1171(CommCase):
    obsmode = 'stis,fuvmama,f25lya'
    spectrum = 'rn(icat(k93models,44500,0.0,5.0),band(johnson,v),18,vegamag)'


class Test1172(Test1171):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)+(spec(el1215a.fits)+'
                'spec(el1302a.fits)+spec(el1356a.fits)+spec(el2471a.fits))')


class Test1173(CommCase):
    obsmode = 'stis,fuvmama,f25nd3'
    spectrum = 'rn(icat(k93models,44500,0.0,5.0),band(johnson,v),18,vegamag)'


class Test1174(Test1173):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)+(spec(el1215a.fits)+'
                'spec(el1302a.fits)+spec(el1356a.fits)+spec(el2471a.fits))')


class Test1175(CommCase):
    obsmode = 'stis,fuvmama,f25ndq1'
    spectrum = 'rn(icat(k93models,44500,0.0,5.0),band(johnson,v),18,vegamag)'


class Test1176(Test1175):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)+(spec(el1215a.fits)+'
                'spec(el1302a.fits)+spec(el1356a.fits)+spec(el2471a.fits))')


class Test1177(CommCase):
    obsmode = 'stis,fuvmama,f25ndq3'
    spectrum = 'rn(icat(k93models,44500,0.0,5.0),band(johnson,v),18,vegamag)'


class Test1178(Test1177):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)+(spec(el1215a.fits)+'
                'spec(el1302a.fits)+spec(el1356a.fits)+spec(el2471a.fits))')


class Test1179(CommCase):
    obsmode = 'stis,fuvmama,f25qtz'
    spectrum = 'rn(icat(k93models,30000,0.0,4.0),band(johnson,v),26,vegamag)'


class Test1180(Test1179):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)+(spec(el1215a.fits)+'
                'spec(el1302a.fits)+spec(el1356a.fits)+spec(el2471a.fits))')


class Test1181(CommCase):
    obsmode = 'stis,fuvmama,f25srf2'
    spectrum = 'rn(icat(k93models,30000,0.0,4.0),band(johnson,v),26,vegamag)'


class Test1182(Test1181):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)+(spec(el1215a.fits)+'
                'spec(el1302a.fits)+spec(el1356a.fits)+spec(el2471a.fits))')


class Test1183(CommCase):
    obsmode = 'stis,fuvmama,g140l'
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)')


class Test1184(Test1183):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)+(spec(el1215a.fits)+'
                'spec(el1302a.fits)+spec(el1356a.fits)+spec(el2471a.fits))')


class Test1185(CommCase):
    obsmode = 'stis,fuvmama,g140l,s52x01'
    spectrum = 'rn(spec(ngc1068_template.fits),band(johnson,v),9,vegamag)'


class Test1186(CommCase):
    obsmode = 'stis,fuvmama,g140l,s52x2'
    spectrum = 'rn(icat(k93models,44500,0.0,5.0),band(johnson,v),13,vegamag)'


class Test1187(Test1186):
    spectrum = 'rn(icat(k93models,44500,0.0,5.0),band(johnson,v),14,vegamag)'


class Test1188(Test1186):
    spectrum = 'rn(icat(k93models,44500,0.0,5.0),band(johnson,v),14.1,vegamag)'


class Test1189(Test1186):
    spectrum = 'rn(icat(k93models,44500,0.0,5.0),band(johnson,v),27.5,vegamag)'


class Test1190(Test1186):
    spectrum = ('rn(spec($PYSYN_CDBS/calspec/agk_81d266_stis_001.fits),'
                'band(johnson,v),12.77,vegamag)')


class Test1191(Test1186):
    spectrum = ('rn(spec($PYSYN_CDBS/calspec/grw_70d5824_stis_001.fits),'
                'band(johnson,v),10.516,vegamag)')


class Test1192(Test1186):
    spectrum = 'spec($PYSYN_CDBS/calspec/grw_70d5824_stis_001.fits)'


class Test1193(CommCase):
    obsmode = 'stis,fuvmama,g140m,c1567'
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)+(spec(el1215a.fits)+'
                'spec(el1302a.fits)+spec(el1356a.fits)+spec(el2471a.fits))')


class Test1194(CommCase):
    obsmode = 'stis,fuvmama,g140m,c1567,s52x2'
    spectrum = 'spec($PYSYN_CDBS/calspec/agk_81d266_stis_001.fits)'


class Test1195(CommCase):
    obsmode = 'stis,g140l,fuvmama,s52x2'
    spectrum = '$PYSYN_CDBS/calspec/g191b2b_mod_004.fits'


class Test1196(Test1195):
    spectrum = '$PYSYN_CDBS/calspec/gd153_mod_004.fits'


class Test1197(Test1195):
    spectrum = '$PYSYN_CDBS/calspec/gd71_mod_005.fits'


class Test1198(Test1195):
    spectrum = 'el1215a.fits'
    force = 'extrap'


class Test1199(Test1195):
    spectrum = 'el1302a.fits'
    force = 'extrap'


class Test1200(Test1195):
    spectrum = 'el1356a.fits'
    force = 'extrap'


# Both ASTROLIB PYSYNPHOT and ``synphot`` report this that this combo
# gives DisjointError, so skipping this one.
# class Test1201(Test1195):
#    spectrum = 'el2471a.fits'

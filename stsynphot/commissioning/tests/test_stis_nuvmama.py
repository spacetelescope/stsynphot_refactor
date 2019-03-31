"""This module contains STIS/NUVMAMA commissioning tests.
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
             'el2471a.fits', 'HS20270651.dat', 'Zodi.fits']


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


class Test1202(CommCase):
    obsmode = 'stis,g230l,nuvmama,s52x2'
    spectrum = '$PYSYN_CDBS/calspec/g191b2b_mod_004.fits'


class Test1203(Test1202):
    spectrum = '$PYSYN_CDBS/calspec/gd153_mod_004.fits'


class Test1204(Test1202):
    spectrum = '$PYSYN_CDBS/calspec/gd71_mod_005.fits'


class Test1214(CommCase):
    obsmode = 'stis,nuvmama,25mama'
    spectrum = 'rn(icat(k93models,30000,0.0,4.0),band(johnson,v),26,vegamag)'


class Test1215(Test1214):
    spectrum = 'rn(icat(k93models,5860,0.0,4.4),band(johnson,v),5,vegamag)'


class Test1216(Test1214):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)+(spec(el1215a.fits)+'
                'spec(el1302a.fits)+spec(el1356a.fits)+spec(el2471a.fits))')


class Test1217(CommCase):
    obsmode = 'stis,nuvmama,e230h,c2263'
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)+(spec(el1215a.fits)+'
                'spec(el1302a.fits)+spec(el1356a.fits)+spec(el2471a.fits))')


class Test1218(CommCase):
    obsmode = 'stis,nuvmama,e230h,c2263,s02x02'
    spectrum = 'rn(bb(50000),band(johnson,v),10.516,vegamag)'


class Test1219(Test1218):
    spectrum = ('rn(icat(k93models,44500,0.0,5.0),band(johnson,v),10.516,'
                'vegamag)')


class Test1220(Test1218):
    spectrum = 'rn(pl(4000.0,-1.0,flam),band(johnson,v),10.516,vegamag)'


class Test1221(Test1218):
    spectrum = 'rn(pl(4000.0,0.0,flam),band(johnson,v),10.516,vegamag)'


class Test1222(Test1218):
    spectrum = ('rn(spec($PYSYN_CDBS/calspec/bd_28d4211_stis_001.fits),'
                'band(johnson,v),10.516,vegamag)')


class Test1223(Test1218):
    spectrum = ('rn(spec($PYSYN_CDBS/calspec/bd_28d4211_stis_001.fits),'
                'box(2000.0,1.0),1.0e-12,flam)')


class Test1224(Test1218):
    spectrum = 'rn(unit(1.0,flam),band(johnson,v),10.516,vegamag)'


class Test1225(Test1218):
    spectrum = 'spec($PYSYN_CDBS/calspec/bd_28d4211_stis_001.fits)'


class Test1226(CommCase):
    obsmode = 'stis,nuvmama,e230m,c1978'
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)+(spec(el1215a.fits)+'
                'spec(el1302a.fits)+spec(el1356a.fits)+spec(el2471a.fits))')


class Test1227(CommCase):
    obsmode = 'stis,nuvmama,e230m,c1978,s02x02'
    spectrum = 'rn(icat(k93models,44500,0.0,5.0),band(johnson,v),18.5,vegamag)'


class Test1228(Test1227):
    spectrum = 'spec($PYSYN_CDBS/calspec/bd_28d4211_stis_001.fits)'


class Test1229(CommCase):
    obsmode = 'stis,nuvmama,f25ciii'
    spectrum = 'rn(icat(k93models,44500,0.0,5.0),band(johnson,v),18,vegamag)'


class Test1230(Test1229):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)+(spec(el1215a.fits)+'
                'spec(el1302a.fits)+spec(el1356a.fits)+spec(el2471a.fits))')


class Test1231(CommCase):
    obsmode = 'stis,nuvmama,f25cn182'
    spectrum = 'rn(icat(k93models,44500,0.0,5.0),band(johnson,v),18,vegamag)'


class Test1232(Test1231):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)+(spec(el1215a.fits)+'
                'spec(el1302a.fits)+spec(el1356a.fits)+spec(el2471a.fits))')


class Test1233(CommCase):
    obsmode = 'stis,nuvmama,f25cn270'
    spectrum = 'rn(icat(k93models,44500,0.0,5.0),band(johnson,v),18,vegamag)'


class Test1234(Test1233):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)+(spec(el1215a.fits)+'
                'spec(el1302a.fits)+spec(el1356a.fits)+spec(el2471a.fits))')


class Test1235(CommCase):
    obsmode = 'stis,nuvmama,f25mgii'
    spectrum = 'rn(icat(k93models,44500,0.0,5.0),band(johnson,v),18,vegamag)'


class Test1236(Test1235):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)+(spec(el1215a.fits)+'
                'spec(el1302a.fits)+spec(el1356a.fits)+spec(el2471a.fits))')


class Test1237(CommCase):
    obsmode = 'stis,nuvmama,f25nd5'
    spectrum = 'rn(icat(k93models,44500,0.0,5.0),band(johnson,v),18,vegamag)'


class Test1238(Test1237):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)+(spec(el1215a.fits)+'
                'spec(el1302a.fits)+spec(el1356a.fits)+spec(el2471a.fits))')


class Test1239(CommCase):
    obsmode = 'stis,nuvmama,f25ndq2'
    spectrum = 'rn(icat(k93models,44500,0.0,5.0),band(johnson,v),18,vegamag)'


class Test1240(Test1239):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)+(spec(el1215a.fits)+'
                'spec(el1302a.fits)+spec(el1356a.fits)+spec(el2471a.fits))')


class Test1241(CommCase):
    obsmode = 'stis,nuvmama,f25ndq4'
    spectrum = 'rn(icat(k93models,44500,0.0,5.0),band(johnson,v),18,vegamag)'


class Test1242(Test1241):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)+(spec(el1215a.fits)+'
                'spec(el1302a.fits)+spec(el1356a.fits)+spec(el2471a.fits))')


class Test1243(CommCase):
    obsmode = 'stis,nuvmama,f25qtz'
    spectrum = 'rn(icat(k93models,44500,0.0,5.0),band(johnson,v),18,vegamag)'


class Test1244(Test1243):
    spectrum = 'rn(icat(k93models,44500,0.0,5.0),band(johnson,v),20,vegamag)'


class Test1245(Test1243):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)+(spec(el1215a.fits)+'
                'spec(el1302a.fits)+spec(el1356a.fits)+spec(el2471a.fits))')


class Test1246(CommCase):
    obsmode = 'stis,nuvmama,f25srf2'
    spectrum = 'rn(icat(k93models,30000,0.0,4.0),band(johnson,v),26,vegamag)'


class Test1247(Test1246):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)+(spec(el1215a.fits)+'
                'spec(el1302a.fits)+spec(el1356a.fits)+spec(el2471a.fits))')


class Test1248(CommCase):
    obsmode = 'stis,nuvmama,g230l'
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)')


class Test1249(Test1248):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)+(spec(el1215a.fits)+'
                'spec(el1302a.fits)+spec(el1356a.fits)+spec(el2471a.fits))')


class Test1250(CommCase):
    # Original test used gal1 but it is no longer supported, so we use gal3
    obsmode = 'stis,nuvmama,g230l,s52x2'
    spectrum = ('rn(icat(k93models,44500,0.0,5.0)*ebmvx(0.5,gal3),'
                'band(johnson,v),15,vegamag)')


class Test1251(Test1250):
    # Original test used lmc but it is no longer supported, so we use lmcavg
    spectrum = ('rn(icat(k93models,44500,0.0,5.0)*ebmvx(0.5,lmcavg),'
                'band(johnson,v),15,vegamag)')


class Test1252(Test1250):
    # Original test used smc but it is no longer supported, so we use smcbar
    spectrum = ('rn(icat(k93models,44500,0.0,5.0)*ebmvx(0.5,smcbar),'
                'band(johnson,v),15,vegamag)')


class Test1253(Test1250):
    # Original test used xgal but it is no longer supported, so we use xgalsb
    spectrum = ('rn(icat(k93models,44500,0.0,5.0)*ebmvx(0.5,xgalsb),'
                'band(johnson,v),15,vegamag)')


class Test1254(Test1250):
    spectrum = 'rn(icat(k93models,44500,0.0,5.0),band(johnson,v),24,vegamag)'


class Test1255(Test1250):
    spectrum = 'spec($PYSYN_CDBS/calspec/grw_70d5824_stis_001.fits)'


class Test1256(CommCase):
    obsmode = 'stis,nuvmama,g230m,c2818'
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)')


class Test1257(CommCase):
    obsmode = 'stis,nuvmama,g230m,c2818,s52x2'
    spectrum = 'spec($PYSYN_CDBS/calspec/agk_81d266_stis_001.fits)'


class Test1258(CommCase):
    obsmode = 'stis,nuvmama,prism'
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)+(spec(el1215a.fits)+'
                'spec(el1302a.fits)+spec(el1356a.fits)+spec(el2471a.fits))')


class Test1259(CommCase):
    obsmode = 'stis,nuvmama,prism,s52x01'
    spectrum = 'spec(HS20270651.dat)'
    force = 'extrap'


class Test1260(Test1259):
    obsmode = 'stis,nuvmama,prism,s52x2'

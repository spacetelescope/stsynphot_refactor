"""This module contains WFC3/IR commissioning tests.
Adapted from ``astrolib/pysynphot/from_commissioning/wfc3_ir/test*.py``.
"""

# STDLIB
import os
import shutil

# THIRD-PARTY
from astropy.utils.data import get_pkg_data_filename

# LOCAL
from ..utils import ThermCase

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


class Test1361(ThermCase):
    # Original test used gal1 but it is no longer supported, so we use gal3
    obsmode = 'wfc3,ir,f160w'  # IRAF thermback=0.1359
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_100.fits)'
                ',band(cousins,i),28.0,vegamag)*ebmvx(0.04,gal3)')


class Test1362(Test1361):
    # Original test used smc but it is no longer supported, so we use smcbar
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_100.fits)'
                ',band(cousins,i),28.0,vegamag)*ebmvx(0.16,smcbar)')


class Test1363(Test1361):
    # Original test used lmc but it is no longer supported, so we use lmcavg
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_100.fits)'
                ',band(cousins,i),28.0,vegamag)*ebmvx(0.2,lmcavg)')


class Test1364(Test1361):
    # Original test used xgal but it is no longer supported, so we use xgalsb
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_100.fits)'
                ',band(cousins,i),28.0,vegamag)*ebmvx(0.24,xgalsb)')


class Test1365(Test1361):
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_11.fits),'
                'band(cousins,i),28.0,vegamag)*ebmvx(0.12,gal3)')


class Test1366(Test1361):
    # Original test used lmc but it is no longer supported, so we use lmcavg
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_11.fits),'
                'band(cousins,i),28.0,vegamag)*ebmvx(0.2,lmcavg)')


class Test1367(Test1361):
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_114.fits)'
                ',band(cousins,i),28.0,vegamag)*ebmvx(0.12,gal3)')


class Test1368(Test1361):
    # Original test used smc but it is no longer supported, so we use smcbar
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_117.fits)'
                ',band(cousins,i),28.0,vegamag)*ebmvx(0.16,smcbar)')


class Test1369(Test1361):
    # Original test used lmc but it is no longer supported, so we use lmcavg
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_118.fits)'
                ',band(cousins,i),28.0,vegamag)*ebmvx(0.2,lmcavg)')


class Test1370(Test1361):
    # Original test used smc but it is no longer supported, so we use smcbar
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_12.fits),'
                'band(cousins,i),28.0,vegamag)*ebmvx(0.16,smcbar)')


class Test1371(Test1361):
    # Original test used xgal but it is no longer supported, so we use xgalsb
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_12.fits),'
                'band(cousins,i),28.0,vegamag)*ebmvx(0.24,xgalsb)')


class Test1372(Test1361):
    # Original test used lmc but it is no longer supported, so we use lmcavg
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_13.fits),'
                'band(cousins,i),28.0,vegamag)*ebmvx(0.2,lmcavg)')


class Test1373(Test1361):
    # Original test used gal1 but it is no longer supported, so we use gal3
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_14.fits),'
                'band(cousins,i),28.0,vegamag)*ebmvx(0.08,gal3)')


class Test1374(Test1361):
    # Original test used xgal but it is no longer supported, so we use xgalsb
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_14.fits),'
                'band(cousins,i),28.0,vegamag)*ebmvx(0.24,xgalsb)')


class Test1375(Test1361):
    # Original test used gal1 but it is no longer supported, so we use gal3
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_15.fits),'
                'band(cousins,i),28.0,vegamag)*ebmvx(0.04,gal3)')


class Test1376(Test1361):
    # Original test used gal1 but it is no longer supported, so we use gal3
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_16.fits),'
                'band(cousins,i),28.0,vegamag)*ebmvx(0.08,gal3)')


class Test1377(Test1361):
    # Original test used smc but it is no longer supported, so we use smcbar
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_16.fits),'
                'band(cousins,i),28.0,vegamag)*ebmvx(0.16,smcbar)')


class Test1378(Test1361):
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_17.fits),'
                'band(cousins,i),28.0,vegamag)*ebmvx(0.12,gal3)')


class Test1379(Test1361):
    # Original test used lmc but it is no longer supported, so we use lmcavg
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_17.fits),'
                'band(cousins,i),28.0,vegamag)*ebmvx(0.2,lmcavg)')


class Test1380(Test1361):
    # Original test used smc but it is no longer supported, so we use smcbar
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_18.fits),'
                'band(cousins,i),28.0,vegamag)*ebmvx(0.16,smcbar)')


class Test1381(Test1361):
    # Original test used xgal but it is no longer supported, so we use xgalsb
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_18.fits),'
                'band(cousins,i),28.0,vegamag)*ebmvx(0.24,xgalsb)')


class Test1382(Test1361):
    # Original test used gal1 but it is no longer supported, so we use gal3
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_19.fits),'
                'band(cousins,i),28.0,vegamag)*ebmvx(0.04,gal3)')


class Test1383(Test1361):
    # Original test used lmc but it is no longer supported, so we use lmcavg
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_19.fits),'
                'band(cousins,i),28.0,vegamag)*ebmvx(0.2,lmcavg)')


class Test1384(Test1361):
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_2.fits),'
                'band(cousins,i),28.0,vegamag)*ebmvx(0.12,gal3)')


class Test1385(Test1361):
    # Original test used smc but it is no longer supported, so we use smcbar
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_2.fits),'
                'band(cousins,i),28.0,vegamag)*ebmvx(0.16,smcbar)')


class Test1386(Test1361):
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_20.fits),'
                'band(cousins,i),28.0,vegamag)*ebmvx(0.12,gal3)')


class Test1387(Test1361):
    # Original test used xgal but it is no longer supported, so we use xgalsb
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_20.fits),'
                'band(cousins,i),28.0,vegamag)*ebmvx(0.24,xgalsb)')


class Test1388(Test1361):
    # Original test used gal1 but it is no longer supported, so we use gal3
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_22.fits),'
                'band(cousins,i),28.0,vegamag)*ebmvx(0.08,gal3)')


class Test1389(Test1361):
    # Original test used xgal but it is no longer supported, so we use xgalsb
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_23.fits),'
                'band(cousins,i),28.0,vegamag)*ebmvx(0.24,xgalsb)')


class Test1390(Test1361):
    # Original test used smc but it is no longer supported, so we use smcbar
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_24.fits),'
                'band(cousins,i),28.0,vegamag)*ebmvx(0.16,smcbar)')


class Test1391(Test1361):
    # Original test used lmc but it is no longer supported, so we use lmcavg
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_25.fits),'
                'band(cousins,i),28.0,vegamag)*ebmvx(0.2,lmcavg)')


class Test1392(Test1361):
    # Original test used xgal but it is no longer supported, so we use xgalsb
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_26.fits),'
                'band(cousins,i),28.0,vegamag)*ebmvx(0.24,xgalsb)')


class Test1393(Test1361):
    # Original test used gal1 but it is no longer supported, so we use gal3
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_27.fits),'
                'band(cousins,i),28.0,vegamag)*ebmvx(0.04,gal3)')


class Test1394(Test1361):
    # Original test used gal1 but it is no longer supported, so we use gal3
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_29.fits),'
                'band(cousins,i),28.0,vegamag)*ebmvx(0.08,gal3)')


class Test1395(Test1361):
    # Original test used lmc but it is no longer supported, so we use lmcavg
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_3.fits),'
                'band(cousins,i),28.0,vegamag)*ebmvx(0.2,lmcavg)')


class Test1396(Test1361):
    # Original test used gal1 but it is no longer supported, so we use gal3
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_31.fits),'
                'band(cousins,i),28.0,vegamag)*ebmvx(0.04,gal3)')


class Test1397(Test1361):
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_33.fits),'
                'band(cousins,i),28.0,vegamag)*ebmvx(0.12,gal3)')


class Test1398(Test1361):
    # Original test used smc but it is no longer supported, so we use smcbar
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_34.fits),'
                'band(cousins,i),28.0,vegamag)*ebmvx(0.16,smcbar)')


class Test1399(Test1361):
    # Original test used xgal but it is no longer supported, so we use xgalsb
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_36.fits),'
                'band(cousins,i),28.0,vegamag)*ebmvx(0.24,xgalsb)')


class Test1400(Test1361):
    # Original test used gal1 but it is no longer supported, so we use gal3
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_37.fits),'
                'band(cousins,i),28.0,vegamag)*ebmvx(0.04,gal3)')


class Test1401(Test1361):
    # Original test used gal1 but it is no longer supported, so we use gal3
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_38.fits),'
                'band(cousins,i),28.0,vegamag)*ebmvx(0.08,gal3)')


class Test1402(Test1361):
    # Original test used xgal but it is no longer supported, so we use xgalsb
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_4.fits),'
                'band(cousins,i),28.0,vegamag)*ebmvx(0.24,xgalsb)')


class Test1403(Test1361):
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_40.fits),'
                'band(cousins,i),28.0,vegamag)*ebmvx(0.12,gal3)')


class Test1404(Test1361):
    # Original test used gal1 but it is no longer supported, so we use gal3
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_5.fits),'
                'band(cousins,i),28.0,vegamag)*ebmvx(0.04,gal3)')


class Test1405(Test1361):
    # Original test used gal1 but it is no longer supported, so we use gal3
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_5.fits),'
                'band(cousins,i),28.0,vegamag)*ebmvx(0.08,gal3)')


class Test1406(Test1361):
    # Original test used xgal but it is no longer supported, so we use xgalsb
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_50.fits),'
                'band(cousins,i),28.0,vegamag)*ebmvx(0.24,xgalsb)')


class Test1407(Test1361):
    # Original test used gal1 but it is no longer supported, so we use gal3
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_51.fits),'
                'band(cousins,i),28.0,vegamag)*ebmvx(0.04,gal3)')


class Test1408(Test1361):
    # Original test used gal1 but it is no longer supported, so we use gal3
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_52.fits),'
                'band(cousins,i),28.0,vegamag)*ebmvx(0.08,gal3)')


class Test1409(Test1361):
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_53.fits),'
                'band(cousins,i),28.0,vegamag)*ebmvx(0.12,gal3)')


class Test1410(Test1361):
    # Original test used smc but it is no longer supported, so we use smcbar
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_54.fits),'
                'band(cousins,i),28.0,vegamag)*ebmvx(0.16,smcbar)')


class Test1461(ThermCase):
    obsmode = 'wfc3,ir,g141'
    spectrum = 'rn(icat(k93models,9230,0.0,4.1),band(johnson,v),18.0,vegamag)'


class Test1462(Test1461):
    spectrum = 'rn(icat(k93models,9230,0.0,4.1),band(johnson,v),23.0,vegamag)'


class Test1463(Test1461):
    # Original test used gal1 but it is no longer supported, so we use gal3
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_1.fits),'
                'band(cousins,i),23.0,vegamag)*ebmvx(0.04,gal3)')


class Test1464(Test1461):
    # Original test used gal1 but it is no longer supported, so we use gal3
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_1.fits),'
                'band(cousins,i),23.0,vegamag)*ebmvx(0.08,gal3)')


class Test1465(Test1461):
    # Original test used smc but it is no longer supported, so we use smcbar
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_10.fits),'
                'band(cousins,i),23.0,vegamag)*ebmvx(0.16,smcbar)')


class Test1466(Test1461):
    # Original test used lmc but it is no longer supported, so we use lmcavg
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_11.fits),'
                'band(cousins,i),23.0,vegamag)*ebmvx(0.2,lmcavg)')


class Test1467(Test1461):
    # Original test used xgal but it is no longer supported, so we use xgalsb
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_12.fits),'
                'band(cousins,i),23.0,vegamag)*ebmvx(0.24,xgalsb)')


class Test1468(Test1461):
    # Original test used gal1 but it is no longer supported, so we use gal3
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_14.fits),'
                'band(cousins,i),23.0,vegamag)*ebmvx(0.08,gal3)')


class Test1469(Test1461):
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_2.fits),'
                'band(cousins,i),23.0,vegamag)*ebmvx(0.12,gal3)')


class Test1470(Test1461):
    # Original test used smc but it is no longer supported, so we use smcbar
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_2.fits),'
                'band(cousins,i),23.0,vegamag)*ebmvx(0.16,smcbar)')


class Test1471(Test1461):
    # Original test used lmc but it is no longer supported, so we use lmcavg
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_3.fits),'
                'band(cousins,i),23.0,vegamag)*ebmvx(0.2,lmcavg)')


class Test1472(Test1461):
    # Original test used xgal but it is no longer supported, so we use xgalsb
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_4.fits),'
                'band(cousins,i),23.0,vegamag)*ebmvx(0.24,xgalsb)')


class Test1473(Test1461):
    # Original test used gal1 but it is no longer supported, so we use gal3
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_5.fits),'
                'band(cousins,i),23.0,vegamag)*ebmvx(0.04,gal3)')


class Test1474(Test1461):
    # Original test used gal1 but it is no longer supported, so we use gal3
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_5.fits),'
                'band(cousins,i),23.0,vegamag)*ebmvx(0.08,gal3)')


class Test1475(Test1461):
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_6.fits),'
                'band(cousins,i),23.0,vegamag)*ebmvx(0.12,gal3)')


class Test1476(Test1461):
    # Original test used gal1 but it is no longer supported, so we use gal3
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_9.fits),'
                'band(cousins,i),23.0,vegamag)*ebmvx(0.04,gal3)')


class Test1477(ThermCase):
    obsmode = 'wfc3,ir,g141,bkg'
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),band(johnson,v),'
                '21.7,vegamag)+(spec(el1215a.fits)+spec(el1302a.fits)+'
                'spec(el1356a.fits)+spec(el2471a.fits))')


class Test1478(Test1477):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),band(johnson,v),'
                '22.1,vegamag)+(spec(el1215a.fits)+spec(el1302a.fits)+'
                'spec(el1356a.fits)+spec(el2471a.fits))')


class Test1479(Test1477):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),band(johnson,v),'
                '22.424602593467696,vegamag)+(spec(el1215a.fits)+'
                'spec(el1302a.fits)+spec(el1356a.fits)+spec(el2471a.fits))')


class Test1480(Test1477):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),band(johnson,v),'
                '22.7,vegamag)+(spec(el1215a.fits)+spec(el1302a.fits)+'
                'spec(el1356a.fits)+spec(el2471a.fits))')


class Test1481(Test1477):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),band(johnson,v),'
                '23.3,vegamag)+(spec(el1215a.fits)+spec(el1302a.fits)+'
                'spec(el1356a.fits)+spec(el2471a.fits))')


class Test1482(Test1477):
    spectrum = ('spec(earthshine.fits)*0.5+spec(Zodi.fits)*0.5+'
                '(spec(el1215a.fits)+spec(el1302a.fits)+spec(el1356a.fits)+'
                'spec(el2471a.fits))')

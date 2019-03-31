"""This module contains WFC3/UVIS2 commissioning tests.
Adapted from ``astrolib/pysynphot/from_commissioning/wfc3_uvis1/test*.py``
but using the other detector.
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


class Test1533(CommCase):
    obsmode = 'wfc3,uvis2,f390m'
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)+(spec(el1215a.fits)+'
                'spec(el1302a.fits)+spec(el1356a.fits)+spec(el2471a.fits))')


class Test1534(CommCase):
    obsmode = 'wfc3,uvis2,f390w'
    spectrum = 'rn(icat(k93models,9230,0.0,4.1),band(johnson,v),22.0,vegamag)'


class Test1535(Test1534):
    spectrum = 'rn(icat(k93models,9230,0.0,4.1),band(johnson,v),28.0,vegamag)'


class Test1536(Test1534):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)+(spec(el1215a.fits)+'
                'spec(el1302a.fits)+spec(el1356a.fits)+spec(el2471a.fits))')


class Test1537(CommCase):
    obsmode = 'wfc3,uvis2,f395n'
    spectrum = 'rn(icat(k93models,9230,0.0,4.1),band(johnson,v),22.0,vegamag)'


class Test1538(Test1537):
    spectrum = 'rn(icat(k93models,9230,0.0,4.1),band(johnson,v),28.0,vegamag)'


class Test1539(Test1537):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)+(spec(el1215a.fits)+'
                'spec(el1302a.fits)+spec(el1356a.fits)+spec(el2471a.fits))')


class Test1540(CommCase):
    obsmode = 'wfc3,uvis2,f410m'
    spectrum = 'rn(icat(k93models,9230,0.0,4.1),band(johnson,v),22.0,vegamag)'


class Test1541(Test1540):
    spectrum = 'rn(icat(k93models,9230,0.0,4.1),band(johnson,v),28.0,vegamag)'


class Test1542(Test1540):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)+(spec(el1215a.fits)+'
                'spec(el1302a.fits)+spec(el1356a.fits)+spec(el2471a.fits))')


class Test1543(CommCase):
    obsmode = 'wfc3,uvis2,f438w'
    spectrum = 'rn(icat(k93models,9230,0.0,4.1),band(johnson,v),22.0,vegamag)'


class Test1544(Test1543):
    spectrum = 'rn(icat(k93models,9230,0.0,4.1),band(johnson,v),28.0,vegamag)'


class Test1545(Test1543):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)+(spec(el1215a.fits)+'
                'spec(el1302a.fits)+spec(el1356a.fits)+spec(el2471a.fits))')


class Test1546(CommCase):
    obsmode = 'wfc3,uvis2,f467m'
    spectrum = 'rn(icat(k93models,9230,0.0,4.1),band(johnson,v),22.0,vegamag)'


class Test1547(Test1546):
    spectrum = 'rn(icat(k93models,9230,0.0,4.1),band(johnson,v),28.0,vegamag)'


class Test1548(Test1546):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)+(spec(el1215a.fits)+'
                'spec(el1302a.fits)+spec(el1356a.fits)+spec(el2471a.fits))')


class Test1549(CommCase):
    obsmode = 'wfc3,uvis2,f469n'
    spectrum = 'rn(icat(k93models,9230,0.0,4.1),band(johnson,v),22.0,vegamag)'


class Test1550(Test1549):
    spectrum = 'rn(icat(k93models,9230,0.0,4.1),band(johnson,v),28.0,vegamag)'


class Test1551(Test1549):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)+(spec(el1215a.fits)+'
                'spec(el1302a.fits)+spec(el1356a.fits)+spec(el2471a.fits))')


class Test1552(CommCase):
    obsmode = 'wfc3,uvis2,f475w'
    spectrum = 'rn(icat(k93models,9230,0.0,4.1),band(johnson,v),22.0,vegamag)'


class Test1553(Test1552):
    spectrum = 'rn(icat(k93models,9230,0.0,4.1),band(johnson,v),28.0,vegamag)'


class Test1554(Test1552):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)+(spec(el1215a.fits)+'
                'spec(el1302a.fits)+spec(el1356a.fits)+spec(el2471a.fits))')


class Test1555(CommCase):
    obsmode = 'wfc3,uvis2,f475x'
    spectrum = 'rn(icat(k93models,9230,0.0,4.1),band(johnson,v),22.0,vegamag)'


class Test1556(Test1555):
    spectrum = 'rn(icat(k93models,9230,0.0,4.1),band(johnson,v),28.0,vegamag)'


class Test1557(Test1555):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)+(spec(el1215a.fits)+'
                'spec(el1302a.fits)+spec(el1356a.fits)+spec(el2471a.fits))')


class Test1558(CommCase):
    obsmode = 'wfc3,uvis2,f487n'
    spectrum = 'rn(icat(k93models,9230,0.0,4.1),band(johnson,v),22.0,vegamag)'


class Test1559(Test1558):
    spectrum = 'rn(icat(k93models,9230,0.0,4.1),band(johnson,v),28.0,vegamag)'


class Test1560(Test1558):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)+(spec(el1215a.fits)+'
                'spec(el1302a.fits)+spec(el1356a.fits)+spec(el2471a.fits))')


class Test1561(CommCase):
    obsmode = 'wfc3,uvis2,f502n'
    spectrum = 'rn(icat(k93models,9230,0.0,4.1),band(johnson,v),22.0,vegamag)'


class Test1562(Test1561):
    spectrum = 'rn(icat(k93models,9230,0.0,4.1),band(johnson,v),28.0,vegamag)'


# ASTROLIB PYSYNPHOT did not require extrapolation because its flat spectrum
# has pre-define waveset using default waveset but not stsynphot.
class Test1563(Test1561):
    spectrum = ('rn(unit(1.0,flam),band(sdss,r),28.0,vegamag)+'
                'em(5007.0,5.0,1.0E-13,flam)')
    force = 'extrap'


class Test1564(Test1561):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)+(spec(el1215a.fits)+'
                'spec(el1302a.fits)+spec(el1356a.fits)+spec(el2471a.fits))')


class Test1565(CommCase):
    obsmode = 'wfc3,uvis2,f547m'
    spectrum = 'rn(icat(k93models,9230,0.0,4.1),band(johnson,v),22.0,vegamag)'


class Test1566(Test1565):
    spectrum = 'rn(icat(k93models,9230,0.0,4.1),band(johnson,v),28.0,vegamag)'


class Test1567(Test1565):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)+(spec(el1215a.fits)+'
                'spec(el1302a.fits)+spec(el1356a.fits)+spec(el2471a.fits))')


class Test1568(CommCase):
    obsmode = 'wfc3,uvis2,f555w'
    spectrum = 'rn(icat(k93models,9230,0.0,4.1),band(johnson,v),22.0,vegamag)'


class Test1569(Test1568):
    spectrum = 'rn(icat(k93models,9230,0.0,4.1),band(johnson,v),28.0,vegamag)'


class Test1570(Test1568):
    spectrum = ('rn(z(spec($PYSYN_CDBS/calspec/agk_81d266_stis_001.fits),'
                '0.05),band(johnson,b),28.0,vegamag)')
    force = 'extrap'


class Test1571(Test1568):
    spectrum = ('rn(z(spec($PYSYN_CDBS/calspec/alpha_lyr_stis_003.fits),'
                '0.15),band(johnson,b),28.0,vegamag)')


class Test1572(Test1568):
    spectrum = ('rn(z(spec($PYSYN_CDBS/calspec/bd_28d4211_stis_001.fits),'
                '0.1),band(johnson,b),28.0,vegamag)')


class Test1573(Test1568):
    spectrum = ('rn(z(spec($PYSYN_CDBS/calspec/bd_75d325_stis_001.fits),'
                '0.15),band(johnson,b),28.0,vegamag)')


class Test1574(Test1568):
    spectrum = ('rn(z(spec($PYSYN_CDBS/calspec/feige110_stis_001.fits),0.25),'
                'band(johnson,b),28.0,vegamag)')


class Test1575(Test1568):
    spectrum = ('rn(z(spec($PYSYN_CDBS/calspec/feige34_stis_001.fits),0.2),'
                'band(johnson,b),28.0,vegamag)')


class Test1576(Test1568):
    spectrum = ('rn(z(spec($PYSYN_CDBS/calspec/g191b2b_mod_004.fits),0.25),'
                'band(johnson,b),28.0,vegamag)')


class Test1577(Test1568):
    spectrum = ('rn(z(spec($PYSYN_CDBS/calspec/g93_48_004.fits),0.3),'
                'band(johnson,b),28.0,vegamag)')


class Test1578(Test1568):
    spectrum = ('rn(z(spec($PYSYN_CDBS/calspec/gd108_005.fits),0.1),'
                'band(johnson,b),28.0,vegamag)')
    force = 'extrap'


class Test1579(Test1568):
    spectrum = ('rn(z(spec($PYSYN_CDBS/calspec/gd153_mod_004.fits),0.15),'
                'band(johnson,b),28.0,vegamag)')


class Test1580(Test1568):
    spectrum = ('rn(z(spec($PYSYN_CDBS/calspec/gd50_004.fits),0.3),'
                'band(johnson,b),28.0,vegamag)')


class Test1581(Test1568):
    spectrum = ('rn(z(spec($PYSYN_CDBS/calspec/gd71_mod_005.fits),0.05),'
                'band(johnson,b),28.0,vegamag)')


class Test1582(Test1568):
    spectrum = ('rn(z(spec($PYSYN_CDBS/calspec/grw_70d5824_stis_001.fits),'
                '0.2),band(johnson,b),28.0,vegamag)')


class Test1633(CommCase):
    obsmode = 'wfc3,uvis2,f625w'
    spectrum = 'rn(icat(k93models,9230,0.0,4.1),band(johnson,v),28.0,vegamag)'


class Test1634(Test1633):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)+(spec(el1215a.fits)+'
                'spec(el1302a.fits)+spec(el1356a.fits)+spec(el2471a.fits))')


class Test1635(CommCase):
    obsmode = 'wfc3,uvis2,f631n'
    spectrum = 'rn(icat(k93models,9230,0.0,4.1),band(johnson,v),22.0,vegamag)'


class Test1636(Test1635):
    spectrum = 'rn(icat(k93models,9230,0.0,4.1),band(johnson,v),28.0,vegamag)'


class Test1637(Test1635):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)+(spec(el1215a.fits)+'
                'spec(el1302a.fits)+spec(el1356a.fits)+spec(el2471a.fits))')


class Test1638(CommCase):
    obsmode = 'wfc3,uvis2,f645n'
    spectrum = 'rn(icat(k93models,9230,0.0,4.1),band(johnson,v),22.0,vegamag)'


class Test1639(Test1638):
    spectrum = 'rn(icat(k93models,9230,0.0,4.1),band(johnson,v),28.0,vegamag)'


class Test1640(Test1638):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)+(spec(el1215a.fits)+'
                'spec(el1302a.fits)+spec(el1356a.fits)+spec(el2471a.fits))')


class Test1641(CommCase):
    obsmode = 'wfc3,uvis2,f656n'
    spectrum = 'rn(icat(k93models,9230,0.0,4.1),band(johnson,v),22.0,vegamag)'


class Test1642(Test1641):
    spectrum = 'rn(icat(k93models,9230,0.0,4.1),band(johnson,v),28.0,vegamag)'


class Test1643(Test1641):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)+(spec(el1215a.fits)+'
                'spec(el1302a.fits)+spec(el1356a.fits)+spec(el2471a.fits))')


class Test1644(CommCase):
    obsmode = 'wfc3,uvis2,f657n'
    spectrum = 'rn(icat(k93models,9230,0.0,4.1),band(johnson,v),22.0,vegamag)'


class Test1645(Test1644):
    spectrum = 'rn(icat(k93models,9230,0.0,4.1),band(johnson,v),28.0,vegamag)'


class Test1646(Test1644):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)+(spec(el1215a.fits)+'
                'spec(el1302a.fits)+spec(el1356a.fits)+spec(el2471a.fits))')


class Test1647(CommCase):
    obsmode = 'wfc3,uvis2,f658n'
    spectrum = 'rn(icat(k93models,9230,0.0,4.1),band(johnson,v),22.0,vegamag)'


class Test1648(Test1647):
    spectrum = 'rn(icat(k93models,9230,0.0,4.1),band(johnson,v),28.0,vegamag)'


class Test1649(Test1647):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)+(spec(el1215a.fits)+'
                'spec(el1302a.fits)+spec(el1356a.fits)+spec(el2471a.fits))')


class Test1650(CommCase):
    obsmode = 'wfc3,uvis2,f665n'
    spectrum = 'rn(icat(k93models,9230,0.0,4.1),band(johnson,v),22.0,vegamag)'


class Test1651(Test1650):
    spectrum = 'rn(icat(k93models,9230,0.0,4.1),band(johnson,v),28.0,vegamag)'


class Test1652(Test1650):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)+(spec(el1215a.fits)+'
                'spec(el1302a.fits)+spec(el1356a.fits)+spec(el2471a.fits))')


class Test1653(CommCase):
    obsmode = 'wfc3,uvis2,f673n'
    spectrum = 'rn(icat(k93models,9230,0.0,4.1),band(johnson,v),22.0,vegamag)'


class Test1654(Test1653):
    spectrum = 'rn(icat(k93models,9230,0.0,4.1),band(johnson,v),28.0,vegamag)'


class Test1655(Test1653):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)+(spec(el1215a.fits)+'
                'spec(el1302a.fits)+spec(el1356a.fits)+spec(el2471a.fits))')


class Test1656(CommCase):
    obsmode = 'wfc3,uvis2,f680n'
    spectrum = 'rn(icat(k93models,9230,0.0,4.1),band(johnson,v),22.0,vegamag)'


class Test1657(Test1656):
    spectrum = 'rn(icat(k93models,9230,0.0,4.1),band(johnson,v),28.0,vegamag)'


class Test1658(Test1656):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)+(spec(el1215a.fits)+'
                'spec(el1302a.fits)+spec(el1356a.fits)+spec(el2471a.fits))')


class Test1659(CommCase):
    obsmode = 'wfc3,uvis2,f689m'
    spectrum = 'rn(icat(k93models,9230,0.0,4.1),band(johnson,v),22.0,vegamag)'


class Test1660(Test1659):
    spectrum = 'rn(icat(k93models,9230,0.0,4.1),band(johnson,v),28.0,vegamag)'


class Test1661(Test1659):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)+(spec(el1215a.fits)+'
                'spec(el1302a.fits)+spec(el1356a.fits)+spec(el2471a.fits))')


class Test1662(CommCase):
    obsmode = 'wfc3,uvis2,f763m'
    spectrum = 'rn(icat(k93models,9230,0.0,4.1),band(johnson,v),22.0,vegamag)'


class Test1663(Test1662):
    spectrum = 'rn(icat(k93models,9230,0.0,4.1),band(johnson,v),28.0,vegamag)'


class Test1664(Test1662):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)+(spec(el1215a.fits)+'
                'spec(el1302a.fits)+spec(el1356a.fits)+spec(el2471a.fits))')


class Test1665(CommCase):
    obsmode = 'wfc3,uvis2,f775w'
    spectrum = 'rn(icat(k93models,9230,0.0,4.1),band(johnson,v),22.0,vegamag)'


class Test1666(Test1665):
    spectrum = 'rn(icat(k93models,9230,0.0,4.1),band(johnson,v),28.0,vegamag)'


class Test1667(Test1665):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)+(spec(el1215a.fits)+'
                'spec(el1302a.fits)+spec(el1356a.fits)+spec(el2471a.fits))')


class Test1668(CommCase):
    obsmode = 'wfc3,uvis2,f814w'
    spectrum = 'rn(icat(k93models,9230,0.0,4.1),band(johnson,v),22.0,vegamag)'


class Test1669(Test1668):
    spectrum = 'rn(icat(k93models,9230,0.0,4.1),band(johnson,v),28.0,vegamag)'


# Original test used gal1 but it is no longer supported, so we use gal3
class Test1670(Test1668):
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_1.fits),'
                'band(cousins,i),28.0,vegamag)*ebmvx(0.04,gal3)')


# Original test used gal1 but it is no longer supported, so we use gal3
class Test1671(Test1668):
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_1.fits),'
                'band(cousins,i),28.0,vegamag)*ebmvx(0.08,gal3)')


# Original test used gal1 but it is no longer supported, so we use gal3
class Test1672(Test1668):
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_10.fits),'
                'band(cousins,i),28.0,vegamag)*ebmvx(0.08,gal3)')


class Test1673(Test1668):
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_10.fits),'
                'band(cousins,i),28.0,vegamag)*ebmvx(0.12,gal3)')


# Original test used smc but it is no longer supported, so we use smcbar
class Test1674(Test1668):
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_10.fits),'
                'band(cousins,i),28.0,vegamag)*ebmvx(0.16,smcbar)')


# Original test used gal1 but it is no longer supported, so we use gal3
class Test1675(Test1668):
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_100.fits)'
                ',band(cousins,i),28.0,vegamag)*ebmvx(0.04,gal3)')


# Original test used smc but it is no longer supported, so we use smcbar
class Test1676(Test1668):
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_100.fits)'
                ',band(cousins,i),28.0,vegamag)*ebmvx(0.16,smcbar)')


# Original test used lmc but it is no longer supported, so we use lmcavg
class Test1677(Test1668):
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_100.fits)'
                ',band(cousins,i),28.0,vegamag)*ebmvx(0.2,lmcavg)')


# Original test used xgal but it is no longer supported, so we use xgalsb
class Test1678(Test1668):
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_100.fits)'
                ',band(cousins,i),28.0,vegamag)*ebmvx(0.24,xgalsb)')


class Test1679(Test1668):
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_11.fits)'
                ',band(cousins,i),28.0,vegamag)*ebmvx(0.12,gal3)')


# Original test used lmc but it is no longer supported, so we use lmcavg
class Test1680(Test1668):
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_11.fits)'
                ',band(cousins,i),28.0,vegamag)*ebmvx(0.2,lmcavg)')


class Test1681(Test1668):
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_114.fits)'
                ',band(cousins,i),28.0,vegamag)*ebmvx(0.12,gal3)')


# Original test used smc but it is no longer supported, so we use smcbar
class Test1682(Test1668):
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_117.fits)'
                ',band(cousins,i),28.0,vegamag)*ebmvx(0.16,smcbar)')


# Original test used lmc but it is no longer supported, so we use lmcavg
class Test1683(Test1668):
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_118.fits)'
                ',band(cousins,i),28.0,vegamag)*ebmvx(0.2,lmcavg)')


# Original test used smc but it is no longer supported, so we use smcbar
class Test1684(Test1668):
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_12.fits),'
                'band(cousins,i),28.0,vegamag)*ebmvx(0.16,smcbar)')


# Original test used xgal but it is no longer supported, so we use xgalsb
class Test1685(Test1668):
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_12.fits),'
                'band(cousins,i),28.0,vegamag)*ebmvx(0.24,xgalsb)')


# Original test used lmc but it is no longer supported, so we use lmcavg
class Test1686(Test1668):
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_13.fits),'
                'band(cousins,i),28.0,vegamag)*ebmvx(0.2,lmcavg)')


# Original test used gal1 but it is no longer supported, so we use gal3
class Test1687(Test1668):
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_14.fits),'
                'band(cousins,i),28.0,vegamag)*ebmvx(0.08,gal3)')


# Original test used xgal but it is no longer supported, so we use xgalsb
class Test1688(Test1668):
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_14.fits),'
                'band(cousins,i),28.0,vegamag)*ebmvx(0.24,xgalsb)')


# Original test used gal1 but it is no longer supported, so we use gal3
class Test1689(Test1668):
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_15.fits),'
                'band(cousins,i),28.0,vegamag)*ebmvx(0.04,gal3)')


# Original test used gal1 but it is no longer supported, so we use gal3
class Test1690(Test1668):
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_16.fits),'
                'band(cousins,i),28.0,vegamag)*ebmvx(0.08,gal3)')


# Original test used smc but it is no longer supported, so we use smcbar
class Test1691(Test1668):
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_16.fits),'
                'band(cousins,i),28.0,vegamag)*ebmvx(0.16,smcbar)')


class Test1692(Test1668):
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_17.fits),'
                'band(cousins,i),28.0,vegamag)*ebmvx(0.12,gal3)')


# Original test used lmc but it is no longer supported, so we use lmcavg
class Test1693(Test1668):
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_17.fits),'
                'band(cousins,i),28.0,vegamag)*ebmvx(0.2,lmcavg)')


# Original test used smc but it is no longer supported, so we use smcbar
class Test1694(Test1668):
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_18.fits),'
                'band(cousins,i),28.0,vegamag)*ebmvx(0.16,smcbar)')


# Original test used xgal but it is no longer supported, so we use xgalsb
class Test1695(Test1668):
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_18.fits),'
                'band(cousins,i),28.0,vegamag)*ebmvx(0.24,xgalsb)')


# Original test used gal1 but it is no longer supported, so we use gal3
class Test1696(Test1668):
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_19.fits),'
                'band(cousins,i),28.0,vegamag)*ebmvx(0.04,gal3)')


# Original test used lmc but it is no longer supported, so we use lmcavg
class Test1697(Test1668):
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_19.fits),'
                'band(cousins,i),28.0,vegamag)*ebmvx(0.2,lmcavg)')


class Test1698(Test1668):
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_2.fits),'
                'band(cousins,i),28.0,vegamag)*ebmvx(0.12,gal3)')


# Original test used smc but it is no longer supported, so we use smcbar
class Test1699(Test1668):
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_2.fits),'
                'band(cousins,i),28.0,vegamag)*ebmvx(0.16,smcbar)')


class Test1700(Test1668):
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_20.fits),'
                'band(cousins,i),28.0,vegamag)*ebmvx(0.12,gal3)')


# Original test used xgal but it is no longer supported, so we use xgalsb
class Test1701(Test1668):
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_20.fits),'
                'band(cousins,i),28.0,vegamag)*ebmvx(0.24,xgalsb)')


# Original test used gal1 but it is no longer supported, so we use gal3
class Test1702(Test1668):
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_22.fits),'
                'band(cousins,i),28.0,vegamag)*ebmvx(0.08,gal3)')


# Original test used xgal but it is no longer supported, so we use xgalsb
class Test1703(Test1668):
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_23.fits),'
                'band(cousins,i),28.0,vegamag)*ebmvx(0.24,xgalsb)')


# Original test used smc but it is no longer supported, so we use smcbar
class Test1704(Test1668):
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_24.fits),'
                'band(cousins,i),28.0,vegamag)*ebmvx(0.16,smcbar)')


# Original test used lmc but it is no longer supported, so we use lmcavg
class Test1705(Test1668):
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_25.fits),'
                'band(cousins,i),28.0,vegamag)*ebmvx(0.2,lmcavg)')


# Original test used xgal but it is no longer supported, so we use xgalsb
class Test1706(Test1668):
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_26.fits),'
                'band(cousins,i),28.0,vegamag)*ebmvx(0.24,xgalsb)')


# Original test used gal1 but it is no longer supported, so we use gal3
class Test1707(Test1668):
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_27.fits),'
                'band(cousins,i),28.0,vegamag)*ebmvx(0.04,gal3)')


# Original test used gal1 but it is no longer supported, so we use gal3
class Test1708(Test1668):
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_29.fits),'
                'band(cousins,i),28.0,vegamag)*ebmvx(0.08,gal3)')


# Original test used lmc but it is no longer supported, so we use lmcavg
class Test1709(Test1668):
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_3.fits),'
                'band(cousins,i),28.0,vegamag)*ebmvx(0.2,lmcavg)')


# Original test used gal1 but it is no longer supported, so we use gal3
class Test1710(Test1668):
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_31.fits),'
                'band(cousins,i),28.0,vegamag)*ebmvx(0.04,gal3)')


class Test1711(Test1668):
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_33.fits),'
                'band(cousins,i),28.0,vegamag)*ebmvx(0.12,gal3)')


# Original test used smc but it is no longer supported, so we use smcbar
class Test1712(Test1668):
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_34.fits),'
                'band(cousins,i),28.0,vegamag)*ebmvx(0.16,smcbar)')


# Original test used xgal but it is no longer supported, so we use xgalsb
class Test1713(Test1668):
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_36.fits),'
                'band(cousins,i),28.0,vegamag)*ebmvx(0.24,xgalsb)')


# Original test used gal1 but it is no longer supported, so we use gal3
class Test1714(Test1668):
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_37.fits),'
                'band(cousins,i),28.0,vegamag)*ebmvx(0.04,gal3)')


# Original test used gal1 but it is no longer supported, so we use gal3
class Test1715(Test1668):
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_38.fits),'
                'band(cousins,i),28.0,vegamag)*ebmvx(0.08,gal3)')


# Original test used xgal but it is no longer supported, so we use xgalsb
class Test1716(Test1668):
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_4.fits),'
                'band(cousins,i),28.0,vegamag)*ebmvx(0.24,xgalsb)')


class Test1717(Test1668):
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_40.fits),'
                'band(cousins,i),28.0,vegamag)*ebmvx(0.12,gal3)')


# Original test used gal1 but it is no longer supported, so we use gal3
class Test1718(Test1668):
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_5.fits),'
                'band(cousins,i),28.0,vegamag)*ebmvx(0.04,gal3)')


# Original test used gal1 but it is no longer supported, so we use gal3
class Test1719(Test1668):
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_5.fits),'
                'band(cousins,i),28.0,vegamag)*ebmvx(0.08,gal3)')


# Original test used xgal but it is no longer supported, so we use xgalsb
class Test1720(Test1668):
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_50.fits),'
                'band(cousins,i),28.0,vegamag)*ebmvx(0.24,xgalsb)')


# Original test used gal1 but it is no longer supported, so we use gal3
class Test1721(Test1668):
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_51.fits),'
                'band(cousins,i),28.0,vegamag)*ebmvx(0.04,gal3)')


# Original test used gal1 but it is no longer supported, so we use gal3
class Test1722(Test1668):
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_52.fits),'
                'band(cousins,i),28.0,vegamag)*ebmvx(0.08,gal3)')


class Test1723(Test1668):
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_53.fits),'
                'band(cousins,i),28.0,vegamag)*ebmvx(0.12,gal3)')


# Original test used smc but it is no longer supported, so we use smcbar
class Test1724(Test1668):
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_54.fits),'
                'band(cousins,i),28.0,vegamag)*ebmvx(0.16,smcbar)')


# Original test used lmc but it is no longer supported, so we use lmcavg
class Test1725(Test1668):
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_55.fits),'
                'band(cousins,i),28.0,vegamag)*ebmvx(0.2,lmcavg)')


# Original test used xgal but it is no longer supported, so we use xgalsb
class Test1726(Test1668):
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_56.fits),'
                'band(cousins,i),28.0,vegamag)*ebmvx(0.24,xgalsb)')


class Test1727(Test1668):
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_6.fits),'
                'band(cousins,i),28.0,vegamag)*ebmvx(0.12,gal3)')


# Original test used gal1 but it is no longer supported, so we use gal3
class Test1728(Test1668):
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_60.fits),'
                'band(cousins,i),28.0,vegamag)*ebmvx(0.08,gal3)')


# Original test used smc but it is no longer supported, so we use smcbar
class Test1729(Test1668):
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_63.fits),'
                'band(cousins,i),28.0,vegamag)*ebmvx(0.16,smcbar)')


# Original test used lmc but it is no longer supported, so we use lmcavg
class Test1730(Test1668):
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_63.fits),'
                'band(cousins,i),28.0,vegamag)*ebmvx(0.2,lmcavg)')


# Original test used gal1 but it is no longer supported, so we use gal3
class Test1731(Test1668):
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_65.fits),'
                'band(cousins,i),28.0,vegamag)*ebmvx(0.04,gal3)')


# Original test used gal1 but it is no longer supported, so we use gal3
class Test1732(Test1668):
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_65.fits),'
                'band(cousins,i),28.0,vegamag)*ebmvx(0.08,gal3)')


class Test1733(Test1668):
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_65.fits),'
                'band(cousins,i),28.0,vegamag)*ebmvx(0.12,gal3)')


# Original test used smc but it is no longer supported, so we use smcbar
class Test1734(Test1668):
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_67.fits),'
                'band(cousins,i),28.0,vegamag)*ebmvx(0.16,smcbar)')


# Original test used lmc but it is no longer supported, so we use lmcavg
class Test1735(Test1668):
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_67.fits),'
                'band(cousins,i),28.0,vegamag)*ebmvx(0.2,lmcavg)')


# Original test used xgal but it is no longer supported, so we use xgalsb
class Test1736(Test1668):
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_69.fits),'
                'band(cousins,i),28.0,vegamag)*ebmvx(0.24,xgalsb)')


# Original test used gal1 but it is no longer supported, so we use gal3
class Test1737(Test1668):
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_76.fits),'
                'band(cousins,i),28.0,vegamag)*ebmvx(0.08,gal3)')


# Original test used lmc but it is no longer supported, so we use lmcavg
class Test1738(Test1668):
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_87.fits),'
                'band(cousins,i),28.0,vegamag)*ebmvx(0.2,lmcavg)')


# Original test used gal1 but it is no longer supported, so we use gal3
class Test1739(Test1668):
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_9.fits),'
                'band(cousins,i),28.0,vegamag)*ebmvx(0.04,gal3)')


# Original test used gal1 but it is no longer supported, so we use gal3
class Test1740(Test1668):
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_93.fits),'
                'band(cousins,i),28.0,vegamag)*ebmvx(0.04,gal3)')


class Test1741(Test1668):
    spectrum = ('rn(spec($PYSYN_CDBS/grid/pickles/dat_uvk/pickles_uk_95.fits),'
                'band(cousins,i),28.0,vegamag)*ebmvx(0.12,gal3)')


class Test1742(Test1668):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)+(spec(el1215a.fits)+'
                'spec(el1302a.fits)+spec(el1356a.fits)+spec(el2471a.fits))')


class Test1743(CommCase):
    obsmode = 'wfc3,uvis2,f845m'
    spectrum = 'rn(icat(k93models,9230,0.0,4.1),band(johnson,v),22.0,vegamag)'


class Test1744(Test1743):
    spectrum = 'rn(icat(k93models,9230,0.0,4.1),band(johnson,v),28.0,vegamag)'


class Test1745(Test1743):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)+(spec(el1215a.fits)+'
                'spec(el1302a.fits)+spec(el1356a.fits)+spec(el2471a.fits))')


class Test1746(CommCase):
    obsmode = 'wfc3,uvis2,f850lp'
    spectrum = 'rn(icat(k93models,9230,0.0,4.1),band(johnson,v),22.0,vegamag)'


class Test1747(Test1746):
    spectrum = 'rn(icat(k93models,9230,0.0,4.1),band(johnson,v),28.0,vegamag)'


class Test1748(Test1746):
    spectrum = 'rn(pl(4000.0,-2.0,flam),band(Bessell,j),28.0,vegamag)'


class Test1749(Test1746):
    spectrum = 'rn(pl(4000.0,-2.0,flam),band(bessell,h),28.0,vegamag)'


class Test1750(Test1746):
    spectrum = 'rn(pl(4000.0,-2.0,flam),band(bessell,k),28.0,vegamag)'


class Test1751(Test1746):
    spectrum = ('rn(spec(Zodi.fits),band(johnson,v),22.7,vegamag)+'
                '(spec(el1215a.fits)+spec(el1302a.fits)+spec(el1356a.fits)+'
                'spec(el2471a.fits))')


class Test1752(Test1746):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)+(spec(el1215a.fits)+'
                'spec(el1302a.fits)+spec(el1356a.fits)+spec(el2471a.fits))')


class Test1753(Test1746):
    spectrum = ('spec(earthshine.fits)*2.0+rn(spec(Zodi.fits),band(johnson,v),'
                '22.7,vegamag)+(spec(el1215a.fits)+spec(el1302a.fits)+'
                'spec(el1356a.fits)+spec(el2471a.fits))')


class Test1754(Test1746):
    spectrum = ('spec(earthshine.fits)+rn(spec(Zodi.fits),band(johnson,v),'
                '22.7,vegamag)+(spec(el1215a.fits)+spec(el1302a.fits)+'
                'spec(el1356a.fits)+spec(el2471a.fits))')


class Test1755(CommCase):
    obsmode = 'wfc3,uvis2,f953n'
    spectrum = 'rn(icat(k93models,9230,0.0,4.1),band(johnson,v),22.0,vegamag)'


class Test1756(Test1755):
    spectrum = 'rn(icat(k93models,9230,0.0,4.1),band(johnson,v),28.0,vegamag)'


class Test1757(Test1755):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)+(spec(el1215a.fits)+'
                'spec(el1302a.fits)+spec(el1356a.fits)+spec(el2471a.fits))')


class Test1758(CommCase):
    obsmode = 'wfc3,uvis2,fq232n'
    spectrum = 'rn(icat(k93models,9230,0.0,4.1),band(johnson,v),22.0,vegamag)'


class Test1759(Test1758):
    spectrum = 'rn(icat(k93models,9230,0.0,4.1),band(johnson,v),28.0,vegamag)'


class Test1760(Test1758):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)+(spec(el1215a.fits)+'
                'spec(el1302a.fits)+spec(el1356a.fits)+spec(el2471a.fits))')


class Test1761(CommCase):
    obsmode = 'wfc3,uvis2,fq243n'
    spectrum = 'rn(icat(k93models,9230,0.0,4.1),band(johnson,v),22.0,vegamag)'


class Test1762(Test1761):
    spectrum = 'rn(icat(k93models,9230,0.0,4.1),band(johnson,v),28.0,vegamag)'


class Test1763(Test1761):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)+(spec(el1215a.fits)+'
                'spec(el1302a.fits)+spec(el1356a.fits)+spec(el2471a.fits))')


class Test1764(CommCase):
    obsmode = 'wfc3,uvis2,fq378n'
    spectrum = 'rn(icat(k93models,9230,0.0,4.1),band(johnson,v),22.0,vegamag)'


class Test1765(Test1764):
    spectrum = 'rn(icat(k93models,9230,0.0,4.1),band(johnson,v),28.0,vegamag)'


class Test1766(Test1764):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)+(spec(el1215a.fits)+'
                'spec(el1302a.fits)+spec(el1356a.fits)+spec(el2471a.fits))')


class Test1767(CommCase):
    obsmode = 'wfc3,uvis2,fq387n'
    spectrum = 'rn(icat(k93models,9230,0.0,4.1),band(johnson,v),22.0,vegamag)'


class Test1768(Test1767):
    spectrum = 'rn(icat(k93models,9230,0.0,4.1),band(johnson,v),28.0,vegamag)'


class Test1769(Test1767):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)+(spec(el1215a.fits)+'
                'spec(el1302a.fits)+spec(el1356a.fits)+spec(el2471a.fits))')


class Test1770(CommCase):
    obsmode = 'wfc3,uvis2,fq422m'
    spectrum = 'rn(icat(k93models,9230,0.0,4.1),band(johnson,v),22.0,vegamag)'


class Test1771(Test1770):
    spectrum = 'rn(icat(k93models,9230,0.0,4.1),band(johnson,v),28.0,vegamag)'


class Test1772(Test1770):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)+(spec(el1215a.fits)+'
                'spec(el1302a.fits)+spec(el1356a.fits)+spec(el2471a.fits))')


class Test1773(CommCase):
    obsmode = 'wfc3,uvis2,fq436n'
    spectrum = 'rn(icat(k93models,9230,0.0,4.1),band(johnson,v),22.0,vegamag)'


class Test1774(Test1773):
    spectrum = 'rn(icat(k93models,9230,0.0,4.1),band(johnson,v),28.0,vegamag)'


class Test1775(Test1773):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)+(spec(el1215a.fits)+'
                'spec(el1302a.fits)+spec(el1356a.fits)+spec(el2471a.fits))')


class Test1776(CommCase):
    obsmode = 'wfc3,uvis2,fq437n'
    spectrum = 'rn(icat(k93models,9230,0.0,4.1),band(johnson,v),22.0,vegamag)'


class Test1777(Test1776):
    spectrum = 'rn(icat(k93models,9230,0.0,4.1),band(johnson,v),28.0,vegamag)'


class Test1778(Test1776):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)+(spec(el1215a.fits)+'
                'spec(el1302a.fits)+spec(el1356a.fits)+spec(el2471a.fits))')


class Test1779(CommCase):
    obsmode = 'wfc3,uvis2,fq492n'
    spectrum = 'rn(icat(k93models,9230,0.0,4.1),band(johnson,v),22.0,vegamag)'


class Test1780(Test1779):
    spectrum = 'rn(icat(k93models,9230,0.0,4.1),band(johnson,v),28.0,vegamag)'


class Test1781(Test1779):
    spectrum = ('spec(earthshine.fits)*0.5+rn(spec(Zodi.fits),'
                'band(johnson,v),22.7,vegamag)+(spec(el1215a.fits)+'
                'spec(el1302a.fits)+spec(el1356a.fits)+spec(el2471a.fits))')


class Test1782(CommCase):
    obsmode = 'wfc3,uvis2,fq508n'
    spectrum = 'rn(icat(k93models,9230,0.0,4.1),band(johnson,v),22.0,vegamag)'

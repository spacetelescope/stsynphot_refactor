from __future__ import division
import os

import numpy as N

from stpysyn.test import testutil
import pysynphot as S
from pysynphot.units import Units
from pysynphot import extinction, spectrum, units, spparser, reddening, refs


class aticket123(testutil.FPTestCase):
    #Some of the tests below will fail if this is not the FIRST
    #set of tests to be run;they probe side effects on the Cache.
    def setUp(self):
        self.xt=None

    def test1(self):
        self.xt=S.Extinction(0.3,'mwdense')
        self.assert_(isinstance(self.xt,spectrum.SpectralElement))

    def test2(self):
        #test sideeffect of t1
        self.xt=S.Cache.RedLaws['mwdense']
        self.assert_(isinstance(self.xt,reddening.RedLaw))

    def test3(self):
        foo=S.Cache.RedLaws['smcbar']
        self.assert_(os.path.isfile(foo))

    def test4(self):
        self.xt=S.Extinction(0.2,S.Cache.RedLaws['smcbar'])
        self.assert_(isinstance(self.xt,spectrum.SpectralElement))


class ticket125(testutil.FPTestCase):
    def setUp(self):
        self.spstring="rn(icat(k93models,44500,0.0,5.0),band(nicmos,2,f222m),18,vegamag)"
    def testparse(self):
        self.spstring=spparser.parse_spec(self.spstring)


class ticket125_a(ticket125):
    def setUp(self):
        self.spstring="rn(icat(k93models,44500,0.0,5.0),band(v),18,vegamag)"


class ticket125_b(ticket125):
    def setUp(self):
        self.spstring="rn(icat(k93models,44500,0.0,5.0),band(johnson,v),18,vegamag)"


class ticket125_c(ticket125):
    def setUp(self):
        self.oldcwd = os.getcwd()
        os.chdir(os.path.dirname(__file__))
        self.spstring="rn(icat(k93models,44500,0.0,5.0),band(johnson,v),18,vegamag)"
        self.spstring="rn(data/bd_75d325_stis_001.fits,band(u),9.5,vegamag)*band(fos,blue,4.3,g160l)"

    def tearDown(self):
        os.chdir(self.oldcwd)

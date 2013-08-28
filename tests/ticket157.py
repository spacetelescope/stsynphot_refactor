from __future__ import division
import os

import numpy as N

import pysynphot as S
from pysynphot import spparser
from stpysyn.test import testutil
from pysynphot import locations, refs


#Places used by test code
userdir   = os.path.join(os.path.dirname(__file__), 'data')
testdata  = os.path.join(locations.rootdir, 'calspec', 'feige66_002.fits')
testdir   = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data')

old_comptable = None
old_vegafile = None

def setUpModule():
    #Freeze the version of the comptable so tests are not susceptible to
    # updates to CDBS
    global old_comptable
    global old_vegafile

    old_comptable = refs.COMPTABLE
    cmptb_name = os.path.join('mtab', 'r1j2146sm_tmc.fits')
    refs.COMPTABLE = locations._refTable(cmptb_name)
    print "%s:" % os.path.basename(__file__)
    print "   Tests are being run with %s" % refs.COMPTABLE
    print "   Synphot comparison results were computed with r1j2146sm_tmc.fits"
    #Synphot comparison results are identified with the varname synphot_ref.

    #Also set the version of Vega for similar reasons
    old_vegafile = locations.VegaFile
    locations.VegaFile = os.path.join(testdir, 'data/alpha_lyr_stis_002.fits')
    print "Using Vega spectrum: %s" % locations.VegaFile


def tearDownModule():
    refs.COMPTABLE = old_comptable
    locations.VegaFile = old_vegafile


class DiscoveryCase(OverlapBug):
    def setUp(self):
        fname = os.path.join('data', 'qso_template.fits')
        self.old_cwd = os.getcwd()
        os.chdir(os.path.dirname(__file__))
        self.spstring='rn(z(spec(%s),0.03),band(johnson,v),18,vegamag)' %fname
        self.sp=spparser.parse_spec(self.spstring)
        self.sp.convert('photlam')
        self.bp=S.ObsBandpass('stis,ccd,g750l,c7751,s52x02')
        self.refwave=6200
        self.refval=2.97759742e-06

    def tearDown(self):
        os.chdir(self.old_cwd)


#These tests were part of the original nightly pysynphot test suite
#that began failing when #157 was implemented because they really
#did have partial overlap.

class CalcphotTestCase(testutil.FPTestCase):
    #Loosened accuracy for r618 (no taper)
    def setUp(self):
        testdata  = os.path.join(locations.rootdir, 'calspec',
                                 'feige66_002.fits')
        self.sp = S.FileSpectrum(testdata)
        self.bandpass = S.ObsBandpass('acs,hrc,f555w')
        self.refrate = 8.30680E+05
        self.reflam = 5304.462

    def testraises(self):
        self.assertRaises(ValueError,
                          S.Observation,
                          self.sp, self.bandpass)

    def testefflam(self):
        obs=S.Observation(self.sp, self.bandpass, force='extrap')
        tst=obs.efflam()
        self.assertApproxFP(tst, self.reflam, 1e-4)


    def testcountrate(self):
        obs=S.Observation(self.sp, self.bandpass, force='taper')
        tst=obs.countrate()
        self.assertApproxFP(tst, self.refrate, 1e-4)


class ETCTestCase_Imag2(testutil.FPTestCase):

    def setUp(self):
        self.spectrum = "((earthshine.fits*0.5)%2brn(spec(Zodi.fits),band(V),22.7,vegamag)%2b(el1215a.fits*0.5)%2b(el1302a.fits*0.5)%2b(el1356a.fits*0.5)%2b(el2471a.fits*0.5))"
        self.obsmode = "acs,sbc,F140LP"
        self.refrate = 0.0877036
        self.setup2()

    def setup2(self):
       try:
            self.oldpath = os.path.abspath(os.curdir)
            if os.path.isdir(os.path.join(locations.specdir, 'generic')):
                os.chdir(os.path.join(locations.specdir, 'generic'))
            else:
                os.chdir(locations.specdir)
            self.sp = spparser.parse_spec(self.spectrum)
            self.sp = spparser.parse_spec(self.spectrum)
            self.bp = S.ObsBandpass(self.obsmode)
            self.parameters = ["spectrum=%s" % self.spectrum,
                               "instrument=%s" % self.obsmode]
       except AttributeError:
           pass

    def tearDown(self):
        os.chdir(self.oldpath)

    def testraises(self):
        #Replaced answer for r618 (no tapering)
        #The throughput files used in this case don't actually go
        #all the way to zero.
        self.assertRaises(ValueError,
                          S.Observation,
                          self.sp, self.bp)



    def tearDown(self):
        os.chdir(self.oldpath)



class ETCTestCase_Spec2a(ETCTestCase_Imag2):
    def setUp(self):
        self.spectrum = "(spec(crcalspec$grw_70d5824_stis_001.fits))"
        self.obsmode = "stis,fuvmama,g140l,s52x2"
        self.syn_pysyn_id = 'stis_etc_cases:SpecSourcerateSpecCase2'
        self.refrate = 28935.7
        self.setup2()



    def testflux(self):
        self.obs=S.Observation(self.sp,self.bp,force='taper')
        self.obs.convert('counts')

        self.assertApproxFP(float(self.obs.binflux[500]), 35.5329)

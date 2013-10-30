import unittest
import nose.tools

import pysynphot as S
import pysynphot.pysynexcept as exceptions

from stpysyn.test import testutil


# test the obsbandpass.ObsModeBandpass.pixel_range() and .wave_range() methods
class TestPixelWaveRangeMethods(unittest.TestCase):
  def setUp(self):
    self.bp = S.ObsBandpass('acs,hrc,f555w')

  def test_pixel_range_waveunits(self):
    num = self.bp.pixel_range((499.95,500.05),waveunits='nm',round='round')
    self.assertEqual(num,1)

  def test_wave_range_waveunits(self):
    w1, w2 = self.bp.wave_range(500,2,waveunits='nm',round=None)
    self.assertEqual(w1,499.9)
    self.assertEqual(w2,500.1)


# test the spectrum.SpectralElement.unit_response method as it's run
# by obsbandpass.ObsModeBandpass objects. results compared to synphot bandpar.
class TestUnitResponse(testutil.FPTestCase):
  def setUp(self):
    graphtab = 'mtab$u921351jm_tmg.fits'
    comptab = 'mtab$v8h1925fm_tmc.fits'
    thermtab = 'mtab$tae17277m_tmt.fits'

    S.setref(graphtable=graphtab,
             comptable=comptab,
             thermtable=thermtab)

  def tearDown(self):
    S.setref()


  def test_acs_hrc_f555w(self):
    bp = S.ObsBandpass('acs,hrc,f555w')

    ref = 3.0074E-19

    test = bp.unit_response()

    self.assertApproxFP(test,ref,accuracy=1.e-4)

  def test_acs_wfc1_f555w_f814w(self):
    bp = S.ObsBandpass('acs,wfc1,f555w,f814w')

    ref = 1.7308E-13

    test = bp.unit_response()

    self.assertApproxFP(test,ref,accuracy=1.e-4)

  def test_acs_sbc_f125lp(self):
    bp = S.ObsBandpass('acs,sbc,f125lp')

    ref = 1.7218E-17

    test = bp.unit_response()

    self.assertApproxFP(test,ref,accuracy=1.e-4)

  def test_wfc3_uvis1_f395n(self):
    bp = S.ObsBandpass('wfc3,uvis1,f395n')

    ref = 5.9579E-18

    test = bp.unit_response()

    self.assertApproxFP(test,ref,accuracy=1.e-4)

  def test_wfc3_uvis2_fq924n(self):
    bp = S.ObsBandpass('wfc3,uvis2,fq924n')

    ref = 6.9039E-18

    test = bp.unit_response()

    self.assertApproxFP(test,ref,accuracy=1.e-4)

  def test_wfc3_ir_f140w(self):
    bp = S.ObsBandpass('wfc3,ir,f140w')

    ref = 1.4574E-20

    test = bp.unit_response()

    self.assertApproxFP(test,ref,accuracy=1.e-4)

  def test_wfc3_ir_f140w(self):
    bp = S.ObsBandpass('wfc3,ir,f140w')

    ref = 1.4574E-20

    test = bp.unit_response()

    self.assertApproxFP(test,ref,accuracy=1.e-4)

  def test_wfpc2_f555w(self):
    bp = S.ObsBandpass('wfpc2,f555w')

    ref = 4.8968E-19

    test = bp.unit_response()

    self.assertApproxFP(test,ref,accuracy=1.e-4)

  def test_cos_boa_fuv_g130m_c1309(self):
    bp = S.ObsBandpass('cos,boa,fuv,g130m,c1309')

    ref = 3.5520E-15

    test = bp.unit_response()

    self.assertApproxFP(test,ref,accuracy=1.e-4)

  def test_stis_ccd_f25ndq1_a2d4_mjd55555(self):
    bp = S.ObsBandpass('stis,ccd,f25ndq1,a2d4,mjd#55555')

    ref = 3.0650E-18

    test = bp.unit_response()

    self.assertApproxFP(test,ref,accuracy=1.e-4)

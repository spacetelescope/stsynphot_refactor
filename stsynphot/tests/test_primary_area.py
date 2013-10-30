# test various aspects of having an area keyword in graphtable headers and
# propogating that area back to places where it's used

import os

import numpy as np

from pysynphot import locations
from pysynphot import refs
from pysynphot import binning
from pysynphot.tables import GraphTable
from pysynphot.observationmode import ObservationMode
from pysynphot.obsbandpass import ObsBandpass
from pysynphot.spectrum import FlatSpectrum
from pysynphot.spectrum import Integrator
from pysynphot.spectrum import CompositeSpectralElement
from pysynphot.observation import Observation
from pysynphot.pysynexcept import IncompatibleSources

import pysynphot.units as units

# a stock graph table on CDBS
GT_FILE_NO = locations.irafconvert('mtab$n9i1408hm_tmg.fits')

# this copy of a graph table has been modified to have PRIMAREA = 100.0
GT_FILE_100 = os.path.join(os.path.dirname(__file__), 'data', 'cdbs', 'mtab',
                           'n9i1408hm_tmg.fits')


def setUpModule():
    pass


def tearDownModule():
    # Reset refs
    reload(refs)


def test_graph_table1():
  gt = GraphTable(GT_FILE_100)

  assert gt.primary_area == 100.0


def test_graph_table2():
  gt = GraphTable(GT_FILE_NO)

  assert not hasattr(gt, 'primary_area')


def test_observation_mode1():
  obsmode = ObservationMode('acs,hrc,f555w', graphtable=GT_FILE_100)

  assert obsmode.primary_area != refs.PRIMARY_AREA
  assert obsmode.primary_area == 100.0

  # this should have no effect
  refs.setref(area=1.)
  assert refs.PRIMARY_AREA == 1.

  assert obsmode.primary_area != refs.PRIMARY_AREA
  assert obsmode.primary_area == 100.0

def test_observation_mode2():
  obsmode = ObservationMode('acs,hrc,f555w', graphtable=GT_FILE_NO)

  assert obsmode.primary_area == refs.PRIMARY_AREA

  # this should change the obsmode's area
  refs.setref(area=1.)
  assert refs.PRIMARY_AREA == 1.

  assert obsmode.primary_area == refs.PRIMARY_AREA

def test_obs_bandpass1():
  bp = ObsBandpass('acs,hrc,f555w', graphtable=GT_FILE_100)

  assert bp.primary_area != refs.PRIMARY_AREA
  assert bp.primary_area == 100.0

  # this should have no effect
  refs.setref(area=1.)
  assert refs.PRIMARY_AREA == 1.

  assert bp.primary_area != refs.PRIMARY_AREA
  assert bp.primary_area == 100.0


def test_obs_bandpass2():
  bp = ObsBandpass('acs,hrc,f555w', graphtable=GT_FILE_NO)

  assert bp.primary_area == refs.PRIMARY_AREA

  # this should change the bandpass's area
  refs.setref(area=1.)
  assert refs.PRIMARY_AREA == 1.

  assert bp.primary_area == refs.PRIMARY_AREA


def test_observation1():
  spec = FlatSpectrum(1)

  bp = ObsBandpass('acs,hrc,f555w', graphtable=GT_FILE_100)

  obs = Observation(spec, bp)

  assert obs.primary_area != refs.PRIMARY_AREA
  assert obs.primary_area == 100.0

  # this should have no effect
  refs.setref(area=1.)
  assert refs.PRIMARY_AREA == 1.

  assert obs.primary_area != refs.PRIMARY_AREA
  assert obs.primary_area == 100.0


def test_observation2():
  spec = FlatSpectrum(1)

  bp = ObsBandpass('acs,hrc,f555w', graphtable=GT_FILE_NO)

  obs = Observation(spec, bp)

  assert obs.primary_area == refs.PRIMARY_AREA

  # this should change the observations's area
  refs.setref(area=1.)
  assert refs.PRIMARY_AREA == 1.

  assert obs.primary_area == refs.PRIMARY_AREA


# test that you can't combine two bandpasses that don't have the same area
def test_composite_spectral_element():
  bp1 = ObsBandpass('acs,hrc,f555w', graphtable=GT_FILE_100)

  bp2 = ObsBandpass('acs,hrc,f555w', graphtable=GT_FILE_NO)

  np.testing.assert_raises(IncompatibleSources, CompositeSpectralElement,
                            bp1, bp2)


# test that the graph table's area gets used in a method
def test_unit_response():
  bp = ObsBandpass('acs,hrc,f555w', graphtable=GT_FILE_100)

  wave = bp.GetWaveSet()
  thru = bp(wave)

  Int = Integrator()

  ref = units.HC / (100.0 * Int.trapezoidIntegration(wave, thru * wave))

  test = bp.unit_response()

  np.testing.assert_allclose(ref, test)

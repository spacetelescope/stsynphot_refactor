from __future__ import division

# tests for the observation.Observation class

import os.path
import unittest

import numpy as np

import pysynphot as S
from pysynphot import Observation, ObsBandpass, FlatSpectrum
from pysynphot import locations
from stpysyn.test import testutil


# test for changes in ticket #198
# test the the bandpass .binset is the same as the Observation .binwave.
# should be since one comes from the other. also verifies that the bandpass
# has the .binset attribute, which is new in the fix to ticket 198.
def test_observation_binset():
  bp = S.ObsBandpass('acs,hrc,f555w')

  spec = S.FlatSpectrum(1)

  obs = S.Observation(spec,bp)

  assert (bp.binset == obs.binwave).all()

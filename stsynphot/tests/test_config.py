# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""Test config.py module."""
from __future__ import absolute_import, division, print_function, unicode_literals

# STDLIB
import os

# THIRD-PARTY
import numpy as np

# ASTROPY
from astropy.tests.helper import pytest

# SYNPHOT
from synphot.config import conf as synconf
from synphot.utils import generate_wavelengths

# LOCAL
from .. import config


def test_overwrite_synphot():
    """Test if overwriting ``synphot`` defaults is successful."""

    # For some reason, this does not automatically execute during testing.
    config._overwrite_synphot_config()

    vegafile = synconf.vega_file
    assert vegafile.startswith(config.conf.rootdir)
    assert os.path.isfile(vegafile)


class TestConfigChanges(object):
    def setup_class(self):
        self.def_dict = config.getref()

    @pytest.mark.parametrize(
        ('cfgname', 'new_val'),
        [('graphtable', 'mtab$n9i1408hm_tmg.fits'),
         ('comptable', 'mtab$n9i1408im_tmc.fits'),
         ('thermtable', 'mtab$n5k15531m_tmt.fits'),
         ('area', 1)])
    def test_tables_area(self, cfgname, new_val):
        # Same as config.conf.cfgname = new_val
        setattr(config.conf, cfgname, new_val)
        assert getattr(config.conf, cfgname) == new_val

        # Reset to default
        config.conf.reset(cfgname)
        assert getattr(config.conf, cfgname) == self.def_dict[cfgname]

    def test_waveset(self):
        w = generate_wavelengths(minwave=3000, maxwave=5000, num=100, log=False)
        config.conf.waveset_array = w[0].tolist()
        config.conf.waveset = w[1]
        np.testing.assert_allclose(
            [config.conf.waveset_array[0], config.conf.waveset_array[-1]],
            [3000, 4980])
        assert (config.conf.waveset ==
                'Min: 3000, Max: 5000, Num: 100, Delta: None, Log: False')

        # Reset to default
        config.conf.reset('waveset_array')
        config.conf.reset('waveset')
        np.testing.assert_allclose(
            [config.conf.waveset_array[0], config.conf.waveset_array[-1]],
            [500, 25989.72879567])
        assert config.conf.waveset == self.def_dict['waveset']

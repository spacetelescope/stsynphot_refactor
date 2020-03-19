# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""Test config.py module."""

# STDLIB
import os

# THIRD-PARTY
import numpy as np
import pytest

# SYNPHOT
from synphot.config import conf as synconf
from synphot.utils import generate_wavelengths

# LOCAL
from .. import config
from ..stio import get_latest_file, irafconvert


class TestOverwriteSynphot:
    """Test if overwriting ``synphot`` defaults is successful."""
    def setup_class(self):
        # For some reason, this does not automatically execute during testing.
        config.overwrite_synphot_config(config.conf.rootdir)

        self.vegafile = synconf.vega_file

    def test_dirname(self):
        assert self.vegafile.startswith(config.conf.rootdir)

    @pytest.mark.remote_data
    def test_isfile(self):
        if self.vegafile.startswith(('ftp', 'http')):
            # This is the case on Travis CI
            pytest.xfail('Cannot test this over FTP or HTTP')
        else:
            assert os.path.isfile(self.vegafile)


@pytest.mark.remote_data
class TestConfigChanges:
    def setup_class(self):
        self.def_dict = config.getref()

    @pytest.mark.parametrize(
        ('cfgname', 'new_val'),
        [('graphtable', 'mtab$n9i1408hm_tmg.fits'),
         ('comptable', 'mtab$n9i1408im_tmc.fits'),
         ('thermtable', 'mtab$n5k15531m_tmt.fits')])
    def test_tables_area(self, cfgname, new_val):
        # Same as config.conf.cfgname = new_val
        setattr(config.conf, cfgname, new_val)
        assert getattr(config.conf, cfgname) == new_val

        # Reset to default
        config.conf.reset(cfgname)
        old_expanded_val = get_latest_file(irafconvert(
            getattr(config.conf, cfgname)))
        assert old_expanded_val == self.def_dict[cfgname]

    def test_area(self):
        config.conf.area = 1
        assert config.conf.area == 1

        # Reset to default
        config.conf.reset('area')
        assert config.conf.area == self.def_dict['area']

    def test_waveset(self):
        w = generate_wavelengths(
            minwave=3000, maxwave=5000, num=100, log=False)
        config.conf.waveset_array = w[0].value.tolist()
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

# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""Test config.py module."""
from __future__ import division, print_function

# STDLIB
import os

# THIRD-PARTY
import numpy as np

# SYNPHOT
from synphot import config as synconfig

# LOCAL
from .. import config


def _compare_synconfig(root):
    """Make sure `synphot` config is overwritten."""
    # This differs from SYNPHOT default in Travis
    assert synconfig.STDSTAR_DIR() == os.path.join(root, 'calspec')

    # These are same in Travis but can differ in local testing
    assert synconfig.EXTINCTION_DIR() == os.path.join(root, 'extinction')
    assert synconfig.PASSBAND_DIR() == os.path.join(root, 'comp/nonhst')


def test_setdir():
    """Test setdir convenience function."""
    def_dict = config.getdir()

    _compare_synconfig(def_dict[config.ROOTDIR.name])

    # Set to non-default values

    new_root = '/foo/path/'
    config.setdir(root=new_root)

    assert config.ROOTDIR() == new_root
    assert config.CATDIR() == os.path.join(new_root, 'grid')
    assert config.MTABDIR() == os.path.join(new_root, 'mtab')
    _compare_synconfig(new_root)

    # Set back to defaults

    config.setdir()

    for x in (config.ROOTDIR, config.CATDIR, config.MTABDIR,
              synconfig.STDSTAR_DIR, synconfig.EXTINCTION_DIR,
              synconfig.PASSBAND_DIR):
        assert x() == def_dict[x.name]


def test_setref():
    """Test setref convenience function."""
    def_dict = config.getref()

    assert def_dict[config.GRAPHTABLE.name].endswith('.fits')

    # Set to non-default values

    new_graph = 'n9i1408hm_tmg.fits'
    new_comp = 'n9i1408im_tmc.fits'
    new_therm = 'n5k15531m_tmt.fits'
    config.setref(
        graphtable='mtab$'+new_graph, comptable='mtab$'+new_comp,
        thermtable='mtab$'+new_therm, area=1.0,
        waveset=(3000, 5000, 100, 'linear'))

    assert config.GRAPHTABLE() == os.path.join(config.MTABDIR(), new_graph)
    assert config.COMPTABLE() == os.path.join(config.MTABDIR(), new_comp)
    assert config.THERMTABLE() == os.path.join(config.MTABDIR(), new_therm)
    assert config.PRIMARY_AREA() == 1

    wave = config._DEFAULT_WAVESET()
    np.testing.assert_allclose([wave[0], wave[-1]], [3000, 4980])

    # Set back to defaults

    config.setref()

    for x in (config.GRAPHTABLE, config.COMPTABLE, config.THERMTABLE,
              config.PRIMARY_AREA, config._DEFAULT_WAVESET_STR):
        assert x() == def_dict[x.name]

    wave = config._DEFAULT_WAVESET()
    np.testing.assert_allclose([wave[0], wave[-1]], [500, 25989.72879567])

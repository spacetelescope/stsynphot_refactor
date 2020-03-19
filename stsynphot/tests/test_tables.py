# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""Test tables.py module.

.. note::

    Uses local graph and component tables so that the tests
    are not affected by CDBS changes.

"""

# THIRD-PARTY
import numpy as np
import pytest

# ASTROPY
from astropy.utils.data import get_pkg_data_filename

# SYNPHOT
from synphot import exceptions as synexceptions

# LOCAL
from .. import exceptions
from ..tables import GraphTable, CompTable


def test_custom_primarea():
    """Test reading non-default PRIMAREA from graph table."""
    gt = GraphTable(get_pkg_data_filename('data/tables_primarea_tmg.fits'))
    assert gt.primary_area.value == 100


class TestGraphTable:
    """Test graph table."""
    def setup_class(self):
        self.gt = GraphTable(get_pkg_data_filename('data/tables_tmg.fits'))

    def test_primarea(self):
        assert self.gt.primary_area is None

    @pytest.mark.parametrize(
        ('modes', 'innode', 'ans'),
        [(['acs'], 1, 20),
         (['wfc1'], 20, 30),
         (['acs'], 0, -1),
         (['foo'], 1, 100)])
    def test_next_node(self, modes, innode, ans):
        assert self.gt.get_next_node(modes, innode) == ans

    def test_comp(self):
        comp, thcomp = self.gt.get_comp_from_gt(
            ['wfc3', 'ir', 'f098m', 'mjd#'], 1)
        assert (set(comp) == set(
            ['wfc3_ir_mask', 'wfc3_ir_primary', 'clear', 'wfc3_ir_secondary',
             'wfc3_ir_fold', 'wfc3_pom', 'wfc3_ir_mir1', 'wfc3_ir_mir2',
             'wfc3_ir_csm', 'wfc3_ir_f098m_m', 'wfc3_ir_qe', 'wfc3_ir_cor',
             'wfc3_ir_rcp', 'wfc3_ir_win']))
        assert (set(thcomp) == set(
            ['wfc3_ir_mask', 'wfc3_ir_pads', 'wfc3_ir_primary', 'clear',
             'wfc3_ir_secondary', 'wfc3_ir_fold', 'wfc3_pom', 'wfc3_ir_mir1',
             'wfc3_ir_mir2', 'wfc3_ir_csm', 'wfc3_ir_win', 'wfc3_ir_qe',
             'wfc3_ir_rcp', 'wfc3_ir_f098m', 'wfc3_ir_wmring']))

    def test_comp_exceptions(self):
        # Invalid innode
        with pytest.raises(exceptions.UnusedKeyword):
            self.gt.get_comp_from_gt(['acs'], 0)

        # Invalid outnode
        with pytest.raises(exceptions.IncompleteObsmode):
            self.gt.get_comp_from_gt(['acs'], 1)


class TestCompTable:
    """Test optical and thermal component tables."""
    def setup_class(self):
        self.ct = CompTable(get_pkg_data_filename('data/tables_tmc.fits'))
        self.tt = CompTable(get_pkg_data_filename('data/tables_tmt.fits'))

    def test_optical_files(self):
        files = self.ct.get_filenames(['clear', None, '', 'wfc3_ir_mask'])
        np.testing.assert_array_equal(files[:3], 'clear')
        assert files[3].endswith('wfc3_ir_mask_001_syn.fits')

    def test_thermal_files(self):
        files = self.tt.get_filenames(['wfc3_ir_wmring'])
        assert files[0].endswith('wfc3_ir_wmring_001_th.fits')

    def test_exceptions(self):
        with pytest.raises(exceptions.GraphtabError):
            self.ct.get_filenames(['foo'])

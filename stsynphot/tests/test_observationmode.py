# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""Test observationmode.py module."""

# STDLIB
import os

# THIRD-PARTY
import numpy as np
import pytest

# ASTROPY
from astropy import units as u
from astropy.utils.data import get_pkg_data_filename

# SYNPHOT
from synphot import units

# LOCAL
from .. import observationmode
from ..config import conf
from ..stio import irafconvert

GT_FILE = get_pkg_data_filename('data/tables_tmg.fits')
CP_FILE = get_pkg_data_filename('data/tables_tmc.fits')
TH_FILE = get_pkg_data_filename('data/tables_tmt.fits')


@pytest.mark.remote_data
class TestComponent:
    """Test optical component."""
    def setup_class(self):
        self.path = irafconvert('cracscomp$')

    def test_no_interp(self):
        c = observationmode.Component(
            os.path.join(self.path, 'acs_f814w_wfc_006_syn.fits'))
        w = c.throughput.waveset[::2000]
        assert not c.empty
        assert c.throughput_name.endswith('acs_f814w_wfc_006_syn.fits')
        np.testing.assert_allclose(
            c.throughput(w).value,
            [0, 9.02462432e-07, 4.29190891e-07, 2.05288604e-01, 9.57082033e-01,
             9.38818634e-01, 4.94621272e-05, 0])

    def test_interp(self):
        c = observationmode.Component(
            os.path.join(self.path, 'acs_fr656n_006_syn.fits[fr656n#]'),
            interpval=6500)
        w = c.throughput.waveset[::50]
        assert not c.empty
        np.testing.assert_allclose(
            c.throughput(w).value,
            [9.37283281e-07, 1.01895410e-06, 1.20653385e-04, 7.53533347e-03,
             2.38073540e-03, 3.75275078e-04, 3.00504590e-06, 1.00051425e-06])

    def test_empty(self):
        c = observationmode.Component('clear')
        assert c.empty
        assert c.throughput is None


@pytest.mark.remote_data
class TestThermalComponent:
    """Test thermal component."""
    def setup_class(self):
        self.cp_name = irafconvert('crwfc3comp$wfc3_ir_win_001_syn.fits')
        self.th_name = irafconvert('crwfc3comp$wfc3_ir_win_001_th.fits')

    def test_no_interp(self):
        c = observationmode.ThermalComponent(self.cp_name, self.th_name)
        w = c.emissivity.waveset[6200:6350:10]
        assert not c.empty
        assert c.thermal_name.endswith('wfc3_ir_win_001_th.fits')
        np.testing.assert_allclose(
            c.emissivity(w).value,
            [0.03222001, 0.03887004, 0.02471, 0.02999997, 0.01115, 0.03276998,
             0.05794001], rtol=1e-6)

    def test_optical_empty(self):
        c = observationmode.ThermalComponent('clear', self.th_name)
        assert not c.empty
        assert c.throughput is None
        assert c.emissivity is not None

    def test_thermal_empty(self):
        c = observationmode.ThermalComponent(self.cp_name, 'clear')
        assert not c.empty
        assert c.throughput is not None
        assert c.emissivity is None

    def test_both_empty(self):
        c = observationmode.ThermalComponent('clear', 'clear')
        assert c.empty
        assert c.throughput is None
        assert c.emissivity is None


class TestProcessGraphTable:
    """Test graph table processing logic."""
    @pytest.mark.remote_data
    def test_default(self):
        gt, gtname, area = observationmode._process_graphtable(None)
        assert gtname.endswith('tmg.fits')  # Latest from CDBS
        assert area == conf.area * units.AREA

    def test_other_logic(self):
        gt_file = get_pkg_data_filename('data/tables_primarea_tmg.fits')
        gt, gtname, area = observationmode._process_graphtable(gt_file)
        assert area == 100 * units.AREA

        # Cached data
        gt2, gtname2, area2 = observationmode._process_graphtable(gt_file)
        assert gt2 is gt
        assert gtname2 == gtname
        assert area2 == area


@pytest.mark.remote_data
class TestObservationMode:
    """Test observation mode."""
    def setup_class(self):
        observationmode.reset_cache()
        self.obsmode = observationmode.ObservationMode(
            'acs,wfc1,f555w,mjd#56597',
            graphtable=GT_FILE, comptable=CP_FILE)

    def test_cache(self):
        gt_key = list(observationmode._GRAPHDICT.keys())[0]
        assert gt_key.endswith('tables_tmg.fits')

        cp_key = list(observationmode._COMPDICT.keys())[0]
        assert cp_key.endswith('tables_tmc.fits')

        det_key = list(observationmode._DETECTORDICT.keys())[0]
        assert det_key.endswith('detectors.dat')

    def test_base_attributes(self):
        """Some graph, component, and wave table behaviors are tested
        somewhere else, so not repeated here.

        """
        assert self.obsmode.modes == ['acs', 'wfc1', 'f555w', 'mjd#']
        assert self.obsmode.pardict == {'mjd': 56597}
        assert self.obsmode.ctname.endswith('tables_tmc.fits')
        assert self.obsmode.pixscale == 0.05 * u.arcsec
        assert str(self.obsmode) == 'acs,wfc1,f555w,mjd#56597'
        assert len(self.obsmode) == 5
        np.testing.assert_allclose(
            self.obsmode._constant.value, 2277381155648.759, rtol=1e-6)

    def test_components(self):
        for c in self.obsmode.components:
            assert not c.empty

    def test_throughput(self):
        t = self.obsmode.throughput
        w = t.waveset[::1000]
        np.testing.assert_allclose(
            w.value,
            [500, 3797, 4797, 5797, 6797, 7797, 8797, 9797, 10796])
        np.testing.assert_allclose(
            t(w).value,
            [0, 6.87477055e-06, 2.14807644e-01, 2.85725420e-01, 7.34488102e-07,
             2.96078061e-08, 3.57507695e-08, 9.99538418e-07, 0], rtol=1e-3)

    def test_sensitivity(self):
        sens = self.obsmode.sensitivity
        w = sens.waveset[::1000]
        np.testing.assert_allclose(
            w.value,
            [500, 3797, 4797, 5797, 6797, 7797, 8797, 9797, 10796])
        np.testing.assert_allclose(
            sens(w).value,
            [0, 5.94476276e+10, 2.34668703e+15, 3.77214087e+15, 1.13694055e+10,
             5.25738140e+08, 7.16235278e+08, 2.23012046e+10, 0], rtol=1e-3)

    def test_interp_two_params(self):
        obsmode = observationmode.ObservationMode(
            'acs,hrc,fr459m#4610,aper#0.3',
            graphtable=GT_FILE, comptable=CP_FILE)
        assert obsmode.modes == ['acs', 'hrc', 'fr459m#', 'aper#']
        assert obsmode.pardict['aper'] == 0.3
        assert obsmode.pardict['fr459m'] == 4610

    def test_thermal_spec(self):
        """Also see TestThermalObservationMode.
        Whitespace in obsmode should not matter.
        Flux values are from ASTROLIB PYSYNPHOT, except the first value,
        which is supposed to be zero.

        """
        obsmode = observationmode.ObservationMode(
            'wfc3, ir, f153m', graphtable=GT_FILE, comptable=CP_FILE)
        thsp = obsmode.thermal_spectrum(thermtable=TH_FILE)
        w = [6898, 7192, 7486, 7780, 8630, 11190, 13790, 15670, 17954.90234375]
        np.testing.assert_allclose(
            thsp(w).value,
            [2.911303e-30, 9.52169734e-29, 2.32066138e-27, 4.38458258e-26,
             1.86992105e-21, 2.90270169e-15, 3.42776351e-11, 2.15179718e-08,
             7.24300701e-09], rtol=5e-3)


@pytest.mark.remote_data
class TestThermalObservationMode:
    """Test thermal observation mode.

    .. note:: to_spectrum() method is tested in TestObservationMode.

    """
    def setup_class(self):
        self.thmode = observationmode.ThermalObservationMode(
            'wfc3,ir,f153m', graphtable=GT_FILE, comptable=CP_FILE,
            thermtable=TH_FILE)

    def test_cache(self):
        th_key = list(observationmode._THERMDICT.keys())[0]
        assert th_key.endswith('tables_tmt.fits')

    def test_attributes(self):
        assert str(self.thmode) == 'wfc3,ir,f153m (thermal)'

    def test_components(self):
        ans = ['wfc3_ir_primary_001_th.fits',
               'wfc3_ir_pads_001_th.fits',
               'wfc3_ir_secondary_001_th.fits',
               'wfc3_pom_001_th.fits',
               'wfc3_ir_csm_001_th.fits',
               'wfc3_ir_fold_001_th.fits',
               'wfc3_ir_mir1_001_th.fits',
               'wfc3_ir_mir2_001_th.fits',
               'wfc3_ir_mask_001_th.fits',
               'wfc3_ir_rcp_001_th.fits',
               'wfc3_ir_rcp_001_th.fits',
               'wfc3_ir_f153m_002_th.fits',
               'wfc3_ir_wmring_001_th.fits',
               'wfc3_ir_win_001_th.fits',
               'wfc3_ir_qe_003_th.fits',
               'clear']
        for c, a in zip(self.thmode.components, ans):
            s = c.thermal_name
            assert s.endswith(a)
            if s == 'clear':
                assert c.emissivity is None
            else:
                assert c.emissivity is not None

    def test_exceptions(self):
        with pytest.raises(NotImplementedError):
            observationmode.ThermalObservationMode(
                'acs,wfc1,f555w', graphtable=GT_FILE, comptable=CP_FILE,
                thermtable=TH_FILE)


def teardown_module():
    observationmode.reset_cache()
    assert observationmode._GRAPHDICT == {}

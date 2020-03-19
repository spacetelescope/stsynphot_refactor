# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""Module to handle observations based on observation modes."""

# STDLIB
import re
import warnings

# THIRD-PARTY
import numpy as np

# ASTROPY
from astropy import log
from astropy import units as u
from astropy.utils.decorators import lazyproperty
from astropy.utils.exceptions import AstropyUserWarning

# SYNPHOT
from synphot import exceptions as synexceptions
from synphot import units
from synphot.models import Empirical1D
from synphot.spectrum import SourceSpectrum, SpectralElement
from synphot.thermal import ThermalSpectralElement
from synphot.utils import merge_wavelengths

# LOCAL
from . import exceptions, stio
from .config import conf
from .spectrum import Vega, interpolate_spectral_element
from .tables import GraphTable, CompTable
from .wavetable import WAVECAT

__all__ = ['reset_cache', 'Component', 'ThermalComponent',
           'BaseObservationMode', 'ObservationMode', 'ThermalObservationMode']

_band_patt = re.compile(r'band\((.*?)\)', re.IGNORECASE)

# Cache previously loaded graph, component, thermal, and detector tables
_GRAPHDICT = {}
_COMPDICT = {}
_THERMDICT = {}
_DETECTORDICT = {}


def reset_cache():
    """Empty the table dictionaries cache."""
    global _GRAPHDICT, _COMPDICT, _THERMDICT, _DETECTORDICT
    _GRAPHDICT.clear()
    _COMPDICT.clear()
    _THERMDICT.clear()
    _DETECTORDICT.clear()


class Component:
    """Class to handle individual components in `BaseObservationMode`.

    Parameters
    ----------
    throughput_name : str
        Component filename.

    interpval : float or `None`
        If not `None`, interpolate to the given value.
        See :func:`stsynphot.spectrum.interpolate_spectral_element`.

    Attributes
    ----------
    throughput_name : str
        Component filename.

    throughput : `synphot.spectrum.SpectralElement` or `None`
        Component spectrum object.

    """
    def __init__(self, throughput_name, interpval=None):
        self.throughput_name = throughput_name

        # Extract bandpass unless component is a CLEAR filter.
        if throughput_name != conf.clear_filter:
            if interpval is None:
                self.throughput = SpectralElement.from_file(throughput_name)
            else:
                self.throughput = interpolate_spectral_element(
                    throughput_name, interpval)
        else:
            self.throughput = None

    @property
    def empty(self):
        """`True` if ``self.throughput`` is empty."""
        return self.throughput is None

    def __str__(self):
        return str(self.throughput)


class ThermalComponent(Component):
    """Class to handle thermal components in `BaseObservationMode`.

    Parameters
    ----------
    throughput_name, thermal_name : str
        Optical and thermal component filenames.

    interpval : float or `None`
        If not `None`, interpolate to the given value (optical only).
        See :func:`stsynphot.spectrum.interpolate_spectral_element`.


    Attributes
    ----------
    throughput_name, thermal_name : str
        Optical and thermal component filenames.

    throughput : `synphot.spectrum.SpectralElement` or `None`
        Optical component spectrum object.

    emissivity : `synphot.thermal.ThermalSpectralElement` or `None`
        Thermal component spectrum object.

    """
    def __init__(self, throughput_name, thermal_name, interpval=None):
        super(ThermalComponent, self).__init__(
            throughput_name, interpval=interpval)
        self.thermal_name = thermal_name

        # Extract thermal spectrum unless component is a CLEAR filter.
        if thermal_name != conf.clear_filter:
            self.emissivity = ThermalSpectralElement.from_file(thermal_name)
        else:
            self.emissivity = None

    @property
    def empty(self):
        """`True` if component is empty."""
        return self.throughput is None and self.emissivity is None

    def __str__(self):
        return str(self.emissivity)


def _process_graphtable(graphtable):
    """Load and cache graphtable. Get primary area."""
    global _GRAPHDICT

    # Use default graph table if not given
    if graphtable is None:
        gtname = conf.graphtable
    else:
        gtname = graphtable

    # Load and cache graphtable, if not in cache
    if gtname in _GRAPHDICT:
        gt = _GRAPHDICT[gtname]
    else:
        gt = GraphTable(gtname)
        _GRAPHDICT[gtname] = gt

    # Set telescope collecting area
    if gt.primary_area is None:
        area = conf.area
    else:
        area = gt.primary_area
    primary_area = units.validate_quantity(area, units.AREA)

    return gt, gtname, primary_area


class BaseObservationMode:
    """Base class to handle an observation that uses the graph
    and optical component tables, common to both optical and
    thermal observation modes.

    .. note::

        ``modes`` for parameterized mode is set such that the parameterized
        value is stripped away; e.g., ``'acs,wfc1,f555w,mjd#53000'``
        becomes ``['acs', 'wfc1', 'f555w', 'mjd#']``. Instead, the
        parameterized value is kept in ``pardict``; e.g., ``'mjd#53000'``
        becomes ``{'mjd': 53000.0}``.

        ``pixscale`` is set from ``stsynphot.config.conf.detectorfile``,
        which is parsed with :func:`stsynphot.stio.read_detector_pars`.

        ``binset`` is set by ``stsynphot.wavetable.WAVECAT``.

    Parameters
    ----------
    obsmode : str
        Observation mode.

    graphtable : str or `None`
        Graph table filename.
        If `None`, uses ``stsynphot.config.conf.graphtable``.

    comptable : str or `None`
        Optical component table filename.
        If `None`, uses ``stsynphot.config.conf.comptable``.

    Attributes
    ----------
    modes : list
        List of individual modes within observation mode.

    pardict : dict
        Maps parameterized mode to its value.

    gtname, ctname : str
        Graph and component table filenames.

    compnames, thcompnames : list of str
        Optical and thermal components.

    components : list of obj
        List of component objects.

    primary_area : `astropy.units.quantity.Quantity`
        Telescope collecting area.

    pixscale : `astropy.units.quantity.Quantity`
        Detector pixel scale.

    binset : str
        Wavelength table filename/param string from matching obsmode.

    bandwave : `astropy.units.quantity.Quantity`
        Wavelength set defined by ``binset``.

    """
    def __init__(self, obsmode, graphtable=None, comptable=None):
        global _GRAPHDICT, _COMPDICT

        # Strip "band()" syntax if present, and force lowercase
        tmatch = _band_patt.search(obsmode)
        if tmatch:
            self._obsmode = tmatch.group(1).lower()
        else:
            self._obsmode = obsmode.lower()

        # Split obsmode and separate parameterized modes
        modes = self._obsmode.replace(' ', '').split(',')
        self.pardict = {}
        if '#' in self._obsmode:
            self.modes = []
            for m in modes:
                if '#' in m:
                    key, val = m.split('#')
                    self.pardict[key] = float(val)
                    self.modes.append(f'{key:s}#')
                else:
                    self.modes.append(m)
        else:
            self.modes = modes

        # Get graph table and primary area
        gt, self.gtname, self.primary_area = _process_graphtable(graphtable)

        # Get optical and thermal components
        self.compnames, self.thcompnames = gt.get_comp_from_gt(self.modes, 1)

        # Use default optical component table if not given
        if comptable is None:
            self.ctname = conf.comptable
        else:
            self.ctname = comptable

        # Load and cache comptable, if not in cache
        if self.ctname in _COMPDICT:
            ct = _COMPDICT[self.ctname]
        else:
            ct = CompTable(self.ctname)
            _COMPDICT[self.ctname] = ct

        # Set by sub-classes
        self.components = None

        # Get optical component filenames
        self._throughput_filenames = ct.get_filenames(self.compnames)

        # Set detector pixel scale
        self._set_pixscale()

        # For sensitivity calculations
        self._constant = self.primary_area / units.HC

        # Get wavelength set
        try:
            self.binset, self.bandwave = WAVECAT.load_waveset(self._obsmode)
        except (KeyError, exceptions.AmbiguousObsmode):
            self.binset = ''
            self.bandwave = None

    def _set_pixscale(self):
        """Set pixel scale.
        If multiple matches found, only first match is used.

        """
        global _DETECTORDICT

        det_file = stio.irafconvert(conf.detectorfile)

        if det_file in _DETECTORDICT:
            data = _DETECTORDICT[det_file]
        else:
            data = stio.read_detector_pars(det_file)
            _DETECTORDICT[det_file] = data

        obsmode = ','.join(self._obsmode.split(',')[:2])
        pixscales = data[data['OBSMODE'] == obsmode]['SCALE'].data

        if pixscales.size < 1:
            self.pixscale = None
        else:
            self.pixscale = pixscales[0] * u.arcsec

    def _get_components(self):
        raise NotImplementedError('To be implemented by subclasses.')

    def __str__(self):
        return self._obsmode

    def __len__(self):
        return len(self.components)

    @staticmethod
    def _parkey_from_filename(filename):
        """Extract parkey from component filename in the format of
        ``name[parkey#]``.

        """
        if filename.endswith('#]'):
            x = filename.split('[')
            parkey = x[1][:-2]
        else:
            parkey = None
        return parkey

    def showfiles(self):  # pragma: no cover
        """Display optical component filenames.

        .. note:: Similar to IRAF SYNPHOT SHOWFILES.

        """
        info_str = '#Throughput table names:\n'
        for name in self._throughput_filenames:
            if name != conf.clear_filter:
                info_str += f'{name}\n'
        log.info(info_str.rstrip())


class ObservationMode(BaseObservationMode):
    """Class to handle an observation that uses the graph
    and optical component tables.

    See `BaseObservationMode` for additional attributes.

    Parameters
    ----------
    obsmode, graphtable, comptable
        See `BaseObservationMode`.

    component_dict : dict
        Maps component filename to corresponding `Component`.

    """
    def __init__(self, obsmode, graphtable=None, comptable=None,
                 component_dict={}):
        super(ObservationMode, self).__init__(
            obsmode, graphtable=graphtable, comptable=comptable)
        self._component_dict = component_dict
        self.components = self._get_components()

    def _get_components(self):
        """Get optical components."""
        components = []

        for throughput_name in self._throughput_filenames:
            parkey = self._parkey_from_filename(throughput_name)

            # Hack for WFPC2 ramp filters
            if parkey == 'wave' and self.modes[0] == 'wfpc2':
                parkey = 'lrf'

            cdict_key = (throughput_name, self.pardict.get(parkey))

            if cdict_key not in self._component_dict:
                self._component_dict[cdict_key] = Component(
                    cdict_key[0], interpval=cdict_key[1])

            component = self._component_dict[cdict_key]

            if not component.empty:
                components.append(component)

        return components

    def _mul_thru(self, index):
        """Multiply all component spectra starting at given index."""
        product = self.components[index].throughput

        if len(self.components) > index:
            for component in self.components[index + 1:]:
                if not component.empty:
                    product = product * component.throughput

        product.meta['header'] = ''  # Clean up messy header
        return product

    @lazyproperty
    def throughput(self):
        """Combined throughput from multiplying all the components together."""
        try:
            thru = self._mul_thru(0)
        except IndexError as e:  # pragma: no cover
            thru = None
            warnings.warn(
                f'Graph table is broken: {repr(e)}', AstropyUserWarning)
        return thru

    @lazyproperty
    def sensitivity(self):
        """Sensitivity spectrum to convert flux in
        :math:`erg \\; cm^{-2} \\; s^{-1} \\; \\AA^{-1}` to
        :math:`count s^{-1} \\AA^{-1}`. Calculation is done by
        combining the throughput curves with
        :math:`\\frac{h \\; c}{\\lambda}` .

        """
        x = self.throughput.waveset
        y = self.throughput(x)
        thru = y.value * x.value * self._constant.value
        meta = {'expr': f'Sensitivity for {self._obsmode}'}
        return SpectralElement(
            Empirical1D, points=x, lookup_table=thru, meta=meta)

    def thermal_spectrum(self, thermtable=None):
        """Calculate thermal spectrum using
        :func:`ThermalObservationMode.to_spectrum`.

        Parameters
        ----------
        thermtable : str or `None`
            Thermal component table filename.
            If `None`, uses ``stsynphot.config.conf.thermtable``.

        Returns
        -------
        sp : `synphot.spectrum.SourceSpectrum`
            Thermal spectrum in PHOTLAM.

        Raises
        ------
        synphot.exceptions.SynphotError
            Calculation failed.

        """
        thom = ThermalObservationMode(
            self._obsmode, graphtable=self.gtname, comptable=self.ctname,
            thermtable=thermtable)

        try:
            sp = thom.to_spectrum()
        except IndexError as e:  # pragma: no cover
            raise synexceptions.SynphotError(f'Broken graph table: {repr(e)}')

        return sp


class ThermalObservationMode(BaseObservationMode):
    """Class to handle an observation that uses the graph,
    optical component, and thermal component tables.

    See `BaseObservationMode` for additional attributes.

    Parameters
    ----------
    obsmode, graphtable, comptable
        See `BaseObservationMode`.

    thermtable : str or `None`
        Thermal component table filename.
        If `None`, uses ``stsynphot.config.conf.thermtable``.

    Attributes
    ----------
    thname : str
        Thermal component table filename.

    Raises
    ------
    NotImplementedError
        Clear filters only not supported.

    """
    def __init__(self, obsmode, graphtable=None, comptable=None,
                 thermtable=None):
        global _GRAPHDICT, _COMPDICT, _THERMDICT

        super(ThermalObservationMode, self).__init__(
            obsmode, graphtable=graphtable, comptable=comptable)

        # Check here to see if there are any valid filters.
        # "0.0" was added in tae17277m_tmt.fits (Apr 2017).
        if set(self.thcompnames).issubset(set([conf.clear_filter, '', '0.0'])):
            raise NotImplementedError(
                f'No thermal support provided for {self._obsmode}')

        # Use default thermal component table if not given
        if thermtable is None:
            self.thname = conf.thermtable
        else:
            self.thname = thermtable

        # Load and cache thermtable, if not in cache
        if self.thname in _THERMDICT:
            thct = _THERMDICT[self.thname]
        else:
            thct = CompTable(self.thname)
            _THERMDICT[self.thname] = thct

        # Get thermal component filenames
        self._thermal_filenames = thct.get_filenames(self.thcompnames)

        self.components = self._get_components()

    def _get_components(self):
        """Get thermal components."""
        components = []

        for throughput_name, thermal_name in zip(
                self._throughput_filenames, self._thermal_filenames):
            parkey = self._parkey_from_filename(throughput_name)
            component = ThermalComponent(throughput_name, thermal_name,
                                         interpval=self.pardict.get(parkey))
            if not component.empty:
                components.append(component)

        return components

    def __str__(self):
        return f'{self._obsmode} (thermal)'

    def _merge_em_wave(self):
        """Merge emissivity wavelength sets in Angstrom."""
        index = 1

        # Find first wavelength set
        for component in self.components:
            emissivity = component.emissivity
            if emissivity is None:
                index += 1
            else:
                result = emissivity.waveset.value
                break

        # Merge subsequent wavelength sets
        for component in self.components[index:]:
            emissivity = component.emissivity
            if emissivity is not None:
                result = merge_wavelengths(result, emissivity.waveset.value)

        return result

    def _get_wave_intersection(self):
        """Find wavelengths in Angstrom where
        ``stsynphot.config.conf.waveset_array`` intersects with
        ``stsynphot.spectrum.Vega``.

        .. note:: No one knows why Vega is the chosen one.

        """
        def_wave = conf.waveset_array  # Angstrom
        minw = min(def_wave)
        maxw = max(def_wave)

        # Refine min and max wavelengths using thermal components
        for component in self.components[1:]:
            emissivity = component.emissivity
            if emissivity is not None:
                w = emissivity.waveset.value  # Angstrom
                minw = max(minw, w.min())
                maxw = min(maxw, w.max())

        w = self._merge_em_wave()
        result = w[(w > minw) & (w < maxw)]

        # Intersect with Vega
        if Vega is None:
            raise synexceptions.SynphotError('Missing Vega spectrum.')
        w = Vega.waveset.value  # Angstrom

        return result[(result > w.min()) & (result < w.max())]

    def to_spectrum(self):
        """Get thermal spectrum.

        The calculations start with zero-flux spectrum.
        Then for each component:

        #. Multiply with optical throughput.
        #. Add in thermal source spectrum from
           :meth:`synphot.thermal.ThermalSpectralElement.thermal_source`.

        Returns
        -------
        sp : `synphot.spectrum.SourceSpectrum`
            Thermal spectrum in PHOTLAM.

        """
        # Create zero-flux spectrum
        x = self._get_wave_intersection()  # Angstrom
        y = np.zeros_like(x, dtype=np.float64)  # PHOTLAM
        minw, maxw = x[([0, -1], )]
        sp = SourceSpectrum(Empirical1D, points=x, lookup_table=y)

        for component in self.components:
            # Transmissive section (optical passband)
            if component.throughput is not None:
                sp = sp * component.throughput

            # Thermal section
            if component.emissivity is not None:
                sp = sp + component.emissivity.thermal_source()

                # Trim spectrum
                w = sp.waveset.value
                mask = (w >= minw) & (w <= maxw)
                x = w[mask]
                y = sp(x)
                sp = SourceSpectrum(Empirical1D, points=x, lookup_table=y)

        meta = {'expr': f'{self._obsmode} ThermalSpectrum'}
        sp.meta.update(meta)
        return sp

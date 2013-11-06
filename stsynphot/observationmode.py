# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""Module to handle observations based on observation modes."""
from __future__ import absolute_import, division, print_function, unicode_literals

# STDLIB
import re

# THIRD-PARTY
import numpy as np

# ASTROPY
from astropy import log
from astropy import units as u

# SYNPHOT
from synphot import planck, units
from synphot import exceptions as synexceptions
from synphot import spectrum as synspectrum
from synphot.utils import merge_wavelengths

# LOCAL
from . import config, exceptions, io, spectrum, tables
from .wavetable import WAVECAT


__all__ = ['reset_cache', 'Component', 'ThermalComponent',
           'BaseObservationMode', 'ObservationMode', 'ThermalObservationMode']

_band_patt = re.compile(r'band\((.*?)\)', re.IGNORECASE)

# Cache previously loaded graph, component, and thermal tables
_GRAPHDICT = {}
_COMPDICT = {}
_THERMDICT = {}


def reset_cache():
    """Empty the table dictionaries cache."""
    global _GRAPHDICT, _COMPDICT, _THERMDICT
    _GRAPHDICT.clear()
    _COMPDICT.clear()
    _THERMDICT.clear()


class Component(object):
    """Class to handle individual components in `BaseObservationMode`.

    Parameters
    ----------
    throughput_name : str
        Component filename.

    interpval : float or `None`, optional
        If not `None`, interpolate to the given value.
        See :func:`stsynphot.spectrum.interpolate_spectral_element`.

    area : float or `astropy.units.quantity.Quantity`, optional
        Telescope collecting area. If not Quantity, assumed
        to be in :math:`cm^{2}`.

    Attributes
    ----------
    throughput_name : str
        Component filename.

    throughput : `synphot.spectrum.SpectralElement` or `None`
        Component spectrum object.

    primary_area : float or `astropy.units.quantity.Quantity`
        Telescope collecting area. If not Quantity, assumed
        to be in :math:`cm^{2}`.

    """
    def __init__(self, throughput_name, interpval=None, area=None):
        self.throughput_name = throughput_name
        self.primary_area = area
        self._interpval = interpval
        self._empty = True
        self._build_throughput()

    def _build_throughput(self):
        """Extract passband spectrum unless component is a CLEAR filter."""
        if self.throughput_name != tables.CLEAR_FILTER:
            self._empty = False
            if self._interpval is None:
                self.throughput = synspectrum.SpectralElement.from_file(
                    self.throughput_name, area=self.primary_area)
            else:
                self.throughput = spectrum.interpolate_spectral_element(
                    self.throughput_name, self._interpval,
                    area=self.primary_area)
        else:
            self.throughput = None

    def __str__(self):
        return str(self.throughput)

    @property
    def empty(self):
        """`True` if ``self.throughput`` is empty."""
        return self._empty


class ThermalComponent(Component):
    """Class to handle thermal components in `BaseObservationMode`.

    Parameters
    ----------
    throughput_name, thermal_name : str
        Optical and thermal component filenames.

    interpval : float or `None`, optional
        If not `None`, interpolate to the given value (optical only).
        See :func:`stsynphot.spectrum.interpolate_spectral_element`.

    area : float or `astropy.units.quantity.Quantity`, optional
        Telescope collecting area. If not Quantity, assumed
        to be in :math:`cm^{2}`.

    Attributes
    ----------
    throughput_name, thermal_name : str
        Optical and thermal component filenames.

    throughput : `synphot.spectrum.SpectralElement` or `None`
        Optical component spectrum object.

    emissivity : `stsynphot.spectrum.ThermalSpectralElement` or `None`
        Thermal component spectrum object.

    primary_area : float or `astropy.units.quantity.Quantity`
        Telescope collecting area. If not Quantity, assumed
        to be in :math:`cm^{2}`.

    """
    def __init__(self, throughput_name, thermal_name, interpval=None,
                 area=None):
        Component.__init__(
            self, throughput_name, interpval=interpval, area=area)
        self.thermal_name = thermal_name
        self._build_emissivity()

    def _build_emissivity(self):
        """Extract thermal spectrum unless component is a CLEAR filter."""
        if self.thermal_name != tables.CLEAR_FILTER:
            self._empty = False
            self.emissivity = spectrum.ThermalSpectralElement.from_file(
                self.thermal_name, area=self.primary_area)
        else:
            self.emissivity = None


def _process_graphtable(graphtable):
    """Load and cache graphtable. Get primary area."""
    global _GRAPHDICT

    # Use default graph table if not given
    if graphtable is None:
        gtname = config.GRAPHTABLE()
    else:
        gtname = graphtable

    # Load and cache graphtable, if not in cache
    if gtname in _GRAPHDICT:
        gt = _GRAPHDICT[gtname]
    else:
        gt = tables.GraphTable(gtname)
        _GRAPHDICT[gtname] = gt

    # Set telescope collecting area
    if gt.primary_area is None:
        area = config.PRIMARY_AREA()
    else:
        area = gt.primary_area
    primary_area = units.validate_quantity(area, units.AREA)

    return gt, gtname, primary_area


class BaseObservationMode(object):
    """Base class to handle an observation that uses the graph
    and optical component tables, common to both optical and
    thermal observation modes.

    Parameters
    ----------
    obsmode : str
        Observation mode.

    graphtable : str or `None`
        Graph table filename. If `None`, uses ``stsynphot.config.GRAPHTABLE``.

    comptable : str or `None`
        Optical component table filename. If `None`, uses
        ``stsynphot.config.COMPTABLE``.

    Attributes
    ----------
    modes : list
        List of individual modes within observation mode. For parameterized mode, its value is stripped. For example, ``'acs,wfc1,f555w,mjd#53000'`` becomes ``['acs', 'wfc1', 'f555w', 'mjd#']``.

    pardict : dict
        Maps parameterized mode to its value. For example, ``'mjd#53000'`` becomes ``{'mjd': 53000.0}``.

    gtname, ctname : str
        Graph and component table filenames.

    compnames, thcompnames : list of str
        Optical and thermal components.

    components : list of obj
        List of component objects.

    primary_area : `astropy.units.quantity.Quantity`
        Telescope collecting area.

    pixscale : `astropy.units.quantity.Quantity`
        Detector pixel scale from ``stsynphot.config.DETECTORFILE``, which is parsed with :func:`synphot.io.read_detector_pars`.

    binset : str
        Wavelength table filename or parameter string from the  matching observation mode in ``stsynphot.wavetable.WAVECAT``.

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
        modes = self._obsmode.split(',')
        self.pardict = {}
        if '#' in self._obsmode:
            self.modes = []
            for m in modes:
                if '#' in m:
                    key, val = m.split('#')
                    self.pardict[key] = float(val)
                    self.modes.append('{0:s}#'.format(key))
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
            self.ctname = config.COMPTABLE()
        else:
            self.ctname = comptable

        # Load and cache comptable, if not in cache
        if self.ctname in _COMPDICT:
            ct = _COMPDICT[self.ctname]
        else:
            ct = tables.CompTable(self.ctname)
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
        except (KeyError, exceptions.AmbiguousObsmode) as e:
            log.warn(str(e))
            self.binset = ''
            self.bandwave = None

    def _set_pixscale(self):
        """Set pixel scale.
        If multiple matches found, only first match is used.

        """
        data = io.read_detector_pars(io.irafconvert(config.DETECTORFILE()))
        obsmode = ','.join(self._obsmode.split(',')[:2])
        pixscales = data[data['OBSMODE'] == obsmode]['SCALE'].data

        if pixscales.size < 1:
            raise synexceptions.SynphotError(
                '{0} not found in {1}.'.format(obsmode, config.DETECTORFILE()))

        self.pixscale = u.Quantity(pixscales[0], unit=u.arcsec)

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

    def showfiles(self):
        """Display optical component filenames.

        .. note:: Similar to IRAF SYNPHOT SHOWFILES.

        """
        info_str = '#Throughput table names:\n'
        for name in self._throughput_filenames:
            if name != tables.CLEAR_FILTER:
                info_str += '{0}\n'.format(name)
        log.info(info_str.rstrip())


class ObservationMode(BaseObservationMode):
    """Class to handle an observation that uses the graph
    and optical component tables.

    Parameters
    ----------
    obsmode, graphtable, comptable
        See `BaseObservationMode`.

    component_dict : dict
        Maps component filename to corresponding `Component`.

    Attributes
    ----------
    modes, pardict, gtname, ctname, compnames, thcompnames, components, primary_area, pixscale, binset, bandwave
        See `BaseObservationMode`.

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
            cdict_key = (throughput_name, self.pardict.get(parkey))

            if cdict_key not in self._component_dict:
                self._component_dict[cdict_key] = Component(
                    cdict_key[0], interpval=cdict_key[1],
                    area=self.primary_area)

            component = self._component_dict[cdict_key]

            if not component.empty:
                components.append(component)

        return components

    def _mul_thru(self, index):
        """Multiply all component spectra starting at given index."""
        product = self.components[index].throughput
        if len(self.components) > index:
            for component in self.components[index+1:]:
                if not component.empty:
                    product = product * component.throughput
        return product

    def sensitivity(self):
        """Calculate sensitivity spectrum.

        Calculation is done by combining the throughput curves
        with :math:`\\frac{h \\; c}{\\lambda}` to convert
        :math:`erg \\; cm^{-2} \\; s^{-1} \\; \\AA^{-1}` to
        :math:`count s^{-1}`. Multiplying this by the flux in
        :math:`erg \\; cm^{-2} \\; s^{-1} \\; \\AA^{-1}`
        will give :math:`count s^{-1} \\AA^{-1}`.

        Returns
        -------
        sp : `synphot.spectrum.SpectralElement`
            Sensitivity spectrum.

        """
        product = self._mul_thru(0)
        thru = product.thru.value * product.wave.value * self._constant.value
        header = {'expr': 'Sensitivity for {0}'.format(self._obsmode)}
        sp = synspectrum.SpectralElement(
            product.wave, thru, area=self.primary_area, header=header)
        return sp

    def throughput(self):
        """Calculate combined throughput spectrum.
        Calculation is done by multiplying all the components together.

        Returns
        -------
        sp : `synphot.spectrum.SpectralElement` or `None`
            Combined throughput. `None` if calculation failed.

        """
        try:
            sp = self._mul_thru(0)
        except IndexError as e:
            log.warn('Graph table is broken: {0}'.format(str(e)))
            sp = None
        else:
            sp.metadata['expr'] = '*'.join([str(x) for x in self.components])

        return sp

    def thermal_spectrum(self, thermtable=None):
        """Calculate thermal spectrum using
        :func:`ThermalObservationMode.to_spectrum`.

        Parameters
        ----------
        thermtable : str or `None`
            Thermal component table filename. If `None`, uses
            ``stsynphot.config.THERMTABLE``.

        Returns
        -------
        sp : `synphot.spectrum.SourceSpectrum`
            Thermal spectrum.

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
        except IndexError as e:
            raise synexceptions.SynphotError(
                'Broken graph table: {0}'.format(str(e)))

        return sp


class ThermalObservationMode(BaseObservationMode):
    """Class to handle an observation that uses the graph,
    optical component, and thermal component tables.

    Parameters
    ----------
    obsmode, graphtable, comptable
        See `BaseObservationMode`.

    thermtable : str or `None`
        Thermal component table filename. If `None`, uses
        ``stsynphot.config.THERMTABLE``.

    Attributes
    ----------
    modes, pardict, gtname, ctname, compnames, thcompnames, components, primary_area, pixscale, binset, bandwave
        See `BaseObservationMode`.

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

        # Check here to see if there are any valid filters
        if set(self.thcompnames).issubset(set([tables.CLEAR_FILTER, ''])):
            raise NotImplementedError(
                'No thermal support provided for {0}'.format(self._obsmode))

        # Use default thermal component table if not given
        if thermtable is None:
            self.thname = config.THERMTABLE()
        else:
            self.thname = thermtable

        # Load and cache thermtable, if not in cache
        if self.thname in _THERMDICT:
            thct = _THERMDICT[self.thname]
        else:
            thct = tables.CompTable(self.thname)
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
            component = ThermalComponent(
                throughput_name, thermal_name,
                interpval=self.pardict.get(parkey), area=self.primary_area)
            if not component.empty:
                components.append(component)

        return components

    def __str__(self):
        return '{0} (thermal)'.format(self._obsmode)

    def _merge_em_wave(self, wave_unit='angstrom'):
        """Merge emissivity wavelength sets in given unit.

        Returns
        -------
        result : array_like

        """
        index = 1

        # Find first wavelength set
        for component in self.components:
            emissivity = component.emissivity
            if emissivity is None:
                index += 1
            else:
                result = emissivity.wave.to(
                    wave_unit, equivalencies=u.spectral()).value
                break

        # Merge subsequent wavelength sets
        for component in self.components[index:]:
            if component.emissivity is not None:
                w = component.emissivity.wave.to(
                    wave_unit, equivalencies=u.spectral())
                result = merge_wavelengths(result, w.value)

        return result

    def _get_wave_intersection(self):
        """Find wavelengths where ``stsynphot.config._DEFAULT_WAVESET``
        intersects with ``synphot.config.VEGA_FILE``.

        .. note:: No one knows why Vega is the chosen one.

        Returns
        -------
        wave : `astropy.units.quantity.Quantity`

        """
        def_wave = config._DEFAULT_WAVESET()  # Angstrom
        def_wave_unit = u.AA
        minw = def_wave[0]
        maxw = def_wave[-1]

        # Refine min and max wavelengths using thermal components
        for component in self.components[1:]:
            if component.emissivity is not None:
                w = component.emissivity.wave.to(
                    def_wave_unit, equivalencies=u.spectral()).value
                minw = max(minw, w[0])
                maxw = min(maxw, w[-1])

        w = self._merge_em_wave()
        result = w[(w > minw) & (w < maxw)]

        # Intersect with Vega
        if spectrum.Vega is None:
            raise synexceptions.SynphotError('Missing Vega spectrum.')
        w = spectrum.Vega.wave.to(
            def_wave_unit, equivalencies=u.spectral()).value

        return u.Quantity(result[(result > w[0]) & (result < w[-1])],
                          unit=def_wave_unit)

    def to_spectrum(self):
        """Get thermal spectrum.

        The calculations start with zero-flux spectrum.
        Then for each component:
            #. Multiply with optical throughput.
            #. For thermal component:
                #. Calculate blackbody radiation (per square
                   arcsec) for given temperature.
                #. Multiply blackbody with emissivity and
                   beam fill factor.
                #. Add the result to output spectrum.

        Returns
        -------
        sp : `synphot.spectrum.SourceSpectrum`
            Thermal spectrum.

        """
        # Create zero-flux spectrum
        wave = self._get_wave_intersection()
        flux = u.Quantity(np.zeros(wave.shape, dtype=np.float64),
                          unit=units.PHOTLAM)
        sp = synspectrum.SourceSpectrum(
            wave, flux, area=self.primary_area,
            header={'expr': '{0}'.format(str(self))})

        minw = sp.wave.value[0]
        maxw = sp.wave.value[-1]

        for component in self.components:
            # Transmissive section (optical passband)
            if component.throughput is not None:
                sp = sp * component.throughput

            # Thermal section
            if component.emissivity is not None:
                # Blackbody from temperature
                t = component.emissivity.temperature
                bbflux = planck.bb_photlam_arcsec(sp.wave, t)
                sp_bb = synspectrum.SourceSpectrum(
                    sp.wave, bbflux.value, flux_unit=units.PHOTLAM,
                    area=self.primary_area,
                    header={'expr': 'bb_per_arcsec({0})'.format(t)})

                # Thermal spectrum to add
                sp_comp = (sp_bb * component.emissivity *
                           component.emissivity.beam_fill_factor)
                sp = sp + sp_comp

                # Trim spectrum
                sp = sp.trim_spectrum(minw, maxw)

        return sp

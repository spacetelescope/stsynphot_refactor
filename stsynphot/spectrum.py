# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""This module contains spectrum classes specific to STScI formats."""
from __future__ import division, print_function

# STDLIB
import re
import os

# THIRD-PARTY
import numpy as np

# ASTROPY
from astropy import log
from astropy import units as u

# SYNPHOT
from synphot import binning, reddening, units
from synphot import config as synconfig
from synphot import exceptions as synexceptions
from synphot import specio
from synphot import spectrum as synspectrum

# LOCAL
from . import config, stio


__all__ = ['reset_cache', 'interpolate_spectral_element',
           'ThermalSpectralElement', 'ObservationSpectralElement', 'band',
           'ebmvx', 'load_vega', 'Vega']

_interpfilepatt = re.compile('\[(?P<col>.*?)\]')
_REDLAWS = {}  # Cache previously loaded reddening laws
Vega = None  # Cache Vega spectrum


def reset_cache():
    """Empty the reddening laws cache."""
    global _REDLAWS
    _REDLAWS.clear()


def _interp_spec(interpval, waves, lower_val, upper_val, lower_thru,
                 upper_thru, doshift):
    """Interpolate between two spectra to parameter at given value.
    Called by :func:`interpolate_spectral_element`.

    Parameters
    ----------
    interpval : float
        Desired parameter value.

    waves : array_like
        Wavelengths for all the parameterized spectra.

    lower_val, upper_val : float
        Low and high values of parameter to interpolate.

    lower_thru, upper_thru : array_like
        Throughput values are ``lower_val`` and ``upper_val``.

    doshift : bool
        Perform wavelength shift before interpolation.

    Returns
    -------
    thru : array_like
        Interpolated throughput at ``interpval``.

    """
    if doshift:
        # Adjust the wavelength table to bracket the range
        lwave = waves + (lower_val - interpval)
        uwave = waves + (upper_val - interpval)

        # Interpolate the columns at those ranges
        lower_thru = np.interp(lwave, waves, lower_thru)
        upper_thru = np.interp(uwave, waves, upper_thru)

    # Then interpolate between the two columns
    w = (interpval - lower_val) / (upper_val - lower_val)
    return (upper_thru * w) + lower_thru * (1.0 - w)


def _extrap_spec(interpval, lower_val, upper_val, lower_thru, upper_thru):
    """Extrapolate using two spectra to parameter at given value.
    Called by :func:`interpolate_spectral_element`.
    Also see :func:`_interp_spec`.

    """
    m = (upper_thru - lower_thru) / (upper_val - lower_val)
    b = lower_thru - m * lower_val
    return m * interpval + b


def interpolate_spectral_element(parfilename, interpval, ext=1, area=None):
    """Interpolate (or extrapolate) throughput spectra in given
    parameterized FITS table to given parameter value.

    FITS table is parsed with :func:`stsynphot.stio.read_interp_spec`.
    Parameterized values must be in ascending order in the
    table columns.

    If extrapolation is needed but not allowed, default throughput
    from ``THROUGHPUT`` column will be used.

    Parameters
    ----------
    parfilename : str
        Parameterized filename contains a suffix followed by
        a column name specificationin between square brackets.
        For example, ``path/acs_fr656n_006_syn.fits[fr656n#]``.

    interpval : float
        Desired parameter value.

    ext : int, optional
        FITS extension index of the data table.

    area : float or `astropy.units.quantity.Quantity`, optional
        Telescope collecting area.
        If not a Quantity, assumed to be in :math:`cm^{2}`.

    Returns
    -------
    sp : `synphot.spectrum.SpectralElement`
        Throughput spectrum at ``interpval``.

    Raises
    ------
    synphot.exceptions.ExtrapolationNotAllowed
        Extrapolation is not allowed by data table.

    synphot.exceptions.SynphotError
        No columns available for interpolation or extrapolation.

    """
    def_colname = 'THROUGHPUT'
    warnings = {}

    # Separate real filename and column name specification
    xre = _interpfilepatt.search(parfilename)
    filename = parfilename[0:xre.start()]
    col_prefix = xre.group('col').upper()

    # Read data table
    data, wave_unit, doshift, extrapolate = stio.read_interp_spec(
        filename, tab_ext=ext)
    wave0 = data['WAVELENGTH']

    # Determine the columns that bracket the desired value.
    # Grab all columns that begin with the parameter name (e.g. 'MJD#')
    # and then split off the numbers after the '#'.
    col_names = []
    col_pars = []
    for n in data.names:
        cn = n.upper()
        if cn.startswith(col_prefix):
            col_names.append(cn)
            col_pars.append(float(cn.split('#')[1]))

    if len(col_names) < 1:
        raise synexceptions.SynphotError(
            '{0} contains no interpolated columns.'.format(parfilename))

    # Assumes ascending order of parameter values in table.
    min_par = col_pars[0]
    max_par = col_pars[-1]

    # Exact match. No interpolation needed.
    if interpval in col_pars:
        thru = data[col_names[col_pars.index(interpval)]]

    # Need interpolation.
    elif (interpval > min_par) and (interpval < max_par):
        upper_ind = np.searchsorted(col_pars, interpval)
        lower_ind = upper_ind - 1

        thru = _interp_spec(
            interpval, wave0, col_pars[lower_ind], col_pars[upper_ind],
            data[col_names[lower_ind]], data[col_names[upper_ind]], doshift)

    # Need extrapolation, if allowed.
    elif extrapolate:
        # Extrapolate below lowest columns.
        if interpval < min_par:
            thru = _extrap_spec(interpval, min_par, col_pars[1],
                                data[col_names[0]], data[col_names[1]])

        # Extrapolate above highest columns.
        else:  # interpval > max_par
            thru = _extrap_spec(interpval, col_pars[-2], max_par,
                                data[col_names[-2]], data[col_names[-1]])

    # Extrapolation not allowed.
    else:
        # Use default, if available.
        if def_colname in data.names:
            s = 'Extrapolation not allowed, using default throughput for ' \
                '{0}.'.format(parfilename)
            log.warn(s)
            warnings['DefaultThroughput'] = True
            thru = data[def_colname]

        # Nothing can be done.
        else:
            raise synexceptions.ExtrapolationNotAllowed(
                'No default throughput for {0}.'.format(parfilename))

    # Make spectrum and update warnings
    sp = synspectrum.SpectralElement(
        u.Quantity(wave0, unit=wave_unit),
        u.Quantity(thru, unit=units.THROUGHPUT), area=area,
        header={'expr': '{0}#{1:g}'.format(filename, interpval)})
    sp.warnings.update(warnings)

    return sp


class ThermalSpectralElement(synspectrum.BaseUnitlessSpectrum):
    """Class to handle spectral element with associated thermal
    properties.

    This differs from `synphot.spectrum.SpectralElements` in the
    sense that it carries thermal parameters such as temperature
    and beam filling factor.

    .. note::

        This class does not know how to apply itself to an
        existing beam. Its emissivity should be handled explicitly
        outside the class. Also see
        :func:`stsynphot.observationmode.ThermalObservationMode.to_spectrum`.

    Wavelengths must be monotonic ascending/descending without zeroes
    or duplicate values.

    Values for the unitless component (hereafter, known as emissivity)
    must be dimensionless. They are checked for negative values.
    If found, warning is issued and negative values are set to zeroes.

    Parameters
    ----------
    wavelengths : array_like or `astropy.units.quantity.Quantity`
        Wavelength values. If not a Quantity, assumed to be in
        Angstrom.

    emissivity : array_like or `astropy.units.quantity.Quantity`
        Emissivity values. Must be dimensionless.
        If not a Quantity, assumed to be in THROUGHPUT.

    temperature : float or `astropy.units.quantity.Quantity`
        Temperature. If not a Quantity, assumed to be in Kelvin.

    beam_fill_factor : float
        Beam filling factor.

    kwargs : dict
        Keywords accepted by `synphot.spectrum.BaseSpectrum`,
        except ``flux_unit``.

    Attributes
    ----------
    wave, thru : `astropy.units.quantity.Quantity`
        Wavelength and emissivity of the spectrum.

    temperature : `astropy.units.quantity.Quantity`
        Temperature.

    beam_fill_factor : float
        Beam filling factor.

    primary_area : `astropy.units.quantity.Quantity` or `None`
        Area that flux covers in :math:`cm^{2}`.

    metadata : dict
        Metadata. ``self.metadata['expr']`` must contain a descriptive string of the object.

    warnings : dict
        List of warnings related to spectrum object.

    Raises
    ------
    synphot.exceptions.SynphotError
        If wavelengths and emissivity do not match, or if they have
        invalid units.

    synphot.exceptions.DuplicateWavelength
        If wavelength array contains duplicate entries.

    synphot.exceptions.UnsortedWavelength
        If wavelength array is not monotonic.

    synphot.exceptions.ZeroWavelength
        If negative or zero wavelength occurs in wavelength array.

    """
    def __init__(self, wavelengths, emissivity, temperature, beam_fill_factor,
                 **kwargs):
        super(ThermalSpectralElement, self).__init__(
            wavelengths, emissivity, **kwargs)
        self.temperature = units.validate_quantity(temperature, u.K)
        self.beam_fill_factor = float(beam_fill_factor)

    @classmethod
    def from_file(cls, filename, area=None, **kwargs):
        """Creates a thermal spectrum object from file.

        Only FITS is supported. Table extension header
        must have the following keywords:

            * ``DEFT`` - Temperature in Kelvin.
            * ``BEAMFILL`` - Beam filling factor.

        Parameters
        ----------
        filename : str
            Thermal spectrum filename.

        area : float or `astropy.units.quantity.Quantity`, optional
            Telescope collecting area.
            If not a Quantity, assumed to be in :math:`cm^{2}`.

        kwargs : dict
            Keywords acceptable by
            :func:`synphot.stio.read_fits_spec` (if FITS) or
            :func:`synphot.stio.read_ascii_spec` (if ASCII).

        Returns
        -------
        newspec : obj
            New thermal spectrum object.

        Raises
        ------
        synphot.exceptions.SynphotError
            Invalid file format.

        """
        from astropy.io import fits

        if not (filename.endswith('fits') or filename.endswith('fit')):
            raise synexceptions.SynphotError('Only FITS is supported.')

        # Extra info from table header
        ext = kwargs.get('ext', 1)
        tab_hdr = fits.getheader(filename, ext=ext)
        temperature = tab_hdr['DEFT']
        beam_fill_factor = tab_hdr['BEAMFILL']

        if 'flux_unit' not in kwargs:
            kwargs['flux_unit'] = units.THROUGHPUT

        if 'flux_col' not in kwargs:
            kwargs['flux_col'] = 'EMISSIVITY'

        header, wavelengths, fluxes = specstio.read_spec(filename, **kwargs)
        return cls(wavelengths, fluxes, temperature, beam_fill_factor,
                   area=area, header=header)


class ObservationSpectralElement(synspectrum.SpectralElement):
    """Class to handle spectral element from observation mode.

    This class has additional methods that are specific
    to observation mode and instrument-specific wavelength set.

    Wavelengths must be monotonic ascending/descending without zeroes
    or duplicate values.

    Throughput values must be dimensionless.
    They are checked for negative values and nonzero-bounds.
    If found, warning is issued. Negative values are set to zeroes.

    Parameters
    ----------
    wavelengths : array_like or `astropy.units.quantity.Quantity`
        Wavelength values. If not a Quantity, assumed to be in
        Angstrom.

    throughput : array_like or `astropy.units.quantity.Quantity`
        Throughput values. Must be dimensionless.
        If not a Quantity, assumed to be in THROUGHPUT.

    obsmode : `~stsynphot.observationmode.ObservationMode` or `None`, optional
        Observation mode object associated with this spectrum.
        If `None`, some methods will not work.

    kwargs : dict
        Keywords accepted by `synphot.spectrum.BaseSpectrum`,
        except ``flux_unit``.

    Attributes
    ----------
    wave, thru : `astropy.units.quantity.Quantity`
        Wavelength and throughput of the spectrum.

    obsmode : `~stsynphot.observationmode.ObservationMode` or `None`
        Observation mode object associated with this spectrum.

    binwave : `astropy.units.quantity.Quantity` or `None`
        Instrument-specific wavelength set from ``stsynphot.wavetable.WAVECAT``. This is derived from ``obsmode``.

    primary_area : `astropy.units.quantity.Quantity` or `None`
        Area that flux covers in :math:`cm^{2}`. This is derived from ``obsmode``, if defined.

    metadata : dict
        Metadata. ``self.metadata['expr']`` must contain a descriptive string of the object (derived from ``obsmode``, if defined).

    warnings : dict
        List of warnings related to spectrum object.

    Raises
    ------
    synphot.exceptions.SynphotError
        If wavelengths and throughput do not match, or if they have
        invalid units.

    synphot.exceptions.DuplicateWavelength
        If wavelength array contains duplicate entries.

    synphot.exceptions.UnsortedWavelength
        If wavelength array is not monotonic.

    synphot.exceptions.ZeroWavelength
        If negative or zero wavelength occurs in wavelength array.

    """
    def __init__(self, wavelengths, throughput, obsmode=None, **kwargs):
        super(ObservationSpectralElement, self).__init__(
            wavelengths, throughput, **kwargs)
        self.obsmode = obsmode

        # Check for zero bounds in throughput
        if self.thru[0] != 0 or self.thru[-1] != 0:
            log.warn('Throughput not bounded {0:g} and {1:g} when expecting '
                     'zeroes.'.format(self.thru[0], self.thru[-1]))

        # Observation mode attributes
        if obsmode is None:
            self.binwave = None
        else:
            self.binwave = obsmode.bandwave

            # Overwrite class defaults
            self.primary_area = obsmode.primary_area
            self.metadata['expr'] = str(obsmode)

    def _check_binwave(self):
        """All methods that use ``self.binwave`` should call this first."""
        if self.binwave is None:
            raise synexceptions.UndefinedBinset(
                'No binwave specified for this passband.')

    def __len__(self):
        """Get the number of components in ``self.obsmode``."""
        if self.obsmode is None:
            x = 0
        else:
            x = len(self.obsmode)
        return x

    def showfiles(self):
        """Display ``self.obsmode`` optical component filenames.
        Does nothing if ``self.obsmode`` is undefined.

        .. note:: Similar to IRAF SYNPHOT SHOWFILES.

        """
        if self.obsmode is not None:
            self.obsmode.showfiles()

    def thermback(self, thermtable=None):
        """Calculate thermal background count rate for
        ``self.obsmode``.

        Calculation uses
        :func:`stsynphot.observationmode.ObservationMode.thermal_spectrum`
        to extract thermal component source spectrum in
        PHOTLAM per square arcsec. Then this spectrum is
        integrated and multiplied by detector pixel scale
        and telescope collecting area to produce a count rate in
        :math:`count \\; s^{-1} \\; \\textnormal{pix}^{-1}`.
        This unit is non-standard but used widely by STScI
        Exposure Time Calculator.

        .. note::

            Similar to IRAF SYNPHOT THERMBACK.

        Parameters
        ----------
        thermtable : str or `None`
            Thermal component table filename. If `None`, uses
            ``stsynphot.config.THERMTABLE``.

        Returns
        -------
        bg : `astropy.units.quantity.Quantity`
            Thermal background count rate.

        Raises
        ------
        synphot.exceptions.SynphotError
            Calculation failed.

        """
        if self.obsmode is None:
            raise synexceptions.SynphotError(
                'Calculation not possible due to missing obsmode.')

        if self.obsmode.pixscale is None:
            raise synexceptions.SynphotError(
                'Undefined pixel scale for {0}.'.format(self.obsmode))

        sp = self.obsmode.thermal_spectrum(thermtable=thermtable)
        bg = sp.integrate() * self.obsmode.pixscale ** 2 * self.primary_area

        return u.Quantity(bg.value, u.count / u.s / u.pix)

    def wave_range(self, cenwave, npix, **kwargs):
        """Calculate the wavelength range covered by the given number
        of pixels centered on the given central wavelengths of
        ``self.binwave``.

        .. note::

            Similar to :func:`synphot.observation.Observation.wave_range`.

        Parameters
        ----------
        cenwave : float or `astropy.units.quantity.Quantity`
            Desired central wavelength. If not a Quantity,
            assumed to be in the unit of ``self.binwave``.

        npix : int
            Desired number of pixels, centered on ``cenwave``.

        kwargs : dict
            Keywords accepted by :func:`synphot.binning.wave_range`.

        Returns
        -------
        wave1, wave2 : `astropy.units.quantity.Quantity`
            Lower and upper limits of the wavelength range,
            in the unit of ``cenwave``.

        Raises
        ------
        synphot.exceptions.UndefinedBinset
            Missing ``self.binwave``.

        """
        self._check_binwave()

        if isinstance(cenwave, u.Quantity):
            bin_wave = units.validate_quantity(
                self.binwave, cenwave.unit, equivalencies=u.spectral())
        else:
            cenwave = u.Quantity(cenwave, unit=self.binwave.unit)
            bin_wave = self.binwave

        w1, w2 = binning.wave_range(
            bin_wave.value, cenwave.value, npix, **kwargs)
        wave1 = u.Quantity(w1, unit=cenwave.unit)
        wave2 = u.Quantity(w2, unit=cenwave.unit)

        return wave1, wave2

    def pixel_range(self, waverange, **kwargs):
        """Calculate the number of pixels within the given wavelength
        range and ``self.binwave``.

        .. note::

            Similar to :func:`synphot.observation.Observation.pixel_range`.

        Parameters
        ----------
        waverange : tuple of float or `astropy.units.quantity.Quantity`
            Lower and upper limits of the desired wavelength range.
            If not a Quantity, assumed to be in the same unit as
            ``self.binwave``.

        kwargs : dict
            Keywords accepted by :func:`synphot.binning.pixel_range`.

        Returns
        -------
        npix : number
            Number of pixels.

        Raises
        ------
        synphot.exceptions.UndefinedBinset
            Missing ``self.binwave``.

        """
        self._check_binwave()

        w1 = units.validate_quantity(
            waverange[0], self.binwave.unit, equivalencies=u.spectral())
        w2 = units.validate_quantity(
            waverange[-1], self.binwave.unit, equivalencies=u.spectral())

        return binning.pixel_range(
            self.binwave.value, (w1.value, w2.value), **kwargs)

    def to_fits(self, filename, **kwargs):
        """Write the spectrum to a FITS file.

        Throughput column is automatically named 'THROUGHPUT'.
        Graph and optical component tables are written to
        table header (not primary) under these keywords:

            * ``GRFTABLE``
            * ``CMPTABLE``

        Parameters
        ----------
        filename : str
            Output filename.

        kwargs : dict
            Keywords accepted by :func:`synphot.stio.write_fits_spec`.

        """
        kwargs['flux_col'] = 'THROUGHPUT'
        kwargs['flux_unit'] = units.THROUGHPUT

        # There are some standard keywords that should be added
        # to the extension header.
        bkeys = {'expr': (str(self), 'synphot expression'),
                 'tdisp1': 'G15.7',
                 'tdisp2': 'G15.7'}

        if self.obsmode is not None:
            bkeys.update(
                {'grftable': (self.obsmode.gtname, 'graph table used'),
                 'cmptable': (self.obsmode.ctname, 'component table used')})

        if 'ext_header' in kwargs:
            kwargs['ext_header'].update(bkeys)
        else:
            kwargs['ext_header'] = bkeys

        specstio.write_fits_spec(filename, self.wave, self.thru, **kwargs)

    @classmethod
    def from_obsmode(cls, obsmode, graphtable=None, comptable=None,
                     component_dict={}):
        """Create a passband spectrum from observation mode string.

        Parameters
        ----------
        obsmode : str
            Observation mode.

        graphtable : str or `None`
            Graph table filename. If `None`, uses
            ``stsynphot.config.GRAPHTABLE``.

        comptable : str or `None`
            Optical component table filename. If `None`, uses
            ``stsynphot.config.COMPTABLE``.

        component_dict : dict
            Maps component filename to corresponding
            `~stsynphot.observationmode.Component`.

        Returns
        -------
        newspec : obj
            New passband spectrum object.

        Raises
        ------
        synphot.exceptions.SynphotError
            Observation mode yields no throughput.

        """
        from .observationmode import ObservationMode  # To avoid circular import

        ob = ObservationMode(obsmode, graphtable=graphtable,
                             comptable=comptable, component_dict=component_dict)
        sp = ob.throughput()

        if sp is None:
            raise synexceptions.SynphotError(
                '{0} has no throughput.'.format(obsmode))

        return cls(sp.wave, sp.thru, obsmode=ob)


def band(input_str, **kwargs):
    """Convenience function to create passband spectrum
    with observation mode string.

    For more details, see :ref:`synphot-obsmode`.

    Parameters
    ----------
    input_str : str
        Observation mode.

    kwargs : dict
        Keywords accepted by
        :func:`ObservationSpectralElement.from_obsmode`.

    Returns
    -------
    sp : `ObservationSpectralElement`
        Passband spectrum.

    """
    return ObservationSpectralElement.from_obsmode(input_str, **kwargs)


def ebmvx(redlaw_name, ebv, area=None):
    """Convenience function to create extinction curve for
    given reddening law and :math:`E(B-V)`.

    Parameters
    ----------
    redlaw_name : {'lmc30dor', 'lmcavg', 'mwavg', 'mwdense', 'mwrv21', 'mwrv40', 'smcbar', 'xgalsb', 'gal3', `None`}
        Reddening law model name (see
        :func:`synphot.reddening.ReddeningLaw.from_model`). ``gal3`` and `None`
        are same as ``mwavg`` and used for testing only.

    ebv : float or `astropy.units.quantity.Quantity`
        :math:`E(B-V)` value in magnitude. See
        :func:`synphot.reddening.ExtinctionCurve.from_reddening_law`.

    area : float or `astropy.units.quantity.Quantity`, optional
        Telescope collecting area. If not Quantity, assumed to
        be in :math:`cm^{2}`.

    Returns
    -------
    sp : `synphot.reddening.ExtinctionCurve`
        Extinction curve.

    """
    global _REDLAWS

    if redlaw_name in ('gal3', None):
        m = 'mwavg'
        log.info('{0} uses {1} reddening law.'.format(redlaw_name, m))
    else:
        m = redlaw_name

    if m not in _REDLAWS:
        _REDLAWS[m] = reddening.ReddeningLaw.from_model(
            m, area=area, encoding='binary')

    return reddening.ExtinctionCurve.from_reddening_law(_REDLAWS[m], ebv)


def load_vega(vegafile=None, area=None, **kwargs):
    """Convenience function to load Vega spectrum that is
    used throughout `stsynphot`.

    Parameters
    ----------
    vegafile : str or `None`, optional
        Vega spectrum filename. If `None`, use software default.

    area : float or `astropy.units.quantity.Quantity`, optional
        Telescope collecting area. If not Quantity, assumed to
        be in :math:`cm^{2}`.

    kwargs : dict
        Keywords acceptable by :func:`synphot.stio.read_remote_spec`.

    Returns
    -------
    sp : `synphot.spectrum.SourceSpectrum` or `None`
        Vega spectrum. `None` if failed.

    """
    global Vega

    if vegafile is None:
        vegafile = synconfig.VEGA_FILE()

    with synconfig.VEGA_FILE.set_temp(vegafile):
        try:
            Vega = synspectrum.SourceSpectrum.from_vega(area=area, **kwargs)
        except Exception as e:
            Vega = None
            log.warn(
                'Failed to load Vega spectrum from {0}; Functionality '
                'involving Vega will be cripped: {1}'.format(vegafile, str(e)))


# Load default Vega
load_vega(area=config.PRIMARY_AREA(), encoding='binary')

# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""This module contains spectrum classes specific to STScI formats."""

# STDLIB
import os
import re
import warnings

# THIRD-PARTY
import numpy as np

# ASTROPY
from astropy import log
from astropy import units as u
from astropy.utils.exceptions import AstropyUserWarning

# SYNPHOT
from synphot import binning, reddening, units
from synphot import exceptions as synexceptions
from synphot.config import conf as synconf
from synphot.models import Empirical1D
from synphot.spectrum import SourceSpectrum, SpectralElement

# LOCAL
from . import stio
from .exceptions import PixscaleNotFoundError

__all__ = ['reset_cache', 'interpolate_spectral_element',
           'ObservationSpectralElement', 'band', 'ebmvx', 'load_vega', 'Vega']

_interpfilepatt = re.compile(r'\[(?P<col>.*?)\]')
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

    waves : array-like
        Wavelengths for all the parameterized spectra.

    lower_val, upper_val : float
        Low and high values of parameter to interpolate.

    lower_thru, upper_thru : array-like
        Throughput values are ``lower_val`` and ``upper_val``.

    doshift : bool
        Perform wavelength shift before interpolation.

    Returns
    -------
    thru : array-like
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


def interpolate_spectral_element(parfilename, interpval, ext=1):
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

    Returns
    -------
    sp : `synphot.spectrum.SpectralElement`
        Empirical bandpass at ``interpval``.

    Raises
    ------
    synphot.exceptions.ExtrapolationNotAllowed
        Extrapolation is not allowed by data table.

    synphot.exceptions.SynphotError
        No columns available for interpolation or extrapolation.

    """
    def_colname = 'THROUGHPUT'
    warndict = {}

    # Separate real filename and column name specification
    xre = _interpfilepatt.search(parfilename)
    if xre is None:
        raise synexceptions.SynphotError(
            f'{parfilename} must be in the format of "path/filename.fits'
            '[col#]"')
    filename = parfilename[0:xre.start()]
    col_prefix = xre.group('col').upper()

    # Read data table
    try:
        data, wave_unit, doshift, extrapolate = stio.read_interp_spec(
            filename, tab_ext=ext)
    except Exception as e:  # pragma: no cover
        raise IOError(f'Failed to read {filename}[{ext}]: {repr(e)}')
    wave_unit = units.validate_unit(wave_unit)
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
            f'{filename} contains no interpolated columns for {col_prefix}.')

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
            warnings.warn(
                'Extrapolation not allowed, using default throughput for '
                f'{parfilename}.', AstropyUserWarning)
            warndict['DefaultThroughput'] = True
            thru = data[def_colname]

        # Nothing can be done.
        else:
            raise synexceptions.ExtrapolationNotAllowed(
                f'No default throughput for {parfilename}.')

    meta = {'expr': f'{filename}#{interpval:g}',
            'warnings': warndict}
    return SpectralElement(
        Empirical1D, points=wave0 * wave_unit, lookup_table=thru, meta=meta)


class ObservationSpectralElement(SpectralElement):
    """Class to handle bandpass from observation mode.

    This class has additional methods that are specific
    to observation mode and instrument-specific wavelength set.

    .. note::

        For methods that take ``area``, it is *recommended* but
        not required to use `area`.

    Parameters
    ----------
    modelclass, kwargs
        See `~synphot.spectrum.BaseSpectrum`.

    obsmode : `~stsynphot.observationmode.ObservationMode`
        Observation mode for this bandpass.

    """
    def __init__(self, modelclass, obsmode=None, **kwargs):
        if obsmode is None:
            raise synexceptions.SynphotError('Missing OBSMODE.')

        super(ObservationSpectralElement, self).__init__(modelclass, **kwargs)
        self._obsmode = obsmode
        self.meta['expr'] = str(obsmode)

        # Check for zero bounds, if applicable
        try:
            self.bounded_by_zero()
        except synexceptions.SynphotError:  # pragma: no cover
            warnings.warn(
                'Zero-bound check not done due to undefined waveset.',
                AstropyUserWarning)

    @property
    def obsmode(self):
        """Observation mode for this bandpass."""
        return self._obsmode

    @property
    def binset(self):
        """Instrument-specific wavelength set from
        ``stsynphot.wavetable.WAVECAT`` based on `obsmode`."""
        return self.obsmode.bandwave

    @property
    def area(self):
        """Telescope collecting area based on `obsmode`."""
        return self.obsmode.primary_area

    def __len__(self):
        """Get the number of components in `obsmode`."""
        return len(self.obsmode)

    def taper(self, **kwargs):
        """Disabled."""
        raise NotImplementedError('Method disabled.')

    def bounded_by_zero(self, wavelengths=None, verbose=True):
        """Check if sampled throughout is bounded by zeroes.

        Parameters
        ----------
        wavelengths : array-like, `~astropy.units.quantity.Quantity`, or `None`
            Wavelength values for sampling.
            If not a Quantity, assumed to be in Angstrom.
            If `None`, ``self.waveset`` is used.

        verbose : bool
            Print warning if unbounded.

        Returns
        -------
        bounded : bool
            `True` if bounded by zeroes, `False` otherwise.

        """
        thru = self(wavelengths)
        y = thru[::thru.size - 1].value
        bounded = np.all(y == 0)

        if not bounded and verbose:
            warnings.warn(
                f'Unbounded throughput; {y} when expecting zeroes.',
                AstropyUserWarning)

        return bounded

    def showfiles(self):  # pragma: no cover
        """Display ``self.obsmode`` optical component filenames.

        .. note:: Similar to IRAF SYNPHOT SHOWFILES.

        """
        self.obsmode.showfiles()

    def thermback(self, area=None, thermtable=None):
        """Calculate thermal background count rate for
        ``self.obsmode``.

        Calculation uses
        :func:`~stsynphot.observationmode.ObservationMode.thermal_spectrum`
        to extract thermal component source spectrum in
        PHOTLAM per square arcsec. Then this spectrum is
        integrated and multiplied by detector pixel scale
        and telescope collecting area to produce a count rate
        in count/s/pix. This unit is non-standard but used widely
        by STScI Exposure Time Calculator.

        .. note::

            Similar to IRAF SYNPHOT THERMBACK.

        Parameters
        ----------
        area : float, `~astropy.units.quantity.Quantity`, or `None`
            Area that flux covers.
            If not a Quantity, assumed to be in :math:`cm^{2}`.
            If `None`, use `area`.

        thermtable : str or `None`
            Thermal component table filename.
            If `None`, uses ``stsynphot.config.conf.thermtable``.

        Returns
        -------
        bg : `~astropy.units.quantity.Quantity`
            Thermal background count rate.

        Raises
        ------
        stsynphot.exceptions.PixscaleNotFoundError
            Undefined pixel scale for the given observation mode.

        """
        if self.obsmode.pixscale is None:
            raise PixscaleNotFoundError(
                f'Undefined pixel scale for {self.obsmode}.')

        if area is None:
            area = self.area
        area = units.validate_quantity(area, units.AREA)

        sp = self.obsmode.thermal_spectrum(thermtable=thermtable)
        bg = sp.integrate() * self.obsmode.pixscale ** 2 * area

        return bg.value * (u.count / u.s / u.pix)

    def binned_waverange(self, cenwave, npix, **kwargs):
        """Calculate the wavelength range covered by the given number
        of pixels centered on the given central wavelengths of `binset`.

        Parameters
        ----------
        cenwave : float or `~astropy.units.quantity.Quantity`
            Desired central wavelength.
            If not a Quantity, assumed to be in Angstrom.

        npix : int
            Desired number of pixels, centered on ``cenwave``.

        kwargs : dict
            Keywords accepted by :func:`synphot.binning.wave_range`.

        Returns
        -------
        waverange : `~astropy.units.quantity.Quantity`
            Lower and upper limits of the wavelength range,
            in the unit of ``cenwave``.

        Raises
        ------
        synphot.exceptions.UndefinedBinset
            Undefined `binset`.

        """
        if self.binset is None:
            raise synexceptions.UndefinedBinset(
                'No binset specified for this passband.')

        # Calculation is done in the unit of cenwave.
        if not isinstance(cenwave, u.Quantity):
            cenwave = cenwave * self._internal_wave_unit

        bin_wave = units.validate_quantity(
            self.binset, cenwave.unit, equivalencies=u.spectral())

        return binning.wave_range(
            bin_wave.value, cenwave.value, npix, **kwargs) * cenwave.unit

    def binned_pixelrange(self, waverange, **kwargs):
        """Calculate the number of pixels within the given wavelength
        range and `binset`.

        Parameters
        ----------
        waverange : tuple of float or `~astropy.units.quantity.Quantity`
            Lower and upper limits of the desired wavelength range.
            If not a Quantity, assumed to be in Angstrom.

        kwargs : dict
            Keywords accepted by :func:`synphot.binning.pixel_range`.

        Returns
        -------
        npix : number
            Number of pixels.

        Raises
        ------
        synphot.exceptions.UndefinedBinset
            Undefined `binset`.

        """
        if self.binset is None:
            raise synexceptions.UndefinedBinset(
                'No binset specified for this passband.')

        x = units.validate_quantity(
            waverange, self._internal_wave_unit, equivalencies=u.spectral())

        return binning.pixel_range(self.binset.value, x.value, **kwargs)

    def to_fits(self, filename, wavelengths=None, **kwargs):
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

        wavelengths : array-like, `~astropy.units.quantity.Quantity`, or `None`
            Wavelength values for sampling.
            If not a Quantity, assumed to be in Angstrom.
            If `None`, ``self.waveset`` is used.

        kwargs : dict
            Keywords accepted by :func:`synphot.specio.write_fits_spec`.

        """
        bkeys = {
            'grftable': (os.path.basename(self.obsmode.gtname),
                         'graph table used'),
            'cmptable': (os.path.basename(self.obsmode.ctname),
                         'component table used')}

        if 'ext_header' in kwargs:
            kwargs['ext_header'].update(bkeys)
        else:
            kwargs['ext_header'] = bkeys

        super(ObservationSpectralElement, self).to_fits(
            filename, wavelengths=wavelengths, **kwargs)

    @classmethod
    def from_file(cls, filename, **kwargs):
        """Disabled."""
        raise NotImplementedError('Class method disabled.')

    @classmethod
    def from_filter(cls, filtername, **kwargs):
        """Disabled."""
        raise NotImplementedError('Class method disabled.')

    @classmethod
    def from_obsmode(cls, obsmode, graphtable=None, comptable=None,
                     component_dict={}):
        """Create a bandpass from observation mode string.

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

        component_dict : dict
            Maps component filename to corresponding
            `~stsynphot.observationmode.Component`.

        Returns
        -------
        bp : `ObservationSpectralElement`
            Empirical bandpass.

        Raises
        ------
        synphot.exceptions.SynphotError
            Observation mode yields no throughput.

        """
        from .observationmode import ObservationMode  # Avoid circular import

        ob = ObservationMode(
            obsmode, graphtable=graphtable, comptable=comptable,
            component_dict=component_dict)

        if not isinstance(ob.throughput, SpectralElement):  # pragma: no cover
            raise synexceptions.SynphotError(f'{obsmode} has no throughput.')

        return cls(ob.throughput, obsmode=ob)


def band(*args, **kwargs):
    """Convenience function to create a bandpass with
    an observation mode string.

    See :func:`ObservationSpectralElement.from_obsmode` and
    :ref:`stsynphot-obsmode`.

    """
    return ObservationSpectralElement.from_obsmode(*args, **kwargs)


def ebmvx(redlaw_name, ebv):
    """Convenience function to create extinction curve for
    given reddening law and :math:`E(B-V)`.

    Parameters
    ----------
    redlaw_name : str
        Reddening law model name
        (see :meth:`synphot.reddening.ReddeningLaw.from_extinction_model`).
        Choose from 'lmc30dor', 'lmcavg', 'mwavg', 'mwdense', 'mwrv21',
        'mwrv40', 'smcbar', 'xgalsb', 'gal3', or `None`.
        ``gal3`` and `None` are same as ``mwavg`` and used for testing only.

    ebv : float or `~astropy.units.quantity.Quantity`
        :math:`E(B-V)` value in magnitude. See
        :meth:`synphot.reddening.ReddeningLaw.extinction_curve`.

    Returns
    -------
    extcurve : `synphot.reddening.ExtinctionCurve`
        Extinction curve.

    """
    global _REDLAWS

    if redlaw_name in ('gal3', None):
        m = 'mwavg'
        log.info(f'{redlaw_name} uses {m} reddening law.')
    else:
        m = redlaw_name

    if m not in _REDLAWS:
        _REDLAWS[m] = reddening.ReddeningLaw.from_extinction_model(
            m, encoding='binary')

    return _REDLAWS[m].extinction_curve(ebv)


def load_vega(vegafile=None, **kwargs):
    """Convenience function to load Vega spectrum that is
    used throughout `stsynphot`.

    Parameters
    ----------
    vegafile : str or `None`, optional
        Vega spectrum filename.
        If `None`, use ``synphot.config.conf.vega_file``.

    kwargs : dict
        Keywords acceptable by :func:`synphot.specio.read_remote_spec`.

    Returns
    -------
    sp : `synphot.spectrum.SourceSpectrum` or `None`
        Vega spectrum. `None` if failed.

    """
    global Vega

    if vegafile is None:
        vegafile = synconf.vega_file

    with synconf.set_temp('vega_file', vegafile):
        try:
            Vega = SourceSpectrum.from_vega(**kwargs)
        except Exception as e:
            Vega = None
            warnings.warn(
                f'Failed to load Vega spectrum from {vegafile}; Functionality '
                f'involving Vega will be cripped: {repr(e)}',
                AstropyUserWarning)


# Load default Vega
load_vega(encoding='binary')

# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""This module handles :ref:`catalog spectra <stsynphot_catalog>`."""
from __future__ import absolute_import, division, print_function, unicode_literals

# STDLIB
import os

# THIRD-PARTY
import numpy as np

# ASTROPY
from astropy import units as u
from astropy.extern import six

# SYNPHOT
from synphot import exceptions as synexceptions
from synphot import SourceSpectrum, units

# LOCAL
from . import config, exceptions, stio


__all__ = ['reset_cache', 'grid_to_spec']

_CAT_TEMPLATE = os.path.join(config.ROOTDIR(), 'grid', '*', 'catalog.fits')
_KUR_TEMPLATE = os.path.join(config.ROOTDIR(), 'grid', '*')
_PARAM_NAMES = ['T_eff', 'metallicity', 'log_g']
_CACHE = {}  # Stores grid look-up parameters to reduce file I/O.


def reset_cache():
    """Empty the catalog grid cache."""
    global _CACHE
    _CACHE.clear()


def _par_from_parser(x):
    """Convert parser string to parameter value."""
    if isinstance(x, six.string_types):
        y = float(x)
    else:
        y = x
    return y


def _validate_par(x, par_name=''):
    """Make sure parameter value is a number."""
    if not isinstance(x, (int, long, float)):
        raise synexceptions.SynphotError(
            '{0} {1} is not a number.'.format(par_name, x))


def _break_list(in_list, index, parameter):
    """Break input list into upper and lower lists."""
    array = np.array([parameters[index] for parameters in in_list],
                     dtype=np.float64)
    upper_array = array[array >= parameter]
    lower_array = array[array <= parameter]

    if upper_array.size == 0:
        raise exceptions.ParameterOutOfBounds(
            "Parameter '{0}' exceeds data. Max allowed={1}, "
            "entered={2}.".format(_PARAM_NAMES[index], array.max(), parameter))
    if lower_array.size == 0:
        raise exceptions.ParameterOutOfBounds(
            "Parameter '{0}' exceeds data. Min allowed={1}, "
            "entered={2}.".format(_PARAM_NAMES[index], array.min(), parameter))

    upper = upper_array.min()
    lower = lower_array.max()
    upper_list = []
    lower_list = []

    for i, parameters in enumerate(in_list):
        if array[i] >= parameter and array[i] <= upper:
            upper_list.append(parameters)
        if array[i] >= lower and array[i] <= parameter:
            lower_list.append(parameters)

    return upper_list, lower_list


def _get_spectrum(parlist, basename):
    """Get list of spectra for given parameter list and base name."""
    name = parlist[3]

    filename = name.split('[')[0]
    column = name.split('[')[1][:-1]

    filename = _KUR_TEMPLATE.replace('*', os.path.join(basename, filename))
    sp = SourceSpectrum.from_file(filename, flux_col=column)

    result = [member for member in parlist]
    result.pop()
    result.append(sp)

    return result


def _interpolate_spectrum(sp1, sp2, par):
    """Interpolate spectra to the given parameter value."""
    spectrum1 = sp1.pop()
    spectrum2 = sp2.pop()
    par1 = sp1.pop()
    par2 = sp2.pop()

    if par1 == par2:
        sp = spectrum1
    else:
        a = (par1 - par) / (par1 - par2)
        b = 1.0 - a
        sp = a * spectrum2 + b * spectrum1

    result = [member for member in sp1]
    result.append(sp)

    return result


def grid_to_spec(catdir, t_eff, metallicity, log_g, area=None):
    """Extract spectrum from given catalog grid parameters.
    Interpolate if necessary.

    Grid must be defined by ``catdir/catalog.fits``, which
    is parsed with :func:`stsynphot.stio.read_catalog`.

    Grid parameters are only read once and then cached.
    Until the cache is cleared explicitly using
    :func:`reset_cache`, cached values are used.

    Parameters
    ----------
    catdir : {'ck04models', 'k93models', 'phoenix'}
        Name of directory holding the catalogs, relative
        to ``stsynphot.config.CATDIR``.

            * ``ck04models`` - Castelli & Kurucz (2004)
            * ``k93models`` - Kurucz (1993)
            * ``phoenix`` - Allard et al. (2009)

    t_eff : str, float or `astropy.units.quantity.Quantity`
        Effective temperature of model. If not Quantity,
        assumed to be in Kelvin. If string (from parser),
        convert to Quantity.

    metallicity : str, float
        Metallicity of model. Quantity not supported for now.
        If string (from parser), convert to float.

    log_g : str, float
        Log surface gravity for model. Quantity not supported for now.
        If string (from parser), convert to float.

    area : float or `astropy.units.quantity.Quantity`, optional
        Area that fluxes cover. Usually, this is the area of
        the primary mirror of the observatory of interest.
        If not a Quantity, assumed to be in cm^2.

    Returns
    -------
    sp : `synphot.spectrum.SourceSpectrum`
        Extracted spectrum.

    Raises
    ------
    stsynphot.exceptions.ParameterOutOfBounds
        Grid parameter out of bounds.

    synphot.exceptions.SynphotError
        Invalid inputs.

    """
    if catdir not in ('ck04models', 'k93models', 'phoenix'):
        raise synexceptions.SynphotError(
            '{0} is not a supported catalog grid.'.format(catdir))

    # Temperature must be in Kelvin
    t_eff = _par_from_parser(t_eff)
    t_eff = units.validate_quantity(t_eff, u.K)
    _validate_par(t_eff.value, par_name='T_eff')

    # Metallicity (Quantity not supported yet)
    metallicity = _par_from_parser(metallicity)
    _validate_par(metallicity, par_name='Metallicity')

    # Log gravity (Quantity not supported yet)
    log_g = _par_from_parser(log_g)
    _validate_par(log_g, par_name='Log g')

    filename = _CAT_TEMPLATE.replace('*', catdir)

    # If not cached, read from grid catalog and cache it
    if filename not in _CACHE:
        data = stio.read_catalog(filename)  # Ext 1
        _CACHE[filename] = [[float(x) for x in index.split(',')] +
                            [data['FILENAME'][i]]
                            for i, index in enumerate(data['INDEX'])]

    indices = _CACHE[filename]

    list0, list1 = _break_list(indices, 0, t_eff.value)

    list2, list3 = _break_list(list0, 1, metallicity)
    list4, list5 = _break_list(list1, 1, metallicity)

    list6, list7 = _break_list(list2, 2, log_g)
    list8, list9 = _break_list(list3, 2, log_g)
    list10, list11 = _break_list(list4, 2, log_g)
    list12, list13 = _break_list(list5, 2, log_g)

    sp1 = _get_spectrum(list6[0], catdir)
    sp2 = _get_spectrum(list7[0], catdir)
    sp3 = _get_spectrum(list8[0], catdir)
    sp4 = _get_spectrum(list9[0], catdir)
    sp5 = _get_spectrum(list10[0], catdir)
    sp6 = _get_spectrum(list11[0], catdir)
    sp7 = _get_spectrum(list12[0], catdir)
    sp8 = _get_spectrum(list13[0], catdir)

    spa1 = _interpolate_spectrum(sp1, sp2, log_g)
    spa2 = _interpolate_spectrum(sp3, sp4, log_g)
    spa3 = _interpolate_spectrum(sp5, sp6, log_g)
    spa4 = _interpolate_spectrum(sp7, sp8, log_g)

    spa5 = _interpolate_spectrum(spa1, spa2, metallicity)
    spa6 = _interpolate_spectrum(spa3, spa4, metallicity)

    spa7 = _interpolate_spectrum(spa5, spa6, t_eff.value)
    sp = spa7[0]

    header = {'expr': '{0}(T_eff={1:g},Z={2:g},log_g={3:g})'.format(
        catdir, t_eff.value, metallicity, log_g)}

    return SourceSpectrum(sp.wave, sp.flux, area=area, header=header)

# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""This module handles :ref:`catalog spectra <stsynphot-spec-atlas>`."""

# STDLIB
import numbers

# THIRD-PARTY
import numpy as np

# ASTROPY
from astropy import units as u
from astropy.io import fits

# SYNPHOT
from synphot import exceptions as synexceptions
from synphot import units
from synphot.spectrum import SourceSpectrum
from synphot.utils import validate_totalflux

# LOCAL
from . import exceptions, stio

__all__ = ['reset_cache', 'get_catalog_index', 'grid_to_spec',
           'find_valid_g_phoenix', 'plot_phoenix']

_PARAM_NAMES = ['T_eff', 'metallicity', 'log_g']
_CACHE = {}  # Stores grid look-up parameters to reduce file I/O.


def reset_cache():
    """Empty the catalog grid cache."""
    global _CACHE
    _CACHE.clear()


def _par_from_parser(x):
    """Convert parser string to parameter value."""
    if not isinstance(x, (numbers.Real, u.Quantity)):
        x = float(x)
    return x


def _break_list(in_list, index, parameter):
    """Break input list into upper and lower lists."""
    array = np.array([parameters[index] for parameters in in_list],
                     dtype=np.float64)
    upper_array = array[array >= parameter]
    lower_array = array[array <= parameter]

    if upper_array.size == 0:
        raise exceptions.ParameterOutOfBounds(
            f"Parameter '{_PARAM_NAMES[index]}' exceeds data. "
            f"Max allowed={array.max()}, entered={parameter}.")
    if lower_array.size == 0:
        raise exceptions.ParameterOutOfBounds(
            f"Parameter '{_PARAM_NAMES[index]}' exceeds data. "
            f"Min allowed={array.min()}, entered={parameter}.")

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


def _get_spectrum(parlist, catdir):
    """Get list of spectra for given parameter list and base name."""
    name = parlist[3]

    filename = name.split('[')[0]
    column = name.split('[')[1][:-1]

    filename = stio.resolve_filename(catdir, *filename.split('/'))
    sp = SourceSpectrum.from_file(filename, flux_col=column)

    totflux = sp.integrate()
    try:
        validate_totalflux(totflux)
    except synexceptions.SynphotError:
        raise exceptions.ParameterOutOfBounds(
            f"Parameter '{parlist}' has no valid data.")

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


def get_catalog_index(gridname):
    """Extract catalog index (grid parameters).

    It is read once and then cached until the cache is cleared explicitly using
    :func:`reset_cache`.

    Parameters
    ----------
    gridname : str
        See :func:`grid_to_spec`.

    Returns
    -------
    cat_index : list
        List of ``[t_eff, metallicity, log_g, filename]``.

    catdir : str
        Directory containing the requested catalog.

    """
    if gridname == 'ck04models':
        catdir = 'crgridck04$'
    elif gridname == 'k93models':
        catdir = 'crgridk93$'
    elif gridname == 'phoenix':
        catdir = 'crgridphoenix$'
    else:
        raise synexceptions.SynphotError(
            f'{gridname} is not a supported catalog grid.')

    catdir = stio.irafconvert(catdir)
    filename = stio.resolve_filename(catdir, 'catalog.fits')

    # If not cached, read from grid catalog and cache it
    if filename not in _CACHE:
        data = stio.read_catalog(filename)  # EXT 1
        _CACHE[filename] = [list(map(float, index.split(','))) +
                            [data['FILENAME'][i]]
                            for i, index in enumerate(data['INDEX'])]

    return _CACHE[filename], catdir


def grid_to_spec(gridname, t_eff, metallicity, log_g):
    """Extract spectrum from given catalog grid parameters.
    Interpolate if necessary.

    Grid parameters are read with :func:`get_catalog_index`.

    Parameters
    ----------
    gridname : {'ck04models', 'k93models', 'phoenix'}
        Model to use:
            * ``ck04models`` - Castelli & Kurucz (2004)
            * ``k93models`` - Kurucz (1993)
            * ``phoenix`` - Allard et al. (2009)

    t_eff : str, float or `astropy.units.quantity.Quantity`
        Effective temperature of model.
        If not Quantity, assumed to be in Kelvin.
        If string (from parser), convert to Quantity.

    metallicity : str or float
        Metallicity of model.
        If string (from parser), convert to float.

    log_g : str or float
        Log surface gravity for model.
        If string (from parser), convert to float.

    Returns
    -------
    sp : `synphot.spectrum.SourceSpectrum`
        Empirical source spectrum.

    Raises
    ------
    stsynphot.exceptions.ParameterOutOfBounds
        Grid parameter out of bounds.

    synphot.exceptions.SynphotError
        Invalid inputs.

    """
    indices, catdir = get_catalog_index(gridname)

    metallicity = _par_from_parser(metallicity)
    if isinstance(metallicity, u.Quantity):
        raise synexceptions.SynphotError(
            'Quantity is not supported for metallicity.')

    log_g = _par_from_parser(log_g)
    if isinstance(log_g, u.Quantity):
        raise synexceptions.SynphotError(
            'Quantity is not supported for log surface gravity.')

    t_eff = units.validate_quantity(_par_from_parser(t_eff), u.K).value

    list0, list1 = _break_list(indices, 0, t_eff)

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

    spa7 = _interpolate_spectrum(spa5, spa6, t_eff)

    sp = spa7[0]
    sp.meta['expr'] = (f'{gridname}(T_eff={t_eff:g},'
                       f'metallicity={metallicity:g},log_g={log_g:g})')

    return sp


# NOTE: The following functions need refactoring if you want to generalize
# them to work on all the supported catalogs. This is because the catalogs
# do not share the same header structure. Generalization requires reading all
# the spectra tables, not just header, which will have a significant
# performance impact.
# Also see https://github.com/spacetelescope/stsynphot_refactor/issues/45

def find_valid_g_phoenix():  # pragma: no cover
    """Find valid ``log_g`` values in the Phoenix catalog.

    .. note::

        Takes time to run because it has to find the gaps by
        parsing the headers of individual data files in the catalog.

    Returns
    -------
    valid_g : dict
        Dictionary mapping ``(t_eff, metallicity)`` to a list of valid
        ``log_g`` values.

    uniq_metallicity : list
        Unique metallicity values in the catalog.

    """
    indices, catdir = get_catalog_index('phoenix')
    specfiles = {}
    valid_g = {}
    possible_g = set()
    uniq_metallicity = set()

    for a in indices:
        key = tuple(a[:2])
        uniq_metallicity.add(a[1])
        possible_g.add(a[2])

        if key not in specfiles:
            specfiles[key] = a[3].split('[')[0]

    for key, spfile in specfiles.items():
        hdr = fits.getheader(stio.resolve_filename(
            catdir, *spfile.split('/')))['LOGG*']
        valid_g[key] = []
        for val in hdr.values():
            gval = float(val)
            if gval in possible_g:
                valid_g[key].append(gval)

    return valid_g, sorted(uniq_metallicity)


def plot_phoenix(filename=''):  # pragma: no cover
    """Visualize the Phoenix catalog index (grid parameters).

    .. note:: Uses ``matplotlib``.

    .. note::

        Takes time to run because it has to find the gaps by
        parsing the headers of individual data files in the catalog.

    Parameters
    ----------
    filename : str
        If provided, plot is saved to given filename.

    """
    import matplotlib.pyplot as plt

    valid_g, uniq_metallicity = find_valid_g_phoenix()
    n_plots = len(uniq_metallicity)
    ax_map = {}

    fig, axes = plt.subplots(nrows=3, ncols=4)
    axes = axes.flatten()
    n_axes = axes.size

    if n_plots > n_axes:
        raise ValueError(f'Need {n_plots} but only {n_axes} subplots created')

    for i, metallicity in enumerate(uniq_metallicity):
        ax_map[metallicity] = axes[i]

    for i in range(n_plots, n_axes):
        axes[i].remove()

    for key, log_g in valid_g.items():
        metallicity = key[1]
        t_eff = [key[0]] * len(log_g)
        ax = ax_map[metallicity]
        ax.plot(t_eff, log_g, 'b,')
        ax.set_xlabel(r'$T_{\mathrm{eff}}$')
        ax.set_ylabel(r'$\log g$')
        ax.set_title(f'[M/H] = {metallicity:.2f}')
        ax.axvline(0, ls='--', lw=0.5, c='k')

    plt.tight_layout()
    plt.draw()

    if filename:
        fig.savefig(filename)

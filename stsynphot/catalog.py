# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""This module handles :ref:`catalog spectra <stsynphot-spec-atlas>`."""

# STDLIB
import copy
import numbers
from urllib.error import HTTPError

# THIRD-PARTY
import numpy as np
import synphot
from astropy import units as u
from astropy.io import fits
from astropy.utils import minversion
from synphot import exceptions as synexceptions
from synphot import units
from synphot.spectrum import SourceSpectrum
from synphot.utils import validate_totalflux

# LOCAL
from stsynphot import exceptions, stio

__all__ = [
    "find_valid_g_phoenix",
    "get_catalog_index",
    "grid_to_spec",
    "plot_phoenix",
    "reset_cache",
]

_CACHE = {}  # Stores grid look-up parameters to reduce file I/O.
_SPECTRUM_CACHE = {}  # Stores grid spectra (by file and column) to reduce file I/O.

SYNPHOT_LT_1_9 = not minversion(synphot, "1.9.0")
if SYNPHOT_LT_1_9:
    _prihdr_kw = {}
else:
    _prihdr_kw = {"primary_header": False}  # Omit header for performance


def reset_cache():
    """Empty the catalog grid cache, including cached grid spectra.

    Catalog indices and grid spectra are read once and kept for the rest of
    the session. Call this after grid files are changed on disk, so that
    they are read again.
    """
    global _CACHE, _SPECTRUM_CACHE  # noqa: PLW0602
    _CACHE.clear()
    _SPECTRUM_CACHE.clear()


def _par_from_parser(x):
    """Convert parser string to parameter value."""
    if not isinstance(x, (numbers.Real, u.Quantity)):
        x = float(x)
    return x


def _break_list(cachekey, parkey, parameter):
    """Find closest grid neighbors for given parameter name."""

    array = _CACHE[cachekey][parkey]
    diff = array - parameter
    lower_array = array[diff <= 0]
    upper_array = array[diff >= 0]

    if upper_array.size == 0:
        raise exceptions.ParameterOutOfBounds(
            f"Parameter '{parkey}' exceeds data. Max allowed={array.max()}, entered={parameter}."
        )
    if lower_array.size == 0:
        raise exceptions.ParameterOutOfBounds(
            f"Parameter '{parkey}' exceeds data. Min allowed={array.min()}, entered={parameter}."
        )

    lower = max(lower_array)
    upper = min(upper_array)

    return upper, lower


def _get_spectrum(t_eff, metallicity, log_g, cachekey, catdir, cache_only=False):
    """Get list of spectra for given parameter list and base name."""
    key = (cachekey, t_eff, metallicity, log_g)

    # Interpolating one spectrum reads up to 8 grid spectra, and neighbouring
    # parameters (e.g., stars along an isochrone) share most of them, so keep each
    # validated spectrum after its first read. None marks one without valid data.
    # On a grid point, grid_to_spec returns this spectrum itself.
    if key not in _SPECTRUM_CACHE:
        if cache_only:
            raise KeyError(f"{key} is not cached, try again with cache_only=False")

        cat_cache = _CACHE[cachekey]
        name = cat_cache["files"][
            (cat_cache["t_eff"] == t_eff) & (cat_cache["metallicity"] == metallicity) & (cat_cache["log_g"] == log_g)
        ]
        if name.size == 0:
            sp = None
        else:
            name = name[0]  # There can be only one
            filename = name.split("[")[0]
            column = name.split("[")[1][:-1]

            filename = stio.resolve_filename(catdir, *filename.split("/"))

            sp = SourceSpectrum.from_file(filename, flux_col=column, **_prihdr_kw)
            try:
                validate_totalflux(sp.integrate())
            except synexceptions.SynphotError:
                sp = None
        _SPECTRUM_CACHE[key] = sp

    if _SPECTRUM_CACHE[key] is None:
        raise exceptions.ParameterOutOfBounds(f"'{key}' has no valid data.")

    return _SPECTRUM_CACHE[key]


def _interpolate_spectrum(par1, spectrum1, par2, spectrum2, par):
    """Interpolate spectra to the given parameter value.
    These values should already be validated prior.
    """

    if np.allclose(par, par1) or np.allclose(par1, par2):
        return spectrum1

    if np.allclose(par, par2):  # pragma: no cover
        return spectrum2

    a = (par1 - par) / (par1 - par2)
    b = 1.0 - a
    sp = a * spectrum2 + b * spectrum1

    return sp


def get_catalog_index(gridname):
    """Extract catalog index (grid parameters).

    It is read once and then cached until the cache is cleared explicitly using
    :func:`reset_cache`.
    The cache is a dictionary mapping parameter name to its arrays.

    Parameters
    ----------
    gridname : str
        See :func:`grid_to_spec` for supported grids.
        Any other input is assumed to be custom grid stored
        in ``crgrid$`` as expected by :func:`~stsynphot.stio.irafconvert`.

    Returns
    -------
    cache_key : str
        Key of internal cache.

        .. version-changed:: 1.8.0
            The internal cache organization was changed and this is
            reflected directly in return value. Previously, this was
            a list of ``[t_eff, metallicity, log_g, filename]``.

    catdir : str
        Directory containing the requested catalog.

    """
    if gridname == "ck04models":
        catdir = "crgridck04$"
    elif gridname == "k93models":
        catdir = "crgridk93$"
    elif gridname == "phoenix":
        catdir = "crgridphoenix$"
    else:
        catdir = f"crgrid${gridname}"

    catdir = stio.irafconvert(catdir)
    filename = stio.resolve_filename(catdir, "catalog.fits")

    # If not cached, read from grid catalog and cache it
    if filename not in _CACHE:
        try:
            data = stio.read_catalog(filename)  # EXT 1
        except (FileNotFoundError, HTTPError) as e:
            raise synexceptions.SynphotError(f"{gridname} catalog was not found: {e}") from e

        array = np.array([row.split(",") for row in data["INDEX"]], dtype=float)
        _CACHE[filename] = {
            "t_eff": array[:, 0],
            "metallicity": array[:, 1],
            "log_g": array[:, 2],
            "files": data["FILENAME"],
        }

    return filename, catdir


def grid_to_spec(gridname, t_eff, metallicity, log_g):
    """Extract spectrum from given catalog grid parameters.
    Interpolate if necessary.

    Grid parameters are read with :func:`get_catalog_index`.

    The grid spectra are cached: each is read from file and validated the
    first time it is needed, then kept for the rest of the session. Changes
    to the grid files on disk are not seen until :func:`reset_cache` is
    called.

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
    metallicity = _par_from_parser(metallicity)
    if isinstance(metallicity, u.Quantity):
        raise synexceptions.SynphotError("Quantity is not supported for metallicity.")

    log_g = _par_from_parser(log_g)
    if isinstance(log_g, u.Quantity):
        raise synexceptions.SynphotError("Quantity is not supported for log surface gravity.")

    t_eff = units.validate_quantity(_par_from_parser(t_eff), u.K).value

    cachekey, catdir = get_catalog_index(gridname)

    upper_t, lower_t = _break_list(cachekey, "t_eff", t_eff)
    upper_m, lower_m = _break_list(cachekey, "metallicity", metallicity)
    upper_g, lower_g = _break_list(cachekey, "log_g", log_g)

    sp1 = _get_spectrum(upper_t, upper_m, upper_g, cachekey, catdir)
    sp2 = _get_spectrum(upper_t, upper_m, lower_g, cachekey, catdir)
    sp3 = _get_spectrum(upper_t, lower_m, upper_g, cachekey, catdir)
    sp4 = _get_spectrum(upper_t, lower_m, lower_g, cachekey, catdir)
    sp5 = _get_spectrum(lower_t, upper_m, upper_g, cachekey, catdir)
    sp6 = _get_spectrum(lower_t, upper_m, lower_g, cachekey, catdir)
    sp7 = _get_spectrum(lower_t, lower_m, upper_g, cachekey, catdir)
    sp8 = _get_spectrum(lower_t, lower_m, lower_g, cachekey, catdir)

    # upper_t, upper_m, log_g
    spa1 = _interpolate_spectrum(upper_g, sp1, lower_g, sp2, log_g)

    # upper_t, lower_m, log_g
    spa2 = _interpolate_spectrum(upper_g, sp3, lower_g, sp4, log_g)

    # lower_t, upper_m, log_g
    spa3 = _interpolate_spectrum(upper_g, sp5, lower_g, sp6, log_g)

    # lower_t, lower_m, log_g
    spa4 = _interpolate_spectrum(upper_g, sp7, lower_g, sp8, log_g)

    # upper_t, metallicity, log_g
    spa5 = _interpolate_spectrum(upper_m, spa1, lower_m, spa2, metallicity)

    # lower_t, metallicity, log_g
    spa6 = _interpolate_spectrum(upper_m, spa3, lower_m, spa4, metallicity)

    # t_eff, metallicity, log_g
    spa7 = _interpolate_spectrum(upper_t, spa5, lower_t, spa6, t_eff)

    # Copy to avoid accidentally changing cache.
    sp = copy.deepcopy(spa7)
    sp.meta["expr"] = f"{gridname}(T_eff={t_eff:g},metallicity={metallicity:g},log_g={log_g:g})"

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
    cachekey, catdir = get_catalog_index("phoenix")
    a = _CACHE[cachekey]
    specfiles = {}
    valid_g = {}
    possible_g = set(a["log_g"])
    uniq_metallicity = sorted(set(a["metallicity"]))

    for t, m, f in zip(a["t_eff"], a["metallicity"], a["files"]):
        key = (t, m)
        if key not in specfiles:
            specfiles[key] = f.split("[")[0]

    for key, spfile in specfiles.items():
        hdr = fits.getheader(stio.resolve_filename(catdir, *spfile.split("/")))["LOGG*"]
        valid_g[key] = []
        for val in hdr.values():
            gval = float(val)
            if gval in possible_g:
                valid_g[key].append(gval)

    return valid_g, uniq_metallicity


def plot_phoenix(filename=""):  # pragma: no cover
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
        raise ValueError(f"Need {n_plots} but only {n_axes} subplots created")

    for i, metallicity in enumerate(uniq_metallicity):
        ax_map[metallicity] = axes[i]

    for i in range(n_plots, n_axes):
        axes[i].remove()

    for key, log_g in valid_g.items():
        metallicity = key[1]
        t_eff = [key[0]] * len(log_g)
        ax = ax_map[metallicity]
        ax.plot(t_eff, log_g, "b,")
        ax.set_xlabel(r"$T_{\mathrm{eff}}$")
        ax.set_ylabel(r"$\log g$")
        ax.set_title(f"[M/H] = {metallicity:.2f}")
        ax.axvline(0, ls="--", lw=0.5, c="k")

    plt.tight_layout()
    plt.draw()

    if filename:
        fig.savefig(filename)

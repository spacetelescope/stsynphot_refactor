# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""This module handles ``stsynphot``-specific I/O for:

* FITS - See `astropy.io.fits`
* Basic ASCII - See `astropy.io.ascii`

"""
# STDLIB
import fnmatch
import re
import os
import sys
import warnings
from pathlib import Path

# THIRD-PARTY
import numpy as np

# ASTROPY
from astropy import units as u
from astropy.io import ascii, fits
from astropy.utils.data import _find_pkg_data_path
from astropy.utils.exceptions import AstropyUserWarning

# SYNPHOT
from synphot import exceptions as synexceptions
from synphot import units

__all__ = ['resolve_filename', 'irafconvert', 'get_latest_file',
           'read_graphtable', 'read_comptable', 'read_catalog', 'read_wavecat',
           'read_waveset', 'read_detector_pars', 'read_interp_spec']

_irafconvpat = re.compile(r'\$(\w*)')
_irafconvdata = None


def resolve_filename(path, *args):
    """Resolve filename that could be URL or local file.

    Parameters
    ----------
    path : str
        Root directory or URL.

    args : tuple of str
        Any sub-path(s) and the actual filename.

    Returns
    -------
    reg_filename : str
        Resolved filename.

    """
    path_lc = path.lower()
    if path_lc.startswith(('ftp', 'http')):
        sep = '/'
        fname = sep.join(args)
        if path_lc.endswith(sep):
            reg_filename = path + fname
        else:
            reg_filename = path + sep + fname

        # Catch-all to ensure result is OS-independent.
        if sys.platform.startswith('win'):
            reg_filename = reg_filename.replace('\\', sep)
    else:
        reg_filename = str(Path(path) / os.sep.join(args))

    return reg_filename


def _iraf_decode(irafdir):
    """Decode IRAF dir shortcut."""
    from .config import conf  # Put here to avoid circular import error
    global _irafconvdata

    irafdir = irafdir.lower()

    if irafdir == 'synphot':  # Local data
        path = _find_pkg_data_path('data')
    elif irafdir == 'crrefer':  # Root dir
        path = conf.rootdir
    else:  # Read from file
        # Avoid repeated I/O but do not load if not used
        if _irafconvdata is None:
            _irafconvdata = ascii.read(irafconvert(conf.irafshortcutfile))

        mask = _irafconvdata['IRAFNAME'] == irafdir
        if not np.any(mask):
            raise KeyError(f'IRAF shortcut {irafdir} not found in '
                           f'{conf.irafshortcutfile}.')
        relpath = os.path.normpath(_irafconvdata['RELPATH'][mask][0])
        path = os.path.join(conf.rootdir, relpath)

    return path


def irafconvert(iraf_filename, sep='$'):
    """Convert IRAF filename to regular filename.

    Acceptable IRAF formats:

    * ``$path/file`` - ``path`` assumed to be environment variable.
    * ``path$file`` - ``path`` is special IRAF shortcut for CDBS
      data directory (case-insensitive).

    Notes on special IRAF shortcut:

    * ``synphot`` points to software data directory.
    * ``crrefer`` points to ``stsynphot.config.conf.rootdir``.
    * Otherwise, decoded based on
      ``stsynphot.config.conf.irafshortcutfile``
      that must contain the following named columns:

        #. ``IRAFNAME`` - The shortcut for look-up. If multiple matches
           are found, the first match is used.
        #. ``RELPATH`` - Path relative to
           ``stsynphot.config.conf.rootdir``.

    If separator is not found, input is returned as-is.

    Parameters
    ----------
    iraf_filename : str
        IRAF filename.

    sep : char, optional
        Path-file separator.

    Returns
    -------
    reg_filename : str
        Regular filename.

    Raises
    ------
    KeyError
        Environment variable or IRAF shortcut is undefined.

    TypeError
        Input is not a string.

    """
    if not isinstance(iraf_filename, str):
        raise TypeError(f'{iraf_filename} is not a string.')

    # Nothing needs to be done
    if sep not in iraf_filename:
        return iraf_filename

    # Remove duplicate separators and extraneous relative paths.
    iraf_filename = os.path.normpath(iraf_filename)

    # $var/file
    if iraf_filename.startswith(sep):
        match = _irafconvpat.match(iraf_filename)
        path = os.environ[match.group(1)]
        fname = iraf_filename[match.end() + 1:]  # 1 to omit leading slash

    # dir$file
    else:
        irafdir, fname = iraf_filename.split(sep)
        path = _iraf_decode(irafdir)

    return resolve_filename(path, fname)


# TODO: Use CRDS instead.
def get_latest_file(template, raise_error=False, err_msg=''):
    """Find the filename that appears last in sorted order
    based on given template.

    Parameters
    ----------
    template : str
        Search template in the form of ``path/pattern``
        where pattern is acceptable by :py:mod:`fnmatch`.

    raise_error : bool, optional
        Raise an error when no files found.
        Otherwise, will issue warning only.

    err_msg : str
        Alternate message for when no files found.
        If not given, generic message is used.

    Returns
    -------
    filename : str
        Latest filename.

    Raises
    ------
    IOError
        No files found.

    """
    path, pattern = os.path.split(irafconvert(template))
    path_lc = path.lower()

    if not path:
        path = os.curdir

    # Remote HTTP directory
    if path_lc.startswith('http:'):
        from urllib import request
        from bs4 import BeautifulSoup

        with request.urlopen(path) as fin:  # nosec
            soup = BeautifulSoup(fin, 'html.parser')

        allfiles = [x.text for x in soup.find_all('a')]
        sep = '/'

    # Remote FTP directory
    elif path_lc.startswith('ftp:'):
        from urllib import request

        response = request.urlopen(path).read().decode('utf-8').splitlines()  # nosec  # noqa
        allfiles = list(set([x.split()[-1] for x in response]))  # Rid symlink
        sep = '/'

    # Local directory
    elif os.path.isdir(path):
        allfiles = os.listdir(path)
        sep = os.sep

    # Bogus directory
    else:
        allfiles = []

    matched_files = sorted(fnmatch.filter(allfiles, pattern))

    # Last file in sorted listing
    if matched_files:
        filename = path + sep + matched_files[-1]

    # No files found
    else:
        if not err_msg:
            err_msg = f'No files found for {template}'

        if raise_error:
            raise IOError(err_msg)
        else:
            warnings.warn(err_msg, AstropyUserWarning)
            filename = ''

    return filename


def _read_table(filename, ext, dtypes):
    """Generic table reader.

    Parameters
    ----------
    filename : str
        Table filename.
        If suffix is not 'fits' or 'fit', assume ASCII format.

    ext : int
        Data extension.
        This is ignored for ASCII file.

    dtypes : dict
        Dictionary that maps column names to data types.

    Returns
    -------
    data : `~astropy.io.fits.FITS_rec` or `~astropy.table.Table`
        Data table.

    Raises
    ------
    synphot.exceptions.SynphotError
        Failure to parse table.

    """
    # FITS
    if filename.endswith(('.fits', '.fit')):
        with fits.open(filename) as f:
            data = f[ext].data.copy()

        err_str = ''
        for key, val in dtypes.items():
            if not np.issubdtype(data[key].dtype, val):
                err_str += (f'Expect {key} to be {val} but get '
                            f'{data[key].dtype}.\n')
        if err_str:
            raise synexceptions.SynphotError(err_str)

    # ASCII
    else:  # pragma: no cover
        converters = dict(
            [[k, ascii.convert_numpy(v)] for k, v in dtypes.items()])
        data = ascii.read(filename, converters=converters)

    return data


def read_graphtable(filename, tab_ext=1):
    """Read graph table file.

    Table must contain the following named columns:

    #. ``COMPNAME`` - Component name, usually filter name (str)
    #. ``KEYWORD`` - Usually instrument name (str)
    #. ``INNODE`` - Input node number (int)
    #. ``OUTNODE``- Output node number (int)
    #. ``THCOMPNAME`` - Thermal component name, usually filter name (str)
    #. ``COMMENT`` - Comment (str)

    Example:

    +--------+-------+------+-------+----------+--------+
    |COMPNAME|KEYWORD|INNODE|OUTNODE|THCOMPNAME|COMMENT |
    +========+=======+======+=======+==========+========+
    | clear  |nicmos |   1  |  30   |  clear   |idno=100|
    +--------+-------+------+-------+----------+--------+
    | clear  | wfc3  |   1  |  30   |  clear   |        |
    +--------+-------+------+-------+----------+--------+
    | clear  | wfpc  |   1  |  20   |  clear   |idno=100|
    +--------+-------+------+-------+----------+--------+

    Parameters
    ----------
    filename : str
        Graph table filename.
        If suffix is not 'fits' or 'fit', assume ASCII format.

    tab_ext : int, optional
        FITS extension index of the data table.
        This is ignored for ASCII file.

    Returns
    -------
    primary_area : `~astropy.units.quantity.Quantity` or `None`
        Value of PRIMAREA keyword in primary header.
        Always `None` for ASCII file.

    data : `~astropy.io.fits.FITS_rec` or `~astropy.table.Table`
        Data table.

    Raises
    ------
    synphot.exceptions.SynphotError
        Failure to parse graph table.

    """
    graph_dtypes = {
        'COMPNAME': np.str_, 'KEYWORD': np.str_, 'INNODE': np.int32,
        'OUTNODE': np.int32, 'THCOMPNAME': np.str_, 'COMMENT': np.str_}
    data = _read_table(filename, tab_ext, graph_dtypes)

    # Get primary area
    if filename.endswith(('.fits', '.fit')):
        with fits.open(filename) as f:
            primary_area = f[str('PRIMARY')].header.get('PRIMAREA', None)
    else:  # pragma: no cover
        primary_area = None

    if primary_area is not None and not isinstance(primary_area, u.Quantity):
        primary_area = primary_area * units.AREA

    # Check for segmented graph table
    if np.any([x.lower().endswith('graph')
               for x in data['COMPNAME']]):  # pragma: no cover
        raise synexceptions.SynphotError(
            'Segmented graph tables not supported.')

    return primary_area, data


def read_comptable(filename, tab_ext=1):
    """Read component table file (regular or thermal).

    Table must contain the following named columns:

    #. ``TIME`` - Useafter date and time in the format of
       ``MMM DD YYYY HH:MM:SS`` (str)
    #. ``COMPNAME`` - Component name, usually a combination of
       instrument/detector and filter names (str)
    #. ``FILENAME`` - Path to corresponding throughput file in the
       format of ``path_var$filename`` (str)
    #. ``COMMENT`` - Comment (str)

    See :ref:`stsynphot-master-comp` for more details.

    Parameters
    ----------
    filename : str
        Component table filename.
        If suffix is not 'fits' or 'fit', assume ASCII format.

    tab_ext : int, optional
        FITS extension index of the data table.
        This is ignored for ASCII file.

    Returns
    -------
    data : `~astropy.io.fits.FITS_rec` or `~astropy.table.Table`
        Data table.

    """
    return _read_table(filename, tab_ext,
                       {'TIME': np.str_, 'COMPNAME': np.str_,
                        'FILENAME': np.str_, 'COMMENT': np.str_})


def read_catalog(filename, tab_ext=1):
    """Read catalog grid look-up table.

    Table must contain the following named columns:

    #. ``INDEX`` - Grid values (str)
    #. ``FILENAME`` - Relative file path and column name (str)

    Example:

    +----------------+-----------------------------+
    | INDEX          | FILENAME                    |
    +================+=============================+
    | 10000,-0.5,0.0 | ckm05/ckm05_10000.fits[g00] |
    +----------------+-----------------------------+
    | 10000,-0.5,0.5 | ckm05/ckm05_10000.fits[g05] |
    +----------------+-----------------------------+
    | 10000,-0.5,1.0 | ckm05/ckm05_10000.fits[g10] |
    +----------------+-----------------------------+

    Parameters
    ----------
    filename : str
        Catalog filename.
        If suffix is not 'fits' or 'fit', assume ASCII format.

    tab_ext : int, optional
        FITS extension index of the data table.
        This is ignored for ASCII file.

    Returns
    -------
    data : `~astropy.io.fits.FITS_rec` or `~astropy.table.Table`
        Data table.

    """
    return _read_table(filename, tab_ext, {'INDEX': np.str_,
                                           'FILENAME': np.str_})


def read_wavecat(filename):
    """Read wavelength catalog from ASCII file.

    Table must contain two columns without header.
    Comment lines are allowed and will be ignored.
    Columns are automatically named:

    #. ``OBSMODE`` - Observation mode.
    #. ``FILENAME`` - Corresponding wavelength table filename
       or parameters.

    Example::

        # WAVECAT.DAT -- Comments.
        # More comments.
        cos,fuv     (900.0,3000.0,1.0)
        cos,nuv     (1000.0,12000.0,1.0)
        acs,hrc     synphot$wavecats/acs.dat
        acs,wfc1    synphot$wavecats/acs.dat

    Parameters
    ----------
    filename : str
        Wavelength catalog filename. Must be ASCII format.

    Returns
    -------
    data : `~astropy.table.Table`
        Data table.

    """
    return ascii.read(
        filename, names=('OBSMODE', 'FILENAME'),
        guess=False, format='no_header',
        converters={'OBSMODE': [ascii.convert_numpy(str)],
                    'FILENAME': [ascii.convert_numpy(str)]})


def read_waveset(filename, wave_unit=u.AA):
    """Read wavelength table from ASCII file.

    Table must contain a single column without header.
    Comment lines are allowed and will be ignored.
    Column is automatically named ``WAVELENGTH``.

    Example::

        # ACS.DAT -- Comments.
        # More comments.
        1000.
        2000.
        5000.
        9000.

    Parameters
    ----------
    filename : str
        Wavelength table filename. Must be ASCII format.

    wave_unit : str or `~astropy.units.Unit`
        Wavelength unit.

    Returns
    -------
    waveset : `~astropy.units.quantity.Quantity`
        Wavelength set array.

    """
    wave_unit = units.validate_wave_unit(wave_unit)
    data = ascii.read(
        filename, guess=False, format='no_header', names=('WAVELENGTH', ),
        converters={'WAVELENGTH': [ascii.convert_numpy(float)]})
    waveset = data['WAVELENGTH'].data

    if not isinstance(waveset, u.Quantity):
        waveset = waveset * u.AA

    return waveset


def read_detector_pars(filename):
    """Read detector parameters from ASCII file.

    Table must contain 4 columns without header.
    Comment lines are allowed and will be ignored.
    Columns are automatically named:

    #. ``OBSMODE`` - Observation mode.
    #. ``SCALE`` - Pixel scale in arcseconds.
    #. ``NX`` - X dimension in pixels.
    #. ``NY`` - Y dimension in pixels.

    Example::

        # DETECTORS.DAT -- Comments.
        # More comments.
        acs,hrc     0.027   1024  1024
        acs,sbc     0.032   1024  1024
        stis,g140l  0.0244  1024  1024
        stis,g140m  0.0290  1024  1024

    Parameters
    ----------
    filename : str
        Detector parameters filename. Must be ASCII format.

    Returns
    -------
    data : `~astropy.table.Table`
        Data table.

    """
    return ascii.read(
        filename, guess=False, format='no_header', delimiter=r'\s',
        names=('OBSMODE', 'SCALE', 'NX', 'NY'),
        converters={'OBSMODE': [ascii.convert_numpy(str)],
                    'SCALE': [ascii.convert_numpy(float)],
                    'NX': [ascii.convert_numpy(int)],
                    'NY': [ascii.convert_numpy(int)]})


def read_interp_spec(filename, tab_ext=1):
    """Read parameterized (interpolate-able) throughput
    spectra from FITS table.

    Table must contain two or more columns:

    #. ``WAVELENGTH`` - Wavelength values.
    #. ``PAR#VAL1`` - First parameterized column.
    #. ``PAR#VAL2`` - Second parameterized column.
    #. ...

    Example:

    +------------+---------------+---------------+
    | WAVELENGTH | FR656N#6274.0 | FR656N#6331.4 |
    +============+===============+===============+
    | 6136.0     | 0.0012254583  | 0.00019133692 |
    +------------+---------------+---------------+
    | 6141.0     | 0.0016151578  | 0.00021833261 |
    +------------+---------------+---------------+
    | 6146.0     | 0.0021577575  | 0.00025030275 |
    +------------+---------------+---------------+

    Parameters
    ----------
    filename : str
        FITS filename.

    tab_ext : int, optional
        FITS extension index of the data table.

    Returns
    -------
    data : `~astropy.io.fits.FITS_rec`
        Data table.

    wave_unit : str
        Value of ``TUNIT1`` in table header.

    do_wave_shift : bool
        Perform wavelength shift before interpolation.
        This is `True` when primary header has ``PARAMS``
        keyword set to ``WAVELENGTH`` (case-insensitive).

    allow_extrap : bool
        Allow extrapolation. This is only `True` when
        primary header has ``EXTRAP`` keyword explicitly
        set to ``T`` or `True`.

    """
    with fits.open(filename) as f:
        pri_hdr = f[str('PRIMARY')].header

        params = pri_hdr.get('PARAMS', '')
        if params.lower() == 'wavelength':
            do_wave_shift = True
        else:
            do_wave_shift = False

        extrap = pri_hdr.get('EXTRAP', False)
        if extrap in (True, 'T', 't'):
            allow_extrap = True
        else:
            allow_extrap = False

        wave_unit = f[tab_ext].header['TUNIT1'].lower()
        data = f[tab_ext].data.copy()

    return data, wave_unit, do_wave_shift, allow_extrap

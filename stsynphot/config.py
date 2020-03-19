# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""``stsynphot`` configurable items.

The default configuration heavily depends on STScI CDBS structure
but it can be easily re-configured as the user wishes via
`astropy.config`.

``PYSYN_CDBS`` must be a defined system environment variable for
directories to be configured properly. It also overwrites
``synphot`` configurable items.

"""
# STDLIB
import os

# THIRD-PARTY
import numpy as np
from astropy import log
from astropy.config import ConfigNamespace, ConfigItem

# SYNPHOT
from synphot.config import Conf as synconf
from synphot.utils import generate_wavelengths

__all__ = ['conf', 'getref', 'showref', 'overwrite_synphot_config']


class Conf(ConfigNamespace):
    """Configuration parameters."""

    # Set up default wavelength
    _wave, _wave_str = generate_wavelengths(
        minwave=500, maxwave=26000, num=10000, delta=None, log=True,
        wave_unit='angstrom')

    # Root directory
    rootdir = ConfigItem(
        os.environ.get('PYSYN_CDBS', '/grp/hst/cdbs/'),
        'CDBS data root directory')

    # Graph, optical component, and thermal component tables
    graphtable = ConfigItem('mtab$*_tmg.fits', 'Graph table')
    comptable = ConfigItem('mtab$*_tmc.fits', 'Component table')
    thermtable = ConfigItem('mtab$*_tmt.fits', 'Thermal table')

    # Default wavelength in Angstrom and its description
    waveset_array = ConfigItem(
        _wave.value.tolist(),
        'Default wavelength set in Angstrom', 'float_list')
    waveset = ConfigItem(_wave_str, 'Default wavelength set description')

    # Telescope primary mirror collecting area in cm^2
    area = ConfigItem(45238.93416, 'Telescope collecting area in cm^2')

    # Common filter name
    clear_filter = ConfigItem('clear', 'Name for a clear filter')

    # Wavelength catalog file
    wavecatfile = ConfigItem(
        'synphot$wavecats/wavecat.dat', 'Wavelength catalog file')

    # Detector parameters file
    detectorfile = ConfigItem(
        'synphot$detectors.dat', 'Detector parameters file')

    # IRAF shortcuts file for stsynphot.stio.irafconvert()
    irafshortcutfile = ConfigItem(
        'synphot$irafshortcuts.txt',
        'col1=shortcut_name col2=relpath_to_rootdir, has header.')

    # Clean up
    del _wave
    del _wave_str


def _get_synphot_cfgitems():
    """Iterator for ``synphot`` configuration items."""
    for c in synconf.__dict__.values():
        if isinstance(c, ConfigItem):
            yield c


def overwrite_synphot_config(root):
    """Silently overwrite ``synphot`` configurable items to point to
    given root directory.

    Parameters
    ----------
    root : str
        Root directory name.

    """
    subdir_keys = ['calspec', 'extinction', 'nonhst']

    # Need this for Windows support
    if root.startswith(('http', 'ftp')):
        sep = '/'
    else:
        sep = os.sep  # Can be / or \

    for cfgitem in _get_synphot_cfgitems():
        path, fname = os.path.split(cfgitem())

        i = np.where(list(map(path.__contains__, subdir_keys)))[0]
        if len(i) == 0:
            continue

        subdir = subdir_keys[i[0]]

        if subdir == 'nonhst':
            cfgval = sep.join([root, 'comp', subdir, fname])
        else:
            cfgval = sep.join([root, subdir, fname])

        cfgitem.set(cfgval)


conf = Conf()

# Override SYNPHOT configuration
overwrite_synphot_config(conf.rootdir)


def _get_ref_cfgitems():
    """Iterator for configuration items to be displayed."""
    from .stio import get_latest_file, irafconvert

    for cfgitem, do_conv in (
            (Conf.graphtable, True),
            (Conf.comptable, True),
            (Conf.thermtable, True),
            (Conf.area, False),
            (Conf.waveset, False)):
        val = cfgitem()
        if do_conv:
            val = get_latest_file(irafconvert(val))
        yield cfgitem.name, val


def getref():
    """Return current values of select configurable items as a dictionary.

    Returns
    -------
    refdict : dict

    """
    return dict([x for x in _get_ref_cfgitems()])


def showref():  # pragma: no cover
    """Show the values of select configurable items."""
    info_str = '\n'
    for x in _get_ref_cfgitems():
        info_str += f'{x[0]:10s}: {x[1]}\n'
    log.info(info_str)

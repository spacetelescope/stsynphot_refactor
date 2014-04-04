# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""``stsynphot`` configurable items.

The default configuration heavily depends on STScI CDBS structure
but it can be easily re-configured as the user wishes via
`astropy.config`.

``PYSYN_CDBS`` must be a defined system environment variable for
directories to be configured properly. It also overwrites
``synphot`` configurable items.

"""
from __future__ import absolute_import, division, print_function, unicode_literals

# STDLIB
import os

# ASTROPY
from astropy import log
from astropy.config import ConfigNamespace, ConfigItem
from astropy.extern import six

# SYNPHOT
from synphot.config import conf as synconf
from synphot.utils import generate_wavelengths


__all__ = ['conf', 'getref', 'showref']


# Set up default wavelength
_temp = generate_wavelengths(
    minwave=500, maxwave=26000, num=10000, delta=None, log=True,
    wave_unit='angstrom')
_wave = _temp[0].tolist()
_wave_str = _temp[1]
del _temp


class Conf(ConfigNamespace):
    """Configuration parameters."""
    rootdir = ConfigItem(
        os.environ.get('PYSYN_CDBS', '/grp/hst/cdbs/'),
        'CDBS data root directory')

    # Graph, optical component, and thermal component tables
    graphtable = ConfigItem('mtab$*_tmg.fits', 'Graph table')
    comptable = ConfigItem('mtab$*_tmc.fits', 'Component table')
    thermtable = ConfigItem('mtab$*_tmt.fits', 'Thermal table')

    # Default wavelength in Angstrom and its description
    waveset_array = ConfigItem(
        _wave, 'Default wavelength set in Angstrom', cfgtype='float_list')
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


conf = Conf()


def _overwrite_synphot_config():
    """Silently overwrite ``synphot`` configurable items to point to
    ``rootdir``.

    """
    for c in six.itervalues(synconf.__class__.__dict__):
        if isinstance(c, ConfigItem):
            c.set(c().replace('ftp://ftp.stsci.edu/cdbs/', conf.rootdir))


_overwrite_synphot_config()


def getref():
    """Return current values of select configurable items as a dictionary.

    Returns
    -------
    refdict : dict

    """
    return dict([[x, getattr(conf, x)] for x in
        ('graphtable', 'comptable', 'thermtable', 'area', 'waveset')])


def showref():  # pragma: no cover
    """Show the values of select configurable items."""
    info_str = '\n'
    for x in ('graphtable', 'comptable', 'thermtable', 'area', 'waveset'):
        info_str += '{0:10s}: {1}\n'.format(x, getattr(conf, x))
    log.info(info_str)

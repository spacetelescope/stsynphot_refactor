# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""``stsynphot`` configurable items.

The default configuration heavily depends on STScI CDBS structure
but it can be easily re-configured as the user wishes via
`astropy.config`.

``PYSYN_CDBS`` must be a defined system environment variable for
directories to be configured properly.

"""
from __future__ import absolute_import, division, print_function, unicode_literals

# STDLIB
import os

# ASTROPY
from astropy import log
from astropy.config.configuration import ConfigurationItem

# SYNPHOT
from synphot import config as synconfig
from synphot import exceptions as synexceptions


__all__ = ['PRIMARY_AREA', 'ROOTDIR', 'CATDIR', 'MTABDIR', 'GRAPHTABLE',
           'COMPTABLE', 'THERMTABLE', 'WAVECATFILE', 'DETECTORFILE',
           'IRAFSHORTCUTFILE', 'setdir', 'getdir', 'setref', 'getref',
           'showref']

#--------------#
# Configurable #
#--------------#

# These are set with setdir()
ROOTDIR = ConfigurationItem('rootdir', '', 'CDBS data root directory.')
CATDIR = ConfigurationItem('catdir', '', 'Location of catalogs.')
MTABDIR = ConfigurationItem(
    'mtabdir', '', 'Location of graph and component tables.')

# These are set with setref()
GRAPHTABLE = ConfigurationItem('graphtable', '', 'Graph table.')
COMPTABLE = ConfigurationItem('comptable', '', 'Component table.')
THERMTABLE = ConfigurationItem('thermtable', '', 'Thermal table.')
_DEFAULT_WAVESET = ConfigurationItem(
    'waveset_array', [0.0, 0.0], 'Default wavelength set in Angstrom.',
    cfgtype='float_list')
_DEFAULT_WAVESET_STR = ConfigurationItem(
    'waveset', '', 'Default wavelength set description.')

# HST primary mirror collecting area in cm^2
PRIMARY_AREA = ConfigurationItem('area', 45238.93416,
                                 'Telescope collecting area in cm^2.')

# Wavelength catalog file
WAVECATFILE = ConfigurationItem(
    'wavecatfile', 'synphot$wavecats/wavecat.dat', 'Wavelength catalog file.')

# Detector parameters file
DETECTORFILE = ConfigurationItem(
    'detectorfile', 'synphot$detectors.dat', 'Detector parameters file.')

# IRAF shortcuts file for stsynphot.stio.irafconvert()
IRAFSHORTCUTFILE = ConfigurationItem(
    'irafshortcutfile', 'synphot$irafshortcuts.txt',
    'col1=shortcut_name col2=path_rel_to_rootdir, space separated, has header.')


#----------------------------------#
# Config-related utility functions #
#----------------------------------#

def setdir(root=None):
    """Convenience function to change these configuration items:

        * ``ROOTDIR``
        * ``CATDIR`` - 'grid' sub-directory under ``ROOTDIR``
        * ``MTABDIR`` - 'mtab' sub-directory under ``ROOTDIR``

    Also changes all the values in `synphot.config`.

    Parameters
    ----------
    root : str or `None`
        Value for ``ROOTDIR``. If `None`, set to software default.

    """
    # CDBS data root directory from environment variable
    if root is None:
        def_root =  os.environ.get('PYSYN_CDBS', '')
        if not def_root:
            log.warn('PYSYN_CDBS is undefined; falling back to CDBS FTP site.')
            def_root = 'ftp://ftp.stsci.edu/cdbs/'
        ROOTDIR.set(def_root)
    else:
        ROOTDIR.set(root)

    # Catalogs top-level directory (stellar models, etc.)
    CATDIR.set(os.path.join(ROOTDIR(), 'grid'))

    # Directory containing graph and component tables
    MTABDIR.set(os.path.join(ROOTDIR(), 'mtab'))

    # Overwrite SYNPHOT defaults
    synconfig.STDSTAR_DIR.set(os.path.join(ROOTDIR(), 'calspec'))
    synconfig.EXTINCTION_DIR.set(os.path.join(ROOTDIR(), 'extinction'))
    synconfig.PASSBAND_DIR.set(os.path.join(ROOTDIR(), 'comp/nonhst'))
    synconfig.set_files()


def getdir():
    """Return current values of configurable items settable by
    :func:`setdir` as a dictionary.

    Returns
    -------
    refdict : dict

    """
    return dict([[x.name, x()] for x in
                 (ROOTDIR, CATDIR, MTABDIR, synconfig.STDSTAR_DIR,
                  synconfig.EXTINCTION_DIR, synconfig.PASSBAND_DIR)])


def setref(graphtable=None, comptable=None, thermtable=None, area=None,
           waveset=None):
    """Convenience function to change these configuration items:

        * ``stsynphot.config.GRAPHTABLE``
        * ``stsynphot.config.COMPTABLE``
        * ``stsynphot.config.THERMTABLE``
        * ``stsynphot.config.PRIMARY_AREA``
        * ``stsynphot.config._DEFAULT_WAVESET``
        * ``stsynphot.config._DEFAULT_WAVESET_STR``

    If *all* parameters are `None`, reset them to software default.
    Otherwise, `None` means no change from current value, which
    might not be default.

    Parameters
    ----------
    graphtable, comptable, thermtable : str
        Graph, component, and thermal table filenames.
        Full path must be specified. IRAF format is acceptable.

    area : float
        Telescope collecting area in cm^2.

    waveset : tuple
        Wavelength set parameters, in either format:
            * ``(minwave, maxwave, num)``
            * ``(minwave, maxwave, num, spacing)``, where
              ``spacing`` can be 'log' or 'linear'.
        See :func:`synphot.utils.generate_wavelengths` for more details.

    Raises
    ------
    synphot.exceptions.SynphotError
        Invalid ``waveset`` parameters.

    """
    from synphot.specio import get_latest_file
    from synphot.utils import generate_wavelengths
    from . import stio

    # Check for all None, which means reset
    if set([graphtable, comptable, thermtable, area, waveset]) == set([None]):
        GRAPHTABLE.set(get_latest_file(
            os.path.join(MTABDIR(), '*_tmg.fits'),
            err_msg='No graph tables found; functionality will be SEVERELY ' \
            'crippled.'))

        COMPTABLE.set(get_latest_file(
            os.path.join(MTABDIR(), '*_tmc.fits'),
            err_msg='No component tables found; functionality will be ' \
                'SEVERELY crippled.'))

        THERMTABLE.set(get_latest_file(
            os.path.join(MTABDIR(), '*_tmt.fits'),
            err_msg='No thermal tables found; no thermal calculations can ' \
                'be performed.'))

        PRIMARY_AREA.set(PRIMARY_AREA.defaultvalue)

        wave, wave_str = generate_wavelengths(
            minwave=500, maxwave=26000, num=10000, delta=None, log=True,
            wave_unit='angstrom')

    # Otherwise, check them all separately
    else:
        if graphtable is not None:
            GRAPHTABLE.set(stio.irafconvert(graphtable))

        if comptable is not None:
            COMPTABLE.set(stio.irafconvert(comptable))

        if thermtable is not None:
            THERMTABLE.set(stio.irafconvert(thermtable))

        if area is not None:
            PRIMARY_AREA.set(area)

        if waveset is not None:
            if len(waveset) not in (3, 4):  # pragma: no cover
                raise synexceptions.SynphotError(
                    'waveset tuple must be '
                    '(minwave, maxwave, num[, log/linear]).')

            minwave = waveset[0]
            maxwave = waveset[1]
            num = waveset[2]

            if len(waveset) == 3:  # pragma: no cover
                log = True
            else:  # 4
                spacing = waveset[3].lower()
                if spacing == 'log':  # pragma: no cover
                    log = True
                elif spacing == 'linear':
                    log = False
                else:  # pragma: no cover
                    raise synexceptions.SynphotError(
                        'Fourth waveset option must be "log" or "linear".')

            wave, wave_str = generate_wavelengths(
                minwave=minwave, maxwave=maxwave, num=num, log=log,
                wave_unit='angstrom')

    _DEFAULT_WAVESET.set(wave.tolist())
    _DEFAULT_WAVESET_STR.set(wave_str)


def getref():
    """Return current values of configurable items settable by
    :func:`setref` as a dictionary.

    Returns
    -------
    refdict : dict

    """
    return dict([[x.name, x()] for x in (GRAPHTABLE, COMPTABLE, THERMTABLE,
                                         PRIMARY_AREA, _DEFAULT_WAVESET_STR)])


def showref():  # pragma: no cover
    """Show the values settable by :func:`setref`."""
    info_str = '\n'
    for x in (GRAPHTABLE, COMPTABLE, THERMTABLE, PRIMARY_AREA,
              _DEFAULT_WAVESET_STR):
        info_str += '{0:10s}: {1}\n'.format(x.name, x())
    log.info(info_str)


# Set default values
setdir()
setref()

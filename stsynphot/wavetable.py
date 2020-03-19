# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""Module to handle ``stsynphot.config.conf.wavecatfile`` table,
which is used by ETC to select an appropriate wavelength set
for a given observation mode for count rate calculations.

"""

# STDLIB
import warnings

# THIRD-PARTY
import numpy as np

# ASTROPY
from astropy import units as u
from astropy.utils.exceptions import AstropyUserWarning

# SYNPHOT
from synphot import units

# LOCAL
from . import exceptions, stio
from .config import conf

__all__ = ['WAVECAT', 'WaveCatalog', 'load_wavecat']

# This is NSPEC-1 in IRAF SYNPHOT COUNTRATE calcstep.x.
# NSPEC was hardcoded to 2000 as the number of bins into
# which the wavelength set should be divided by default.
_N_SPEC = 1999.0

# Will be initialized by load_wavecat()
WAVECAT = None


class WaveCatalog:
    """Class to handle ``stsynphot.config.conf.wavecatfile`` initialization
    and access.

    Input file is parsed with :func:`stsynphot.stio.read_wavecat`.

    For each observation mode, its wavelength table is defined
    by filename or parameter string. When it is accessed with
    :py:meth:`~object.__getitem__`, the string is replaced by the actual
    wavelengths array. If filename is given, it is parsed with
    :func:`stsynphot.stio.read_waveset`.

    Parameters
    ----------
    fname : str
        Wavecat filename.

    wave_unit : str or `~astropy.units.Unit`
        Wavelength unit.

    Attributes
    ----------
    file : str
        Wavecat filename.

    wave_unit : `~astropy.units.Unit`
        Wavelength unit.

    lookup : dict
        Maps observation mode to corresponding wavelength table
        filename or parameter string.

    setlookup : dict
        Maps individual components of observation mode to its
        string. Used for partial matching.

    """
    def __init__(self, fname, wave_unit=u.AA):
        data = stio.read_wavecat(stio.irafconvert(fname))

        self.file = fname
        self.wave_unit = units.validate_wave_unit(wave_unit)
        self.lookup = {}
        self.setlookup = {}

        for line in data:
            obm = line['OBSMODE']
            coeff = line['FILENAME']
            self.lookup[obm] = coeff
            self.setlookup[frozenset(obm.split(','))] = obm

    def __getitem__(self, key):
        """Fairly smart lookup by observation mode.
        If no exact match, find the most complete match.

        """
        # Find exact match
        try:
            ans = self.lookup[key]
        # Find the next most complete match
        except KeyError:
            ans = None
            # Try a set-wise match.
            # The correct key will be a subset of the input key.
            setkey = set(key.split(','))
            candidates = [k for k in self.setlookup if k.issubset(setkey)]
            n_match = len(candidates)
            # We may have 1, 0, or >1 candidates.
            if n_match == 1:
                ans = self.lookup[self.setlookup[candidates[0]]]
            elif n_match == 0:
                raise KeyError(f'{setkey} not found in {self.file}; '
                               f'candidates: {str(candidates)}')
            elif n_match > 1:
                setlens = np.array([len(k) for k in candidates])
                srtlen = setlens.argsort()
                k, j = srtlen[-2:]
                # It's really ambiguous
                if setlens[k] == setlens[j]:
                    raise exceptions.AmbiguousObsmode(
                        f'{setkey}; candidates: {str(candidates)}')
                # We have a winner
                else:
                    k = candidates[srtlen[-1]]
                    ans = self.lookup[self.setlookup[k]]
        return ans

    @staticmethod
    def _calc_quadratic_coeff(coeff):
        """Calculate quadratic coefficients from parameter string."""
        coefficients = coeff[1:-1].split(',')
        n_coeff = len(coefficients)

        c0 = float(coefficients[0])
        c1 = float(coefficients[1])
        c2 = (c1 - c0) / _N_SPEC
        c3 = c2

        if n_coeff > 2:
            c2 = float(coefficients[2])
            c3 = c2
        if n_coeff > 3:
            c3 = float(coefficients[3])

        nwave = int(2.0 * (c1 - c0) / (c3 + c2)) + 1
        c = c0
        b = c2
        a = (c3 * c3 - c2 * c2) * 0.25 / (c1 - c0)

        return a, b, c, nwave

    def _waveset_from_parstring(self, coeff):
        """Get wavelengths array from parameter string."""
        a, b, c, nwave = self._calc_quadratic_coeff(coeff)
        i = np.arange(nwave, dtype=np.float64)
        return (((a * i) + b) * i + c) * self.wave_unit

    def load_waveset(self, obsmode):
        """Load wavelength table by observation mode.
        If no exact match, find the most complete match.

        Parameters
        ----------
        obsmode : str
            Observation mode.

        Returns
        -------
        par : str
            Matched filename or parameter string.
            May be exact or closest.

        waveset : `astropy.units.quantity.Quantity`
            Corresponding wavelength set.

        """
        par = self.__getitem__(obsmode)
        if par.startswith('('):
            waveset = self._waveset_from_parstring(par)
        else:
            waveset = stio.read_waveset(
                stio.irafconvert(par), wave_unit=self.wave_unit)
        return par, waveset


def load_wavecat(wave_unit=u.AA):
    """Convenience function to update ``stsynphot.wavetable.WAVECAT``
    global variable with the latest ``stsynphot.config.conf.wavecatfile``.

    Parameters
    ----------
    wave_unit : str or `~astropy.units.Unit`
        See `WaveCatalog`.

    """
    global WAVECAT
    WAVECAT = WaveCatalog(conf.wavecatfile, wave_unit=wave_unit)


# Load default wavecat file in Angstrom.
try:
    load_wavecat()
except Exception as e:
    warnings.warn(
        f'Failed to load {conf.wavecatfile}: {repr(e)}', AstropyUserWarning)

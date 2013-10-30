# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""This module contains spectrum classes specific to STScI formats."""
from __future__ import division, print_function

# STDLIB
import re
import os

# THIRD-PARTY
import numpy as np

# SYNPHOT
from synphot import spectrum, synexceptions


class InterpolatedSpectralElement(SpectralElement):
    """
    The InterpolatedSpectralElement class handles spectral elements
    that are interpolated from columns stored in FITS tables

    """

    def __init__(self, fileName, wavelength):
        """
        The file name contains a suffix with a column name specification
        in between square brackets, such as [fr388n#]. The wavelength
        parameter (poorly named -- it is not always a wavelength) is used to
        interpolate between two columns in the file.

        """
        SpectralElement.__init__(self)

        xre = re.search('\[(?P<col>.*?)\]', fileName)
        self.name = os.path.expandvars(fileName[0:(xre.start())])
        colSpec = xre.group('col')

        self.analytic = False
        self.warnings = {}

        self.interpval = wavelength

        with fits.open(self.name) as fs:

            # if the file has the PARAMS header keyword and if it is set to
            # WAVELENGTH then we want to perform a wavelength shift before
            # interpolation, otherwise we don't want to shift.
            if (('PARAMS' in fs[0].header) and
                    (fs[0].header['PARAMS'].lower() == 'wavelength')):
                doshift = True
            else:
                doshift = False

            # check whether we are supposed to extrapolate when we're given an
            # interpolation value beyond the columns of the table.
            # extrapolation is assumed false if the EXTRAP keyword is missing.
            if 'EXTRAP' in fs[0].header and fs[0].header['EXTRAP'] is True:
                extrapolate = True
            else:
                extrapolate = False

            # The wavelength table will have to be adjusted before use
            wave0 = fs[1].data.field('wavelength')

            #Determine the columns that bracket the desired value
            # grab all columns that begin with the parameter name (e.g. 'MJD#')
            # then split off the numbers after the '#'
            colNames = [n for n in fs[1].data.names if
                        n.startswith(colSpec.upper())]
            colWaves = [float(cn.split('#')[1]) for cn in colNames]

            if colNames:
                raise StandardError('File {0} contains no interpolated '
                                    'columns.'.format(fileName))

            # easy case: wavelength matches a column
            if self.interpval in colWaves:
                self._no_interp_init(
                    wave0, fs[1].data[colNames[colWaves.index(wavelength)]])
            # need interpolation
            elif ((self.interpval > colWaves[0]) and
                  (self.interpval < colWaves[-1])):
                upper_ind = np.searchsorted(colWaves, self.interpval)
                lower_ind = upper_ind - 1

                self._interp_init(wave0,
                                  colWaves[lower_ind],
                                  colWaves[upper_ind],
                                  fs[1].data[colNames[lower_ind]],
                                  fs[1].data[colNames[upper_ind]], doshift)
            # extrapolate below lowest columns
            elif extrapolate and self.interpval < colWaves[0]:
                self._extrap_init(wave0,
                                  colWaves[0],
                                  colWaves[1],
                                  fs[1].data[colNames[0]],
                                  fs[1].data[colNames[1]])
            # extrapolate above highest columns
            elif extrapolate and self.interpval > colWaves[-1]:
                self._extrap_init(wave0,
                                  colWaves[-2],
                                  colWaves[-1],
                                  fs[1].data[colNames[-2]],
                                  fs[1].data[colNames[-1]])
            # can't extrapolate, use default
            elif not extrapolate and 'THROUGHPUT' in fs[1].data.names:
                s = 'Extrapolation not allowed, using default throughput ' \
                    'for {0}'.format(fileName)
                warnings.warn(s, UserWarning)
                self.warnings['DefaultThroughput'] = True
                self._no_interp_init(wave0, fs[1].data['THROUGHPUT'])
            # can't extrapolate and no default
            elif not extrapolate and 'THROUGHPUT' not in fs[1].data.names:
                s = 'Cannot extrapolate and no default throughput for %s' % \
                    (fileName,)
                raise synexceptions.ExtrapolationNotAllowed(s)
            # assign units
            self.waveunits = units.Units(fs[1].header['tunit1'].lower())
            self.throughputunits = 'none'

        fs.close()

    def __str__(self):
        return "%s#%g" % (self.name, self.interpval)

    def _no_interp_init(self, waves, throughput):
        self._wavetable = waves
        self._throughputtable = throughput

    def _interp_init(self, waves, lower_val, upper_val, lower_thru, upper_thru,
                     doshift):
        self._wavetable = waves

        if doshift:
            # Adjust the wavelength table to bracket the range
            lwave = waves + (lower_val - self.interpval)
            uwave = waves + (upper_val - self.interpval)

            # Interpolate the columns at those ranges
            lower_thru = np.interp(lwave, waves, lower_thru)
            upper_thru = np.interp(uwave, waves, upper_thru)

        # Then interpolate between the two columns
        w = (self.interpval - lower_val) / (upper_val - lower_val)
        self._throughputtable = (upper_thru * w) + lower_thru * (1.0 - w)

    def _extrap_init(self, waves, lower_val, upper_val, lower_thru, upper_thru):
        self._wavetable = waves

        throughput = []

        for y1, y2 in zip(lower_thru, upper_thru):
            m = (y2 - y1) / (upper_val - lower_val)
            b = y1 - m * lower_val

            throughput.append(m*self.interpval + b)

        self._throughputtable = np.array(throughput)


class ThermalSpectralElement(TabularSpectralElement):
    """
    The ThermalSpectralElement class handles spectral elements
    that have associated thermal properties read from a FITS table.

    ThermalSpectralElements differ from regular SpectralElements in
    that they carry thermal parameters such as temperature and beam
    filling factor, but otherwise they operate just as regular
    SpectralElements. They don't know how to apply themselves to an
    existing beam, in the sense that their emissivities should be
    handled explicitly, outside the objects themselves.

    """
    def __init__(self, fileName):

        TabularSpectralElement.__init__(self,
                                        fileName=fileName,
                                        thrucol='emissivity')
        self.warnings = {}

    def getHeaderKeywords(self, header):
        """
        Overrides base class in order to get thermal keywords.

        """
        self.temperature = header['DEFT']
        self.beamFillFactor = header['BEAMFILL']

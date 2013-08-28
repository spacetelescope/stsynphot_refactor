# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""
The ObsBandpass user interface needs to support either the usual
(acs,hrc,f555w) obsmode style that produce a set of chained throughput
files; or something like (johnson,v) that has a single throughput file.
Thus ObsBandpass must be a factory function, returning either an
ObsModeBandpass (ack, terrible name) or a TabularSpectralElement.

"""
from __future__ import division, print_function

# THIRD-PARTY
import numpy as np

# SYNPHOT
from synphot import binning, spectrum, synexceptions, units

# LOCAL
from . import observationmode


__all__ = []


# This needs to go into to_fits() somewhere
#        bkeys = {
#            'expr': (str(self), 'synphot expression'),
#            'tdisp1': 'G15.7',
#            'tdisp2': 'G15.7',
#            'grftable': (self.bandpass.obsmode.gtname, 'graph table used'),
#            'cmptable': (self.bandpass.obsmode.ctname, 'component table used')}


def ObsBandpass(obstring, graphtable=None, comptable=None, component_dict={}):
    """
    Generate an ObsModeBandPass or TabularSpectralElement instance

    obsband = ObsBandpass(string specifying obsmode; for details
    see the Synphot Data User's Guide at
    http://www.stsci.edu/hst/HST_overview/documents/synphot/hst_synphotTOC.html

    """

    # Temporarily create an Obsmode to determine whether an
    # ObsModeBandpass or a TabularSpectralElement will be returned.
    ob = observationmode.ObservationMode(obstring,
                                         graphtable=graphtable,
                                         comptable=comptable,
                                         component_dict=component_dict)
    if len(ob) > 1:
        return ObsModeBandpass(ob)
    else:
        return spectrum.TabularSpectralElement(ob.components[0].throughput_name)


class ObsModeBandpass(spectrum.SpectralElement):
    """
    Bandpass instantiated from an obsmode string

    """

    def __init__(self, ob):
        """
        Instantiate a COmpositeSpectralElement by means of an
        ObservationMode (which the caller must have already created from
        an  obstring

        """

        #Chain the individual components
        chain = ob.components[0].throughput*ob.components[1].throughput

        for i in range(2, len(ob)-1):
            chain = chain*ob.components[i].throughput

        spectrum.CompositeSpectralElement.__init__(self,
                                                   chain,
                                                   ob.components[-1].throughput)

        self.obsmode = ob
        self.name = self.obsmode._obsmode  # str(self.obsmode)
        self.primary_area = ob.primary_area

        #Check for valid bounds
        self._checkbounds()

        try:
            self.binset = self.obsmode.bandWave()
        except AttributeError:
            # this is to catch an error raised when the self.obsmode
            # object does not have a binset attribute because of some
            # problem with the obsmode used to instatiate it.
            pass

    def __str__(self):
        """
        Defer to ObservationMode component

        """
        return self.name  # self.obsmode._obsmode

    def __len__(self):
        """
        Defer to ObservationMode component

        """
        return len(self.obsmode)

    def showfiles(self):
        """
        Defer to ObservationMode component

        """
        return self.obsmode.showfiles()

    def _checkbounds(self):
        thru = self.throughput
        if thru[0] != 0 or thru[-1] != 0:
            print("Warning: throughput for this obsmode is not bounded by "
                  "zeros. Endpoints: thru[0]=", thru[0], " thru[-1]=", thru[-1])

    def thermback(self):
        """
        Expose the thermal background calculation presently hidden
        in the obsmode class.
        Only bandpasses for which thermal information has been supplied
        in the graph table supports this method; all others will raise a
        NotImplementedError.

        """

        # The obsmode.ThermalSpectrum method will raise an exception if there is
        # no thermal information, and that will just propagate up.
        sp = self.obsmode.ThermalSpectrum()

        #Thermback is always provided in this non-standard set of units.
        #This code was copied from etc.py.
        ans = sp.integrate() * (self.obsmode.pixscale**2 *
                                self.obsmode.primary_area)
        return ans

    def pixel_range(self, waverange, waveunits=None, mode='round'):
        """
        Returns the number of wavelength bins within ``waverange``.

        .. note::

           This calls :func:`synphot.binning.pixel_range` with
           ``self.binset`` as the first argument. See
           :func:`synphot.binning.pixel_range` for full documentation.

        Parameters
        ----------
        waverange : array_like
            Wavelengths.

        waveunits : str or `astropy.units.core.Unit`, optional
            The units of ``waverange``. Defaults to `None`.
            If `None`, the wavelengths are assumed to be in the units of the
            ``self.waveunits`` attribute.

        Returns
        -------
        num: int or float
            Number of wavelength bins within `waverange`.

        Raises
        ------
        synphot.synexceptions.UndefinedBinset
            If the ``self.binset`` attribute is `None`.

        """
        # make sure we have a binset to work with
        if self.binset is None:
            raise synexceptions.UndefinedBinset(
                'No binset specified for this bandpass.')

        # convert waverange to self.waveunits, if necessary
        if waveunits is None:
            waveunits = self.waveunits
        waverange = units.convert_wavelengths(
            waverange, waveunits, self.waveunits)

        return binning.pixel_range(self.binset, waverange, mode=mode)

    def wave_range(self, cenwave, npix, waveunits=None, mode='round'):
        """
        Get the wavelength range covered by a number of pixels, ``npix``,
        centered on wavelength ``cenwave``.

        .. note::

           This calls the :func:`synphot.binning.wave_range` function with
           ``self.binset`` as the first argument. See
           :func:`synphot.binning.wave_range` for full documentation.

        Parameters
        ----------
        cenwave : float
            Central wavelength.

        npix : int
            Number of pixels.

        waveunits : str or `astropy.units.core.Unit`, optional
            Wavelength units of ``cenwave`` and the returned wavelength range.
            Defaults to `None`. If `None`, the wavelengths are assumed to be in
            the units of the ``self.waveunits`` attribute.

        Returns
        -------
        waverange : array_like
            Wavelength range defined by ``(wave1, wave2)``.

        Raises
        ------
        synphot.synexceptions.SynphotError
            If ``waveunits`` is invalid.

        synexceptions.UndefinedBinset
            If the ``self.binset`` attribute is None.

        """
        # make sure we have a binset to work with
        if self.binset is None:
            raise synexceptions.UndefinedBinset(
                'No binset specified for this bandpass.')

        # convert waverange to self.waveunits, if necessary
        if waveunits is None:
            waveunits = self.waveunits
        cenwave = units.convert_wavelengths(
            cenwave, waveunits, self.waveunits)

        waverange = binning.wave_range(self.binset, cenwave, npix, mode=mode)

        # convert back to waveunits, if necessary
        waverange = units.convert_wavelengths(
            waverange, self.waveunits, waveunits)

        return waverange

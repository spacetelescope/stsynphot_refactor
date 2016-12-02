.. doctest-skip-all

.. _stsynphot-tutorials:

Tutorials
=========

This page contains tutorials of specific **stsynphot** functionality not
explicitly covered in other sections.


.. _tutorial_countrate_multi_aper:

Count Rates for Multiple Apertures
----------------------------------

In this tutorial, you will learn how to calculate count rates for observations
of the same source and bandpass, but with different apertures. Note that this
feature is only available for observing modes that allow encircled energy (EE)
radius specification (see :ref:`stsynphot-appendixb`).

Create two observations of Vega (renormalized to 20 STMAG in Johnson *V*) with
ACS/WFC1 F555W bandpass, with 0.3 and 1.0 arcsec EE radii, respectively::

    >>> import stsynphot as STS
    >>> from astropy import units as u
    >>> from synphot import Observation
    >>> sp = STS.Vega.normalize(20 * u.STmag, STS.band('johnson,v'))
    >>> obs03 = Observation(sp, STS.band('acs,wfc1,f555w,aper#0.3'))
    >>> obs10 = Observation(sp, STS.band('acs,wfc1,f555w,aper#1.0'))

Calculate the count rates for both and display the results::

    >>> c03 = obs03.countrate(STS.conf.area)
    >>> c10 = obs10.countrate(STS.conf.area)
    >>> print('Count rate for 0.3" is {:.3f}\n'
    ...       'Count rate for 1.0" is {:.3f}'.format(c03, c10))
    Count rate for 0.3" is 174.801 ct / s
    Count rate for 1.0" is 186.521 ct / s


.. _tutorial_band_stmag:

Bandpass STMAG Zeropoint
------------------------

HST bandpasses store their :ref:`synphot:synphot-formula-uresp` values under
the ``PHOTFLAM`` keyword in image headers. This keyword is then used to compute
STMAG zeropoint for the respective bandpass (e.g.,
`ACS <http://www.stsci.edu/hst/acs/analysis/zeropoints>`_ and
`WFC3 <http://www.stsci.edu/hst/wfc3/phot_zp_lbn>`_).

In this tutorial, you will learn how to calculate the STMAG zeropoint for
the ACS/WFC1 F555W bandpass::

    >>> import numpy as np
    >>> import stsynphot as STS
    >>> bp = STS.band('acs,wfc1,f555w')
    >>> uresp = bp.unit_response(STS.conf.area)
    >>> uresp
    <Quantity 1.9712343504030155e-19 FLAM>
    >>> st_zpt = -2.5 * np.log10(uresp.value) - 21.1
    >>> print('STmag zeropoint for {} is {:.5f}'.format(bp.obsmode, st_zpt))
    STmag zeropoint for acs,wfc1,f555w is 25.66315


.. _tutorial_wavetab:

Custom Wavelength Table
-----------------------

In this tutorial, you will learn how to create a custom wavelength array and
save it to a FITS table using `astropy.io.fits`. Then, you will read the array
back in from file, and use it to define detector binning for an observation.

Suppose we want a wavelength set that ranges from 2000 to 8000 Angstrom, with
1 Angstrom spacing over most of the range, but 0.1 Angstrom spacing
around the [O III] forbidden lines at 4959 and 5007 Angstrom.

Create the 3 regions separately, concatenate them, and display the result::

    >>> import numpy as np
    >>> lowave = np.arange(2000, 4950)
    >>> mdwave = np.arange(4950, 5010, 0.1)  # [O III]
    >>> hiwave = np.arange(5010, 8000)
    >>> wave = np.concatenate([lowave, mdwave, hiwave])
    >>> wave
    array([ 2000.,  2001.,  2002., ...,  7997.,  7998.,  7999.])

Create an Astropy table from the concatenated array above and save it out as a
FITS table::

    >>> from astropy.io import fits
    >>> col = fits.Column(
    ...     name='wavelength', unit='angstrom', format='E', array=wave)
    >>> tabhdu = fits.BinTableHDU.from_columns([col])
    >>> tabhdu.writeto('mywaveset.fits')

Read the custom wavelength set back in from file using Astropy table::

    >>> from astropy.table import QTable
    >>> tab = QTable.read('mywaveset.fits')  # Ignore the UnitsWarning
    WARNING: UnitsWarning: The unit 'angstrom' has been deprecated...
    >>> wave = tab['wavelength']
    >>> wave
    <Quantity [ 2000., 2001., 2002.,...,  7997., 7998., 7999.] Angstrom>

Create an observation of Vega with ACS/WFC1 F555W bandpass, using the custom
wavelength binning above, and then check that the binned wavelength set is
indeed the given one::

    >>> import stsynphot as STS
    >>> from synphot import Observation
    >>> obs = Observation(STS.Vega, STS.band('acs,wfc1,f555w'), binset=wave)
    >>> obs.binset
    <Quantity [ 2000., 2001., 2002.,...,  7997., 7998., 7999.] Angstrom>

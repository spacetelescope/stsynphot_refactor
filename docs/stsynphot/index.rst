.. _stsynphot_index:

*************************************************
Synthetic Photometry for HST/JWST (``stsynphot``)
*************************************************

Introduction
============

This is a module for manipulating spectra. It is intended to be used for
synthetic photometry, i.e., constructing source spectra and spectral element
throughputs for data from HST or JWST.

This package started out as IRAF SYNPHOT used by Hubble Space Telescope
calibrations. For some backward-compatibility, the API of this package is
kept the same as legacy PYSYNPHOT where feasible.

STScI `Exposure Time Calculator (ETC) <http://etc.stsci.edu/etc/>`_ heavily
relies on this software.


Setup
=====

The environment variable ``PYSYN_CDBS`` must be defined to point to the
top level directory where HST or JWST SYNPHOT database is installed.


Getting Started
===============

This section only contains minimal examples.


Using ``stsynphot``
===================

.. toctree::
   :maxdepth: 1

   catalog
   observationmode
   tables
   accuracy


See Also
========

.. _stsynphot-ref-diaz2012:

Diaz, R. I. 2012, pysynphot/Synphot Throughput Files: Mapping to Instrument Components for ACS, COS, and WFC3, CDBS ISR 2012-01 (Baltimore, MD: STScI)

.. _stsynphot-spark-earley1968:

Earley, J. 1968, An Efficient Context-Free Parsing Algorithm, PhD thesis, Carnegie-Mellon Univ.

.. _stsynphot-spark-earley1970:

Earley, J. 1970, An Efficient Context-Free Parsing Algorithm, CACM, 13(2), 94

.. _stsynphot-ref-horne1988:

Horne, K. 1988, in New Directions in Spectophotometry: A Meeting Held in Las Vegas, NV, March 28-30, Application of Synthetic Photometry Techniques to Space Telescope Calibration, ed. A. G. Davis Philip, D. S. Hayes, & S. J. Adelman (Schenectady, NY: L. Davis Press), 145

.. _stsynphot-ref-koornneef1986:

Koornneef, J., Bohlin, R., Buser, R., Horne, K., & Turnshek, D. 1986, Highlights Astron., 7, 833

.. _stsynphot-ref-laidler2005:

Laidler, V., et al. 2005, Synphot User's Guide, Version 5.0 (Baltimore, MD: STScI)

.. _stsynphot-ref-laidler2008:

Laidler, V., et al. 2008, Synphot Data User's Guide, Version 1.2 (Baltimore, MD: STScI)

.. _stsynphot-ref-robitaille2013:

Robitaille, T. P., et al. 2013, A&A, 558, A33


Reference/API
=============

.. automodapi:: stsynphot.catalog

.. automodapi:: stsynphot.config
   :no-inheritance-diagram:

.. automodapi:: stsynphot.exceptions

.. automodapi:: stsynphot.graphtab
   :no-inheritance-diagram:

.. automodapi:: stsynphot.io
   :no-inheritance-diagram:

.. automodapi:: stsynphot.observationmode

.. automodapi:: stsynphot.spark

.. automodapi:: stsynphot.spectrum

.. automodapi:: stsynphot.spparser

.. automodapi:: stsynphot.tables

.. automodapi:: stsynphot.wavetable


Version
=======

.. autodata:: stsynphot.__version__

.. doctest-skip-all

.. _stsynphot-top-level:

#######################
stsynphot Documentation
#######################

This module was part of the ASTROLIB PYSYNPHOT that deals with
HST/JWST-specific synthetic photometry. Currently, ``stsynphot`` is an
astropy-affiliated package. It depends on the following external packages:

* `Astropy-affiliated package synphot <http://www.github.com/spacetelescope/pysynphot>`_
* `Astropy <http://astropy.org>`_ - Currently requires a special version that
  has ``modeling`` that handles composite models and ``sampleset`` property.
* `numpy <http://www.numpy.org/>`_
* `matplotlib <http://matplotlib.org/>`_ (optional, for plotting)

It is designed to work with the following database:

* `HST throughput tables <http://www.stsci.edu/hst/observatory/crds/cdbs_throughput.html>`_
* JWST throughput tables (not yet available).

It is tested with the following Python versions:

* 2.7.5
* 3.2.3
* 3.4.0

If you have questions about this package, please contact ``help[at]stsci.edu``.

Contents:

.. toctree::
   :maxdepth: 1

   stsynphot/index


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

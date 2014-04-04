.. doctest-skip-all

.. _stsynphot_catalog:

********
Catalogs
********

There are several spectral atlases consisting of both observed and model data
that are available for use with `stsynphot`.

Current descriptions and access to all available calibration spectra and
astronomical catalogs can be found at
`this CDBS website <http://www.stsci.edu/hst/observatory/cdbs/astronomical_catalogs.html>`_.
Details are also available from
:ref:`Laidler et al. (2008, Appendix A) <stsynphot-ref-laidler2008>`.


.. _stsynphot-cat-grid:

Grids
=====

Some catalogs come with a grid of basis spectra which are indexed for various
combinations of these properties:

    * Effective temperature in Kelvin (:math:`T_{eff}`)
    * Metallicity (:math:`Z`)
    * Log surface gravity (:math:`\log g`)

Such catalogs are:

    * `Allard et al. (2009) <ftp://ftp.stsci.edu/cdbs/grid/phoenix/AA_README>`_
    * `Castelli & Kurucz (2004) <http://www.stsci.edu/hst/observatory/cdbs/castelli_kurucz_atlas.html>`_
    * `Kurucz (1993) <http://www.stsci.edu/hst/observatory/cdbs/k93models.html>`_

User may specify any combination of the above, so long as each parameter is
within the range defined by the requested catalog. The allowed range of each
parameter depends on the catalog. For example, the Castelli & Kurucz catalog
contains spectra for
:math:`3500 \textnormal{K} \le T_{eff} \le 50000 \textnormal{K}`.
In this case, no spectrum can be constructed for
:math:`T_{eff} = 3499 \textnormal{K}` or :math:`T_{eff} = 50001 \textnormal{K}`.

Examples
--------
>>> from stsynphot.catalog import Icat

Obtain spectrum for a Kurucz model with :math:`T_{eff} = 6000 \textnormal{K}`,
:math:`Z = 0`, and :math:`\log g = 4.3`:

>>> sp = Icat.from_grid('k93models', 6440, 0, 4.3)

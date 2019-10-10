.. _stsynphot_overview:

Overview
========

This section expands upon :ref:`synphot's overview <synphot:synphot_overview>`
to only clarify things that are unique in **stsynphot**. In particular, this
package adds functionalities similar to ASTROLIB PYSYNPHOT that are specific to
STScI database or supported telescopes, including but not limited to:

* :ref:`stsynphot-crds-overview`
* :ref:`stsynphot-spec-atlas`
* :ref:`stsynphot-obsmode`
* :ref:`stsynphot-language-parser`

Spectra are constructed from observation modes or catalogs using files from
the database (e.g., by multiplying data from individual throughput files
together or interpolating between them). Hence, you will be mostly working
with compound models built on `~synphot.models.Empirical1D` models.


.. _stsynphot-quick-guide:

Quick Guide
-----------

The tables below summarize some main functionality of **stsynphot**.
The variables, where appropriate, can be numbers (assumed to be in certain
units) or Quantity. These are only for quick reference. Detailed explanations
are available in their respective sections in the other parts of this document.

.. _stsynphot-quick-bandpass:

Bandpass
^^^^^^^^

+---------------------------+------------------------------------------------+
|Description                |Command                                         |
+===========================+================================================+
|HST observation mode.      |bp = band(obsmode)                              |
+---------------------------+------------------------------------------------+
|``obsmode`` specific       |bp.binset                                       |
|wavelength set that is     |                                                |
|optimal for binned data.   |                                                |
+---------------------------+------------------------------------------------+
|``obsmode`` specific       |bp.area                                         |
|collecting area.           |                                                |
+---------------------------+------------------------------------------------+
|Number of ``obsmode``      |len(bp)                                         |
|components.                |                                                |
+---------------------------+------------------------------------------------+
|``obsmode`` component      |bp.showfiles()                                  |
|filenames.                 |                                                |
+---------------------------+------------------------------------------------+
|Thermal background         |bp.thermback()                                  |
|(only if applicable).      |                                                |
+---------------------------+------------------------------------------------+

.. _stsynphot-quick-other-spectrum:

Other Spectrum
^^^^^^^^^^^^^^

+---------------------------+------------------------------------------------+
|Description                |Command                                         |
+===========================+================================================+
|Extinction curve from      |extcurve = ebmvx(extinction_model_name, ebv)    |
|given model at given       |                                                |
|:math:`E(B-V)`             |                                                |
+---------------------------+------------------------------------------------+
|Vega spectrum (preloaded). |sp = Vega                                       |
+---------------------------+------------------------------------------------+
|Source spectrum            |sp = grid_to_spec(catalog, temperature,         |
|interpolated from catalog. |metallicity, log_gravity)                       |
+---------------------------+------------------------------------------------+

.. _stsynphot-quick-misc:

Miscellaneous
^^^^^^^^^^^^^

+---------------------------+------------------------------------------------+
|Description                |Command                                         |
+===========================+================================================+
|Show current reference data|showref()                                       |
|(graph/component tables,   |                                                |
|default wavelengths, area).|                                                |
+---------------------------+------------------------------------------------+
|Like ``showref()`` but     |refdict = getref()                              |
|returns a ``dict``.        |                                                |
+---------------------------+------------------------------------------------+
|Spectrum from IRAF syntax. |sp = parse_spec(iraf_string)                    |
+---------------------------+------------------------------------------------+


.. _stsynphot-obsmode-overview:

Observing Mode
--------------

The throughput calibrations of the HST and the JWST observatories are
represented in a framework consisting of:

* Component throughput files for every optical component (e.g., mirror, filter,
  polarizer, disperser, and detector).
* A configuration table describing the allowed combinations of the components.

In **stsynphot**, a particular observing mode is specified by a list of
keywords, which might be familiar names of filters, detectors, and gratings.
The keywords are used to trace the light path through the observatory via the
configuration graph file (a.k.a. the TMG file) which helps translating the
keyword list into a list of pointers to data files that contain the individual
component throughput functions.
The grand throughput function of the requested observing mode is then formed
by multiplying together the individual component throughput at each wavelength.
The instrument graph (TMG), component lookup (a.k.a. TMC and TMT tables), and
component throughput tables are all in FITS format.
(See :ref:`stsynphot-appendixb`, :ref:`stsynphot-appendixc`, and
:ref:`Diaz 2012 <stsynphot-ref-diaz2012>` for more details on the internal
structure and functioning of the configuration graph and component throughput
tables.)

To retrieve a particular HST (and soon JWST) bandpass, you furnish the bandpass
generator with a couple of keywords (e.g., ``"wfc3,uvis2,f555w"``).
The bandpass generator uses the keywords to trace a path through the graph
file, multiplies together the bandpass components it encounters along the way,
and returns the evaluated bandpass on a particular wavelength grid. You can
also generate bandpass in functional form (see :ref:`synphot:bandpass-main`).
The bandpass can then be convolved with spectral data
(see :ref:`synphot:source-spectrum-main`) to simulate HST (and soon JWST)
observations of particular targets. See :ref:`stsynphot-obsmode` for more
details.


.. _stsynphot-crds-overview:

CRDS Database
-------------

The **stsynphot** package is entirely data driven. That is, no information
pertaining to the physical description of instruments or their
throughput characteristics is contained within the software, but is
instead contained within an external "database." These data must be
available in order to run any **stsynphot** task. The dataset contains
the HST instrument graph, component lookup, and component throughput
tables, which are maintained and stored within the Calibration
Reference Data System (CRDS) at STScI. New versions of these tables
are created whenever new or updated calibration information become
available for the supported instruments. Users at STScI have automatic access
to the **stsynphot** dataset on all science computing clusters.
Because the dataset is not currently distributed along with this
software, off-site users must retrieve and install it separately before
they will be able to use **stsynphot** (see
:ref:`stsynphot-installation-setup`).

The instrument graph and component lookup tables are contained in
the ``mtab/`` subdirectory and are named ``*_tmg.fits``, ``*_tmc.fits``,
and ``*_tmt.fits``.
The component throughput tables are logically grouped into
subdirectories of ``comp/`` corresponding to each of the HST
instruments (``acs``, ``cos``, ``fgs``, ``foc``, ``fos``, ``hrs``, ``hsp``,
``nicmos``, ``nonhst``, ``ota``, ``stis``, ``wfc3``, ``wfpc``, and ``wfpc2``).
Component throughput table names contain a three digit suffix indicating their
version number.
You can determine which tables are new by comparing either their
names or creation dates with the corresponding set of tables
installed on your machine.

See :ref:`stsynphot-appendixc` for details on the structure of these tables.


.. _stsynphot-accuracy:

Result Accuracy
---------------

Because the **stsynphot** package is entirely data driven, the accuracy
of its results depends entirely on the accuracy of the bandpass
sensitivity curves and zero points in the CRDS database; i.e., dependent
on the instrument and photometric system under consideration.

As a general rule of thumb, synthetic photometry involving photometric
systems that have been defined from the ground, or photometry that is
given in VEGAMAG, should only be considered accurate to about 5%. The
accuracy is a strong function of wavelength and in particular for the
available calibration spectra in ``calspec`` sub-directory, the accuracy
might be about 5% shortward of 1700 Angstrom, where IUE is used,
and around 2% over the
STIS range. The accuracy is > 5% at the longer IR wavelengths where
the dust ring emission dominates (around 2 micron).

Synthetic photometry with the stable HST instrumentation, flying above
the atmosphere, when used in HST instrument natural systems, without
reference to VEGAMAG, can achieve accuracy much better than 5%; for
example, for ACS broadband filters it can be less or about 1%
(:ref:`De Marchi et al. 2004 <stsynphot-ref-demarchi2004>`).
For more details, see the Data Analysis section in the Data Handbooks
for the respective instruments.

In regards to agreement with ASTROLIB PYSYNPHOT, see
:ref:`stsynphot_comm_report`.


.. _stsynphot-other-telescopes:

Usage for Other Telescopes
--------------------------

Because the tasks in **stsynphot** package are data driven (see
:ref:`stsynphot-crds-overview`), support for a new telescope could be added
without changing the software. The easiest way to construct the necessary data
files is to use the existing ones as templates.

You need to provide the following files and store them in ``$PYSYN_CDBS/mtab``
directory:

* One instrument graph table (``*_tmg.fits``).
* One component lookup table (``*_tmc.fits``).
* Optional: One thermal component lookup table (``*_tmt.fits``), which is only
  needed for thermal background calculations (e.g., IR instruments).

For each of the component that appears in the above graph and lookup tables,
you need to provide its throughput table (``*_syn.fits``). These are stored in
``$PYSYN_CDBS/comp/ins``, where ``ins`` is your instrument name (e.g., "acs").
Then, you need a copy of your own
`irafshortcuts.txt <https://github.com/spacetelescope/stsynphot_refactor/blob/master/stsynphot/data/irafshortcuts.txt>`_
and modify it to include a unique "IRAFNAME" to your new ``comp/ins``
sub-directory.

For accurate binning, you can also make your own copies of
`detectors.dat <https://github.com/spacetelescope/stsynphot_refactor/blob/master/stsynphot/data/detectors.dat>`_
(detector pixel scales) and
`wavecat.dat <https://github.com/spacetelescope/stsynphot_refactor/blob/master/stsynphot/data/wavecats/wavecat.dat>`_
(wavelength catalog) and modify them for your own instruments.
If your wavelength catalog points to other files, include those files in the
same directory as well. For accurate count rate calculation, it is important
to set the correct telescope collecting area (see below).

Finally, you can customize **stsynphot** to use the files you created by
utilizing its configuration system (see :ref:`stsynphot-installation-setup`).
The easiest way to do that is to modify your
``$HOME/.astropy/config/stsynphot.cfg`` with the following::

    # Graph, optical component, and thermal component tables
    graphtable = mtab$my_new_tmg.fits
    comptable = mtab$my_new_tmc.fits
    thermtable = mtab$my_new_tmt.fits

    # Telescope primary mirror collecting area in cm^2
    # NOTE: Set this to your actual telescope collecting area!
    area = 331830.72404

    # Wavelength catalog file
    wavecatfile = /my/local/data/wavecat.dat

    # Detector parameters file
    detectorfile = /my/local/data/detectors.dat

    # IRAF shortcuts file for stsynphot.stio.irafconvert()
    irafshortcutfile = /my/local/data/irafshortcuts.txt

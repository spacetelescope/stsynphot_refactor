.. _stsynphot-refdata:

Reference Data
==============

Reference data has its history in IRAF SYNPHOT::

    synphot> lpar refdata
    (area = 45238.93416) Telescope area in cm^2
    (grtbl = "mtab$*_tmg.fits") Instrument graph table
    (cmptbl = "mtab$*_tmc.fits") Instrument component table
    (mode = "a")

In **stsynphot**, this is managed via its configuration system
(``stsynphot.config.conf``). Its overview and setup are explained in
:ref:`stsynphot-installation-setup`. As you can see in its
`stsynphot.cfg <https://github.com/spacetelescope/stsynphot_refactor/blob/master/stsynphot/stsynphot.cfg>`_
file, the reference data management has been expanded to include the following:

* ``rootdir``, which is used in the absence of ``PYSYN_CDBS`` environment
  variable
* ``graphtable``, the instrument graph table
* ``comptable``, the instrument component table
* ``thermtable``, the instrument thermal component table
* ``waveset_array``, default wavelength set (mostly for backward compatibility)
* ``waveset``, description string for ``waveset_array``
* ``area``, the telescope collecting area in :math:`\text{cm}^{2}`
* ``clear_filter``, the string value indicating a clear filter in graph and
  component tables
* ``wavecatfile``, the file containing wavelength bins for all supported
  instruments
* ``detectorfile``, the file containing pixel scales and sizes for all
  supported instruments
* ``irafshortcutfile``, the file containing IRAF-style alias for data
  sub-directories relative to ``rootdir``

For the same telescope, most of the above configurable items are
set-and-forget, except for graph and component tables, which can be updated
from time to time as component throughput curves are revised. Leaving their
filenames as wildcards (``*``) ensures that you pick up the latest versions.
If you need to use specific tables (e.g., to reproduce an older result), you
can also set them to specific filenames. It is also possible to
:ref:`provide your data for other telescopes <stsynphot-other-telescopes>`.

For backward compatibilty, :func:`~stsynphot.config.showref` and
:func:`~stsynphot.config.getref` convenience functions are provided::

    >>> import stsynphot as stsyn
    >>> stsyn.showref()  # doctest: +SKIP
    graphtable: /my/local/dir/cdbs/mtab/0bf2050hm_tmg.fits
    comptable : /my/local/dir/cdbs/mtab/0ac1951am_tmc.fits
    thermtable: /my/local/dir/cdbs/mtab/tae17277m_tmt.fits
    area      : 45238.93416
    waveset   : Min: 500, Max: 26000, Num: 10000, Delta: None, Log: True
     [stsynphot.config]
    >>> stsyn.getref()  # doctest: +SKIP
    {'area': 45238.93416,
     'comptable': '/my/local/dir/cdbs/mtab/0ac1951am_tmc.fits',
     'graphtable': '/my/local/dir/cdbs/mtab/0bf2050hm_tmg.fits',
     'thermtable': '/my/local/dir/cdbs/mtab/tae17277m_tmt.fits',
     'waveset': 'Min: 500, Max: 26000, Num: 10000, Delta: None, Log: True'}

To change a configurable item's value, use the machinery of
:ref:`Astropy configuration system <astropy:astropy_config>`.
Examples shown are only for ``graphtable`` but they are similar for others
(in fact, usually all the graph and component tables are changed together)::

    >>> stsyn.conf.graphtable = '/path/to/my_new_tmg.fits'  # Entire session
    >>> stsyn.conf.reload('graphtable')  # Reload from stsynphot.cfg
    'mtab$*_tmg.fits'
    >>> stsyn.conf.reload()  # Reload everything
    >>> stsyn.conf.reset('graphtable')  # Reset to software default
    >>> stsyn.conf.reset()  # Reset everything
    >>> with stsyn.conf.set_temp('graphtable', '/path/to/my_new_tmg.fits'):
    ...     pass  # graphtable will only change inside this block


.. _refdata-graph-comp-tab:

Graph and Component Tables
--------------------------

The HST bandpass for available :ref:`observation modes <stsynphot-obsmode>`
are defined by ``graphtable`` and ``comptable``. In addition, for IR
instruments, thermal component is defined by ``thermtable``. These files are
described in detail in :ref:`Appendix C <stsynphot-appendixc>`.

The tables decide which throughput files will be used for a particular
observation mode. They can be displayed using
:meth:`~stsynphot.spectrum.ObservationSpectralElement.showfiles`.
A bandpass that does not rely on the tables does not have this feature.
For example::

    >>> bp_hst = stsyn.band('wfc3,ir,f105w')  # doctest: +SKIP
    >>> bp_hst.showfiles()  # doctest: +SKIP
    /my/local/dir/cdbs/comp/wfc3/wfc3_ir_primary_001_syn.fits
    /my/local/dir/cdbs/comp/wfc3/wfc3_ir_secondary_001_syn.fits
    /my/local/dir/cdbs/comp/wfc3/wfc3_pom_001_syn.fits
    /my/local/dir/cdbs/comp/wfc3/wfc3_ir_csm_001_syn.fits
    /my/local/dir/cdbs/comp/wfc3/wfc3_ir_fold_001_syn.fits
    /my/local/dir/cdbs/comp/wfc3/wfc3_ir_mir1_001_syn.fits
    /my/local/dir/cdbs/comp/wfc3/wfc3_ir_mir2_001_syn.fits
    /my/local/dir/cdbs/comp/wfc3/wfc3_ir_mask_001_syn.fits
    /my/local/dir/cdbs/comp/wfc3/wfc3_ir_rcp_001_syn.fits
    /my/local/dir/cdbs/comp/wfc3/wfc3_ir_f105w_004_syn.fits
    /my/local/dir/cdbs/comp/wfc3/wfc3_ir_win_001_syn.fits
    /my/local/dir/cdbs/comp/wfc3/wfc3_ir_qe_003_syn.fits
    /my/local/dir/cdbs/comp/wfc3/wfc3_ir_cor_004_syn.fits  [...]

    >>> from synphot import SpectralElement
    >>> bp_nonhst = SpectralElement.from_filter('johnson_v')  # doctest: +REMOTE_DATA
    >>> bp_nonhst.showfiles()  # doctest: +SKIP
    AttributeError: 'SpectralElement' object has no attribute 'showfiles'


.. _stsynphot-area:

Area
----

Some calculations require the telescope collecting area; e.g., flux conversion
involving count/OBMAG or :ref:`synphot:synphot-formula-uresp` calculation.
When an area is required, you may use the ``area`` value from **stsynphot**
configuration for convenience, as it is always set to the telescope collecting
area.

For :class:`~stsynphot.spectrum.ObservationSpectralElement` constructed
with :func:`~stsynphot.spectrum.band`, it also has its own
`~stsynphot.spectrum.ObservationSpectralElement.area` property, which is
usually the same as the configuration value *except* when overwritten by the
value (in :math:`\text{cm}^{2}`) of ``PRIMAREA`` keyword in the graph table's
primary header. This behavior is retained from ASTROLIB PYSYNPHOT to be
backward compatible. When in doubt, always provide the desired telescope area
explicitly by passing it into the ``area`` keyword, where applicable.


.. _refdata-wavecatfile:

Wavelength Catalog
------------------

Every HST observation mode has an optimally binned wavelength set (``binset``),
which ensures proper coverage and resolution, for constructing an
:ref:`synphot:synphot_observation`. The ``binset`` is set according to a
pre-defined wavelength catalog in ``wavecatfile`` and can be accessed via
`~stsynphot.spectrum.ObservationSpectralElement.binset`. For example::

    >>> from synphot import Observation
    >>> obs = Observation(stsyn.Vega, bp_hst, binset=bp_hst.binset)  # doctest: +SKIP
    >>> bp_hst.binset  # doctest: +SKIP
    <Quantity [  7000.,  7001.,  7002.,...,  17998., 17999., 18000.] Angstrom>
    >>> obs.binset  # doctest: +SKIP
    <Quantity [  7000.,  7001.,  7002.,...,  17998., 17999., 18000.] Angstrom>

For more details on how the catalog works, see the `~stsynphot.wavetable`
module. In most cases, there is no need to modify the catalog file as you can
simply use Numpy or other methods to generate your own wavelength array to be
used as ``binset`` should the catalog is insufficient.


.. _stsynphot-wavelength-table:

Wavelength Table
----------------

The wavelength table is a feature inherited from IRAF SYNPHOT, in which it is
known as ``wavetab``. It is used to specify the name of a file containing
a list of wavelength values that determine the wavelength grid to be used in
calculations and plotting. In **synphot** and **stsynphot**, this has been
replaced by various alternatives such as
`~synphot.spectrum.BaseSpectrum.waveset`,
`~synphot.observation.Observation.binset`, or simply providing sampling of
your choice in :py:meth:`~object.__call__`.

Nevertheless, for backward compatibility, the ``waveset_array`` is provided
and its default consists of 10000 points covering approximately 500 to 26000
Angstrom (sufficient for most HST calculations), spaced logarithmically with
:func:`~numpy.logspace` such that:

.. math::

    \log \lambda = \log \lambda_{\text{min}} + (\log \lambda_{\text{max}} - \log \lambda_{\text{min}}) \frac{i}{N}

where

* :math:`N` is the number of data points
* :math:`i` is the index value, starting from 0
* :math:`\lambda_{\text{min}}` and :math:`\lambda_{\text{max}}` are the
  wavelength limits

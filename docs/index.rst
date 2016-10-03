.. doctest-skip-all

.. _stsynphot_index:

*********************************************
Synthetic Photometry for HST/JWST (stsynphot)
*********************************************

Introduction
============

**stsynphot** is an extension to :ref:`synphot:astropy_synphot`
(:ref:`Lim 2016 <stsynphot-ref-lim2016>`) that implements
synthetic photometry package for HST (and soon JWST) support. The documentation
in this package is meant to *complement* that of **synphot**, which already
documents the non-observatory specific functionalities. It is recommended that
you read both for full understanding of its capabilities.

This package, in particular, allows you to:

* Construct spectra from various grids of model atmosphere spectra,
  parameterized spectrum models, and atlases of stellar spectrophotometry.
* Simulate observations specific to HST (and soon JWST).
* Compute photometric calibration parameters for any supported instrument mode.
* Plot instrument-specific sensitivity curves and calibration target spectra.

Like ASTROLIB PYSYNPHOT (:ref:`Lim et al. 2015 <stsynphot-ref-lim2015>`),
**stsynphot** can help HST (and soon JWST) observers to perform
cross-instrument simulations and examine the transmission curve of the
Optical Telescope Assembly (OTA) and spectra of calibration targets.

If you use **stsynphot** in your work, please cite it as,
"*Lim, P. L. 2016, stsynphot User's Guide
(Baltimore, MD: STScI), http://stsynphot.readthedocs.io/en/latest/*"

If you have questions or concerns regarding the software, please open an issue
at https://github.com/spacetelescope/stsynphot_refactor/issues (if not already
reported) or contact STScI Help Desk via ``help[at]stsci.edu``.


.. _stsynphot-installation-setup:

Installation and Setup
======================

**stsynphot** works under both Python 2 and 3. It requires the following
packages:

* numpy (>= 1.9)
* astropy (>= 1.3)
* scipy (>= 0.14)
* synphot (>= 0.1)
* matplotlib (optional for plotting)

You can install **stsynphot** using one of the following ways
(`AstroConda <http://astroconda.readthedocs.io/en/latest/>`_ support is planned
for a future release):

* From standalone release::

    pip install git+https://github.com/spacetelescope/stsynphot_refactor.git@0.1b1

* From source (example shown is for the ``dev`` version)::

    git clone https://github.com/spacetelescope/stsynphot_refactor.git
    cd stsynphot_refactor
    python setup.py install

As with ASTROLIB PYSYNPHOT, the data files for **stsynphot** are distributed
separately by
`Calibration Reference Data System <http://www.stsci.edu/hst/observatory/crds/throughput.html>`_.
They are expected to follow a certain directory structure under the root
directory, identified by the ``PYSYN_CDBS`` environment variable that *must* be
set prior to using this package. In the examples below, the root directory is
arbitrarily named ``/my/local/dir/cdbs/``.

In bash shell::

    export PYSYN_CDBS=/my/local/dir/cdbs/

In csh shell::

    setenv PYSYN_CDBS /my/local/dir/cdbs/

Below are the instructions to install:

.. toctree::
   :maxdepth: 1

   stsynphot/data_atlas
   stsynphot/data_hst
   stsynphot/data_jwst

To ensure consistency for all data files used, **stsynphot silently overwrites
synphot data file locations within the Python session**. For example::

    >>> from synphot.config import conf as syn_conf
    >>> print(syn_conf.johnson_v_file)
    ftp://ftp.stsci.edu/cdbs/comp/nonhst/johnson_v_004_syn.fits
    >>> from stsynphot.config import conf
    >>> print(conf.rootdir)
    /my/local/dir/cdbs/
    >>> print(syn_conf.johnson_v_file)
    /my/local/dir/cdbs//comp/nonhst/johnson_v_004_syn.fits

You can also take advantage of :ref:`astropy:astropy_config` to manage
**stsynphot** configuration and data files. For example, you can copy
`stsynphot.cfg <https://github.com/spacetelescope/stsynphot_refactor/blob/master/stsynphot/stsynphot.cfg>`_
to your ``$HOME/.astropy/config/`` directory and modify it to your needs::

    # This replaces the need to set PYSYN_CDBS environment variable
    rootdir = /my/local/dir/cdbs/

::

    # This pins lookup tables to a specific files
    graphtable = /my/local/dir/cdbs/mtab/07r1502mm_tmg.fits
    comptable = /my/local/dir/cdbs/mtab/07r1502nm_tmc.fits
    thermtable = /my/local/dir/cdbs/mtab/tae17277m_tmt.fits

::

    # JWST primary mirror collecting area in cm^2
    area = 331830.72404

.. note::

    In theory, you can use any ``astropy.config`` functionality
    (e.g. ``set_temp()``) to manage **stsynphot** configuration items.
    However, due to the complicated relationships between instrument-specific
    data files, it is not recommended unless you know what you are doing.


.. _stsynphot_getting_started:

Getting Started
===============

This section only contains minimal examples showing how to use this package.
For detailed documentation, see :ref:`stsynphot_using`. It is recommended that
you familiarize yourself with
:ref:`basic synphot functionality <synphot:synphot_getting_started>` first
before proceeding.

Display the current settings for graph and component tables, telescope area
(in squared centimeter), and default wavelength set (in Angstrom)::

    >>> import stsynphot as STS
    >>> STS.showref()
    graphtable: /my/local/dir/cdbs/mtab/07r1502mm_tmg.fits
    comptable : /my/local/dir/cdbs/mtab/07r1502nm_tmc.fits
    thermtable: /my/local/dir/cdbs/mtab/tae17277m_tmt.fits
    area      : 45238.93416
    waveset   : Min: 500, Max: 26000, Num: 10000, Delta: None, Log: True
     [stsynphot.config]

Note that **stsynphot** also overwrites **synphot** file locations for
consistency, as stated in :ref:`stsynphot-installation-setup` (the double
slash in path name does not affect software operation)::

    >>> import synphot
    >>> synphot.conf.vega_file
    '/my/local/dir/cdbs//calspec/alpha_lyr_stis_008.fits'

Plot the built-in Vega spectrum, which is used to compute VEGAMAG. This is
pre-loaded at start-up for convenience:

.. plot::
    :include-source:

    import stsynphot as STS
    from synphot import units
    STS.Vega.plot(right=20000, flux_unit=units.FLAM, title='Vega spectrum')

Construct a bandpass for HST/ACS camera using WFC1 detector and F555W filter;
Then, show all the individual throughput files used in its construction::

    >>> bp = STS.band('acs,wfc1,f555w')
    >>> bp.showfiles()
    INFO: #Throughput table names:
    /my/local/dir/cdbs/comp/ota/hst_ota_007_syn.fits
    /my/local/dir/cdbs/comp/acs/acs_wfc_im123_004_syn.fits
    /my/local/dir/cdbs/comp/acs/acs_f555w_wfc_006_syn.fits
    /my/local/dir/cdbs/comp/acs/acs_wfc_ebe_win12f_005_syn.fits
    /my/local/dir/cdbs/comp/acs/acs_wfc_ccd1_mjd_021_syn.fits [...]

Construct a source spectrum from Kurucz 1993 Atlas of Model Atmospheres for a
star with blackbody temperature of 5770 Kelvin, at solar metallicity, and log
surface gravity of 4.5, renormalized to 20 VEGAMAG in Johnson *V* filter,
using IRAF SYNPHOT syntax::

    >>> sp = STS.parse_spec(
    ...     'rn(icat(k93models,5770,0.0,4.5),band(johnson,v),20,vegamag)')

Construct an extinction curve for Milky Way (diffuse) with :math:`E(B-V)` of
0.7 mag. Then, apply the extinction to the source spectrum from before::

    >>> ext = STS.ebmvx('mwavg', 0.7)
    >>> sp_ext = sp * ext

Construct an observation using the ACS bandpass and the extincted source
spectrum. (For accurate detector binning, you can pass in the binned wavelength
centers into ``binset``. In this case, the bin centers for that particular
observation mode is stored in ``bp.binset``.) Then, compute the count rate
for HST collecting area::

    >>> from synphot import Observation
    >>> obs = Observation(sp_ext, bp, binset=bp.binset)
    >>> obs.countrate(area=STS.config.conf.area)
    <Quantity 23.839134880103543 ct / s>

To find out exactly how ``bp.binset`` was computed, you can use the following
command, which states that the information for this particular ACS observation
mode in use is stored in ``wavecats/acs.dat`` in the **stsynphot** software
data directory (``synphot$``, which is named so for backward compatibility
with ASTROLIB PYSYNPHOT)::

    >>> STS.wavetable.WAVECAT['acs,wfc1,f555w']
    'synphot$wavecats/acs.dat'

Calculate thermal background for a HST/WFC3 bandpass for its IR detector using
F110W filter::

    >>> wfc3 = STS.band('wfc3,ir,f110w')
    >>> wfc3.thermback()
    <Quantity 0.051636304994833425 ct / (pix s)>


.. _stsynphot_using:

Using **stsynphot**
===================

# UNTIL HERE - reorganize?

.. toctree::
   :maxdepth: 1

   stsynphot/overview
   stsynphot/from_pysyn_iraf
   stsynphot/obsmode
##   stsynphot/spectrum
##   stsynphot/catalog
##   stsynphot/tables
   stsynphot/commissioning
   stsynphot/ref_api
   stsynphot/biblio

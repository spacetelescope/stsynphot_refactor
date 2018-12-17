.. doctest-skip-all

.. _atlas_data_files:

Atlases and calibration spectra files
=====================================

These data files are needed for calculations involving source spectra.
To install them locally, first download these tarballs:

* http://ssb.stsci.edu/cdbs/tarfiles/synphot2.tar.gz
* http://ssb.stsci.edu/cdbs/tarfiles/synphot3.tar.gz
* http://ssb.stsci.edu/cdbs/tarfiles/synphot4.tar.gz
* http://ssb.stsci.edu/cdbs/tarfiles/synphot5.tar.gz
* http://ssb.stsci.edu/cdbs/tarfiles/synphot6.tar.gz

Move them to the appropriate location and then extract them::

    $ tar -xzf synphot2.tar.gz
    $ tar -xzf synphot3.tar.gz
    $ tar -xzf synphot4.tar.gz
    $ tar -xzf synphot5.tar.gz
    $ tar -xzf synphot6.tar.gz
    $ rm *.tar.gz

.. note::

    Downloading and extracting the files might take a while as the
    tarballs combined are almost 700 MB.

Once installation is complete, you will see some sub-directories containing
data as described below:

+------------------------------------------+----------------+---------------+
|Description                               |Sub-directory   |Tarball        |
+==========================================+================+===============+
|Interstellar extinction curves            |extinction      |synphot2.tar.gz|
+------------------------------------------+----------------+               |
|AGN templates                             |grid/agn        |               |
+------------------------------------------+----------------+               |
|Bruzual-Charlot galaxy spectra            |grid/bc95       |               |
+------------------------------------------+----------------+               |
|Buser-Kurucz stellar atlas                |grid/bkmodels   |               |
+------------------------------------------+----------------+               |
|Bruzual-Persson-Gunn-Stryker stellar atlas|grid/bpgs       |               |
+------------------------------------------+----------------+               |
|Bruzual stellar atlas                     |grid/bz77       |               |
+------------------------------------------+----------------+               |
|Galactic emission line objects            |grid/galactic   |               |
+------------------------------------------+----------------+               |
|Gunn-Stryker atlas                        |grid/gunnstryker|               |
+------------------------------------------+----------------+               |
|Jacobi-Hunter-Christian stellar atlas     |grid/jacobi     |               |
+------------------------------------------+----------------+               |
|Kinney-Calzetti galaxy spectra            |grid/kc96       |               |
+------------------------------------------+----------------+               |
|Pickles stellar atlas                     |grid/pickles    |               |
+------------------------------------------+----------------+---------------+
|Castelli & Kurucz (2004) stellar atlas    |grid/ck04models |synphot3.tar.gz|
+------------------------------------------+----------------+---------------+
|Kurucz (1993) stellar atlas               |grid/k93models  |synphot4.tar.gz|
+------------------------------------------+----------------+---------------+
|Phoenix stellar atlas                     |grid/phoenix    |synphot5.tar.gz|
+------------------------------------------+----------------+---------------+
|HST calibration spectra                   |calspec         |synphot6.tar.gz|
+------------------------------------------+----------------+---------------+

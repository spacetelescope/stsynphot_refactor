.. _atlas_data_files:

Atlases and calibration spectra files
=====================================

These data files are needed for calculations involving source spectra.
To install them locally, please download the relevant tarballs from
`HLSP Reference Atlases <https://archive.stsci.edu/hlsp/reference-atlases>`_.
Then, move them to the appropriate location and extract them::

    $ tar -xvf <filename>.tar
    $ rm <filename>.tar

.. note::

    Downloading and extracting the files might take a while as the
    tarballs combined are over 700 MB.

Once installation is complete, you will see some sub-directories containing
data as described below:

+------------------------------------------+----------------+
|Description                               |Sub-directory   |
+==========================================+================+
|Interstellar extinction curves            |extinction      |
+------------------------------------------+----------------+
|AGN templates                             |grid/agn        |
+------------------------------------------+----------------+
|Bruzual-Charlot galaxy spectra            |grid/bc95       |
+------------------------------------------+----------------+
|Buser-Kurucz stellar atlas                |grid/bkmodels   |
+------------------------------------------+----------------+
|Bruzual-Persson-Gunn-Stryker stellar atlas|grid/bpgs       |
+------------------------------------------+----------------+
|Brown galaxy atlas                        |grid/brown      |
+------------------------------------------+----------------+
|Bruzual stellar atlas                     |grid/bz77       |
+------------------------------------------+----------------+
|Galactic emission line objects            |grid/galactic   |
+------------------------------------------+----------------+
|Gunn-Stryker atlas                        |grid/gunnstryker|
+------------------------------------------+----------------+
|Jacobi-Hunter-Christian stellar atlas     |grid/jacobi     |
+------------------------------------------+----------------+
|Kinney-Calzetti galaxy spectra            |grid/kc96       |
+------------------------------------------+----------------+
|Pickles stellar atlas                     |grid/pickles    |
+------------------------------------------+----------------+
|Castelli & Kurucz (2004) stellar atlas    |grid/ck04models |
+------------------------------------------+----------------+
|Kurucz (1993) stellar atlas               |grid/k93models  |
+------------------------------------------+----------------+
|Phoenix stellar atlas                     |grid/phoenix    |
+------------------------------------------+----------------+
|HST calibration spectra                   |calspec         |
+------------------------------------------+----------------+

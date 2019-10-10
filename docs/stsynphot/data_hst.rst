.. _hst_data_files:

HST data files
==============

These data files are needed for calculations involving HST bandpasses.
To install them locally, first download
http://ssb.stsci.edu/cdbs/tarfiles/synphot1.tar.gz .
Move it to the appropriate location and then extract it::

    $ tar -xzf synphot1.tar.gz
    $ rm synphot1.tar.gz

.. note::

    Downloading and extracting the files might take a while as the
    tarball itself is almost 100 MB.

Once installation is complete, you will see some sub-directories containing
data as described below:

+----------------------------+-------------+
|Description                 |Sub-directory|
+============================+=============+
|Master tables               |mtab         |
+----------------------------+-------------+
|HST/ACS throughput tables   |comp/acs     |
+----------------------------+-------------+
|HST/COS throughput tables   |comp/cos     |
+----------------------------+-------------+
|HST/FGS throughput tables   |comp/fgs     |
+----------------------------+-------------+
|HST/FOC throughput tables   |comp/foc     |
+----------------------------+-------------+
|HST/FOS throughput tables   |comp/fos     |
+----------------------------+-------------+
|HST/HRS throughput tables   |comp/hrs     |
+----------------------------+-------------+
|HST/HSP throughput tables   |comp/hsp     |
+----------------------------+-------------+
|HST/NICMOS throughput tables|comp/nicmos  |
+----------------------------+-------------+
|HST/OTA throughput tables   |comp/ota     |
+----------------------------+-------------+
|HST/STIS throughput tables  |comp/stis    |
+----------------------------+-------------+
|HST/WFC3 throughput tables  |comp/wfc3    |
+----------------------------+-------------+
|HST/WFPC1 throughput tables |comp/wfpc    |
+----------------------------+-------------+
|HST/WFPC2 throughput tables |comp/wfpc2   |
+----------------------------+-------------+
|Non-HST throughput tables   |comp/nonhst  |
+----------------------------+-------------+

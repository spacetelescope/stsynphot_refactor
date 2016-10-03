.. doctest-skip-all

.. _hst_data_files:

HST data files
==============

These data files are needed for calculations involving HST bandpasses.
To install them locally via anonymous FTP::

    $ cd /my/local/dir/cdbs
    $ ftp ftp.stsci.edu
    Name: anonymous
    Password: (Enter your email address)
    ftp> cd cdbs/tarfiles
    ftp> get synphot1.tar.gz
    ftp> quit
    $ tar -xzf synphot1.tar.gz
    $ rm synphot1.tar.gz

.. note::

    Downloading and extracting the files might take a while as the
    tarball itself is almost 100 MB. This is recommended for first-time
    installation.

    If you only need select files, you can also choose to download them
    individually from ftp://ftp.stsci.edu/cdbs/ to the relevant sub-directory.
    This is recommended for updating existing installation.

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

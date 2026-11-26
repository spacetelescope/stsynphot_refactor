# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""Test catalog.py module."""

# THIRD-PARTY
import numpy as np
import pytest
from astropy import units as u
from astropy.table import Table
from synphot import exceptions as synexceptions
from synphot import units

# LOCAL
from stsynphot import catalog, exceptions
from stsynphot import conf as stsyn_conf
from stsynphot.catalog import SYNPHOT_LT_1_9


@pytest.mark.remote_data
def test_grid_to_spec_k93():
    """Test creating spectrum from grid, and related cache."""
    sp = catalog.grid_to_spec("k93models", 6440, 0, 4.3)
    w = sp.waveset
    w_first_50 = w[:50]
    y_first_50 = units.convert_flux(w_first_50, sp(w_first_50), units.FLAM)
    w_last_50 = w[-50:]
    y_last_50 = units.convert_flux(w_last_50, sp(w_last_50), units.FLAM)

    assert "k93" in sp.meta["expr"]
    assert "header" not in sp.meta
    np.testing.assert_allclose(
        w_first_50.value,
        [
            90.90000153,
            93.50000763,
            96.09999847,
            97.70000458,
            99.59999847,
            102,
            103.80000305,
            105.6000061,
            107.70000458,
            110.40000153,
            114,
            117.79999542,
            121.30000305,
            124.79999542,
            127.09999847,
            128.40000916,
            130.5,
            132.3999939,
            133.90000916,
            136.6000061,
            139.80000305,
            143.30000305,
            147.19999695,
            151,
            155.20001221,
            158.80000305,
            162.00001526,
            166,
            170.30000305,
            173.40000916,
            176.80000305,
            180.20001221,
            181.69999695,
            186.1000061,
            191,
            193.8999939,
            198.40000916,
            201.80000305,
            205,
            210.5,
            216.20001221,
            219.80000305,
            223,
            226.80000305,
            230,
            234,
            240,
            246.5,
            252.3999939,
            256.80001831,
        ],
    )
    np.testing.assert_array_equal(y_first_50.value, 0)
    np.testing.assert_allclose(
        w_last_50.value,
        [
            83800,
            84200,
            84600,
            85000,
            85400,
            85800,
            86200,
            86600,
            87000,
            87400,
            87800,
            88200,
            88600,
            89000,
            89400,
            89800,
            90200,
            90600,
            91000,
            91400,
            91800,
            92200,
            92600,
            93000,
            93400,
            93800,
            94200,
            94600,
            95000,
            95400,
            95800,
            96200,
            96600,
            97000,
            97400,
            97800,
            98200,
            98600,
            99000,
            99400,
            99800,
            100200,
            200000,
            400000,
            600000,
            800000,
            1000000,
            1200000,
            1400000,
            1600000,
        ],
    )
    np.testing.assert_allclose(
        y_last_50.value,
        [
            2.52510792e03,
            2.47883842e03,
            2.43311637e03,
            2.38843415e03,
            2.34455095e03,
            2.30190141e03,
            2.25982266e03,
            2.21930715e03,
            2.17950029e03,
            2.14031198e03,
            2.10216378e03,
            2.06411734e03,
            2.02789000e03,
            1.99191291e03,
            1.95752853e03,
            1.92259620e03,
            1.88976666e03,
            1.85768178e03,
            1.82475330e03,
            1.79369145e03,
            1.76356796e03,
            1.73377904e03,
            1.70432192e03,
            1.67572220e03,
            1.64739969e03,
            1.61997833e03,
            1.59299008e03,
            1.56657219e03,
            1.54066436e03,
            1.51508799e03,
            1.49065412e03,
            1.46606232e03,
            1.44255637e03,
            1.41922753e03,
            1.39555249e03,
            1.37360936e03,
            1.35179525e03,
            1.33041182e03,
            1.30944458e03,
            1.28851215e03,
            1.26828580e03,
            1.24841065e03,
            8.04744247e01,
            5.03657385e00,
            9.88851448e-01,
            3.10885179e-01,
            1.26599425e-01,
            6.07383728e-02,
            3.26344365e-02,
            1.90505413e-02,
        ],
    )

    # Test cache
    key = list(catalog._CACHE.keys())[0]
    assert key.endswith("grid/k93models/catalog.fits")
    assert sorted(catalog._CACHE[key]) == ["files", "log_g", "metallicity", "t_eff"]

    # Reset cache
    catalog.reset_cache()
    assert catalog._CACHE == {}


@pytest.mark.remote_data
def test_grid_to_spec_phoenix():
    # Combo that is sensitive to grid search algorithm change
    sp = catalog.grid_to_spec("phoenix", 40500, -1.5, 4.2)
    np.testing.assert_allclose(sp([10, 9e06] * u.AA), [5.32014480e-36, 4.21149959e10] * units.PHOTLAM)

    # Make sure it copies on grid point
    sp = catalog.grid_to_spec("phoenix", 14000, -2.5, 2)
    sp.meta["changed"] = True
    sp2 = catalog.grid_to_spec("phoenix", 14000, -2.5, 2)
    assert "changed" not in sp2.meta
    assert sp2 is not sp


@pytest.mark.remote_data
@pytest.mark.parametrize(
    ("t", "m", "g"), [(3499, 0, 4.3), (50001, 0, 4.3), (6440, -6, 4.3), (6440, 2, 4.3), (6440, 0, -1), (6440, 0, 10)]
)
def test_grid_to_spec_bounds_check(t, m, g):
    """Test out of bounds check."""
    with pytest.raises(exceptions.ParameterOutOfBounds, match=".* exceeds data"):
        catalog.grid_to_spec("k93models", t, m, g)


def test_grid_to_spec_exceptions_1():
    """Test other exceptions."""
    with pytest.raises(synexceptions.SynphotError, match=".* catalog was not found"):
        catalog.grid_to_spec("foo", 6440, 0, 4.3)


@pytest.mark.remote_data
def test_grid_to_spec_exceptions_2():
    with pytest.raises(synexceptions.SynphotError, match="Quantity is not supported"):
        catalog.grid_to_spec("k93models", 6440, 0 * u.dimensionless_unscaled, 4.3)
    with pytest.raises(synexceptions.SynphotError, match="Quantity is not supported"):
        catalog.grid_to_spec("k93models", 6440, 0, 4.3 * u.dimensionless_unscaled)


def test_get_catalog_index_custom(tmp_path):
    """Test custom catalogs."""

    crgrid = tmp_path / "grid"  # As defined in irafshortcuts.txt
    crgrid.mkdir()

    # Mock a custom catalog.
    custom_name = "BTSettl_2015_test"
    custom_dir = crgrid / custom_name
    custom_dir.mkdir()
    data = [
        ("10000,-0.5,0.0", "BTSettl_2015_test_00000.fits"),
        ("10000,-0.5,0.5", "BTSettl_2015_test_00001.fits"),
        ("10000,-0.5,1.0", "BTSettl_2015_test_00002.fits"),
    ]
    cat_tab = Table(rows=data, names=["INDEX", "FILENAME"], dtype=["S14", "S46"])
    cat_tab.write(custom_dir / "catalog.fits", format="fits", overwrite=True)

    with stsyn_conf.set_temp("rootdir", str(tmp_path)):
        # Test whether we can get a valid catalog path for a custom catalog
        catkey, catdir = catalog.get_catalog_index(custom_name)
        catfiles = catalog._CACHE[catkey]["files"]
        assert catdir.endswith(custom_name)
        assert catfiles.size == 3


def test_get_spectrum_cache(tmp_path):
    """Each grid spectrum is read and validated once, until reset_cache()."""
    # Fake spectrum file
    wave = np.linspace(3000, 10000, 50) * u.AA
    flux = np.ones(50) * units.FLAM
    t = Table([wave, flux, np.zeros(50) * units.FLAM], names=["WAVELENGTH", "g40", "g45"])
    t.write(tmp_path / "grid_00001.fits", format="fits")

    # Desired parameters
    t_eff = 5000.0
    metallicity = 0.0
    log_g = 4.0
    fname = "grid_00001.fits[g40]"

    # Build a fake catalog cache because this is not a real catalog.
    catalog.reset_cache()
    catdir = str(tmp_path)
    cachekey = str(tmp_path / "catalog.fits")
    catalog._CACHE[cachekey] = {
        "t_eff": np.array([t_eff]),
        "metallicity": np.array([metallicity]),
        "log_g": np.array([log_g]),
        "files": np.array([fname]),
    }

    with pytest.raises(KeyError, match=".* is not cached"):
        catalog._get_spectrum(t_eff, metallicity, log_g, cachekey, catdir, cache_only=True)

    sp_1 = catalog._get_spectrum(t_eff, metallicity, log_g, cachekey, catdir)

    # Header should have been discarded on read for synphot 1.9 or later.
    if SYNPHOT_LT_1_9:
        assert "SIMPLE" in sp_1.meta["header"]
    else:
        assert sp_1.meta["header"] == {}

    sp_2 = catalog._get_spectrum(t_eff, metallicity, log_g, cachekey, catdir, cache_only=True)
    assert sp_2 is sp_1

    # A spectrum without valid data raises every time, from one read.
    bad_g = 4.5
    with pytest.raises(exceptions.ParameterOutOfBounds, match=".* no valid data"):
        catalog._get_spectrum(t_eff, metallicity, bad_g, cachekey, catdir)
    with pytest.raises(exceptions.ParameterOutOfBounds, match=".* no valid data"):
        catalog._get_spectrum(t_eff, metallicity, bad_g, cachekey, catdir, cache_only=True)

    catalog.reset_cache()
    assert catalog._CACHE == {}
    assert catalog._SPECTRUM_CACHE == {}

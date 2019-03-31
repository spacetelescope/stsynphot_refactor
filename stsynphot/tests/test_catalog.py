# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""Test catalog.py module."""

# THIRD-PARTY
import numpy as np
import pytest

# ASTROPY
from astropy import units as u

# SYNPHOT
from synphot import exceptions as synexceptions
from synphot import units

# LOCAL
from .. import catalog, exceptions


@pytest.mark.remote_data
def test_grid_to_spec():
    """Test creating spectrum from grid, and related cache."""
    sp = catalog.grid_to_spec('k93models', 6440, 0, 4.3)
    w = sp.waveset
    w_first_50 = w[:50]
    y_first_50 = units.convert_flux(w_first_50, sp(w_first_50), units.FLAM)
    w_last_50 = w[-50:]
    y_last_50 = units.convert_flux(w_last_50, sp(w_last_50), units.FLAM)

    assert 'k93' in sp.meta['expr']
    np.testing.assert_allclose(
        w_first_50.value,
        [90.90000153, 93.50000763, 96.09999847, 97.70000458, 99.59999847, 102,
         103.80000305, 105.6000061, 107.70000458, 110.40000153, 114,
         117.79999542, 121.30000305, 124.79999542, 127.09999847, 128.40000916,
         130.5, 132.3999939, 133.90000916, 136.6000061, 139.80000305,
         143.30000305, 147.19999695, 151, 155.20001221, 158.80000305,
         162.00001526, 166, 170.30000305, 173.40000916, 176.80000305,
         180.20001221, 181.69999695, 186.1000061, 191, 193.8999939,
         198.40000916, 201.80000305, 205, 210.5, 216.20001221, 219.80000305,
         223, 226.80000305, 230, 234, 240, 246.5, 252.3999939, 256.80001831])
    np.testing.assert_array_equal(y_first_50.value, 0)
    np.testing.assert_allclose(
        w_last_50.value,
        [83800, 84200, 84600, 85000, 85400, 85800, 86200, 86600, 87000, 87400,
         87800, 88200, 88600, 89000, 89400, 89800, 90200, 90600, 91000, 91400,
         91800, 92200, 92600, 93000, 93400, 93800, 94200, 94600, 95000, 95400,
         95800, 96200, 96600, 97000, 97400, 97800, 98200, 98600, 99000, 99400,
         99800, 100200, 200000, 400000, 600000, 800000, 1000000, 1200000,
         1400000, 1600000])
    np.testing.assert_allclose(
        y_last_50.value,
        [2.52510792e+03, 2.47883842e+03, 2.43311637e+03, 2.38843415e+03,
         2.34455095e+03, 2.30190141e+03, 2.25982266e+03, 2.21930715e+03,
         2.17950029e+03, 2.14031198e+03, 2.10216378e+03, 2.06411734e+03,
         2.02789000e+03, 1.99191291e+03, 1.95752853e+03, 1.92259620e+03,
         1.88976666e+03, 1.85768178e+03, 1.82475330e+03, 1.79369145e+03,
         1.76356796e+03, 1.73377904e+03, 1.70432192e+03, 1.67572220e+03,
         1.64739969e+03, 1.61997833e+03, 1.59299008e+03, 1.56657219e+03,
         1.54066436e+03, 1.51508799e+03, 1.49065412e+03, 1.46606232e+03,
         1.44255637e+03, 1.41922753e+03, 1.39555249e+03, 1.37360936e+03,
         1.35179525e+03, 1.33041182e+03, 1.30944458e+03, 1.28851215e+03,
         1.26828580e+03, 1.24841065e+03, 8.04744247e+01, 5.03657385e+00,
         9.88851448e-01, 3.10885179e-01, 1.26599425e-01, 6.07383728e-02,
         3.26344365e-02, 1.90505413e-02])

    # Test cache
    key = list(catalog._CACHE.keys())[0]
    assert key.endswith('grid/k93models/catalog.fits')
    assert isinstance(catalog._CACHE[key], list)

    # Reset cache
    catalog.reset_cache()
    assert catalog._CACHE == {}


@pytest.mark.remote_data
@pytest.mark.parametrize(
    ('t', 'm', 'g'),
    [(3499, 0, 4.3),
     (50001, 0, 4.3),
     (6440, -6, 4.3),
     (6440, 2, 4.3),
     (6440, 0, -1),
     (6440, 0, 10)])
def test_grid_to_spec_bounds_check(t, m, g):
    """Test out of bounds check."""
    with pytest.raises(exceptions.ParameterOutOfBounds):
        catalog.grid_to_spec('k93models', t, m, g)


@pytest.mark.remote_data
def test_phoenix_gap():
    """
    https://github.com/spacetelescope/stsynphot_refactor/issues/44
    """
    catalog.grid_to_spec('phoenix', 2700, -1, 5.1)  # OK
    with pytest.raises(exceptions.ParameterOutOfBounds):
        catalog.grid_to_spec('phoenix', 2700, -0.5, 5.1)
    with pytest.raises(exceptions.ParameterOutOfBounds):
        catalog.grid_to_spec('phoenix', 2700, -0.501, 5.1)


def test_grid_to_spec_exceptions():
    """Test other exceptions."""
    # Invalid catalog
    with pytest.raises(synexceptions.SynphotError):
        catalog.grid_to_spec('foo', 6440, 0, 4.3)

    # Quantity is not acceptable for log values
    with pytest.raises(synexceptions.SynphotError):
        catalog.grid_to_spec(
            'k93models', 6440, 0 * u.dimensionless_unscaled, 4.3)
    with pytest.raises(synexceptions.SynphotError):
        catalog.grid_to_spec(
            'k93models', 6440, 0, 4.3 * u.dimensionless_unscaled)

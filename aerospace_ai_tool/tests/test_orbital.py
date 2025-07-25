import os
import pytest
from physics_modules import orbital_mechanics

def test_hohmann_delta_v():
    r1 = 6771000  # LEO (m)
    r2 = 42164000  # GEO (m)
    delta_v, dv1, dv2 = orbital_mechanics.hohmann_delta_v(r1, r2)
    assert delta_v > 0
    assert abs(dv1) > 0
    assert abs(dv2) > 0

def test_tsiolkovsky_fuel_mass():
    m0 = 10000
    delta_v = 10000
    Isp = 300
    fuel_mass, mf = orbital_mechanics.tsiolkovsky_fuel_mass(m0, delta_v, Isp)
    assert fuel_mass > 0
    assert mf > 0
    assert m0 > mf

def test_burn_time():
    fuel_mass = 1000
    Isp = 300
    thrust = 10000
    burn = orbital_mechanics.burn_time(fuel_mass, Isp, thrust)
    assert burn > 0

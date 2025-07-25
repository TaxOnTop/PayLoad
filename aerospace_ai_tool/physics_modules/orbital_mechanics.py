import numpy as np

def hohmann_delta_v(r1, r2, mu=3.986e14):
    """
    Calculate the total delta-v for a Hohmann transfer between two circular orbits.
    r1: initial orbit radius (meters)
    r2: target orbit radius (meters)
    mu: standard gravitational parameter (Earth default)
    Returns: (delta_v_total, delta_v1, delta_v2)
    """
    v1 = np.sqrt(mu / r1)
    v2 = np.sqrt(mu / r2)
    a_transfer = (r1 + r2) / 2
    v_transfer1 = np.sqrt(mu * (2/r1 - 1/a_transfer))
    v_transfer2 = np.sqrt(mu * (2/r2 - 1/a_transfer))
    delta_v1 = v_transfer1 - v1
    delta_v2 = v2 - v_transfer2
    delta_v_total = abs(delta_v1) + abs(delta_v2)
    return delta_v_total, delta_v1, delta_v2

def tsiolkovsky_fuel_mass(m0, delta_v, Isp, g0=9.80665):
    """
    Calculate fuel mass required using the Tsiolkovsky rocket equation.
    m0: initial mass (kg)
    delta_v: required delta-v (m/s)
    Isp: specific impulse (s)
    g0: standard gravity (m/s^2)
    Returns: fuel_mass (kg), final_mass (kg)
    """
    mf = m0 / np.exp(delta_v / (Isp * g0))
    fuel_mass = m0 - mf
    return fuel_mass, mf

def burn_time(fuel_mass, Isp, thrust, g0=9.80665):
    """
    Calculate total burn time.
    fuel_mass: mass of propellant (kg)
    Isp: specific impulse (s)
    thrust: engine thrust (N)
    g0: standard gravity (m/s^2)
    Returns: burn_time (seconds)
    """
    mdot = thrust / (Isp * g0)
    return fuel_mass / mdot

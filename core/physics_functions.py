#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  8 20:32:53 2025

@author: haleycole

Inputs: TLE/orbit params (alt, inc, eccentricity), spacecraft area/mass or ballistic coefficient (optional), chosen epoch.
Core outputs (MVP): atmospheric density estimate at orbit alt, predicted drag acceleration (or ballistic drag coefficient × density), estimated orbital decay trend (delta semi-major axis or lifetime estimate), confidence indicator.
Optional overlay (MVP+): upstream space-weather forecast panel (Kp / F10.7 / solar flux trend) and simple “impact score” for drag anomalies.

Pick the core atmospheric model(s):
    Start with a well-known empirical model: NRLMSISE-00 (or JB2008 if licensing permits). Have an architecture allowing model swap-in later.

Identify required space-weather data sources:
    Solar flux indices (F10.7), geomagnetic indices (Kp, Ap, Dst), solar wind (OMNI/DSCOVR). Use public feeds (NOAA SWPC, NASA OMNI) for MVP.

Collect historical datasets for validation:
    Historical TLE archives (Celestrak), satellite reentry/decay logs, and historical indices from OMNI/NOAA.
"""
import spaceweather as sw
import pandas as pd
import numpy as np

def calc_drag_acceleration(Cd, A, m, rho, v_rel):
    """
    
    | Symbol           | Meaning                                            | Typical Units                                 |
    | ---------------- | -------------------------------------------------- | --------------------------------------------- |
    | (a_d)            | Drag acceleration (opposite velocity)              | m/s²                                          |
    | (C_D)            | Drag coefficient (depends on shape/surface)        | dimensionless (≈ 2.0–2.5 for most satellites) |
    | (A)              | Cross-sectional area exposed to flow               | m²                                            |
    | (m)              | Mass of spacecraft                                 | kg                                            |
    | (\rho)           | Atmospheric density at orbital altitude            | kg/m³                                         |
    | (v_{\text{rel}}) | Relative velocity of spacecraft through atmosphere | m/s                                           |

    Area-to-mass ratio (A/m) is a key design parameter; small satellites often 
    have A/m∼0.01−0.1 m2/kg
    Input could be A and m or just the ratio directly.
    """
    
    a_d = -1/2 * Cd * A/m * rho * v_rel**2
    return a_d


def get_atm_density():
    # Total mass density
    return 0


# Constants
omega_E = 7.2921159e-5  # rad/s
R_E = 6371e3  # m

def relative_velocity(r_eci, v_eci):
    """Compute relative velocity vector and magnitude (m/s)"""
    omega_vec = np.array([0, 0, omega_E])
    v_atm = np.cross(omega_vec, r_eci)  # co-rotating atmosphere
    v_rel = v_eci - v_atm
    return v_rel, np.linalg.norm(v_rel)

print("A satellite travelling at 10 m/s at 1000 km would have a relative velocity of:", relative_velocity([500, 500, 1000], 10))


# Input: Date and time
# Output: Kp and Ap indices
df_3h = sw.ap_kp_3h()
print(df_3h.loc["2000-01-01 01:30:00"])


# Get the combined daily space weather data
# The 'update=True' argument ensures the latest data is downloaded if available.
# 'update_interval' can be adjusted, e.g., '1day', '7days', '30days'
sw_data = sw.celestrak.sw_daily(update=True)

# The returned object is a pandas DataFrame,
# containing columns for various space weather indices, including 'f107_obs' (observed F10.7)
# and 'f107_adj' (1 AU adjusted F10.7).

# To access the F10.7 observed values:
f107_observed = sw_data['f107_obs']

# To access the F10.7 1 AU adjusted values:
f107_adjusted = sw_data['f107_adj']

# You can also filter for specific dates if needed.
# For example, to get F10.7 for a specific date:
# specific_date = pd.Timestamp('2025-10-26')
# f107_on_date = sw_data.loc[specific_date, 'f107_obs']

print("Observed F10.7 data (first 5 entries):")
print(f107_observed.head())

print("\n1 AU Adjusted F10.7 data (first 5 entries):")
print(f107_adjusted.head())


"""
https://kauai.ccmc.gsfc.nasa.gov/instantrun/nrlmsis/
Input:
    lat
    lon
    alt
    date and time
    F10.7 daily and 3 month average
    AP (magnetic index) daily 
    
Output of the model includes:
    Helium number density
    Oxygen(O) number density
    Oxygen (O2) number density
    Nitrogen (N) number density
    Nitrogen (N2) number density
    Argon number density
    H Hydrogen number density
    total mass density
    Anomalous oxygen number density
    Exospheric temperature
    temperature at altitude


"""





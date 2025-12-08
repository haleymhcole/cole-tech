#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov  9 05:18:00 2025

@author: haleycole
"""

import numpy as np
from scipy.integrate import solve_ivp
from datetime import datetime
import ppigrf # or PyGeopack for better accuracy in complex environments
import pandas as pd


# def decimal_year(dt):
#     year_start = datetime(dt.year, 1, 1)
#     year_end = datetime(dt.year + 1, 1, 1)
#     return dt.year + ((dt - year_start).total_seconds() /
#                       (year_end - year_start).total_seconds())


def to_decimal_year(dt):
    """Convert datetime or pandas Timestamp to decimal year float."""
    if not isinstance(dt, datetime):
        dt = pd.to_datetime(dt)  # if user passed string or Timestamp

    year_start = datetime(dt.year, 1, 1)
    year_end = datetime(dt.year + 1, 1, 1)
    return dt.year + ((dt - year_start).total_seconds() /
                      (year_end - year_start).total_seconds())



# Function to calculate magnetic field (using IGRF as example)

def get_B_field(lat, lon, alt, date):
    """
    Compute the Earth's magnetic field vector using IGRF.

    Parameters:
        lat (float): Geodetic latitude [deg]
        lon (float): Geodetic longitude [deg]
        alt (float): Altitude above mean sea level [km]
        date (float): Decimal year (e.g., 2025.85)

    Returns:
        dict: {
            "Bx": float,  # ECEF X-component [T]
            "By": float,  # ECEF Y-component [T]
            "Bz": float,  # ECEF Z-component [T]
            "B_total": float,  # total field magnitude [T]
            "declination": float,  # magnetic declination [deg, east of north]
            "inclination": float   # magnetic inclination [deg, positive down]
        }
    """
    # --- Compute local magnetic field components (East, North, Up) in nT ---
    Be, Bn, Bu = ppigrf.igrf(lon, lat, alt, date)

    # --- Convert nT -> Tesla ---
    Be_T = Be * 1e-9
    Bn_T = Bn * 1e-9
    Bu_T = Bu * 1e-9

    # --- Derived scalar quantities (in local ENU frame) ---
    B_total = np.sqrt(Be_T**2 + Bn_T**2 + Bu_T**2)

    # Magnetic declination: eastward angle from geographic north
    declination = np.degrees(np.arctan2(Be_T, Bn_T))

    # Magnetic inclination: downward angle from horizontal (positive down)
    inclination = np.degrees(np.arctan2(Bu_T, np.sqrt(Be_T**2 + Bn_T**2)))

    # --- Convert to Earth-Centered Earth-Fixed (ECEF) Cartesian components ---
    lat_rad = np.radians(lat)
    lon_rad = np.radians(lon)

    # Convert from local ENU (Be, Bn, Bu) to ECEF (Bx, By, Bz)
    Bx = -np.sin(lat_rad)*np.cos(lon_rad)*Bn_T - np.sin(lon_rad)*Be_T + np.cos(lat_rad)*np.cos(lon_rad)*Bu_T
    By = -np.sin(lat_rad)*np.sin(lon_rad)*Bn_T + np.cos(lon_rad)*Be_T + np.cos(lat_rad)*np.sin(lon_rad)*Bu_T
    Bz = np.cos(lat_rad)*Bn_T + np.sin(lat_rad)*Bu_T

    return {
        "Bx": Bx,
        "By": By,
        "Bz": Bz,
        "B_total": B_total,
        "declination": declination,
        "inclination": inclination
    }


# Function to solve the equation of motion for a charged particle (Lorentz force)
def particle_trajectory(t, state, charge, mass, date):
    # state = [x, y, z, vx, vy, vz]
    x, y, z, vx, vy, vz = state
    lat, lon, alt = ... # convert cartesian to geodetic for B field model input
    decimal_yr = to_decimal_year(date)
    Bx, By, Bz = get_B_field(lat, lon, alt, decimal_yr)
    
    # Lorentz force F = q(E + v x B) - assuming E=0 for this simplified model
    # a = F/m = (q/m) * (v x B)
    # dv/dt = (charge/mass) * np.cross([vx, vy, vz], [Bx, By, Bz])
    ax, ay, az = ... # calculate components
    
    return [vx, vy, vz, ax, ay, az]


if __name__ == "__main__":
    # Example: Boulder, CO, altitude 1.6 km, November 2025
    lat, lon, alt = 40.0, -105.3, 1.6
    date = datetime(2025, 11, 1)
    
    #decimal = to_decimal_year(date)
    # print("Decimal Year:", decimal)
    # print("\n")
    B = get_B_field(lat, lon, alt, date)
    print(B)
    
    

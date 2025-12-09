# -*- coding: utf-8 -*-
"""
Created on Fri Dec  5 07:22:39 2025

@author: haley
https://docs.sunpy.org/en/stable/generated/gallery/plotting/solar_cycle_example.html
"""
import matplotlib.pyplot as plt
import astropy.units as u
from astropy.time import Time, TimeDelta
from astropy.visualization import time_support
import sunpy.timeseries as ts
from sunpy.net import Fido
from sunpy.net import attrs as a
from sunpy.time import TimeRange
import numpy as np
from scipy.optimize import curve_fit
import pandas as pd
import os


# =============================================================================
# Load Data
# =============================================================================
time_range = TimeRange("1700-01-01 00:00", Time.now())
result = Fido.search(a.Time(time_range), a.Instrument('noaa-indices'))
f_noaa_indices = Fido.fetch(result)
result = Fido.search(a.Time(time_range.end, time_range.end + TimeDelta(4 * u.year)),
                     a.Instrument('noaa-predict'))
f_noaa_predict = Fido.fetch(result)

noaa = ts.TimeSeries(f_noaa_indices, source='noaaindices').truncate(time_range)
noaa_predict = ts.TimeSeries(f_noaa_predict, source='noaapredictindices')

# =============================================================================
# Fit Data
# =============================================================================
sc_db =  pd.read_excel(os.path.join("Data", "Solar Cycle Database.xlsx"))
sc_db = sc_db[['Solar Cycle', 'Year', 'Month', 'Quarter', 'Timestep', 
              'Duration (Mo.)', 'Is_Final_Timestep', 'Magnetic Cycle Even']]

sn = noaa.quantity('sunspot RI')
sc_db["Sunspot Number"] = None
for t,time in enumerate(noaa.time):
    yr = time.ymdhms.year
    mo = time.ymdhms.month
    # row_to_update = sc_db.loc[(sc_db['Year']==yr)&(sc_db['Month']==mo)]

    # Boolean mask of the matching row(s)
    mask = (sc_db["Year"] == yr) & (sc_db["Month"] == mo)

    # Update the matching row(s) with the sunspot value
    sc_db.loc[mask, "Sunspot Number"] = sn[t]
    
sn_fits = {}
for solcyc in range(6,25): #sc_db['Solar Cycle'].unique():
    # Fit.
    t = sc_db['Timestep'].loc[sc_db['Solar Cycle']==solcyc].values
    y = sc_db['Sunspot Number'].loc[sc_db['Solar Cycle']==solcyc].values
    years = sc_db['Year'].loc[sc_db['Solar Cycle']==solcyc]
    months = sc_db['Month'].loc[sc_db['Solar Cycle']==solcyc]
    SN0 = sc_db['Sunspot Number'].loc[sc_db['Solar Cycle']==solcyc-1].iloc[-1]
    
    def custom_fit(t, mu1, mu2, sigma1, sigma2, A1, A2):
        """
        Based on asymmetric Gaussian function.
        t = timestep
        SN0 = starting sunspot number, or last sunspot number from previous cycle
        """
        curve1 = A1 * np.exp(-((t - mu1)**2) / (2 * sigma1**2))
        curve2 = A2 * np.exp(-((t - mu2)**2) / (2 * sigma2**2))
        return SN0 + curve1 + curve2
    
    # Estimate parameters.
    A1 = np.nanmax(y)
    A2 = A1
    sigma1 = 40  # Spread on the left side
    sigma2 = -60  # Spread on the right side
    mu = t[np.argmax(y)] if len(y) > 0 else 0  # Peak location
    mu1 = mu-5
    mu2 = mu+5
    try:
        params,__ = curve_fit(custom_fit, t, y, p0=(mu1, mu2, sigma1, sigma2, A1, A2))
    except:
        params = np.ones(6)*np.nan
    fit = custom_fit(t, *params)
    
    dates = []
    for i in range(len(years)):
        dates.append(Time(f"{years.iloc[i]}-{months.iloc[i]:02d}-01", format="iso"))
    sn_fits[solcyc] = (dates, fit)

# =============================================================================
# Plot
# =============================================================================
time_support()
fig, ax = plt.subplots(figsize=(12,4))
ax.plot(noaa.time, noaa.quantity('sunspot RI'), label='Sunspot Number', lw=1)
ax.plot(
    noaa_predict.time, noaa_predict.quantity('sunspot'),
    color='grey', label='Near-term Prediction'
)
ax.fill_between(
    noaa_predict.time, noaa_predict.quantity('sunspot low'),
    noaa_predict.quantity('sunspot high'), alpha=0.3, color='grey'
)

for solcyc in sn_fits:
    (dates, fit) = sn_fits[solcyc]
    ax.plot(Time(dates), fit, color='red')

ax.set_xlim(Time('1950-01-01'), Time('2025-01-01'))
ax.set_ylim(bottom=0)
ax.set_ylabel('Sunspot Number')
ax.set_xlabel('Year')
ax.legend()
plt.show()
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  4 09:32:35 2025

@author: haley

Combine the CME and Solar Cycle (SC) databases.
"""
import os
import pandas as pd
from datetime import datetime
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def asymmetric_gaussian(x, mu, sigma_1, sigma_2, A):
    """
    Asymmetric Gaussian function.
    """
    return np.where(
        x <= mu,
        A * np.exp(-((x - mu)**2) / (2 * sigma_1**2)),  # Left side
        A * np.exp(-((x - mu)**2) / (2 * sigma_2**2))   # Right side
    )

cme_db = pd.read_excel(os.path.join("Data", "CDAW Nominal and Severe Database.xlsx"))
sc_db =  pd.read_excel(os.path.join("Data", "Solar Cycle Database.xlsx"))

sc_db = sc_db.loc[sc_db['Year']>=1996]

def continuous_day_calendar(row):
    # Convert year, month, and day to the count of days since a set epoch.
    # Set epoch to midnight on Jan 1, 1996.
    epoch = datetime(1996, 1, 1, 0, 0, 0)
    year = int(row['Year'])
    month = int(row['Month'])
    date = datetime(year, month, 1, 0, 0, 0)
    
    # Get total seconds since epoch. Convert seconds to days.
    diff_seconds = (date - epoch).total_seconds()
    diff_days = diff_seconds/86400
    return diff_days

sc_db['Days Since Epoch'] = sc_db.apply(continuous_day_calendar, axis=1)

# According to the conventions used by NOAA Space Weather Prediction Center (SWPC)
# — and the historical sunspot-number database maintained by SILSO / Royal 
# Observatory of Belgium — the “smoothed monthly sunspot number” is computed 
# using a 13-month moving average. Use the same window size to get the 
# moving average for CME data.
window_size = 13 # months
window_size = window_size * 30 # days
raw_data = cme_db['Linear Speed [km/s]'].values
moving_ave = np.ones(raw_data.shape)*np.nan
for i in range(window_size, len(raw_data)-window_size):
    window = raw_data[i-window_size:i+window_size]
    average = np.mean(window)
    moving_ave[i] = average
    
cme_db['Smoothed Linear Speed [km/s]'] = moving_ave


fig, ax1 = plt.subplots(figsize=(10,6))
ax1.scatter(cme_db['Days Since Epoch'], cme_db['Linear Speed [km/s]'], s=5, color='skyblue', label='Linear Speed [km/s]')
ax1.plot(cme_db['Days Since Epoch'], cme_db['Smoothed Linear Speed [km/s]'], color='tab:blue', label='Smoothed Linear Speed [km/s]')
ax1.set_yscale('log')
ax1.set_ylabel('Linear Speed [km/s]')
ax1.set_xlabel('Time Index')

ax2 = ax1.twinx()
ax2.plot(sc_db['Days Since Epoch'], sc_db['ssn'], marker='.', color='orange', label='Sunspot Number')
ax2.plot(sc_db['Days Since Epoch'], sc_db['smoothed_ssn'], color='red', label='Smoothed Sunspot Number')
ax2.set_ylabel('Sunspot Number')
fig.legend(loc="upper left", bbox_to_anchor=(0.15, 0.85)) # Adjust legend position 
plt.savefig(os.path.join("Images", "linear speed vs SC.png"), dpi=300)
plt.close()



start_index = 7500
fig, ax1 = plt.subplots(figsize=(10,6))
#ax1.scatter(cme_db['Days Since Epoch'], cme_db['Linear Speed [km/s]'], s=5, color='skyblue', label='Linear Speed [km/s]')
ax1.plot(cme_db['Days Since Epoch'], cme_db['Smoothed Linear Speed [km/s]'], color='tab:blue', label='Smoothed Linear Speed [km/s]')
ax1.set_yscale('log')
ax1.set_ylabel('Linear Speed [km/s]')
ax1.set_xlabel('Time Index')
cme_data = cme_db['Smoothed Linear Speed [km/s]'].loc[cme_db['Days Since Epoch']>start_index]
ax1.set_ylim([cme_data.min(), cme_data.max()])  #[1e2, 1e3])

ax2 = ax1.twinx()
ax2.plot(sc_db['Days Since Epoch'], sc_db['ssn'], marker='.', color='orange', label='Sunspot Number')
ax2.plot(sc_db['Days Since Epoch'], sc_db['smoothed_ssn'], color='red', label='Smoothed Sunspot Number')
ax2.set_ylabel('Sunspot Number')

ax1.set_xlim([start_index, max(cme_db['Days Since Epoch'])])
fig.legend(loc="upper left", bbox_to_anchor=(0.15, 0.85)) # Adjust legend position 
plt.savefig(os.path.join("Images", "linear speed vs SC -- realtime.png"), dpi=300)
plt.show()
plt.close()

# Compare smoothed CME linear speed with smoothed sunspot number.
plt.figure(figsize=(8,4))
speed = cme_db['Smoothed Linear Speed [km/s]'] / cme_db['Smoothed Linear Speed [km/s]'].max()
plt.plot(cme_db['Days Since Epoch'], speed, color='tab:blue', label='Smoothed Linear Speed [km/s]')
plt.xlabel('Time Index')
ssn = sc_db['smoothed_ssn'] / sc_db['smoothed_ssn'].max()
plt.plot(sc_db['Days Since Epoch'], ssn, color='red', label='Smoothed Sunspot Number')

A = sc_db['A']
mu = sc_db['mu']
sigma_1 = sc_db['sigma_1']
sigma_2 = sc_db['sigma_2']
fit = asymmetric_gaussian(sc_db['Timestep'], mu, sigma_1, sigma_2, A)
plt.plot(sc_db['Days Since Epoch'], fit/np.nanmax(fit), color='m', label='SN Fit')

test = asymmetric_gaussian(sc_db['Timestep'], mu, sigma_1*1.3, sigma_2*1.9, A/4+100)
plt.plot(sc_db['Days Since Epoch'], test/np.nanmax(test), color='k', label='Fit Speed from SN') 

plt.legend()
plt.show()
# plt.savefig(os.path.join("Images", "linear speed vs SC.png"), dpi=300)
plt.close()

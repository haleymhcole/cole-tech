"""
Column Name 	Description
year	The observation year.
month	The observation month.
day	The observation day.
bsrn	Bartels Solar Rotation Number.
f10.7_obs	Observed 10.7 cm solar radio flux (F10.7 flux).
f10.7_adj	F10.7 flux adjusted to 1 AU (Astronomical Unit).
f10.7_obs_81d	Centered 81-day arithmetic average of observed F10.7 flux.
f10.7_adj_81d	Centered 81-day arithmetic average of F10.7 flux adjusted to 1 AU.
kp_daily	Daily Kp index (planetary K-index, a measure of geomagnetic activity).
Ap_daily	Daily Ap index (planetary equivalent amplitude index).
Ap_0000_0300	Planetary Equivalent Amplitude (Ap) for 0000-0300 UT (and similarly for subsequent 3-hour intervals).
Ap_0300_0600	Planetary Equivalent Amplitude (Ap) for 0300-0600 UT.
Ap_0600_0900	Planetary Equivalent Amplitude (Ap) for 0600-0900 UT.
Ap_0900_1200	Planetary Equivalent Amplitude (Ap) for 0900-1200 UT.
Ap_1200_1500	Planetary Equivalent Amplitude (Ap) for 1200-1500 UT.
Ap_1500_1800	Planetary Equivalent Amplitude (Ap) for 1500-1800 UT.
Ap_1800_2100	Planetary Equivalent Amplitude (Ap) for 1800-2100 UT.
Ap_2100_0000	Planetary Equivalent Amplitude (Ap) for 2100-0000 UT.

rotd
The rotd column in the sw.celestrak.sw_daily() function output represents the 
Number of Day within the Bartels 27-day cycle. The values range from 01 to 27. 
The Bartels Solar Rotation Number (bsrn column) is a sequence of 27-day 
intervals counted continuously from February 8, 1832. The rotd column indicates 
which day of that specific cycle the data corresponds to. 

Cp
The Cp column in the data returned by the spaceweather.celestrak.sw_daily() 
function refers to the Planetary Daily Equivalent Amplitude. 
The Cp index is a measure of the day's overall geomagnetic activity and is a 
linear scale derived from the 3-hourly Kp indices. While the Kp index is quasi-
logarithmic and ranges from 0 to 9, the Ap and Cp indices use a linear scale, 
which can be more suitable for averaging and certain types of scientific analysis. 


The data provided in this column is part of the daily space weather indices used 
for tasks such as atmospheric density modeling for satellite operations. 
"""

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import spaceweather as sw  # assuming this is the library you're using
import pandas as pd 
import tkinter as tk
from tkinter import messagebox


def plot_kp(time_frame):
    # --- Load and slice the data ---
    sw_data = sw.celestrak.sw_daily(update=True)
    
    # Ensure datetime index
    sw_data.index = pd.to_datetime(sw_data.index)
    
    current_datetime = datetime.utcnow()
    one_week_ago = current_datetime - timedelta(weeks=1)
    one_month_ago = current_datetime - timedelta(days=30)
    
    
    if time_frame == "Week":
        ago = one_week_ago
    elif time_frame == "Month":
        ago = one_month_ago
    else:
        messagebox.showerror("Error", "Invalid time frame selected for Kp trend.")
    
    # Filter data for the last week
    data_range = sw_data.loc[ago:current_datetime]
    
    # Extract datetime and Kp
    times = data_range.index
    kp_values = data_range["Kp0"].astype(float)  # make sure it's numeric
    
    # --- Plot ---
    plt.figure(figsize=(10, 5))
    scatter = plt.scatter(
        times,
        kp_values,
        c=kp_values,
        cmap="RdYlGn_r",  # reversed so low=green, high=red
        s=100,
        edgecolor="k",
        zorder=10
    )
    
    # Colorbar
    cbar = plt.colorbar(scatter)
    cbar.set_label("Kp Index", fontsize=12)
    
    # Axes and formatting
    plt.title(f"Kp Index — Past {time_frame}", fontsize=14)
    plt.ylabel("Kp Value")
    plt.xlabel("Date (UTC)")
    plt.ylim(0, 9)
    plt.grid(True, linestyle="--", alpha=0.5)
    
    # Format date axis
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
    plt.close()
    
        


if __name__ == "__main__":
    # --- Load and slice the data ---
    sw_data = sw.celestrak.sw_daily(update=True)
    
    # Ensure datetime index
    sw_data.index = pd.to_datetime(sw_data.index)
    
    current_datetime = datetime.utcnow()
    one_week_ago = current_datetime - timedelta(weeks=1)
    one_month_ago = current_datetime - timedelta(days=30)
    
    # Filter data for the last week
    data_range = sw_data.loc[one_month_ago:current_datetime]
    
    # Extract datetime and Kp
    times = data_range.index
    kp_values = data_range["Kp0"].astype(float)  # make sure it's numeric
    
    # --- Plot ---
    plt.figure(figsize=(10, 5))
    scatter = plt.scatter(
        times,
        kp_values,
        c=kp_values,
        cmap="RdYlGn_r",  # reversed so low=green, high=red
        s=100,
        edgecolor="k",
        zorder=10
    )
    
    # Colorbar
    cbar = plt.colorbar(scatter)
    cbar.set_label("Kp Index", fontsize=12)
    
    # Axes and formatting
    plt.title("Kp Index — Past Week", fontsize=14)
    plt.ylabel("Kp Value")
    plt.xlabel("Date (UTC)")
    plt.ylim(0, 9)
    plt.grid(True, linestyle="--", alpha=0.5)
    
    # Format date axis
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
    plt.close()
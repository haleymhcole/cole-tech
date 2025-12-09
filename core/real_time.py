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


| Column         | Meaning                                          |
| -------------- | ------------------------------------------------ |
| bsrn           | Bartels solar rotation number                    |
| rotd           | Day of Bartels rotation (1–27)                   |
| Kp0…Kp21       | Kp geomagnetic index for each 3-hour UT interval |
| Kpsum          | Sum of all 8 daily Kp values                     |
| Ap0…Ap21       | Ap (linear Kp) for each 3-hour interval          |
| Apavg          | Daily mean Ap index                              |
| Cp             | Daily geomagnetic activity index (0–2.5)         |
| C9             | Same as Cp but 0–9 scale                         |
| isn            | International Sunspot Number                     |
| f107_adj       | Daily F10.7 adjusted                             |
| f107_81ctr_adj | 81-day centered running mean (adjusted)          |
| f107_81lst_adj | 81-day backward running mean (adjusted)          |
| f107_obs       | Daily observed F10.7                             |
| f107_81ctr_obs | 81-day centered observed mean                    |
| f107_81lst_obs | 81-day backward observed mean                    |
| Q              | Solar quiet-level X-ray background index         |

"""
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import spaceweather as sw  
import pandas as pd 
import streamlit as st
import numpy as np
from core import forecast
import plotly.express as px
import plotly.graph_objs as go

def get_data():
    # --- Load and slice the data ---
    sw_data = sw.celestrak.sw_daily(update=True)
    sw_data.index = pd.to_datetime(sw_data.index)
    current_datetime = datetime.utcnow()
    current_data = sw_data.loc[:current_datetime].iloc[-1]
    prev_data = sw_data.loc[:current_datetime].iloc[-2]
    
    agos = [current_datetime - timedelta(weeks=1),
            current_datetime - timedelta(days=30),
            current_datetime - timedelta(days=365),
            current_datetime - timedelta(days=90)]
    
    # kp_index = current_data["Kp0"].astype(float)
    Apavg = current_data["Apavg"].astype(float)
    f107_observed = current_data["f107_obs"].astype(float)
    
    # Daily geomagnetic activity index (0–2.5)
    Cp = current_data['Cp'].astype(float)
    
    # International sunspot number
    isn = current_data['isn'].astype(float)
    
    bsrn = current_data['bsrn'].astype(float)
    rotd = current_data['rotd'].astype(float)
    
    properties = {"Ap":"Apavg",
                      "Solar Flux (Adjusted to 1 AU)":"f107_adj", 
                      "Cp":"Cp", 
                      "Sunspot Number":"isn",
                      "Bartels Solar Rotation Number":"bsrn",
                      "Bartels Rotation Day":"rotd"}
    
    current_datetime = current_data.name
        
    return sw_data, current_datetime, agos, properties

    
def plot(sw_data, current_datetime, time_frame, ago, title, var_name):
    if time_frame == "Forecasting":
        # data_range = sw_data.loc[current_datetime - timedelta(days=90):current_datetime + timedelta(days=30)]
        # data_range[var_name] = np.nan
        data_range = sw_data.loc[current_datetime - timedelta(days=90):current_datetime]
        trendline = forecast.get_trend(data_range[var_name].values)
        data_range = sw_data.loc[current_datetime - timedelta(days=90):current_datetime + timedelta(days=30)]
        data_range[var_name].loc[current_datetime:current_datetime + timedelta(days=30)] = np.nan #TODO: swap so that current data is not changed to NAN
        x = np.arange(1, len(data_range)+1)
    else:
        # Filter data for the time frame of interest.
        data_range = sw_data.loc[ago:current_datetime]
    
    # Extract datetime and y-values.
    times = data_range.index
    values = data_range[var_name].values.astype(float) 
    
    # --- Plot ---
    # Create base scatter
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=times,
        y=values,
        mode="markers",
        marker=dict(
            size=10,
            color=values,
            colorscale="RdYlGn_r",   # low=green, high=red
            showscale=True,
            colorbar=dict(title=title),
            line=dict(color="black", width=0.7)
        ),
        name=title,
        # hovertemplate=(
        #     "<b>Date:</b> %{times}<br>"
        #     f"<b>{title}:</b> %{values}<extra></extra>"
        # )
        
        hovertemplate = (
                "<b>Date:</b> %{x}<br>"
                f"<b>{title}:</b> %{{y}}<extra></extra>"
            )
    ))

    height = 400

    # Add trendline if forecasting mode
    if time_frame == "Forecasting":
        height = 500
        
        if trendline is not None and data_range is not None:
            fig.add_trace(go.Scatter(
                x=data_range.index,
                y=trendline(np.arange(len(data_range))),
                mode="lines",
                line=dict(color="red", width=2),
                name="Trend",
                #hovertemplate="<b>Trend:</b> %{trendline(np.arange(len(data_range)))}<extra></extra>"
                hoverinfo="skip"  # don't hover on trendline
            ))
        

    # Layout (titles, labels, etc.)
    fig.update_layout(
        title=f"{title} — {time_frame}",
        xaxis_title="Date (UTC)",
        yaxis_title=title,
        template="ggplot2",
        hovermode="closest",     # ← important
        height=height,
        margin=dict(l=40, r=20, t=60, b=40),
        legend=dict(
            orientation="h",  # Horizontal orientation for better fit at the bottom
            yanchor="bottom", # Anchor the legend to its bottom edge
            y=-0.4,           # Adjust this value to position the legend below the plot area
            xanchor="center", # Anchor the legend to its center horizontally
            x=0.5             # Center the legend horizontally
            )
    )

    if "Kp" in title:
        fig.update_yaxis(range=[0, 9])
    
    # Format date axis
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
    plt.xticks(rotation=45)
    
    # plt.tight_layout()
    
    # On hover, only show data for closest point, not all data.
    #fig.update_layout(hovermode='closest')
    
    # Update the layout to position the legend at the bottom
    # fig.update_layout(
    #     legend=dict(
    #         orientation="h",  # Horizontal orientation for better fit at the bottom
    #         yanchor="bottom", # Anchor the legend to its bottom edge
    #         y=-0.5,           # Adjust this value to position the legend below the plot area
    #         xanchor="center", # Anchor the legend to its center horizontally
    #         x=0.5             # Center the legend horizontally
    #         )
    #     )
        
    

    return fig


# -*- coding: utf-8 -*-
"""
Created on Thu Dec 18 14:27:37 2025

@author: haley
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
import plotly.io as pio

# Optional: Set as default template
pio.templates.default = "ggplot2"

plt.rcParams['figure.figsize'] = [8, 5]
plt.rcParams['lines.linewidth'] = 2
plt.rcParams['axes.grid'] = True


# plt.rcParams['axes.titlesize'] = 18    # Fontsize of the axes title
plt.rcParams['axes.labelsize'] = 16    # Fontsize of the x and y labels
plt.rcParams['xtick.labelsize'] = 12   # Fontsize of the x tick labels
plt.rcParams['ytick.labelsize'] = 12   # Fontsize of the y tick labels
plt.rcParams['legend.fontsize'] = 14   # Fontsize of the legend

# You can also use string values like 'small', 'medium', 'large', 'x-large', etc.

    
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
            size=15 if "Year" not in time_frame else 10,
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
        # title=f"{title} — {time_frame}" if "Historical" not in time_frame else "",
        xaxis_title="Date (UTC)",
        yaxis_title=title,
        # template="ggplot2",
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
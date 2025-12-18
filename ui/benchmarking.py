#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  7 15:40:48 2025

@author: haleycole
"""

import streamlit as st
import pandas as pd
import datetime as dt
import numpy as np
#from data import load_data
# from get_paths import get_root
from core import real_time
from core import plotting
import os

import plotly.io as pio
pio.templates.default = "ggplot2"

from pathlib import Path

def get_root():
    # Path to project root (one directory up from ui/)
    ROOT = Path(__file__).resolve().parents[1]
    #DATA_DIR = os.path.join(ROOT, "data")
    return ROOT

def swap_boolean_for_check(x):
    # Swap 1s and 0s (or True and False) for ✔ check marks.
    if x:
        return "✓"
    else:
        return ""

def render():
    # --- Main Page Content ---
    st.title("⌛ Historical Benchmarking")
    
    sw_data, current_datetime, agos, properties = real_time.get_data() # TODO: Avoid repeating this function (currently also in dashboard.py for real-time stats)
    
    # c1, c2, c3 = st.columns([3,2,1])
    # with c1:
    #     st.header("🚀 In-Depth Analysis")
        
    # with c2:
    
    # st.space(size="medium") # Adds a medium-sized vertical space height="medium"
    
# =============================================================================
#     Get mission timeline 
# =============================================================================
    c1, c2, c3 = st.columns([1,1,1])
    with c1:
        st.header("Mission Info")
    with c2:
        default_start = dt.datetime(2003, 10, 25, 16, 45) 
        start_mission = st.datetime_input("Mission Start:", default_start)
    with c3:
        default_end = dt.datetime(2003, 11, 5, 16, 45) 
        end_mission = st.datetime_input("Mission End:", default_end)
    
    if start_mission > end_mission:
        st.error("Please select appropriate start and end dates.")
        
    st.markdown("---")
    
# =============================================================================
#     Plot
# =============================================================================
    c1, c2 = st.columns([1,1])
    with c1:
        st.markdown("<h3 style='text-align: center; color: black;'>Geomagnetic Activity During Mission</h3>", unsafe_allow_html=True)
        selected_option = "Ap"
        fig = plotting.plot(sw_data, end_mission, "Historical Benchmarking", start_mission, selected_option, properties[selected_option])
        st.plotly_chart(fig, width='stretch', theme=None)
    
    with c2:
        st.markdown("<h3 style='text-align: center; color: black;'>Solar Activity During Mission</h3>", unsafe_allow_html=True)
        selected_option = "Solar Flux (Adjusted to 1 AU)"
        fig = plotting.plot(sw_data, end_mission, "Historical Benchmarking", start_mission, selected_option, properties[selected_option])
        st.plotly_chart(fig, width='stretch', theme=None)
    
    st.markdown("---")
    
    
# =============================================================================
#     DB
# =============================================================================
    st.markdown("<h3 style='text-align: center; color: black;'>Reported CME During Mission</h3>", unsafe_allow_html=True)
    
    # st.file_uploader("Upload CSV", type=["csv"])
    
    # CME Database
    ROOT = get_root()
    cme_db_file = os.path.join(ROOT, "core", "data", "CDAW_CME_Catalog_Processed.csv")
    cme_db = pd.read_csv(cme_db_file)
    cme_db.drop(['2nd-order Speed at final height [km/s]',
                 '2nd-order Speed at 20 Rs [km/s]'], axis=1, inplace=True)
    
    cme_db['Mild Event'] = cme_db['Mild Event'].apply(swap_boolean_for_check)
    cme_db['Measurement Difficulties'] = cme_db['Measurement Difficulties'].apply(swap_boolean_for_check)
    
    # num_rows = st.slider("Number of rows", 1, 100, 25)
    
    config = {
    #     #"Preview": st.column_config.ImageColumn(),
    #     "Linear Speed [km/s]": st.column_config.ProgressColumn(),
    }
    
    # Ensure the Date column is datetime type
    cme_db['Date'] = pd.to_datetime(cme_db['Date'])
    
    # Create a mask for rows within the date range (inclusive)
    mask = (cme_db['Date'] >= start_mission) & (cme_db['Date'] <= end_mission)
    
    # Apply the mask to the DataFrame
    truncated_df = cme_db.loc[mask]
    
    st.dataframe(truncated_df, column_config=config, width='stretch')
    
    # if st.toggle("Enable editing"):
    #     edited_data = st.data_editor(cme_db, column_config=config, use_container_width=True)
    # else:
    #     st.dataframe(cme_db, column_config=config, use_container_width=True)



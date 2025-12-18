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
import os

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
    
    c1, c2 = st.columns([1,2])
    with c1:
        #st.subheader("⏱️ Real-Time Properties")
        selected_option = st.selectbox("Choose a property to analyze:", properties.keys())
        st.write("**Track how key environmental variables evolve over time, and explore short-term to seasonal trends using the interactive plots on the right.**")
        # Text for article/user-guide: This section provides continuously updated environmental and space-weather indicators relevant to satellite operators, atmospheric scientists, and mission planners. 
        st.write("Select a time window to analyze recent behavior, identify anomalies, and compare today’s conditions with historical context.")
        
        
        with st.expander("❓ How to Use This Panel"):
            st.markdown("""
            **Welcome to the Real-Time Properties Dashboard**  
            - Select a time frame in the left panel (e.g., Past Month).
            - The plot on the right will update automatically to reflect the chosen time span and dataset resolution.
            - Hover over the plot for details.
            - Use the download button under the plot to save the data (Pro-only).
            """)
            
            st.markdown("""
            #### Past Week
            Ideal for short-term operational awareness.
            Use this view to detect recent disturbances—such as geomagnetic spikes or rapid density changes—that could affect orbit propagation or drag calculations.
            
            #### Past Month
            Useful for medium-scale monitoring and pattern recognition.
            This window highlights gradual shifts in solar or atmospheric conditions that may indicate the onset of storms or long-period trends.
        
            #### Past Year
            Explore broader behavior across seasons, solar rotation periods, or extended quiet/active intervals.
            This perspective helps contextualize today’s environment within the larger solar cycle.
            
            #### Why This Matters
            Understanding how these properties change across multiple time scales allows operators to:
            - anticipate drag changes,
            - evaluate risk conditions,
            - improve scheduling and uplink/downlink planning,
            - correlate anomalies with environmental triggers, and
            - support long-term system performance assessment.
            """)
    
    with c2:
        tab_names = ["Past Week", "Past Month", "Past Year"]
        tabs_dict = st.tabs(tab_names) # tab1, tab2, tab3
        for t, time_frame in enumerate(tab_names):
            tab = tabs_dict[t]
            with tab:
                #st.subheader(f"Kp Index -- {tab_name}")
                fig = real_time.plot(sw_data, current_datetime, time_frame, agos[t], selected_option, properties[selected_option])
                #st.pyplot(fig)
                st.plotly_chart(fig, use_container_width=True)
    
    start = st.date_input("Start Date")
    end = st.date_input("End Date")
    
    if start > end:
        st.error("Please select appropriate start and end dates.")
    
    st.write("Upload comparison data:")
    # st.file_uploader("Upload CSV", type=["csv"])
    
    # CME Database
    ROOT = get_root()
    cme_db_file = os.path.join(ROOT, "data", "CDAW_CME_Catalog_Processed.csv")
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
    
    if st.toggle("Enable editing"):
        edited_data = st.data_editor(cme_db, column_config=config, use_container_width=True)
    else:
        st.dataframe(cme_db, column_config=config, use_container_width=True)



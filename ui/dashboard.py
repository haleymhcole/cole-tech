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
from core import get_realtime_data

def render():
    # ---------------------------
    #     HERO SECTION
    # ---------------------------
    st.title("Dashboard")
    
    # ---------------------------
    #     QUICK STATUS CARDS
    # ---------------------------
    st.header("Current Space Weather Status")
    
    # Replace these placeholder values with your live data pipeline
    # kp_index = 3
    kp_index = get_realtime_data.kp()
    solar_flux = 145.2
    sunspot_num = 78
    latest_cme = "No CME detected (past 24h)"
    
    c1, c2, c3, c4 = st.columns(4)
    
    with c1:
        st.metric("Kp Index", kp_index)
    
    with c2:
        st.metric("Solar Flux (F10.7)", solar_flux)
    
    with c3:
        st.metric("Sunspot Number", sunspot_num)
    
    with c4:
        st.metric("Latest CME", latest_cme)
    
    
    st.markdown("---")
    
    
    
    
    
    # ---------------------------
    #     MINI PLOT SECTION
    # ---------------------------
    st.header("Kp Index")

    tab_names = ["Past Week", "Past Month", "Past Year"]
    tabs_dict = st.tabs(tab_names) # tab1, tab2, tab3

    for t, tab_name in enumerate(tab_names):
        tab = tabs_dict[t]
        with tab:
            #st.subheader(f"Kp Index -- {tab_name}")
            fig = get_realtime_data.plot_kp(tab_name)
            st.pyplot(fig)
        
    
    
    
    
    st.header("Solar Activity — Last 12 Months")
    
    # Fake data plot — insert your NOAA data instead
    dates = pd.date_range(end=dt.datetime.now(), periods=365)
    fake_sunspots = np.random.normal(80, 10, size=365)
    
    st.line_chart(pd.DataFrame({"Sunspots": fake_sunspots}, index=dates))
    
    st.markdown("---")
    
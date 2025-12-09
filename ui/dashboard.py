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
from core import real_time

def render():
    # ---------------------------
    #     HERO SECTION
    # ---------------------------
    st.title("Dashboard")
    
    # ---------------------------
    #     GET REALTIME DATA
    # ---------------------------
    sw_data, current_datetime, agos, now_properties = real_time.get_data()
    
    
    # ---------------------------
    #     QUICK STATUS CARDS
    # ---------------------------
    st.header("Current Space Weather Status")
    
    # Replace these placeholder values with your live data pipeline
    # kp_index = 3
    # kp_index = real_time.kp()
    #solar_flux = 145.2
    sunspot_num = 78
    latest_cme = "No CME detected (past 24h)"
    
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.metric("Ap Index", now_properties['Apavg'])
        st.metric("Geomagnetic Activity Cp Index (0–2.5)", now_properties['Cp'])
    
    with c2:
        st.metric("Sunspot Number", now_properties['isn'])
        st.metric("Solar Flux (F10.7)", now_properties['f107_observed'])
        
        
    with c3:
        st.metric("Bartels Solar Rotation Number", now_properties['bsrn'])
        st.metric("Bartels Rotation Day (1–27)", now_properties['rotd'])
    
    # with c4:
    #     st.metric("Latest CME", latest_cme)
    
    
    st.markdown("---")
    
    
    
    
    # ---------------------------
    #     MINI PLOT SECTION
    # ---------------------------
    
    for var_name in ["Kp Index", "Solar Flux (F10.7)"]:
        st.header(var_name)
        tab_names = ["Past Week", "Past Month", "Past Year"]
        tabs_dict = st.tabs(tab_names) # tab1, tab2, tab3
        for t, time_frame in enumerate(tab_names):
            tab = tabs_dict[t]
            with tab:
                #st.subheader(f"Kp Index -- {tab_name}")
                fig = real_time.plot(sw_data, current_datetime, time_frame, agos[t], var_name)
                st.pyplot(fig)
        
    
    
    
    st.header("Solar Activity — Last 12 Months")
    
    # Fake data plot — insert your NOAA data instead
    dates = pd.date_range(end=dt.datetime.now(), periods=365)
    fake_sunspots = np.random.normal(80, 10, size=365)
    
    st.line_chart(pd.DataFrame({"Sunspots": fake_sunspots}, index=dates))
    
    st.markdown("---")
    
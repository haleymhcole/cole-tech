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

def render():
    # ---------------------------
    #     HERO SECTION
    # ---------------------------
    st.title("Space Weather Insights")
    st.subheader("Real-Time Monitoring, Smarter Forecasting")
    
    st.write(
        "Track sunspots, geomagnetic activity, solar flux, and CME alerts — all in one place. "
        "Built for researchers, hobbyists, forecasters, and the simply curious."
    )
    
    col1, col2 = st.columns(2)
    with col1:
        st.button("🚀 Launch Dashboard")
    with col2:
        st.button("🔒 Unlock Pro Tools")
    
    
    st.markdown("---")
    
    # ---------------------------
    #     QUICK STATUS CARDS
    # ---------------------------
    st.header("Current Space Weather Status")
    
    # Replace these placeholder values with your live data pipeline
    kp_index = 3
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
    st.header("Solar Activity — Last 12 Months")
    
    # Fake data plot — insert your NOAA data instead
    dates = pd.date_range(end=dt.datetime.now(), periods=365)
    fake_sunspots = np.random.normal(80, 10, size=365)
    
    st.line_chart(pd.DataFrame({"Sunspots": fake_sunspots}, index=dates))
    
    st.markdown("---")
    
    # ---------------------------
    #     FEATURES OVERVIEW TABLE
    # ---------------------------
    st.header("Features Overview")
    
    features = {
        "Feature": [
            "Realtime indices (Kp, F10.7, SSN)",
            "CME Alerts",
            "Detailed Nowcasting Models",
            "Forecasting Tools (cycle phase, rise/decay)",
            "Historical Benchmarking",
            "Custom Threshold Alerts",
            "Exportable plots/data",
        ],
        "Free": ["✓", "✓", "—", "—", "—", "—", "—"],
        "Pro": ["✓", "✓", "✓", "✓", "✓", "✓", "✓"],
    }
    
    df_features = pd.DataFrame(features)
    
    st.table(df_features)
    
    st.markdown(
        "<br><center><a href='#' style='font-size:18px;'>See Full Feature List →</a></center><br>",
        unsafe_allow_html=True,
    )
    
    st.markdown("---")
    
    # ---------------------------
    #     EDUCATIONAL SECTION
    # ---------------------------
    st.header("What Is Space Weather?")
    st.write("""
    Space weather refers to solar activity — like sunspots, flares, 
    and coronal mass ejections — that affects Earth.
    
    These disturbances can influence satellites, GPS accuracy, aviation routes, 
    orbital debris, power grids, and even radio communication.
    
    This app brings together real data and predictive modeling to make 
    space weather easier to understand, monitor, and plan around.
    """)
    
    st.markdown("---")
    
    # ---------------------------
    #     COMMUNITY & FEEDBACK
    # ---------------------------
    st.header("Community & Feedback")
    
    st.write("Have ideas for new features or improvements? We'd love to hear from you.")
    
    st.button("💬 Submit Feedback")
    st.write("Join our newsletter for weekly solar cycle updates.")


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
    st.header("☀️ Current Space Weather Status")
    
    # Replace these placeholder values with your live data pipeline
    # kp_index = 3
    # kp_index = real_time.kp()
    #solar_flux = 145.2
    # sunspot_num = 78
    # latest_cme = "No CME detected (past 24h)"
    
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.metric("Ap Index", now_properties['Ap'][1])
        st.metric("Geomagnetic Activity Cp Index (0–2.5)", now_properties['Cp'][1])
    
    with c2:
        st.metric("Sunspot Number", now_properties['Sunspot Number'][1])
        st.metric("Solar Flux (F10.7)", now_properties['Solar Flux (Adjusted to 1 AU)'][1])
        
        
    with c3:
        st.metric("Bartels Solar Rotation Number", now_properties['Bartels Solar Rotation Number'][1])
        st.metric("Bartels Rotation Day (1–27)", now_properties['Bartels Rotation Day'][1])
    
    # with c4:
    #     st.metric("Latest CME", latest_cme)
    
    
    st.markdown("---")
    
    # ---------------------------
    #     MINI PLOT SECTION
    # ---------------------------
    
    c1, c2, c3 = st.columns([2,1,2])
    with c1:
        st.header("🚀 In-Depth Analysis")
    with c2:
        selected_option = st.selectbox("Choose a property to analyze:", now_properties.keys())
    
    st.space(size="medium") # Adds a medium-sized vertical space height="medium"
    
    c1, c2 = st.columns([1,2])
    with c1:
        st.subheader("⏱️ Real-Time Properties")
        st.write("**Track how key environmental variables evolve over time, and explore short-term to seasonal trends using interactive plots.**")
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
                fig = real_time.plot(sw_data, current_datetime, time_frame, agos[t], selected_option, now_properties[selected_option][0])
                #st.pyplot(fig)
                st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("📈 Forecasting")
    fig = real_time.plot(sw_data, current_datetime, "Forecasting", agos[t], selected_option, now_properties[selected_option][0])
    st.plotly_chart(fig, use_container_width=True)
    
    
    # for var_name in ["Kp Index", "Solar Flux (F10.7)"]:
    #     st.header(var_name)
    #     tab_names = ["Past Week", "Past Month", "Past Year"]
    #     tabs_dict = st.tabs(tab_names) # tab1, tab2, tab3
    #     for t, time_frame in enumerate(tab_names):
    #         tab = tabs_dict[t]
    #         with tab:
    #             #st.subheader(f"Kp Index -- {tab_name}")
    #             fig = real_time.plot(sw_data, current_datetime, time_frame, agos[t], var_name)
    #             st.pyplot(fig)
        
    
    
    
    # st.header("Solar Activity — Last 12 Months")
    
    # # Fake data plot — insert your NOAA data instead
    # dates = pd.date_range(end=dt.datetime.now(), periods=365)
    # fake_sunspots = np.random.normal(80, 10, size=365)
    
    # st.line_chart(pd.DataFrame({"Sunspots": fake_sunspots}, index=dates))
    
    # st.markdown("---")
    
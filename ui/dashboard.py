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
# from ui.animations import stars
import os

import plotly.io as pio
pio.templates.default = "ggplot2"

def report_env(env, color):
    st.write(f'Environment is <span  style="color:{color}">**{env.upper()}**</span>.', unsafe_allow_html=True)

# def get_green_to_red_gradient(num_colors):
#     colors = []
#     for i in range(num_colors):
#         # Interpolate the green and red components
#         # Green starts at 255 and decreases to 0
#         # Red starts at 0 and increases to 255
#         green_component = int(255 * (1 - i / (num_colors - 1)))
#         red_component = int(255 * (i / (num_colors - 1)))
#         blue_component = 0  # Blue component remains 0 for green to red

#         # Format the RGB values into a hex string
#         hex_color = f"#{red_component:02x}{green_component:02x}{blue_component:02x}"
#         colors.append(hex_color)
#     return colors

# def get_green_to_red_gradient(num_colors):
#     import matplotlib.cm as cm
#     import matplotlib.colors as mcolors
    
#     # Get the RdYlGn colormap
#     cmap = cm.get_cmap('RdYlGn')
    
#     # Generate evenly spaced values between 0 and 1
#     # These values will be mapped to colors by the colormap
#     color_values = np.linspace(0, 1, num_colors)
    
#     # Get the RGBA values for each color and convert to hex codes
#     hex_colors = [mcolors.to_hex(cmap(value)) for value in color_values]
    
#     return hex_colors[::-1]

green_to_red = ['#006837', '#4bb05c', '#b7e075', '#feffbe', '#fdbf6f', '#ea5739', '#a50026']


def render():
    
    st.markdown("""
    <style>
    .argos-style {
        font-family: 'Arial';
        font-size: 100px;
        color: #5645a6;
        font-weight: bold;
        font-style: italic;
    }
    </style>
    """, unsafe_allow_html=True)
    
    pro_on = st.session_state.argos_on
    
    # ---------------------------
    #     HERO SECTION
    # ---------------------------
    # st.title("Dashboard")
    
    #argos_on = st.session_state.argos_on
    
    # ---------------------------
    #     GET REALTIME DATA
    # ---------------------------
    sw_data, current_datetime, agos, properties = real_time.get_data()
    
    current_data = sw_data.loc[:current_datetime].iloc[-1]
    prev_data = sw_data.loc[:current_datetime].iloc[-2]
    
    Ap = current_data[properties['Ap']]
    Ap_env_label, Ap_env_color, Ap_env_caption = real_time.get_Ap_env(Ap)
    
    f107 = current_data[properties['Solar Flux (Adjusted to 1 AU)']]
    f107_env_label, f107_env_color, f107_env_caption = real_time.get_f107_env(f107)
    
    # ---------------------------
    #     QUICK STATUS CARDS
    # ---------------------------
    if st.session_state.argos_on:
        st.markdown(
        f"""
        <h2>
            🌎 Geomagnetic activity level:
            <span style="color:{Ap_env_color}; font-weight:600;">
                {Ap_env_label.upper()}
            </span>
        </h2>
        """,
        unsafe_allow_html=True
        )
            
        st.markdown(
        f"""
        <h2>
            ☀️ Solar activity level:
            <span style="color:{f107_env_color}; font-weight:600;">
                {f107_env_label.upper()}
            </span>
        </h2>
        """,
        unsafe_allow_html=True
        )

    else:
        st.header("☀️ Current Space Weather Status") 
    
    
    # st.write("Today's Environment:", )
        # st.write("Data updated daily from CelesTrak, Helmholtz Centre, and NASA databases. Numbers below the property value refer to the change from yesterday's environment.")
    
    # Replace these placeholder values with your live data pipeline
    # kp_index = 3
    # kp_index = real_time.kp()
    #solar_flux = 145.2
    # sunspot_num = 78
    # latest_cme = "No CME detected (past 24h)"
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Ap Index", Ap, delta=prev_data[properties['Ap']] if pro_on else None)
        st.metric("Geomagnetic Activity Cp Index (0–2.5)", current_data[properties['Cp']], delta=prev_data[properties['Cp']] if pro_on else None)
    
    with c2:
        st.metric("Sunspot Number", current_data[properties['Sunspot Number']], delta=prev_data[properties['Sunspot Number']] if pro_on else None)
        st.metric("Solar Flux (F10.7)", current_data[properties['Solar Flux (Adjusted to 1 AU)']], delta=prev_data[properties['Solar Flux (Adjusted to 1 AU)']] if pro_on else None)
        
    with c3:
        st.metric("Bartels Solar Rotation Number", current_data[properties['Bartels Solar Rotation Number']], delta=prev_data[properties['Bartels Solar Rotation Number']] if pro_on else None)
        st.metric("Bartels Rotation Day (1–27)", current_data[properties['Bartels Rotation Day']], delta=prev_data[properties['Bartels Rotation Day']] if pro_on else None)
    
    # with c4:
    #     st.metric("Latest CME", latest_cme)
    
    if st.session_state.argos_on:
        c1, c2 = st.columns([1,20])
        
        with c1:
            st.image(os.path.join("assets", "SWAN-icon.png"))
        with c2:
            st.markdown('<p class="argos-style">SWAN Insight Engine</p>', unsafe_allow_html=True)
            st.write(f"The geomagnetic environment is {Ap_env_label.lower()}. {Ap_env_caption} The solar flux environment is {f107_env_label.lower()}. {f107_env_caption}")
            
            #AP indices rank geomagnetic activity from quiet to severe, with Quiet (<15), Active (15-48), Moderate (80-132), Strong (132-207), Severe (207-294), Extreme (294-388), and Extreme+ (>=388), based on NOAA's Space Weather Scales, where higher numbers mean greater magnetic storm intensity affecting technology and power grids. 
            # if Ap < 15:
            #     report_env("Quiet", green_to_red[0])
            #     st.write("Very low activity, minimal impact.")
            # elif Ap < 48:
            #     report_env("Active", green_to_red[1])
            #     st.write("Minor disturbances, potentially visible auroras at high latitudes.")
            # elif Ap < 132:
            #     report_env("Moderate", green_to_red[2])
            #     st.write("Noticeable geomagnetic changes, minor power grid fluctuations possible.")
            # elif Ap < 207:
            #     report_env("Strong", green_to_red[3])
            #     st.write("Significant geomagnetic storms, increased radio blackouts, potential for widespread power grid issues.")
            # elif Ap < 294:
            #     report_env("Severe", green_to_red[4])
            #     st.write("Major storms, voltage control problems in power systems, transformer damage, potential for grid collapse.")
            # elif Ap < 388:
            #     report_env("Extreme", green_to_red[5])
            #     st.write("Widespread voltage control issues, large power grid failures, protective systems struggle.")
            # else:
            #     report_env("Extreme+", green_to_red[6])
            #     st.write("Maximum severity, extreme grid instability, widespread blackouts, critical infrastructure risk.")
           
            # The Ap index reflects the average intensity of Earth's magnetic field disturbances over a day, with higher values indicating more severe space weather

            
    
    # st.markdown("---")
    
    # ---------------------------
    #     MINI PLOT SECTION
    # ---------------------------
    
    
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
    